# -*- coding: utf-8 -*-
"""
SOLIDWORKS COM API 通用引导模块（SW2022 验证通过）
用法:
    import sys; sys.path.insert(0, r"<skill目录>\\scripts")
    from sw_api import *
    sw = connect()
    model, sm, fm, ext = new_part(sw)
    ...
"""
import os, sys, math, time, glob
import win32com.client as wc
import win32com.client.gencache as gencache

# 版本号 -> 类型库 GUID 映射表（已知版本；查不到的版本从注册表读）
TYPELIB_GUIDS = {
    30: "{83A33D31-27C5-11CE-BFD4-00400513BB57}",  # SOLIDWORKS 2022
}
SW_VERSION = 30          # 2022；2023=31, 2024=32 ...
PROG_IDS = ("SldWorks.Application.%d" % SW_VERSION, "SldWorks.Application")

TEMPLATE_CANDIDATES = [
    r"C:\ProgramData\SOLIDWORKS\SOLIDWORKS %d\templates\gb_part.prtdot" % (2000 + SW_VERSION - 8),
]

def log(msg):
    print("[sw] " + str(msg), flush=True)

def val(x):
    """COM 成员在早绑定下有时是属性有时是方法，统一取值"""
    return x() if callable(x) else x

def _load_mod():
    guid = TYPELIB_GUIDS.get(SW_VERSION)
    if not guid:
        raise RuntimeError("未知 SW 版本 %d，请从注册表 HKCR\\CLSID\\<CLSID>\\TypeLib 查 GUID" % SW_VERSION)
    return gencache.EnsureModule(guid, 0, SW_VERSION, 0)

_mod = None

def wrap(obj, iface):
    """把裸 CDispatch 包装成类型库接口类"""
    global _mod
    if obj is None:
        return None
    if _mod is None:
        _mod = _load_mod()
    try:
        cls = getattr(_mod, iface)
        if isinstance(obj, cls):
            return obj
        return cls(obj._oleobj_)
    except Exception:
        return obj

def connect(visible=True):
    """连接/启动 SOLIDWORKS，返回包装好的 ISldWorks"""
    last = None
    for pid in PROG_IDS:
        try:
            sw = wrap(wc.Dispatch(pid), "ISldWorks")
            log("COM connected: " + pid)
            if visible:
                sw.Visible = True
            time.sleep(3)
            return sw
        except Exception as e:
            last = e
            log("dispatch failed %s: %s" % (pid, e))
    raise RuntimeError("无法创建 SldWorks COM 对象: %s" % last)

def find_template():
    for p in TEMPLATE_CANDIDATES:
        if os.path.exists(p):
            return p
    roots = [r"C:\ProgramData\SOLIDWORKS", r"D:\Program Files\SOLIDWORKS Corp",
             r"C:\Program Files\SOLIDWORKS Corp"]
    for root in roots:
        if not os.path.isdir(root):
            continue
        cands = glob.glob(os.path.join(root, "**", "*.prtdot"), recursive=True)
        pref = [p for p in cands if os.path.basename(p).lower() == "gb_part.prtdot"]
        if pref:
            return pref[0]
        if cands:
            return cands[0]
    return None

def close_all(sw):
    try:
        sw.CloseAllDocuments(True)
    except Exception:
        pass

def new_part(sw, template=None):
    """新建零件，返回 (model, sm, fm, ext)，全部已包装"""
    tmpl = template or find_template()
    if not tmpl:
        raise RuntimeError("找不到零件模板 (*.prtdot)")
    raw = sw.NewDocument(tmpl, 0, 0.0, 0.0)
    if raw is None:
        raise RuntimeError("NewDocument 返回 None")
    model = wrap(raw, "IModelDoc2")
    log("new part: " + str(val(model.GetTitle)))
    sm  = wrap(model.SketchManager,  "ISketchManager")
    fm  = wrap(model.FeatureManager, "IFeatureManager")
    ext = wrap(model.Extension,      "IModelDocExtension")
    return model, sm, fm, ext

