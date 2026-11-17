# -*- coding: utf-8 -*-
"""
齿轮-传动轴装配体（solidworks-modeling 技能包）
策略: 两个零件都按"原点即配合基准"建模，装配时直接原点重合，
      再用三个基准面重合配合完全定位（不依赖面选择，最稳）。
轴: Ø15 轴段 z∈[-10, +50]mm, Ø25 轴肩 z∈[-10, 0]mm  (肩顶面 z=0 与齿轮前面贴合)
齿轮: z∈[0, 20]mm (已验证)
"""
import os, sys, math

SKILL_SCRIPTS = r"C:\Users\Administrator\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills\solidworks-modeling\scripts"
sys.path.insert(0, SKILL_SCRIPTS)
from sw_api import *
import win32com.client.gencache as g
g.EnsureModule('{4687F359-55D0-4CD3-B6CF-2EB42C11F989}', 0, 30, 0)
from win32com.client import constants

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
GEAR     = os.path.join(OUT_DIR, "齿轮.SLDPRT")
SHAFT    = os.path.join(OUT_DIR, "传动轴.SLDPRT")
ASM      = os.path.join(OUT_DIR, "齿轮轴装配.SLDASM")
PNG      = os.path.join(OUT_DIR, "装配体预览.png")
ASM_TMPL = r"C:\ProgramData\SOLIDWORKS\SOLIDWORKS 2022\templates\gb_assembly.asmdot"

sw = connect()
close_all(sw)

# ---------- 1. 建传动轴 ----------
model, sm, fm, ext = new_part(sw)
front = refplanes(model)[0]

def sketch_circle(r):
    model.ClearSelection2(True); front.Select2(False, 0); sm.InsertSketch(True)
    sm.AddToDB = True
    sm.CreateCircle(0.0, 0.0, 0.0, r, 0.0, 0.0)
    sm.AddToDB = False
    sm.InsertSketch(True)
    model.ClearSelection2(True); last_feature(model).Select2(False, 0)

# 轴肩 Ø25: 反向(-Z)拉伸 10mm → z∈[-10,0]
sketch_circle(0.0125)
f = fm.FeatureExtrusion2(True, False, True, 0, 0, 0.010, 0.0,
                         False, False, False, False, 0.0, 0.0,
                         False, False, False, False, True, True, True, 0, 0.0, False)
assert f is not None, "shoulder failed"
log("shoulder OK")

# 轴段 Ø15: 双向拉伸 +Z 50mm / -Z 10mm → z∈[-10, +50]
sketch_circle(0.0075)
f = fm.FeatureExtrusion2(False, False, False, 0, 0, 0.050, 0.010,
                         False, False, False, False, 0.0, 0.0,
                         False, False, False, False, True, True, True, 0, 0.0, False)
assert f is not None, "shaft failed"
log("shaft OK")

iso_view(model)
save_part(ext, SHAFT)

# ---------- 2. 新建装配体并插入组件 ----------
raw = sw.NewDocument(ASM_TMPL, 0, 0.0, 0.0)
asm = wrap(raw, "IAssemblyDoc")
amodel = wrap(raw, "IModelDoc2")
aext = wrap(amodel.Extension, "IModelDocExtension")   # 必须从 .Extension 属性取再包!
asm_title = str(val(amodel.GetTitle))
log("assembly: %s" % asm_title)

def insert_comp(path):
    """官方套路: 先 OpenDoc6 静默打开零件 -> 切回装配体 -> AddComponent5 -> 按路径找新组件"""
    sw.OpenDoc6(path, 1, 1, "", 0, 0)                       # options=1 静默
    sw.ActivateDoc3(asm_title, False, 0, 0)
    a = wrap(sw.ActiveDoc, "IAssemblyDoc")
    before = len(a.GetComponents(False) or [])
    a.AddComponent5(path, 0, "", False, "", 0.0, 0.0, 0.0)
    comps = a.GetComponents(False) or []
    if len(comps) <= before:
        raise RuntimeError("组件未插入: " + path)
    base = os.path.splitext(os.path.basename(path))[0]
    for c in comps:   # GetComponents 顺序是特征树顺序, 不是插入顺序 — 按名字找
        cc = wrap(c, "IComponent2")
        if cc.Name2.split("-")[0] == base:
            return a, cc
    return a, wrap(comps[-1], "IComponent2")

asm, c1 = insert_comp(SHAFT)
log("comp1: %s fixed=%s" % (c1.Name2, val(c1.IsFixed)))
asm, c2 = insert_comp(GEAR)
log("comp2: %s fixed=%s" % (c2.Name2, val(c2.IsFixed)))

# ---------- 3. 基准面重合配合 (前视↔前视 防转动, 右视↔右视, 上视↔上视) ----------
PLANES = [("前视基准面", 0), ("右视基准面", 0), ("上视基准面", 0)]  # 全重合对齐
asm_title = str(val(amodel.GetTitle)).replace(".SLDASM", "").replace(".sldasm", "")
mate_ok = 0
for pname, align in PLANES:
    amodel.ClearSelection2(True)
    n1 = "%s@%s@%s" % (pname, c2.Name2, asm_title)
    n2 = "%s@%s@%s" % (pname, c1.Name2, asm_title)
    s1 = aext.SelectByID2(n1, "PLANE", 0, 0, 0, False, 0, None, 0)
    s2 = aext.SelectByID2(n2, "PLANE", 0, 0, 0, True, 0, None, 0)
    if not (s1 and s2):
        log("mate %s: select failed (%s, %s)" % (pname, s1, s2))
        continue
    try:
        r = asm.AddMate3(constants.swMateCOINCIDENT, align, False,
                         0.0, 0.0, 0.0, 1, 1, 0.0, 0.0, 0.0,
                         False, 0)      # 14参: 末位 ErrorStatus
        status = r[-1] if isinstance(r, tuple) else r
        feat = r[0] if isinstance(r, tuple) else r
        log("mate %s: status=%s" % (pname, status))
        if status == 1:
            mate_ok += 1
    except Exception as e:
        log("mate %s exc: %s" % (pname, e))

log("mates ok: %d/3" % mate_ok)
amodel.EditRebuild3()

# ---------- 4. 保存 + 渲染 ----------
iso_view(amodel)
aext.SaveAs(ASM, 0, 1, None, 0, 0)
log("asm saved: %s" % os.path.exists(ASM))
aext.SaveAs(PNG, 0, 1, None, 0, 0)
log("DONE")
