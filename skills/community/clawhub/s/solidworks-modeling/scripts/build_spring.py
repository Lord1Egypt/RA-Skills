# -*- coding: utf-8 -*-
"""弹簧: 圆草图 → InsertHelix 螺旋线 → CircularProfile 扫描"""
import os, sys
sys.path.insert(0, r"C:\Users\Administrator\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills\solidworks-modeling\scripts")
from sw_api import *

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SLDPRT = os.path.join(OUT_DIR, "弹簧.SLDPRT")

sw = connect()
close_all(sw)
model, sm, fm, ext = new_part(sw)
top = refplanes(model)[1]

# ---- 1. 螺旋线: 选中 Ø40 圆草图后 InsertHelix ----
model.ClearSelection2(True); top.Select2(False, 0); sm.InsertSketch(True)
sm.AddToDB = True
sm.CreateCircle(0.0, 0.0, 0.0, 0.020, 0.0, 0.0)
sm.AddToDB = False
sm.InsertSketch(True)
model.ClearSelection2(True)
last_feature(model).Select2(False, 0)
helix = None
for hd in (0, 1, 2):   # Helixdef: 0=螺距+圈数?
    r = model.InsertHelix(False, False, False, False, hd, 0.050, 0.005, 10, 0.0, 0.0)
    helix = last_feature(model)
    if helix and ("螺旋" in helix.Name or "Helix" in helix.Name or "Curve" in val(helix.GetTypeName2)):
        log("helix OK (Helixdef=%d): %s" % (hd, helix.Name))
        break
    log("helix try Helixdef=%d ret=%s last=%s" % (hd, r, helix.Name if helix else None))
assert helix is not None, "helix failed"

# ---- 2. 圆形截面扫描: 螺旋线 Mark=4, Merge=False ----
feat = None
for seltype in ("REFERENCECURVES", "HELIX", "EXTSKETCHSEGMENT"):
    model.ClearSelection2(True)
    ok = ext.SelectByID2(helix.Name, seltype, 0, 0, 0, True, 4, None, 0)
    log("select %s as %s -> %s" % (helix.Name, seltype, ok))
    if not ok:
        continue
    feat = fm.InsertProtrusionSwept4(False, False, 0, False, False, 0, 0,
                                     False, 0.0, 0.0, 0, 0,
                                     False, True, True, 0.0, True,
                                     True, 0.003, False)
    if feat is not None:
        log("sweep OK: %s" % feat.Name)
        break
assert feat is not None, "sweep failed"

# ---- 3. 保存 + 渲染 ----
model.ClearSelection2(True)
ext.SelectByID2(helix.Name, "REFERENCECURVES", 0, 0, 0, True, 0, None, 0)
try: model.BlankRefGeom()   # 隐藏螺旋参考曲线, 否则蓝色线框刷屏
except Exception: pass
model.ClearSelection2(True)
save_part(ext, SLDPRT)
iso_view(model)
export_png(model, ext, os.path.join(OUT_DIR, "弹簧预览.png"))
log("volume=%.6e" % (volume(ext) or -1))
log("DONE")
