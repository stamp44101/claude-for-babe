// Vercel serverless function: streams a Claude reply for the chat box.
// Env: ANTHROPIC_API_KEY (required), ANTHROPIC_MODEL (optional), CHAT_PASSCODE (optional)

const MODEL = process.env.ANTHROPIC_MODEL || "claude-sonnet-5-5";
const MAX_MSGS = 24, MAX_CHARS = 4000;

const SYSTEM = `คุณคือ Claude ที่แสตมป์ (แฟนของอั๊ย) ตั้งไว้ให้อั๊ยถามเรื่องงาน Capstone Design ของกลุ่ม ETHAVERTEX (โรงงาน bioethanol → hydrogen, จุฬาฯ)
ตอบเป็นภาษาไทย น้ำเสียงอบอุ่น เป็นกันเอง สุภาพ (เรียกเธอว่า "อั๊ย" แทนตัวเองว่า "Claude") ใช้ศัพท์วิศวกรรมเป็นภาษาอังกฤษตามจริง อธิบายให้เข้าใจง่ายสำหรับนิสิตวิศวกรรมเคมี ตอบกระชับก่อน ถ้าอั๊ยอยากรู้ลึกค่อยขยาย
ถ้าไม่แน่ใจหรือเอกสารไม่ได้ระบุ ให้บอกตรง ๆ และแนะนำให้เช็คกับอาจารย์ อย่าเดาค่า setpoint, design pressure หรือข้อมูลที่เอกสารไม่มี

<context>
หน้าเว็บนี้คือรีวิว P&ID ของ R-101 (Reformer) เทียบกับ HAZOP ใน Memo 6 (ตารางที่ 14) + BFD + สไลด์ Memo 5&6
- R-101: ethanol steam reformer, catalyst LSTN 650 (perovskite, exsolved Ni — pyrophoric ต้อง N₂ passivation ก่อนเปิด), 600–650°C, 1 bar, S/E = 3, รับความร้อน 5.99 MW จาก F-101
- F-101 reformer furnace: เชื้อเพลิงหลักคือ PSA tail gas (Stream 16, 6.01 MW = 73.7%) + natural gas makeup 2.15 MW + air; flue gas ไป CCU (B-201 → C-201…)
- Feed มาจาก E-104 (superheated ~500°C); syngas ออกไป E-101 → R-102 (HT-WGS)

P&ID เดิมของอั๊ย: FT/FIC-101 → FCV-101, CV-101 (check valve), TT/TIC-101 → TCV-101 (NG), PT/PIC-101 → control valve บน syngas outlet (ไม่มี tag), PSV ไป flare (เส้นประ, ไม่มี tag), I-101 รับ FIC/TIC/PIC แต่สั่งปิดแค่ XV-101 บน NG

HAZOP (L×S): 1A Temp Higher 12 High · 1B Temp Lower 6 · 2A Flow Higher 9 · 2B Flow Lower 6 · 2C No Flow 10 High · 3A Pressure Higher 15 Very High · 3B Pressure Lower 6

ข้อค้นพบหลัก: (1) ไม่มีเส้น tail gas/air และ interlock ตัดแค่ NG → fuel cut-off ไม่ครบ (2) interlock ไม่ตัด feed (3A) (3) trip ใช้ transmitter ตัวเดียวกับ control (4) feed เข้า-ออกกลางถัง ไม่ผ่าน catalyst bed, เส้นประใช้แทน heat (5) PSV ไม่มี tag/เส้นประ (6) control valve ไม่มี tag/fail position (7) ไม่มี alarm tag (8) off-page ไม่ระบุ from/to (9) ไม่มี flame detection (10) ไม่มี N₂ purge/drain/vent/sample

เฉลยเวอร์ชันพื้นฐาน: R-101 เป็น catalyst tubes ใน F-101 (feed เข้าบน ออกล่าง), เพิ่ม tail gas + XV-103, XV-102 บน feed, I-101 ตัด XV-101/102/103 เมื่อ flow ต่ำมาก/temp สูงมาก/pressure สูงมาก, PSV-101 อยู่บน syngas outlet ก่อน PCV-101 ไป flare, alarm H/L/HH/LL, N₂ purge
เฉลย REV B (ละเอียด) เพิ่ม: FT/TT/PT-102 แยกไว้ trip, XV-104 (FO) ระบาย tail gas ไป flare, FC/FO ทุกวาล์ว, TY-101 feed-forward, BE-101 flame, AT-101 O₂, bypass รอบ FCV, spectacle blind, vent/drain/sample
สมมติฐานที่ยังต้องยืนยัน: ชนิดของ R-101, set pressure PSV, tag FD fan, tail gas เข้า E-104 ด้วยไหม

งานก่อนหน้า (Memo 2): P&ID PSA 2-bed (AB-101/102) มีจุดผิด เช่น V-106 ซ้ำ, FT/PI ควรเป็น PT, FC+PC สั่งวาล์วเดียวกัน, ท่อ H₂→tail gas ไม่มีวาล์ว, ไม่มี PSV, รูป "Young Fan" หลุด
</context>`;

module.exports = async (req, res) => {
  if (req.method !== "POST") { res.status(405).json({ error: "POST only" }); return; }
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) { res.status(503).json({ error: "ยังไม่ได้ใส่ ANTHROPIC_API_KEY ใน Vercel นะ" }); return; }

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = {}; } }
  const pass = process.env.CHAT_PASSCODE;
  if (pass && (body?.passcode || "") !== pass) { res.status(401).json({ error: "passcode ไม่ถูก" }); return; }

  const msgs = (Array.isArray(body?.messages) ? body.messages : [])
    .filter(m => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string" && m.content.trim())
    .slice(-MAX_MSGS)
    .map(m => ({ role: m.role, content: m.content.slice(0, MAX_CHARS) }));
  while (msgs.length && msgs[0].role !== "user") msgs.shift();
  if (!msgs.length || msgs[msgs.length - 1].role !== "user") { res.status(400).json({ error: "ไม่มีข้อความ" }); return; }

  let upstream;
  try {
    upstream = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01" },
      body: JSON.stringify({ model: MODEL, max_tokens: 1500, system: SYSTEM, messages: msgs, stream: true }),
    });
  } catch (e) { res.status(502).json({ error: "ติดต่อ Claude ไม่ได้: " + e.message }); return; }

  if (!upstream.ok || !upstream.body) {
    const t = await upstream.text().catch(() => "");
    let msg = t; try { msg = JSON.parse(t).error?.message || t; } catch {}
    res.status(upstream.status || 502).json({ error: `Claude API error (${upstream.status}): ${msg}`.slice(0, 400) });
    return;
  }

  res.writeHead(200, { "content-type": "text/plain; charset=utf-8", "cache-control": "no-cache, no-transform", "x-accel-buffering": "no" });
  const reader = upstream.body.getReader(), dec = new TextDecoder();
  let buf = "";
  try {
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      let i;
      while ((i = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
        if (!line.startsWith("data:")) continue;
        let ev; try { ev = JSON.parse(line.slice(5)); } catch { continue; }
        if (ev.type === "content_block_delta" && ev.delta?.type === "text_delta") res.write(ev.delta.text);
        else if (ev.type === "error") res.write(`\n\n[error: ${ev.error?.message || "unknown"}]`);
      }
    }
  } catch (e) { res.write(`\n\n[ขาดการเชื่อมต่อ: ${e.message}]`); }
  res.end();
};
