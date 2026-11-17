# -*- coding: utf-8 -*-
"""
渐开线直齿轮（solidworks-modeling 技能包）
参数: 模数 m, 齿数 z, 压力角 alpha, 齿宽 b, 中心孔径 d_bore
齿廓: 渐开线 + 齿顶圆弧 + 齿根圆弧（径向线段过渡基圆以下），整体单轮廓一次拉伸
"""
import os, sys, math

SKILL_SCRIPTS = r"C:\Users\Administrator\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills\solidworks-modeling\scripts"
sys.path.insert(0, SKILL_SCRIPTS)
from sw_api import *

# ---- 参数（米/弧度） ----
M      = 0.003          # 模数 3mm
Z      = 20             # 齿数
ALPHA  = math.radians(20)
B      = 0.020          # 齿宽
BORE_R = 0.0075         # 中心孔半径 Ø15
KEY_W  = 0.005          # 键槽宽 5mm (GB/T 1095: 轴径12~17 配 5x5 平键)
KEY_T2 = 0.0023         # 轮毂侧键槽深 2.3mm

# ---- 派生尺寸 ----
R  = M * Z / 2                  # 分度圆 30mm
RB = R * math.cos(ALPHA)        # 基圆
RA = R + M                      # 齿顶圆
RF = R - 1.25 * M               # 齿根圆
inv = lambda a: math.tan(a) - a

def half_tooth_angle(rho):
    """半径 rho 处半齿厚角"""
    a_r = math.acos(min(1.0, RB / rho))
    return math.pi / (2 * Z) + inv(ALPHA) - inv(a_r)

def pt(rho, ang):
    return (rho * math.cos(ang), rho * math.sin(ang))

def gear_outline(n_flank=10, n_tip=4, n_root=6):
    """逆时针生成整圈轮廓点"""
    pts = []
    r0 = max(RF, RB)            # 渐开线起始半径
    for i in range(Z):
        c = 2 * math.pi * i / Z
        eta0 = half_tooth_angle(r0)
        # 左齿面: 从根部升到齿顶 (角度随半径增大而增大)
        if RF < RB:             # 基圆以下用径向线段
            pts.append(pt(RF, c - eta0))
        for k in range(n_flank + 1):
            rho = r0 + (RA - r0) * k / n_flank
            pts.append(pt(rho, c - half_tooth_angle(rho)))
        # 齿顶圆弧
        et = half_tooth_angle(RA)
        for k in range(1, n_tip + 1):
            pts.append(pt(RA, c - et + 2 * et * k / n_tip))
        # 右齿面: 从齿顶降到根部
        for k in range(1, n_flank + 1):
            rho = RA - (RA - r0) * k / n_flank
            pts.append(pt(rho, c + half_tooth_angle(rho)))
        if RF < RB:
            pts.append(pt(RF, c + eta0))
        # 齿根圆弧到下一齿
        c_next = 2 * math.pi * (i + 1) / Z
        a0, a1 = c + eta0, c_next - eta0
        for k in range(1, n_root + 1):
            pts.append(pt(RF, a0 + (a1 - a0) * k / n_root))
    return pts

def bore_keyway_pts(n_arc=48):
    """中心孔+键槽合成单轮廓(逆时针采样点)：圆在键槽处开口，凸出矩形键槽"""
    hw = KEY_W / 2                       # 键槽半宽 2.5mm
    yi = math.sqrt(BORE_R**2 - hw**2)    # 键槽侧边与孔圆交点高度 7.071mm
    yt = BORE_R + KEY_T2                 # 键槽顶 9.8mm
    # 交点对应圆心角
    a_r = math.atan2(yi, hw)             # 右交点角 ~19.5°
    a_l = math.pi - a_r                  # 左交点角
    pts = [(hw, yi), (hw, yt), (-hw, yt), (-hw, yi)]   # 键槽矩形(从下往上绕顶)
    # 孔圆弧: 从左交点逆时针走大半圈到右交点
    for k in range(1, n_arc + 1):
        a = a_l + (2 * math.pi - (a_l - a_r)) * k / n_arc
        pts.append((BORE_R * math.cos(a), BORE_R * math.sin(a)))
    return pts                            # 末点=右交点，与首点闭合

