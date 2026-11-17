# -*- coding: utf-8 -*-
"""
花朵建模（solidworks-modeling 技能包实战测试）
结构: 花茎(拉伸) + 6花瓣(单草图多轮廓拉伸, 偏移起始) + 叶子(拉伸) + 花心(旋转球)
"""
import os, sys, math

SKILL_SCRIPTS = r"C:\Users\Administrator\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills\solidworks-modeling\scripts"
sys.path.insert(0, SKILL_SCRIPTS)
from sw_api import *   # connect/new_part/refplanes/last_feature/save_part/export_png/volume/...

# ---- 参数（米） ----
STEM_R, STEM_H   = 0.005, 0.1015     # 花茎半径/高(顶端高出花瓣板, 避免面-面相切导致合并失败)
PETAL_N          = 6                 # 花瓣数
PETAL_R0, PETAL_R1 = 0.004, 0.040    # 花瓣基部(伸进花茎内)/尖端半径; R0>=4mm 低于此值 SW 拒绝建弧
PETAL_HALF_ANG   = math.radians(28)  # 花瓣半张角
PETAL_T          = 0.003             # 花瓣厚度
PETAL_Y0         = 0.098             # 花瓣板起始高度(嵌入茎身)
CENTER_R         = 0.015             # 花心球半径

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
SLDPRT = os.path.join(OUT_DIR, "花朵.SLDPRT")
PNG    = os.path.join(OUT_DIR, "花朵预览.png")

sw = connect()
close_all(sw)
model, sm, fm, ext = new_part(sw)
top, front = refplanes(model)[1], refplanes(model)[0]

def extrude(t1, d1, t0=0, start_offset=0.0):
    return fm.FeatureExtrusion2(True, False, False, t1, 0, d1, 0.0,
                                False, False, False, False, 0.0, 0.0,
                                False, False, False, False,
                                True, True, True, t0, start_offset, False)

# ---- 1. 花茎：上视基准面圆 + 拉伸 ----
model.ClearSelection2(True); top.Select2(False, 0); sm.InsertSketch(True)
sm.CreateCircle(0.0, 0.0, 0.0, STEM_R, 0.0, 0.0)
sm.InsertSketch(True)
model.ClearSelection2(True); last_feature(model).Select2(False, 0)
f = extrude(0, STEM_H)                        # 盲孔拉伸 STEM_H
assert f is not None, "stem extrude failed"
log("stem OK: " + wrap(f, "IFeature").Name)

# ---- 2. 花瓣：每瓣独立草图(双弧月牙形) + 偏移拉伸到茎顶并合并 ----
# 花瓣基部(R0=4mm)伸进花茎(R=5mm)内部，保证与茎合并为单一实体
for k in range(PETAL_N):
    a = 2 * math.pi * k / PETAL_N
    p1 = (PETAL_R0 * math.cos(a - PETAL_HALF_ANG), PETAL_R0 * math.sin(a - PETAL_HALF_ANG))
    p2 = (PETAL_R0 * math.cos(a + PETAL_HALF_ANG), PETAL_R0 * math.sin(a + PETAL_HALF_ANG))
    tip   = (PETAL_R1 * math.cos(a), PETAL_R1 * math.sin(a))
    belly = (PETAL_R0 * 3 * math.cos(a), PETAL_R0 * 3 * math.sin(a))
    model.ClearSelection2(True); top.Select2(False, 0); sm.InsertSketch(True)
    sm.Create3PointArc(p1[0], p1[1], 0.0, p2[0], p2[1], 0.0, tip[0], tip[1], 0.0)      # 外弧
    sm.Create3PointArc(p2[0], p2[1], 0.0, p1[0], p1[1], 0.0, belly[0], belly[1], 0.0)  # 内弧
    sm.InsertSketch(True)
    model.ClearSelection2(True); last_feature(model).Select2(False, 0)
    # T0=3 从草图面偏移，嵌入茎身保证合并；失败时降级为不合并多实体
    f = extrude(0, PETAL_T, t0=3, start_offset=PETAL_Y0)
    if f is None:
        model.ClearSelection2(True); last_feature(model).Select2(False, 0)
        f = fm.FeatureExtrusion2(True, False, False, 0, 0, PETAL_T, 0.0,
                                 False, False, False, False, 0.0, 0.0,
                                 False, False, False, False,
                                 False, True, True, 3, PETAL_Y0, False)
        log("petal %d OK (no-merge fallback)" % k)
    else:
        log("petal %d OK" % k)
    assert f is not None, "petal %d extrude failed" % k

# ---- 3. 叶子：一个轮廓，基线弦穿过花茎内部，偏移拉伸到茎中部 ----
model.ClearSelection2(True); top.Select2(False, 0); sm.InsertSketch(True)
l1, l2 = (0.002, -0.004), (0.002, 0.004)        # 弦在花茎截面内(距原点<STEM_R)
sm.Create3PointArc(l1[0], l1[1], 0.0, l2[0], l2[1], 0.0, 0.045, 0.0, 0.0)   # 外弧
sm.Create3PointArc(l2[0], l2[1], 0.0, l1[0], l1[1], 0.0, 0.012, 0.0, 0.0)   # 内弧
sm.InsertSketch(True)
model.ClearSelection2(True); last_feature(model).Select2(False, 0)
f = extrude(0, PETAL_T, t0=3, start_offset=STEM_H / 2 - 0.002)
assert f is not None, "leaf extrude failed"
log("leaf OK: " + wrap(f, "IFeature").Name)

# ---- 4. 花心：前视基准面半圆 + 中心线，旋转成球 ----
cy = STEM_H + CENTER_R - 0.004                 # 球心略嵌入花瓣
model.ClearSelection2(True); front.Select2(False, 0); sm.InsertSketch(True)
sm.Create3PointArc(0.0, cy - CENTER_R, 0.0, 0.0, cy + CENTER_R, 0.0, CENTER_R, cy, 0.0)
sm.CreateLine(0.0, cy + CENTER_R, 0.0, 0.0, cy - CENTER_R, 0.0)
sm.CreateCenterLine(0.0, cy - CENTER_R - 0.005, 0.0, 0.0, cy + CENTER_R + 0.005, 0.0)
sm.InsertSketch(True)
model.ClearSelection2(True); last_feature(model).Select2(False, 0)
f = fm.FeatureRevolve2(True, True, False, False, False, False,
                       0, 0, 2 * math.pi, 0.0,
                       False, False, 0.0, 0.0, 0, 0.0, 0.0, True, True, True)
assert f is not None, "center revolve failed"
log("center OK: " + wrap(f, "IFeature").Name)

# ---- 5. 保存 + 验证 ----
iso_view(model)
save_part(ext, SLDPRT)
export_png(model, ext, PNG)
log("volume=%.6e m^3" % (volume(ext) or -1))
log("DONE")