def all_features(model):
    feats = []
    f = wrap(model.FirstFeature(), "IFeature")
    while f is not None:
        feats.append(f)
        try:
            f = wrap(f.GetNextFeature(), "IFeature")
        except Exception:
            break
    return feats

def refplanes(model):
    """按特征树顺序返回基准面 [前视, 上视, 右视]（不依赖本地化名称）"""
    return [f for f in all_features(model) if val(f.GetTypeName2) == "RefPlane"]

def last_feature(model):
    feats = all_features(model)
    return feats[-1] if feats else None

def iso_view(model):
    try:
        model.ShowNamedView2("*等轴测", 7)
        model.ViewZoomtofit2()
    except Exception as e:
        log("view warn: %s" % e)

def save_part(ext, path):
    """静默保存。返回 (ok, err, warn)。覆盖已存在文件。"""
    if os.path.exists(path):
        os.remove(path)
    res = ext.SaveAs(path, 0, 1, None, 0, 0)
    ok = bool(res[0]) and os.path.exists(path)
    log("save %s -> %s (size=%d)" % (os.path.basename(path), ok,
        os.path.getsize(path) if os.path.exists(path) else -1))
    return res

def export_png(model, ext, path):
    """把当前视图渲染成 PNG（用于视觉自查）"""
    iso_view(model)
    if os.path.exists(path):
        os.remove(path)
    try:
        res = ext.SaveAs(path, 0, 1, None, 0, 0)
        log("png %s -> %s" % (os.path.basename(path), res))
        return res
    except Exception as e:
        log("png warn: %s" % e)
        return None

def volume(ext):
    try:
        mp = wrap(val(ext.CreateMassProperty), "IMassProperty")
        return float(val(mp.Volume))
    except Exception as e:
        log("mass warn: %s" % e)
        return None

# ---------- 几何遍历 + 圆角（探针10 验证） ----------

def call0(obj, name):
    """GetFaces/GetEdges/CircleParams 等成员属性/方法二义，统一取值"""
    return val(getattr(obj, name))

def circle_edges(model):
    """遍历所有实体, 返回 [(IEdge, (cx,cy,cz,ax,ay,az,r))]（仅圆边）"""
    part = wrap(model, "IPartDoc")
    out = []
    for b in (part.GetBodies2(0, True) or []):
        for face in (call0(wrap(b, "IBody2"), "GetFaces") or []):
            for e in (call0(wrap(face, "IFace2"), "GetEdges") or []):
                e = wrap(e, "IEdge")
                c = wrap(e.GetCurve(), "ICurve")
                try:
                    if c.IsCircle():
                        out.append((e, tuple(call0(c, "CircleParams"))))
                except Exception:
                    pass
    return out

def fillet_circle_edge(model, fm, cy, r, fr, tol=0.0005):
    """按几何特征(圆心高度cy, 半径r)定位棱边并倒圆角 fr。
    比 SelectByID2 坐标点选可靠: 坐标点选按最近边+容差匹配, 已倒角的边会消失导致误选。"""
    for e, p in circle_edges(model):
        if abs(p[1] - cy) < tol and abs(p[6] - r) < tol:
            model.ClearSelection2(True)
            if not wrap(e, "IEntity").Select4(True, None):
                return None
            for opt, ov in ((2, 0), (2, 1), (0, 0)):   # 2=UniformRadius; Ftyp 必须 0(Simple)
                feat = fm.FeatureFillet3(opt, fr, 0.0, 0.0, 0, ov, 0,
                                         None, None, None, None, None, None, None)
                if feat is not None:
                    log("fillet cy=%.1f r=%.1f fr=%.1fmm -> %s" % (cy*1000, r*1000, fr*1000, feat.Name))
                    return feat
            return None
    log("fillet: edge cy=%.1f r=%.1f not found" % (cy*1000, r*1000))
    return None
