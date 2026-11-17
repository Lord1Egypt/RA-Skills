# -*- coding: utf-8 -*-
"""工程图: 法兰盘 → A4 图纸(主视+俯视+等轴测) → SLDDRW + PDF"""
import os, sys
sys.path.insert(0, r"C:\Users\Administrator\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills\solidworks-modeling\scripts")
from sw_api import *

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(OUT_DIR, "法兰盘.SLDPRT")
SLDDRW = os.path.join(OUT_DIR, "法兰盘工程图.SLDDRW")
PDF = os.path.join(OUT_DIR, "法兰盘工程图.pdf")

sw = connect()
close_all(sw)
raw = sw.NewDocument(r"C:\ProgramData\SOLIDWORKS\SOLIDWORKS 2022\templates\gb_a4.drwdot", 0, 0.0, 0.0)
assert raw, "drawing template failed"
model = wrap(raw, "IModelDoc2")
draw = wrap(raw, "IDrawingDoc")
ext = wrap(model.Extension, "IModelDocExtension")
log("drawing: %s" % val(model.GetTitle))

def add_view(name, x, y):
    v = draw.CreateDrawViewFromModelView3(PART, name, x, y, 0.0)
    log("view %s -> %s" % (name, wrap(v, "IView").Name if v else "FAIL"))
    return v

# GB 用第一角投影: 主视(前视)在左, 俯视在主视上方? 第一角: 俯视图在主视图下方
add_view("*前视", 0.085, 0.155)
add_view("*上视", 0.075, 0.092)   # 第一角: 上视投影放在主视下方, 避开右下标题栏
add_view("*等轴测", 0.185, 0.155)

# 模型尺寸标注(整模型导入, 可能较乱, 先试)
try:
    model.ClearSelection2(True)
    r = draw.InsertModelAnnotations3(0, 16384, True, False, False, False)  # 16384=swInsertDimensionsMarkedForDrawing?
    log("annotations -> %s" % r)
except Exception as e:
    log("annotations warn: %s" % e)

model.EditRebuild3()
model.ClearSelection2(True)

# 保存 SLDDRW + 导出 PDF
for path, desc in ((SLDDRW, "slddrw"), (PDF, "pdf")):
    if os.path.exists(path):
        os.remove(path)
    r = ext.SaveAs(path, 0, 1, None, 0, 0)
    log("%s -> %s (exists=%s)" % (desc, r, os.path.exists(path)))
log("DONE")
