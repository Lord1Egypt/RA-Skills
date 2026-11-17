# -*- coding: utf-8 -*-
"""起重吊钩: 前视面样条曲线路径(单段, 避免多段接头失败) + CircularProfile 圆形截面扫描 + 顶部凸缘"""
import os, sys, math, pythoncom
import win32com.client as wc
sys.path.insert(0, r"C:\Users\Administrator\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills\solidworks-modeling\scripts")
from sw_api import *

HOOK_D  = 0.012          # 钩体截面直径
SHANK_L = 0.055          # 直柄长
ARC_R   = 0.022          # 弯钩半径
COLLAR_R, COLLAR_L = 0.010, 0.012

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SLDPRT = os.path.join(OUT_DIR, "吊钩.SLDPRT")

sw = connect()
close_all(sw)
model, sm, fm, ext = new_part(sw)
front, top = planes0 = refplanes(model)[:2]

# ---- 1. 样条路径(前视面): 竖直柄 + J 形弯钩, 单段保证相切连续 ----
pts = [(0.0, SHANK_L), (0.0, SHANK_L*0.66), (0.0, SHANK_L*0.33), (0.0, 0.0)]
cx, cy = ARC_R, 0.0
for ang in (225, 270, 315, 360, 30):
    pts.append((cx + ARC_R*math.cos(math.radians(ang)), cy + ARC_R*math.sin(math.radians(ang))))
flat = []
for x, y in pts:
    flat += [x, y, 0.0]

model.ClearSelection2(True); front.Select2(False, 0); sm.InsertSketch(True)
sm.AddToDB = True
sp = sm.CreateSpline(wc.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, flat))
sm.AddToDB = False
sm.InsertSketch(True)
try: model.EditRebuild3()
except Exception: pass
assert sp is not None, "spline failed"
path_sk = last_feature(model)
log("path sketch: %s (spline, %d pts)" % (path_sk.Name, len(pts)))

# ---- 2. 圆形截面扫描: 路径用 SelectByID2 Mark=4, Merge=False(首实体必须) ----
model.ClearSelection2(True)
ok = ext.SelectByID2(path_sk.Name, "SKETCH", 0, 0, 0, True, 4, None, 0)
feat = fm.InsertProtrusionSwept4(False, False, 0, False, False, 0, 0,
                                 False, 0.0, 0.0, 0, 0,
                                 False, True, True, 0.0, True,
                                 True, HOOK_D, False)
assert feat is not None, "sweep failed"
log("sweep OK: %s (d=%.0fmm)" % (feat.Name, HOOK_D * 1000))

# ---- 3. 顶部凸缘(上视面圆, 圆心在柄顶投影点即原点, 沿 +Y 拉伸) ----
model.ClearSelection2(True); top.Select2(False, 0); sm.InsertSketch(True)
sm.AddToDB = True
sm.CreateCircle(0.0, 0.0, 0.0, COLLAR_R, 0.0, 0.0)
sm.AddToDB = False
sm.InsertSketch(True)
model.ClearSelection2(True); last_feature(model).Select2(False, 0)
col = None
for dr in (True, False):
    col = fm.FeatureExtrusion2(True, False, dr, 0, 0, COLLAR_L, 0.0,
                               False, False, False, False, 0.0, 0.0,
                               False, False, False, False,
                               True, True, True, 0, 0.0, False)
    if col is not None:
        log("collar OK (Dir=%s)" % dr)
        break
assert col is not None, "collar failed"

# ---- 4. 保存 + 双视角渲染 ----
save_part(ext, SLDPRT)
iso_view(model)
export_png(model, ext, os.path.join(OUT_DIR, "吊钩预览.png"))
model.ShowNamedView2("*前视", 1); model.ViewZoomtofit2()
ext.SaveAs(os.path.join(OUT_DIR, "吊钩正视图.png"), 0, 1, None, 0, 0)
log("volume=%.6e" % (volume(ext) or -1))
log("DONE")