def shoelace(pts):
    s = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SLDPRT = os.path.join(OUT_DIR, "齿轮.SLDPRT")
PNG    = os.path.join(OUT_DIR, "齿轮预览.png")

outline = gear_outline()
log("outline points: %d  (m=%.0fmm z=%d alpha=%.0f° 分度圆Ø%.0f 顶圆Ø%.0f 根圆Ø%.2f)" %
    (len(outline), M * 1000, Z, math.degrees(ALPHA), 2 * R * 1000, 2 * RA * 1000, 2 * RF * 1000))

sw = connect()
close_all(sw)
model, sm, fm, ext = new_part(sw)
front = refplanes(model)[0]

# ---- 第1步: 齿廓实心拉伸 ----
model.ClearSelection2(True); front.Select2(False, 0); sm.InsertSketch(True)
sm.AddToDB = True   # 大批量绘制时绕过实时求解器(否则闭合处线段会被随机拒绝)
n_fail = 0
n_skip = 0
for i in range(len(outline)):
    x1, y1 = outline[i]
    x2, y2 = outline[(i + 1) % len(outline)]
    if math.hypot(x2 - x1, y2 - y1) < 1e-9:   # 跳过零长度退化段(齿间根弧首尾重复点)
        n_skip += 1
        continue
    if sm.CreateLine(x1, y1, 0.0, x2, y2, 0.0) is None:
        n_fail += 1
sm.AddToDB = False
sm.InsertSketch(True)
try: model.EditRebuild3()
except Exception: pass
log("outline lines drawn, skipped dup: %d, failed: %d" % (n_skip, n_fail))

model.ClearSelection2(True)
sk = last_feature(model)
log("outline sketch: %s sel=%s" % (sk.Name, sk.Select2(False, 0)))
f = fm.FeatureExtrusion2(True, False, False, 0, 0, B, 0.0,
                         False, False, False, False, 0.0, 0.0,
                         False, False, False, False,
                         True, True, True, 0, 0.0, False)
assert f is not None, "gear extrude failed"
log("gear blank OK: " + wrap(f, "IFeature").Name)

# ---- 第2步: 中心孔+键槽单轮廓, FeatureCut3 完全贯穿切除 (Dir=True 朝材料内部) ----
bore = bore_keyway_pts()
model.ClearSelection2(True); front.Select2(False, 0); sm.InsertSketch(True)
sm.AddToDB = True   # 必须! 否则自动几何关系会把采样点吸到水平/竖直方向, 轮廓变形
n_fail = 0
for i in range(len(bore)):
    x1, y1 = bore[i]
    x2, y2 = bore[(i + 1) % len(bore)]
    if math.hypot(x2 - x1, y2 - y1) < 1e-9:
        continue
    if sm.CreateLine(x1, y1, 0.0, x2, y2, 0.0) is None:
        n_fail += 1
sm.AddToDB = False
sm.InsertSketch(True)
try: model.EditRebuild3()
except Exception: pass
log("bore+keyway sketch drawn (%d pts), failed: %d" % (len(bore), n_fail))

model.ClearSelection2(True)
sk2 = last_feature(model)
log("cut sketch: %s sel=%s" % (sk2.Name, sk2.Select2(False, 0)))
c = fm.FeatureCut3(True, False, True, 1, 0, 0.01, 0.0,
                   False, False, False, False, 0.0, 0.0,
                   False, False, False, False,
                   False, True, True, True,
                   False, False, 0, 0.0, False)   # 26参, T1=1 完全贯穿
assert c is not None, "bore+keyway cut failed"
log("cut OK: " + wrap(c, "IFeature").Name)

# ---- 保存 + 验证 ----
iso_view(model)
save_part(ext, SLDPRT)
export_png(model, ext, PNG)

v = volume(ext)
theory = (shoelace(outline) - shoelace(bore)) * B
if v:
    log("volume=%.6e theory=%.6e diff=%.2f%%" % (v, theory, abs(v - theory) / theory * 100))
log("DONE")
