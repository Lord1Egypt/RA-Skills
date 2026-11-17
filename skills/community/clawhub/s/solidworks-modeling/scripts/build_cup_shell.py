# -*- coding: utf-8 -*-
"""抽壳水杯: 实心圆柱 → 选中顶面 → InsertFeatureShell 2mm → 杯口棱边圆角"""
import os, sys
sys.path.insert(0, r"C:\Users\Administrator\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills\solidworks-modeling\scripts")
from sw_api import *

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SLDPRT = os.path.join(OUT_DIR, "薄壁水杯.SLDPRT")

sw = connect()
close_all(sw)
model, sm, fm, ext = new_part(sw)
top = refplanes(model)[1]

# ---- 1. 实心圆柱 Ø60 x 70mm ----
model.ClearSelection2(True); top.Select2(False, 0); sm.InsertSketch(True)
sm.AddToDB = True
sm.CreateCircle(0.0, 0.0, 0.0, 0.030, 0.0, 0.0)
sm.AddToDB = False
sm.InsertSketch(True)
model.ClearSelection2(True); last_feature(model).Select2(False, 0)
boss = None
for dr in (True, False):
    boss = fm.FeatureExtrusion2(True, False, dr, 0, 0, 0.070, 0.0,
                                False, False, False, False, 0.0, 0.0,
                                False, False, False, False,
                                True, True, True, 0, 0.0, False)
    if boss is not None:
        log("boss OK (Dir=%s)" % dr)
        break
assert boss is not None, "boss failed"

# ---- 2. 顶面抽壳 2mm (顶面高度从几何实测: r=30 圆边的最大 cy) ----
ces = circle_edges(model)
top_y = max(p[1] for e, p in ces if abs(p[6] - 0.030) < 0.0005)
log("cylinder spans to top_y=%.1fmm" % (top_y * 1000))
model.ClearSelection2(True)
ok = ext.SelectByID2("", "FACE", 0.0, top_y, 0.0, True, 0, None, 0)
log("top face select=%s" % ok)
model.InsertFeatureShell(0.002, False)   # 返回值恒 None! 用特征树+错误码验证
shell = None
for f in all_features(model):
    if "抽壳" in f.Name:
        err = f.GetErrorCode2(False)
        if (err[0] if isinstance(err, tuple) else err) == 0:
            shell = f
assert shell is not None, "shell failed"
log("shell OK: %s" % shell.Name)

# ---- 3. 杯口棱边圆角 R1 ----
model.EditRebuild3()
fillet_circle_edge(model, fm, top_y, 0.030, 0.001)

# ---- 4. 保存 + 渲染 ----
save_part(ext, SLDPRT)
iso_view(model)
export_png(model, ext, os.path.join(OUT_DIR, "薄壁水杯预览.png"))
model.ShowNamedView2("*前视", 1); model.ViewZoomtofit2()
ext.SaveAs(os.path.join(OUT_DIR, "薄壁水杯正视图.png"), 0, 1, None, 0, 0)
log("volume=%.6e" % (volume(ext) or -1))
log("DONE")
