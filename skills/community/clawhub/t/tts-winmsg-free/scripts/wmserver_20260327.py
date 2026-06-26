# -*- coding: utf-8 -*-
"""winmsg-tts v1.3 - 精确关闭quit机制"""
import ctypes, win32gui, subprocess, threading, queue, os, base64, re
import tkinter as tk

SD = os.path.dirname(os.path.abspath(__file__))
CD = os.path.join(os.path.dirname(SD), "config")
os.makedirs(CD, exist_ok=True)
HWND_F = os.path.join(CD, "wmserver_hwnd.txt")
SPD_F  = os.path.join(CD, "tts_speed.txt")
VOL_F  = os.path.join(CD, "volume.txt")

try:
    with open(SPD_F) as f: init_spd = int(f.read().strip())
except: init_spd = 0
try:
    with open(VOL_F) as f: init_vol = int(f.read().strip())
except: init_vol = 100

cs, cv = init_spd, init_vol
playq = queue.Queue()

class CDS(ctypes.Structure):
    _fields_ = [("d",ctypes.c_longlong),("b",ctypes.c_ulong),("p",ctypes.c_wchar_p)]

lbl_ref = [None]
root_ref = [None]

def play_one(t):
    global cs, cv
    for fn, gv in [(SPD_F,"cs"),(VOL_F,"cv")]:
        try:
            with open(fn) as f:
                v = int(f.read().strip())
                if gv == "cs": cs = v
                else: cv = v
        except: pass
    r = root_ref[0]
    if r:
        r.after(0, lambda: lbl_ref[0].config(text=t))
    cmd = (
        f"Add-Type -AssemblyName System.Speech; "
        f"$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.Rate={cs};$s.Volume={cv};$s.Speak('{t.replace(chr(39),chr(39)+chr(39))}')"
    )
    b64 = base64.b64encode(cmd.encode("utf-16-le")).decode()
    subprocess.run(
        ["powershell","-ExecutionPolicy","Bypass","-NoProfile",
         "-EncodedCommand", b64],
        timeout=30, capture_output=True,
        creationflags=0x08000000)

def pq():
    while True:
        t = playq.get(block=True)
        play_one(t)

def Wp(h,m,w,l):
    if m == 0x4A:
        d = ctypes.cast(l, ctypes.POINTER(CDS)).contents
        if d.p:
            txt = d.p
            # quit 命令：精确关闭自己的窗口
            if txt == "__QUIT__":
                r = root_ref[0]
                if r:
                    r.after(0, lambda: r.quit())
                return 0
            if lbl_ref[0]:
                lbl_ref[0].config(text=txt)
            # 按标点分割，保留标点在句子末尾
            pattern = r'([。；：！？…….,;:!?])'
            parts = re.split(pattern, txt)
            i = 0
            while i < len(parts):
                seg = ""
                if i + 1 < len(parts) and parts[i + 1] in '。；：！？…….,;:!?':
                    seg = parts[i].strip() + parts[i + 1]
                    i += 2
                elif parts[i].strip():
                    seg = parts[i].strip()
                    i += 1
                else:
                    i += 1
                if seg:
                    playq.put(seg)
        return 0
    return win32gui.DefWindowProc(h,m,w,l)

wc = win32gui.WNDCLASS()
wc.lpfnWndProc = Wp
wc.lpszClassName = "JCls"
win32gui.RegisterClass(wc)

root = tk.Tk()
root.title("Jarvis TTS")
root.geometry("320x90")
root.overrideredirect(True)
root.attributes("-topmost", True)
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.geometry(f"320x90+{sw-320-10}+{sh-90-60}")
root.configure(bg="#2d2d2d")
root_ref[0] = root

lbl = tk.Label(root, text="等待中...",
               font=("微软雅黑", 10, "bold"),
               fg="#FFFFFF", bg="#2d2d2d",
               anchor="w", justify="left")
lbl.place(x=10, y=10, width=300, height=25)
lbl_ref[0] = lbl

class WS:
    def __init__(self, master, x, y, cw, lo, hi, init, ll, lr, cb):
        self.cb = cb
        self.cv = tk.Canvas(master, width=cw, height=16, bg="#2d2d2d", highlightthickness=0, cursor="hand2")
        self.cv.place(x=x, y=y)
        self.cv.create_rectangle(0, 6, cw, 10, fill="#555555", outline="")
        self.lo, self.hi, self.cw = lo, hi, cw
        self.val = init
        px = self._v2p(init)
        self.handle = self.cv.create_oval(px-5, 1, px+5, 11, fill="#FFFFFF", outline="")
        self.cv.bind("<Button-1>", self._c)
        self.cv.bind("<B1-Motion>", self._m)
        tk.Label(master, text=ll, font=("微软雅黑",8), fg="#888888", bg="#2d2d2d").place(x=x, y=y-1)
        tk.Label(master, text=lr, font=("微软雅黑",8), fg="#888888", bg="#2d2d2d").place(x=x+cw-12, y=y-1)

    def _p2v(self, px): return int(self.lo + max(0,min(1,px/self.cw))*(self.hi-self.lo))
    def _v2p(self, v): return int((v-self.lo)/(self.hi-self.lo)*self.cw)
    def _redraw(self):
        px = self._v2p(self.val)
        self.cv.coords(self.handle, px-5, 1, px+5, 11)
    def _c(self, e):
        self.val = self._p2v(e.x); self._redraw(); self.cb(self.val)
    def _m(self, e):
        if 0 <= e.x <= self.cw:
            self.val = self._p2v(e.x); self._redraw(); self.cb(self.val)

def s(v): global cs; cs=int(v); open(SPD_F,"w").write(str(cs))
def vv(v): global cv; cv=int(v); open(VOL_F,"w").write(str(cv))

WS(root, 24, 42, 270, -10, 10,  init_spd, "慢", "快", s)
WS(root, 24, 62, 270,   0, 100, init_vol, "小", "大", vv)

h = win32gui.CreateWindowEx(0,"JCls","JSer",0,0,0,0,0,0,0,0,None)
with open(HWND_F,"w") as f: f.write(str(h))
print("HWND=" + str(h), flush=True)

threading.Thread(target=pq, daemon=True).start()
root.mainloop()
