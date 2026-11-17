# -*- coding: utf-8 -*-
"""法兰盘: 圆盘拉伸 → 单孔切除 → FeatureCircularPattern4 圆周阵列 6 孔"""
import os, sys, math
sys.path.insert(0, r"C:\Users\Administrator\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills\solidworks-modeling\scripts")
from sw_api import *

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SLDPRT = os.path.join(OUT_DIR, "法兰盘.SLDPRT")

sw = connect()
close_all(sw)
model, sm, fm, ext = new_part(sw)
top = refplanes(model)[1]

# ---- 1. 圆盘 Ø80 x 10mm ----
model.ClearSelection2(True); top.Select2(False, 0); sm.InsertSketch(True)
sm.AddToDB = True
sm.CreateCircle(0.0, 0.0, 0.0, 0.040, 0.0, 0.0)
sm.AddToDB = False
sm.InsertSketch(True)
model.ClearSelection2(True); last_feature(model).Select2(False, 0)
boss = None
for dr in (True, False):
    boss = fm.FeatureExtrusion2(True, False, dr, 0, 0, 0.010, 0.0,
                                False, False, False, False, 0.0, 0.0,
                                False, False, False, False,
                                True, True, True, 0, 0.0, False)
    if boss is not None:
        break
assert boss is not None, "boss failed"
log("disk OK")

# ---- 2. 单孔 Ø10 @ 半径 30mm, 完全贯穿 ----
model.ClearSelection2(True); top.Select2(False, 0); sm.InsertSketch(True)
sm.AddToDB = True
sm.CreateCircle(0.030, 0.0, 0.0, 0.035, 0.0, 0.0)
sm.AddToDB = False
sm.InsertSketch(True)
model.ClearSelection2(True); last_feature(model).Select2(False, 0)
cut = None
for dr in (True, False):
    cut = fm.FeatureCut3(True, False, dr, 1, 0, 0.01, 0.0,
                         False, False, False, False, 0.0, 0.0,
                         False, False, False, False,
                         False, True, True, True,
                         False, False, 0, 0.0, False)
    if cut is not None:
        log("hole OK (Dir=%s)" % dr)
        break
assert cut is not None, "hole cut failed"

# ---- 3. 圆周阵列 6x: 选孔特征(Mark=0) + 圆柱面作轴(Mark=1) ----
disk_top_y = max(p[1] for e, p in circle_edges(model) if abs(p[6] - 0.040) < 0.0005)
pat = None
for fmark, amark in ((0, 1), (4, 1), (0, 0)):
    model.ClearSelection2(True)
    if not cut.Select2(False, fmark):
        continue
    ok = ext.SelectByID2("", "FACE", 0.040, disk_top_y - 0.005, 0.0, True, amark, None, 0)
    if not ok:
        log("axis face pick fail (fmark=%d amark=%d)" % (fmark, amark))
        continue
    pat = fm.FeatureCircularPattern4(6, 2.0 * math.pi, False, "", False, True, False)
    if pat is not None:
        log("pattern OK (fmark=%d amark=%d): %s" % (fmark, amark, pat.Name))
        break
    log("pattern FAIL (fmark=%d amark=%d)" % (fmark, amark))
if pat is None:
    # 树验证(假失败可能性)
    for f in all_features(model):
        if "阵列" in f.Name or "Pattern" in f.Name:
            pat = f
            log("pattern found in tree: %s" % f.Name)
            break
assert pat is not None, "pattern failed"

# ---- 4. 保存 + 渲染 ----
model.ClearSelection2(True)
save_part(ext, SLDPRT)
iso_view(model)
export_png(model, ext, os.path.join(OUT_DIR, "法兰盘预览.png"))
log("volume=%.6e" % (volume(ext) or -1))
log("DONE")
