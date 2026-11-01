import sys
o=[]
def a(s): o.append(s)
INK="#16202b"; RED="#d6283f"; NOTE="#8a1c2b"; SUB="#456"
MONO="IBM Plex Mono, monospace"
_open=[False]
def step(n):
    if _open[0]: a('</g>')
    a(f'<g data-step="{n}">'); _open[0]=True
def esc(t): return t.replace("&","&amp;")
def line(pts,dash=False,w=1.8,arrow=False):
    d="M"+" L".join(f"{x},{y}" for x,y in pts)
    a(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{1.2 if dash else w}"'+(' stroke-dasharray="5 4"' if dash else '')+(' marker-end="url(#ar)"' if arrow else '')+'/>')
def text(x,y,t,size=11,anchor="middle",weight=400,color=INK,family="IBM Plex Sans Thai, sans-serif"):
    a(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{color}" font-family="{family}">{esc(t)}</text>')
def bubble(x,y,top,num,note=None,nside="right"):
    a(f'<circle cx="{x}" cy="{y}" r="20" fill="#fff" stroke="{INK}" stroke-width="1.4"/>')
    a(f'<line x1="{x-20}" y1="{y}" x2="{x+20}" y2="{y}" stroke="{INK}" stroke-width="1.1"/>')
    text(x,y-4,top,10,weight=600,family=MONO); text(x,y+13,num,9.5,family=MONO)
    if note:
        if nside=="right": text(x+25,y-6,note,9.5,"start",color=NOTE,family=MONO)
        else: text(x-25,y-6,note,9.5,"end",color=NOTE,family=MONO)
def body(x,y,vertical,s,w=1.5):
    if not vertical: a(f'<path d="M{x-s},{y-s} L{x+s},{y+s} L{x+s},{y-s} L{x-s},{y+s} Z" fill="#fff" stroke="{INK}" stroke-width="{w}"/>')
    else: a(f'<path d="M{x-s},{y-s} L{x+s},{y-s} L{x-s},{y+s} L{x+s},{y+s} Z" fill="#fff" stroke="{INK}" stroke-width="{w}"/>')
def valve(x,y,vertical=False,label=None,act=None,fail=None,lx=None):
    body(x,y,vertical,9)
    if act=="dia":
        a(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y-20}" stroke="{INK}" stroke-width="1.3"/><path d="M{x-11},{y-20} A11 9 0 0 1 {x+11},{y-20} Z" fill="#fff" stroke="{INK}" stroke-width="1.3"/>')
    if act=="esd":
        a(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y-16}" stroke="{INK}" stroke-width="1.3"/><rect x="{x-13}" y="{y-28}" width="26" height="12" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
        text(x,y-19,"S",8.5,weight=600,family=MONO)
    if act=="side":
        a(f'<line x1="{x}" y1="{y}" x2="{x+16}" y2="{y}" stroke="{INK}" stroke-width="1.3"/><rect x="{x+16}" y="{y-6}" width="12" height="12" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
        text(x+22,y+3,"S",8,weight=600,family=MONO)
    if label:
        text(x if lx is None else lx,y+24,label,9.5,weight=600,family=MONO)
        if fail: text(x if lx is None else lx,y+35,fail,8.5,color=NOTE,family=MONO)
def hv(x,y,vertical=False,s=6): body(x,y,vertical,s,1.2)
def check(x,y,label):
    a(f'<path d="M{x-9},{y-8} L{x+7},{y} L{x-9},{y+8} Z" fill="#fff" stroke="{INK}" stroke-width="1.4"/><line x1="{x+8}" y1="{y-9}" x2="{x+8}" y2="{y+9}" stroke="{INK}" stroke-width="1.6"/>')
    text(x,y+24,label,9.5,weight=600,family=MONO)
def offpage(x,y,t,dirn="right",w=150,sub=None):
    h=30
    if dirn=="right": a(f'<path d="M{x},{y-h/2} L{x+w-14},{y-h/2} L{x+w},{y} L{x+w-14},{y+h/2} L{x},{y+h/2} L{x+12},{y} Z" fill="#eef6ff" stroke="{INK}" stroke-width="1.3"/>')
    else: a(f'<path d="M{x+w},{y-h/2} L{x+14},{y-h/2} L{x},{y} L{x+14},{y+h/2} L{x+w},{y+h/2} L{x+w-12},{y} Z" fill="#eef6ff" stroke="{INK}" stroke-width="1.3"/>')
    text(x+w/2+3,y+(-2 if sub else 4),t,10,weight=600)
    if sub: text(x+w/2+3,y+10,sub,8.5,color=SUB)
def delta(x,y,n):
    a(f'<path d="M{x},{y-12} L{x+12},{y+9} L{x-12},{y+9} Z" fill="{RED}"/>'); text(x,y+6,n,9.5,weight=700,color="#fff",family=MONO)
def psv(x,y,label):  # inlet from top, apex at (x,y), outlet right
    a(f'<path d="M{x-9},{y-18} L{x+9},{y-18} L{x},{y} Z" fill="#fff" stroke="{INK}" stroke-width="1.4"/>')
    a(f'<path d="M{x},{y} L{x+18},{y-9} L{x+18},{y+9} Z" fill="#fff" stroke="{INK}" stroke-width="1.4"/>')
    a(f'<path d="M{x},{y} l-3,5 l6,4 l-6,4 l6,4 l-3,4" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    text(x-14,y+2,label,9.5,"end",weight=600,family=MONO)

W,H=1400,860
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
a('<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="#16202b"/></marker>'
  '<pattern id="cat" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#16202b" stroke-width="1.2"/></pattern></defs>')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')

# ===== FEED =====
step("Feed line · FT/FIC-101 · FCV-101 + bypass · XV-102")
offpage(20,170,"From E-104","right",150,"Superheated feed · 500°C, 1 bar")
line([(170,170),(640,170),(640,245)],arrow=True)
bubble(215,115,"FT","101"); line([(215,135),(215,170)])
bubble(300,70,"FIC","101","FAH/FAL")
line([(215,95),(215,70),(280,70)],dash=True)
hv(262,170); valve(300,170,act="dia"); hv(338,170)
text(300,197,"FCV-101",9.5,weight=600,family=MONO); text(300,208,"FC",8.5,color=NOTE,family=MONO)
line([(300,90),(300,150)],dash=True)
line([(250,170),(250,228),(350,228),(350,170)]); hv(300,228); text(300,245,"bypass",8.5,color=SUB)
bubble(390,115,"FT","102","FALL"); line([(390,135),(390,170)])
check(440,170,"NRV-101")
valve(505,170,act="esd",label="XV-102",fail="FC")
line([(620,170),(620,152)]); hv(620,146,vertical=True,s=5); text(632,149,"V",9,"start",weight=600)
# N2 purge into vertical leg
step("N₂ purge + spectacle blind")
offpage(482,224,"N₂ purge","right",86)
line([(568,224),(640,224)],arrow=True); hv(585,224); hv(622,224)
a('<circle cx="603" cy="224" r="4" fill="#fff" stroke="#16202b" stroke-width="1.2"/>')
text(530,252,"spectacle blind",7.5,color=SUB)

# ===== F-101 firebox with R-101 tubes =====
step("F-101 firebox + R-101 catalyst tubes")
a('<rect x="580" y="230" width="320" height="330" fill="#fbfaf6" stroke="#16202b" stroke-width="2.2"/>')
a('<path d="M840,230 L840,205 L880,205 L880,230" fill="#fbfaf6" stroke="#16202b" stroke-width="2"/>')
line([(640,245),(790,245)],w=2.4)
for tx in (660,705,750):
    a(f'<rect x="{tx-9}" y="245" width="18" height="235" fill="url(#cat)" stroke="#16202b" stroke-width="1.5"/>')
line([(651,480),(840,480),(840,490),(900,490)],w=2.4)
text(705,505,"R-101 · catalyst tubes (LSTN 650)",10.5,weight=600)
text(705,519,"steam reformer · 600–650°C, 1 bar",9,color=SUB)
text(840,272,"F-101",16,weight=700); text(840,289,"Reformer furnace",9,color=SUB)
for bx in (680,780):
    a(f'<path d="M{bx-10},560 L{bx},540 L{bx+10},560 Z" fill="#fff" stroke="#16202b" stroke-width="1.3"/>')
    line([(bx,560),(bx,620)])
line([(330,620),(800,620)],w=2); text(540,612,"fuel gas header",8.5,color=SUB)
# combustion air (inbound from right)
offpage(1020,690,"Combustion air","left",150,"FD fan · tag TBC")
line([(1020,690),(870,690),(870,562)],arrow=True)
hv(950,690); text(950,678,"damper",8,color=SUB)

# ===== Flue gas =====
step("Flue gas → CCU · AT-101 (O₂)")
line([(860,205),(860,190),(1250,190)])
offpage(1250,190,"To B-201 → CCU","right",140,"Flue gas · C-201")
bubble(1200,145,"AT","101","O₂"); line([(1200,165),(1200,190)])

# ===== Flame detection =====
step("Flame detection BE-101")
bubble(545,470,"BE","101","BSL",nside="left"); line([(565,470),(580,470)])
line([(545,490),(545,522)],dash=True,arrow=True); text(545,535,"to I-101",8.5,color=NOTE,family=MONO)

# ===== Syngas outlet =====
step("Syngas outlet · TT/PT · PCV-101 · PSV-101")
line([(900,490),(1260,490)])
offpage(1260,490,"To E-101 → R-102","right",135,"Syngas · ~600°C")
bubble(940,440,"TT","101"); line([(940,460),(940,490)])
bubble(990,440,"TT","102","TSHH"); line([(990,460),(990,490)])
bubble(1060,440,"PT","101"); line([(1060,460),(1060,490)])
bubble(1110,440,"PT","102","PSHH"); line([(1110,460),(1110,490)])
bubble(940,370,"TIC","101","TAH/TAL",nside="left"); line([(940,420),(940,390)],dash=True)
bubble(1060,370,"PIC","101","PAH/PAL"); line([(1060,420),(1060,390)],dash=True)
valve(1225,490,act="dia",label="PCV-101",fail="FO")
line([(1080,370),(1225,370),(1225,470)],dash=True)
line([(1160,490),(1160,540)]); psv(1160,558,"PSV-101")
text(1146,574,"set P TBC",8.5,"end",color=NOTE,family=MONO)
line([(1178,558),(1260,558)]); offpage(1260,558,"To Flare","right",120)
line([(1010,490),(1010,520)]); hv(1010,527,vertical=True,s=5); text(1020,531,"D",9,"start",weight=600)
line([(1085,490),(1085,520)]); hv(1085,527,vertical=True,s=5); text(1095,531,"SP-101",8.5,"start",weight=600,family=MONO)

# ===== Fuel lines =====
step("Fuel: PSA tail gas + NG makeup")
offpage(20,620,"From PS-101","right",150,"PSA tail gas · Stream 16")
line([(170,620),(330,620)])
valve(300,620,act="esd",label="XV-103",fail="FC")
line([(230,620),(230,690),(330,690)]); valve(230,660,vertical=True,act="side")
text(212,656,"XV-104",9.5,"end",weight=600,family=MONO); text(212,668,"FO",8.5,"end",color=NOTE,family=MONO)
offpage(330,690,"To Flare","right",110)
offpage(20,755,"Natural gas makeup","right",150,"supplemental · 2.15 MW")
line([(170,755),(600,755),(600,620)])
valve(300,755,act="esd",label="XV-101",fail="FC")
valve(470,755,act="dia",label="TCV-101",fail="FC")

# ===== TIC + FIC feed-forward → TY → TCV =====
step("Control: TIC-101 + feed-forward → TCV-101")
bubble(470,300,"TY","101","Σ FF")
line([(940,350),(940,128),(425,128),(425,300),(450,300)],dash=True)
line([(320,70),(470,70),(470,280)],dash=True)
line([(470,320),(470,727)],dash=True)

# ===== I-101 interlock =====
step("I-101 SIS / ESD logic")
a('<rect x="700" y="62" width="64" height="56" fill="#fff" stroke="#16202b" stroke-width="1.5"/>')
a('<path d="M732,66 L760,90 L732,114 L704,90 Z" fill="#fff" stroke="#16202b" stroke-width="1.5"/>')
text(732,88,"I",11,weight=700,family=MONO); text(732,103,"101",9,family=MONO)
text(694,108,"SIS / ESD logic",8.5,"end",color=SUB)
line([(390,95),(390,45),(690,45),(690,80),(700,80)],dash=True,arrow=True)
line([(990,420),(990,100),(764,100)],dash=True,arrow=True)
line([(1110,420),(1110,110),(990,110)],dash=True)
text(775,62,"trip: FALL-102 · TSHH-102 · PSHH-102 · BSL-101",8.5,"start",color=NOTE,family=MONO)
text(775,75,"→ close XV-101/102/103 · open XV-104",8.5,"start",color=NOTE,family=MONO)
line([(732,62),(732,18),(270,18),(270,727)],dash=True)
line([(270,140),(505,140)],dash=True)
line([(270,592),(300,592)],dash=True)
line([(270,660),(258,660)],dash=True)
line([(270,727),(300,727)],dash=True)

# ===== deltas =====
step("Δ markers")
for n,(x,y) in {"1":(345,655),"2":(535,140),"3":(358,108),"4":(790,330),"5":(1205,598),"6":(1255,455),"7":(985,355),"8":(1340,462),"9":(575,442),"10":(452,226)}.items():
    delta(x,y,n)

# ===== legend + title =====
step("Legend + title block")
a('<rect x="20" y="805" width="1360" height="45" fill="#fff" stroke="#16202b" stroke-width="1.3"/>')
line([(35,828),(75,828)]); text(82,832,"process line",9,"start")
line([(170,828),(210,828)],dash=True); text(217,832,"signal (electrical)",9,"start")
a('<circle cx="330" cy="828" r="9" fill="#fff" stroke="#16202b"/><line x1="321" y1="828" x2="339" y2="828" stroke="#16202b"/>'); text(345,832,"instrument · control room",9,"start")
delta(500,828,"n"); text(516,832,"แก้ตาม finding #n",9,"start")
text(640,832,"FC = fail closed · FO = fail open",9,"start",color=NOTE)
text(880,832,"TBC = ต้องยืนยันข้อมูล",9,"start",color=NOTE)
text(1370,824,"P&ID R-101 / F-101 · REV B (เฉลย draft)",10.5,"end",weight=700)
text(1370,839,"ETHAVERTEX · for review — not issued",8.5,"end",color=SUB)
a('</g>'); a('</svg>')
open(sys.argv[1],'w').write("\n".join(o))
