# -*- coding: utf-8 -*-
"""放样吊钩(锻造型): 11 个水平圆轮廓沿问号形脊线变径放样 + 顶部凸缘
   脊线 y 单调下降 -> 每个轮廓独占一张偏移参考面(constraint 8)"""
import os, sys, math
sys.path.insert(0, r"C:\Users\Administrator\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills\solidworks-modeling\scripts")
from sw_api import *

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SLDPRT = os.path.join(OUT_DIR, "放样吊钩.SLDPRT")

# 站位: (脊线x mm, 高度y mm, 半径mm)  y 严格单调下降
# 注意: 负偏移参考面会导致放样失败(实测), 整体抬高 30mm 使所有 y>=0
ARC_R = 22.0
LIFT = 30.0
stations = [(0.0, 55.0, 8.0), (0.0, 45.0, 7.0), (0.0, 35.0, 6.5),
            (0.0, 25.0, 6.5), (0.0, 15.0, 6.5), (0.0, 6.0, 7.0)]
for ang, r in ((200, 7.5), (225, 7.0), (250, 6.0), (270, 2.5)):
    stations.append((ARC_R + ARC_R*math.cos(math.radians(ang)),
                     ARC_R*math.sin(math.radians(ang)), r))
stations = [(x, y + LIFT, r) for x, y, r in stations]
ys = [s[1] for s in stations]
assert all(ys[i] > ys[i+1] for i in range(len(ys)-1)), "y 必须单调"

sw = connect()
close_all(sw)
model, sm, fm, ext = new_part(sw)
top = refplanes(model)[1]

# ---- 1. 每站位: 偏移参考面 + 圆轮廓 ----
sketches = []
for x, y, r in stations:
    if abs(y) < 1e-9:
        pname = "上视基准面"
    else:
        model.ClearSelection2(True)
        ext.SelectByID2("上视基准面", "PLANE", 0, 0, 0, False, 0, None, 0)
        rp = fm.InsertRefPlane(8, y / 1000.0, 0, 0.0, 0, 0.0)
        assert rp is not None, "refplane failed y=%s" % y
        pname = rp.Name
    model.ClearSelection2(True)
    ext.SelectByID2(pname, "PLANE", 0, 0, 0, False, 0, None, 0)
    sm.InsertSketch(True)
    sm.AddToDB = True
    c = sm.CreateCircle(x / 1000.0, 0.0, 0.0, (x + r) / 1000.0, 0.0, 0.0)
    sm.AddToDB = False
    sm.InsertSketch(True)
    assert c is not None, "circle failed y=%s" % y
    sk = last_feature(model)
    sketches.append(sk)
log("profiles: %d sketches" % len(sketches))

# ---- 2. 放样: 轮廓按序 Mark=1 ----
model.ClearSelection2(True)
for sk in sketches:
    ok = ext.SelectByID2(sk.Name, "SKETCH", 0, 0, 0, True, 1, None, 0)
    assert ok, "select failed %s" % sk.Name
feat = fm.InsertProtrusionBlend(False, False, False, 0.0, 0, 0,
                                1.0, 1.0, False, False,
                                False, 0.0, 0.0, 0,
                                False, True, True)
assert feat is not None, "loft failed"
log("loft OK: %s" % feat.Name)

# ---- 3. 顶部凸缘: 最顶站位面(y=55)上 Ø20 圆向上拉伸 ----
model.ClearSelection2(True)
ext.SelectByID2(sketches[0].Name, "SKETCH", 0, 0, 0, False, 0, None, 0)  # 其所在面
# 直接用第一张偏移面重画 Ø20 圆
model.ClearSelection2(True)
ext.SelectByID2("基准面1", "PLANE", 0, 0, 0, False, 0, None, 0)
sm.InsertSketch(True)
sm.AddToDB = True
sm.CreateCircle(0.0, 0.0, 0.0, 0.010, 0.0, 0.0)
sm.AddToDB = False
sm.InsertSketch(True)
model.ClearSelection2(True); last_feature(model).Select2(False, 0)
col = None
for dr in (True, False):
    col = fm.FeatureExtrusion2(True, False, dr, 0, 0, 0.012, 0.0,
                               False, False, False, False, 0.0, 0.0,
                               False, False, False, False,
                               True, True, True, 0, 0.0, False)
    if col is not None:
        log("collar OK (Dir=%s)" % dr)
        break
assert col is not None, "collar failed"

# ---- 3.5 凸缘上下棱边圆角(几何遍历定位): 顶圈 y=85 r=10 倒 2mm, 底圈 y=73 r=10 倒 1.5mm ----
assert fillet_circle_edge(model, fm, 0.085, 0.010, 0.002) is not None, "top fillet failed"
assert fillet_circle_edge(model, fm, 0.073, 0.010, 0.0015) is not None, "bottom fillet failed"

# ---- 4. 隐藏参考面 + 保存 + 双视角渲染 ----
model.ClearSelection2(True)
for i in range(1, 12):
    if ext.SelectByID2("基准面%d" % i, "PLANE", 0, 0, 0, True, 0, None, 0):
        pass
try: model.BlankRefGeom()
except Exception: pass
save_part(ext, SLDPRT)
iso_view(model)
export_png(model, ext, os.path.join(OUT_DIR, "放样吊钩预览.png"))
model.ShowNamedView2("*前视", 1); model.ViewZoomtofit2()
ext.SaveAs(os.path.join(OUT_DIR, "放样吊钩正视图.png"), 0, 1, None, 0, 0)
log("volume=%.6e" % (volume(ext) or -1))
log("DONE")
