import sys
o=[]
def a(s): o.append(s)
INK="#16202b"; RED="#d6283f"; NOTE="#3d4a57"; SUB="#456"
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

