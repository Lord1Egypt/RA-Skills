# -*- coding: utf-8 -*-
"""
示例：马克杯自动建模（杯体旋转 + 把手拉伸）
尺寸参数在顶部修改。运行: python build_mug.py [输出目录]
"""
import os, sys, math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sw_api import *   # connect, new_part, refplanes, ...

# ---- 参数（米） ----
R_OUT, R_IN = 0.040, 0.036     # 杯体外/内半径 (Ø80, 壁厚4mm)
H, BOTTOM   = 0.100, 0.005     # 杯高, 底厚
HANDLE_RO, HANDLE_RI = 0.028, 0.016
HANDLE_T = 0.012               # 把手厚度(中面拉伸)

OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
SLDPRT = os.path.join(OUT_DIR, "马克杯.SLDPRT")
PNG    = os.path.join(OUT_DIR, "马克杯预览.png")

sw = connect()
close_all(sw)
model, sm, fm, ext = new_part(sw)

# ---- 1. 杯体：前视基准面 L 形截面 + 旋转 360° ----
front = refplanes(model)[0]
model.ClearSelection2(True)
front.Select2(False, 0)
sm.InsertSketch(True)                       # 进入草图（退出也是同一个方法）

pts = [(0.0, 0.0), (R_OUT, 0.0), (R_OUT, H), (R_IN, H), (R_IN, BOTTOM), (0.0, BOTTOM)]
for i in range(len(pts)):
    x1, y1 = pts[i]
    x2, y2 = pts[(i + 1) % len(pts)]
    sm.CreateLine(x1, y1, 0.0, x2, y2, 0.0)
sm.CreateCenterLine(0.0, -0.01, 0.0, 0.0, H + 0.01, 0.0)   # 旋转轴 = y 轴
sm.InsertSketch(True)                       # 退出草图

sketch1 = last_feature(model)
log("cup sketch: " + sketch1.Name)
model.ClearSelection2(True)
sketch1.Select2(False, 0)

rev = fm.FeatureRevolve2(True, True, False, False, False, False,
                         0, 0, 2 * math.pi, 0.0,
                         False, False, 0.0, 0.0, 0, 0.0, 0.0,
                         True, True, True)
if rev is None:
    sys.exit("FATAL: revolve failed")
log("revolve OK: " + wrap(rev, "IFeature").Name)

# ---- 2. 把手：右视基准面半圆环 + 中面拉伸 ----
right = refplanes(model)[2]
model.ClearSelection2(True)
right.Select2(False, 0)
sm.InsertSketch(True)

cx, cy = R_OUT, H / 2                        # 圆心贴在杯壁, 高度居中
top_o, bot_o = (cx, cy + HANDLE_RO), (cx, cy - HANDLE_RO)
top_i, bot_i = (cx, cy + HANDLE_RI), (cx, cy - HANDLE_RI)
mid_o, mid_i = (cx + HANDLE_RO, cy), (cx + HANDLE_RI, cy)
sm.Create3PointArc(top_o[0], top_o[1], 0.0, bot_o[0], bot_o[1], 0.0, mid_o[0], mid_o[1], 0.0)
sm.Create3PointArc(bot_i[0], bot_i[1], 0.0, top_i[0], top_i[1], 0.0, mid_i[0], mid_i[1], 0.0)
sm.CreateLine(top_o[0], top_o[1], 0.0, top_i[0], top_i[1], 0.0)
sm.CreateLine(bot_o[0], bot_o[1], 0.0, bot_i[0], bot_i[1], 0.0)
sm.InsertSketch(True)

sketch2 = last_feature(model)
log("handle sketch: " + sketch2.Name)
model.ClearSelection2(True)
sketch2.Select2(False, 0)

feat = fm.FeatureExtrusion2(True, False, False, 6, 0, HANDLE_T, HANDLE_T,
                            False, False, False, False, 0.0, 0.0,
                            False, False, False, False,
                            True, True, True, 0, 0.0, False)   # T1=6 中面
if feat is None:
    log("WARN: handle extrude failed")
else:
    log("extrude OK: " + wrap(feat, "IFeature").Name)

# ---- 3. 保存 + 验证 ----
iso_view(model)
save_part(ext, SLDPRT)
export_png(model, ext, PNG)

v = volume(ext)
theory = math.pi * (R_OUT**2 * H - R_IN**2 * (H - BOTTOM)) \
       + 0.5 * math.pi * (HANDLE_RO**2 - HANDLE_RI**2) * HANDLE_T
if v:
    log("volume=%.6e  theory=%.6e  diff=%.1f%%" % (v, theory, abs(v - theory) / theory * 100))
log("DONE")
