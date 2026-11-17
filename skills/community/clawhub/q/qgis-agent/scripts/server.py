# -*- coding: utf-8 -*-
"""
QGISAgent Server
================
在 QGIS 自带的 Python 环境下运行的 HTTP 服务端。
把 QGIS Processing 框架中的 1000+ 算法（QGIS 原生 / GDAL / GRASS / SAGA /
3D / 点云等）通过简洁的 HTTP API 暴露给 AI 智能体。

架构：智能体(Agent) --HTTP--> scripts/server.py (PyQGIS) --> QGIS 4.x

启动方式（Windows，OSGeo4W）：
    "C:/Program Files/QGIS 4.0.3/bin/python-qgis.bat" scripts/server.py 8767
或直接运行 scripts/start_server.bat

API 一览（全部返回 JSON，UTF-8）：
    GET  /health                健康检查（含算法总数）
    GET  /modules               列出全部算法提供器（provider）及数量
    GET  /module/{provider}     列出某提供器下全部算法（id + 名称）
    GET  /search?q=关键词       按关键词搜索算法（id / 名称 / 分组）
    GET  /tool/{algorithm_id}   查看算法的完整参数签名
    POST /call                  执行算法 {"name": "native:buffer", "arguments": {...}}
    GET  /project               当前工程信息（图层列表、CRS、范围）
    POST /project/open          打开工程 {"path": "C:/data/demo.qgz"}
    POST /project/save          保存工程 {"path": "C:/out/demo.qgz"}（缺省保存到原路径）
    POST /render                渲染当前工程为 PNG {"output": "...", "width": 1024, "height": 768,
                                 "layers": [可选，图层id列表], "extent": [minx,miny,maxx,maxy] 可选}
    POST /pyqgis                执行任意 PyQGIS 代码（默认关闭，设 PYQGIS_ENABLE_EXEC=1 开启）
                                 {"code": "from qgis.core import *; ..."}

安全：
    - 服务只监听 127.0.0.1
    - 路径白名单：设置环境变量 QGIS_ALLOWED_PATHS（分号分隔）后，
      /call 与 /pyqgis 中出现的文件路径必须位于白名单目录内
"""

import json
import os
import re
import sys
import time
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote, parse_qs

# ---------------------------------------------------------------------------
# PyQGIS 初始化（必须在导入 qgis.core 前设置好环境，python-qgis.bat 已代劳）
# ---------------------------------------------------------------------------
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
    QgsRectangle,
    QgsMapSettings,
    QgsMapRendererCustomPainterJob,
    QgsProcessingContext,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    Qgis,
)
from qgis.PyQt.QtGui import QColor, QImage, QPainter
from qgis.PyQt.QtCore import QSize

QgsApplication.setPrefixPath(os.environ.get("QGIS_PREFIX_PATH", ""), True)
QGIS_APP = QgsApplication([], False)  # 无 GUI 模式
QGIS_APP.initQgis()

# 独立脚本模式下 processing 包位于 QGIS 的 python/plugins 目录，手动加入 sys.path
import sys as _sys  # noqa: E402
_plugins_dir = os.path.join(QGIS_APP.prefixPath() or os.environ.get("QGIS_PREFIX_PATH", ""), "python", "plugins")
if os.path.isdir(_plugins_dir) and _plugins_dir not in _sys.path:
    _sys.path.append(_plugins_dir)

# 初始化 Processing 框架（加载 QGIS/GDAL/GRASS/SAGA 等全部提供器）
import processing  # noqa: E402
from processing.core.Processing import Processing  # noqa: E402

Processing.initialize()

REGISTRY = QgsApplication.processingRegistry()
VERSION = "1.0"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8767

# 路径白名单（空 = 不限制；强烈建议生产环境设置）
ALLOWED_PATHS = [
    os.path.normpath(p.strip().rstrip("/\\"))
    for p in os.environ.get("QGIS_ALLOWED_PATHS", "").split(";")
    if p.strip()
]
PYQGIS_EXEC_ENABLED = os.environ.get("PYQGIS_ENABLE_EXEC", "0") == "1"

VECTOR_EXTS = {".shp", ".gpkg", ".geojson", ".json", ".sqlite", ".tab", ".kml", ".csv"}

# 形如 "xmin,xmax,ymin,ymax [EPSG:xxxx]" 的范围字符串（QGIS Processing 官方顺序！）
EXTENT_RE = re.compile(
    r"^\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,"
    r"\s*(-?\d+(?:\.\d+)?)\s*(?:\[\s*([^\]\s]+)\s*\])?\s*$"
)


def preprocess_args(args):
    """预处理参数：
    1. 范围字符串按 QGIS Processing 官方顺序 xmin,xmax,ymin,ymax 解析为 QgsRectangle。
    2. 若范围带 CRS 后缀且与目标 CRS（算法 CRS 参数 / 工程 CRS）不同，则自动做坐标转换。
    """
    if not isinstance(args, dict):
        return args
    # 目标 CRS：优先取参数里的 CRS / TARGET_CRS，其次工程 CRS
    target_crs = None
    for key in ("CRS", "TARGET_CRS", "DEST_CRS"):
        v = args.get(key)
        if isinstance(v, str) and v.strip():
            c = QgsCoordinateReferenceSystem(v.strip())
            if c.isValid():
                target_crs = c
                break
    if target_crs is None:
        target_crs = QgsProject.instance().crs()

    out = {}
    for k, v in args.items():
        if isinstance(v, str):
            m = EXTENT_RE.match(v)
            if m:
                xmin, xmax, ymin, ymax = (float(m.group(i)) for i in range(1, 5))
                rect = QgsRectangle(xmin, ymin, xmax, ymax)
                suffix = m.group(5)
                if suffix:
                    src = QgsCoordinateReferenceSystem(suffix)
                    if src.isValid() and target_crs.isValid() and src != target_crs:
                        try:
                            xform = QgsCoordinateTransform(src, target_crs, QgsProject.instance())
                            rect = xform.transformBoundingBox(rect)
                        except Exception:
                            pass
                out[k] = rect
                continue
        out[k] = v
    return out


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------
def check_paths(args):
    """校验参数中的文件路径是否在白名单内。"""
    if not ALLOWED_PATHS:
        return None
    for v in args.values() if isinstance(args, dict) else []:
        if not isinstance(v, str):
            continue
        if re.match(r"^[a-zA-Z]:[/\\]", v) or v.startswith("/") or "/" in v and "." in os.path.basename(v):
            norm = os.path.normpath(v)
            if not any(norm.lower().startswith(root.lower() + os.sep) or
                       norm.lower().startswith(root.lower() + "/") for root in ALLOWED_PATHS):
                return v
    return None


def summarize_value(v):
    """对输出文件路径补充要素数、几何类型、文件大小等信息。"""
    if not (isinstance(v, str) and os.path.exists(v) and os.path.isfile(v)):
        return v
    info = {"path": v, "size_mb": round(os.path.getsize(v) / 1048576, 2)}
    ext = os.path.splitext(v)[1].lower()
    if ext in VECTOR_EXTS:
        try:
            vl = QgsVectorLayer(v, "probe", "ogr")
            if vl.isValid():
                info["feature_count"] = vl.featureCount()
                info["geometry_type"] = QgsWkbTypes.displayString(vl.wkbType())
        except Exception:
            pass
    return info


def ok(payload, **extra):
    body = {"status": "ok", **payload, **extra}
    return body


def err(message, suggestion="", **extra):
    return {"status": "error", "message": str(message), "suggestion": suggestion, **extra}


def find_algorithm(alg_id):
    alg = REGISTRY.algorithmById(alg_id)
    if alg is None:
        # 宽松匹配：允许 "native_buffer" / "buffer" 之类的写法
        for a in REGISTRY.algorithms():
            if a.id().lower().replace(":", "_") == alg_id.lower().replace(":", "_"):
                return a
    return alg


def algorithm_signature(alg):
    params = []
    for p in alg.parameterDefinitions():
        d = {
            "name": p.name(),
            "description": p.description(),
            "type": type(p).__name__,
            "required": not p.flags() or True,
        }
        try:
            default = p.defaultValue()
            d["default"] = default if isinstance(default, (int, float, str, bool, type(None))) else str(default)
        except Exception:
            pass
        params.append(d)
    outputs = [{"name": o.name(), "description": o.description(), "type": type(o).__name__}
               for o in alg.outputDefinitions()]
    return {
        "id": alg.id(),
        "name": alg.displayName(),
        "provider": alg.provider().id() if alg.provider() else "",
        "group": alg.group(),
        "short_description": alg.shortDescription(),
        "parameters": params,
        "outputs": outputs,
    }


# ---------------------------------------------------------------------------
# HTTP 处理器
# ---------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "QGISAgentServer/" + VERSION

    def log_message(self, fmt, *args):  # 精简日志
        sys.stderr.write("[qgis-agent] %s\n" % (fmt % args))

    # -- 基础设施 -----------------------------------------------------------
    def _send(self, obj, code=200):
        data = json.dumps(obj, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length == 0:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            return {}

    # -- GET 路由 -----------------------------------------------------------
    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path).rstrip("/") or "/"
        qs = parse_qs(parsed.query)

        if path == "/":
            return self._send(self.api_docs())
        if path == "/health":
            return self._send(ok({
                "server": "qgis-mcp-server",
                "version": VERSION,
                "qgis_version": QGIS_APP.applicationVersion(),
                "algorithms": len(REGISTRY.algorithms()),
                "providers": len(REGISTRY.providers()),
                "project": os.path.basename(QgsProject.instance().fileName()) or None,
            }, server="qgis-agent-server"))
        if path == "/modules":
            mods = {}
            for prov in REGISTRY.providers():
                mods[prov.id()] = {
                    "name": prov.name(),
                    "algorithms": len(prov.algorithms()),
                }
            return self._send(ok({"modules": mods, "total": len(REGISTRY.algorithms())}))
        if path.startswith("/module/"):
            pid = path[len("/module/"):]
            prov = next((p for p in REGISTRY.providers() if p.id().lower() == pid.lower()), None)
            if prov is None:
                return self._send(err("provider not found: %s" % pid,
                                      "use GET /modules to list providers"), 404)
            algs = [{"id": a.id(), "name": a.displayName(), "group": a.group()}
                    for a in sorted(prov.algorithms(), key=lambda x: (x.group(), x.displayName()))]
            return self._send(ok({"provider": prov.id(), "count": len(algs), "algorithms": algs}))
        if path == "/search":
            q = (qs.get("q") or [""])[0].lower()
            if not q:
                return self._send(err("missing ?q= keyword"))
            hits = [{"id": a.id(), "name": a.displayName(), "group": a.group()}
                    for a in REGISTRY.algorithms()
                    if q in a.id().lower() or q in a.displayName().lower() or q in a.group().lower()]
            return self._send(ok({"query": q, "count": len(hits), "results": hits[:50]}))
        if path.startswith("/tool/"):
            alg_id = path[len("/tool/"):]
            alg = find_algorithm(alg_id)
            if alg is None:
                return self._send(err("algorithm not found: %s" % alg_id,
                                      "use GET /search?q= to find correct algorithm id"), 404)
            return self._send(ok({"tool": algorithm_signature(alg)}))
        if path == "/project":
            return self._send(ok({"project": project_info()}))
        if path == "/layers":
            return self._send(ok({"layers": layer_list()}))
        return self._send(err("unknown endpoint, GET / for docs"), 404)

    # -- POST 路由 ----------------------------------------------------------
    def do_POST(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path).rstrip("/")
        body = self._body()

        if path == "/call":
            return self.handle_call(body)
        if path == "/project/open":
            return self.handle_project_open(body)
        if path == "/project/save":
            return self.handle_project_save(body)
        if path == "/render":
            return self.handle_render(body)
        if path == "/pyqgis":
            return self.handle_pyqgis(body)
        return self._send(err("unknown endpoint, GET / for docs"), 404)

    # -- 具体动作 ------------------------------------------------------------
    def handle_call(self, body):
        name = body.get("name") or body.get("algorithm")
        args = body.get("arguments") or {}
        if not name:
            return self._send(err("missing 'name' (algorithm id), e.g. native:buffer"))
        alg = find_algorithm(name)
        if alg is None:
            return self._send(err("algorithm not found: %s" % name,
                                  "use GET /search?q= to find the correct id"), 404)
        bad = check_paths(args)
        if bad:
            return self._send(err("path outside whitelist: %s" % bad,
                                  "set env QGIS_ALLOWED_PATHS to allow this directory"), 403)
        t0 = time.time()
        try:
            # 显式单位上下文：无 GUI 模式下 Distance/Area 参数默认单位异常（可能按毫米解释），
            # 必须强制米制，否则 buffer/grid 间距等参数会产生灾难性错误结果
            ctx = QgsProcessingContext()
            ctx.setDistanceUnit(Qgis.DistanceUnit.Meters)
            try:
                ctx.setAreaUnit(Qgis.AreaUnit.SquareMeters)
            except Exception:
                pass
            ctx.setProject(QgsProject.instance())  # 允许按图层名引用工程内图层
            result = processing.run(alg.id(), preprocess_args(args), context=ctx)
        except Exception as e:
            msg = str(e)
            hint = "check parameter names via GET /tool/%s" % alg.id()
            if "Cannot find" in msg or "not found" in msg.lower():
                hint = "input dataset path may not exist; verify path and extension"
            return self._send(err(msg, suggestion=hint,
                                  traceback=traceback.format_exc()[-1500:]))
        elapsed = round(time.time() - t0, 2)
        summary = {k: summarize_value(v) for k, v in (result or {}).items()}
        return self._send(ok({"tool": alg.id(), "elapsed_sec": elapsed, "result": summary}))

    def handle_project_open(self, body):
        p = body.get("path")
        if not p or not os.path.exists(p):
            return self._send(err("invalid project path: %s" % p))
        bad = check_paths({"path": p})
        if bad:
            return self._send(err("path outside whitelist: %s" % bad), 403)
        if not QgsProject.instance().read(p):
            return self._send(err("failed to open project %s" % p))
        return self._send(ok({"opened": p, "project": project_info()}))

    def handle_project_save(self, body):
        p = body.get("path") or QgsProject.instance().fileName()
        if not p:
            return self._send(err("no project loaded and no 'path' given"))
        bad = check_paths({"path": p})
        if bad:
            return self._send(err("path outside whitelist: %s" % bad), 403)
        if not QgsProject.instance().write(p):
            return self._send(err("failed to save project to %s" % p))
        return self._send(ok({"saved": p}))

    def handle_render(self, body):
        out = body.get("output")
        if not out:
            return self._send(err("missing 'output' (png path)"))
        bad = check_paths({"output": out})
        if bad:
            return self._send(err("path outside whitelist: %s" % bad), 403)
        project = QgsProject.instance()
        layers = project.mapLayers()
        if not layers:
            return self._send(err("no layers loaded in project"))
        ids = body.get("layers") or list(layers.keys())
        w = int(body.get("width") or 1024)
        h = int(body.get("height") or 768)

        if body.get("extent"):
            rect = QgsRectangle(*[float(x) for x in body["extent"]])
        else:
            rect = QgsRectangle()
            for lid in ids:
                if lid in layers:
                    rect.combineExtentWith(layers[lid].extent())
            if rect.isEmpty():
                return self._send(err("empty extent"))

        settings = QgsMapSettings()
        settings.setLayers([layers[lid] for lid in ids if lid in layers])
        settings.setBackgroundColor(QColor(255, 255, 255))
        settings.setOutputSize(QSize(w, h))
        settings.setExtent(rect)
        settings.setFlag(settings.Flag.Antialiasing, True)

        image = QImage(settings.outputSize(), QImage.Format.Format_ARGB32_Premultiplied)
        image.fill(0xFFFFFFFF)
        painter = QPainter(image)
        job = QgsMapRendererCustomPainterJob(settings, painter)
        job.start()
        job.waitForFinished()
        painter.end()
        if not image.save(out, "PNG"):
            return self._send(err("failed to save render to %s" % out))
        return self._send(ok({"rendered": out, "width": w, "height": h,
                              "size_mb": round(os.path.getsize(out) / 1048576, 2)}))

    def handle_pyqgis(self, body):
        if not PYQGIS_EXEC_ENABLED:
            return self._send(err("PyQGIS exec is disabled",
                                  "start server with env PYQGIS_ENABLE_EXEC=1 to enable /pyqgis"), 403)
        code = body.get("code")
        if not code:
            return self._send(err("missing 'code'"))
        bad = check_paths({"code": code})
        if bad:
            return self._send(err("path outside whitelist: %s" % bad), 403)
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        g = {"QgsApplication": QgsApplication, "QgsProject": QgsProject,
             "QgsVectorLayer": QgsVectorLayer, "QgsRectangle": QgsRectangle,
             "QgsWkbTypes": QgsWkbTypes, "Processing": Processing, "registry": REGISTRY,
             "processing": __import__("processing")}
        t0 = time.time()
        try:
            with redirect_stdout(buf):
                exec(code, g)  # noqa: S102 - 显式开启的逃生舱口
        except Exception as e:
            return self._send(err(e, traceback=traceback.format_exc()[-1500:]))
        return self._send(ok({"stdout": buf.getvalue(),
                              "elapsed_sec": round(time.time() - t0, 2)}))

    # -- API 文档 ------------------------------------------------------------
    def api_docs(self):
        return ok({
            "server": "qgis-agent-server",
            "version": VERSION,
            "endpoints": {
                "GET /health": "健康检查（算法总数、工程名）",
                "GET /modules": "全部算法提供器及算法数量",
                "GET /module/{provider}": "某提供器的全部算法（id+名称+分组）",
                "GET /search?q=关键词": "按关键词搜索算法",
                "GET /tool/{algorithm_id}": "算法完整参数签名",
                "POST /call": "执行算法 {name, arguments}",
                "GET /project | POST /project/open | POST /project/save": "工程管理",
                "POST /render": "渲染当前工程为 PNG",
                "POST /pyqgis": "执行任意 PyQGIS 代码（需 PYQGIS_ENABLE_EXEC=1）",
            },
            "example_call": {
                "name": "native:buffer",
                "arguments": {"INPUT": "C:/data/roads.shp",
                              "DISTANCE": 500,
                              "OUTPUT": "C:/out/roads_buf.gpkg"},
            },
            "whitelist": ALLOWED_PATHS or "(未设置，允许任意路径；建议设置 QGIS_ALLOWED_PATHS)",
        })


# ---------------------------------------------------------------------------
# 工程信息辅助
# ---------------------------------------------------------------------------
def layer_list():
    project = QgsProject.instance()
    out = []
    for lid, layer in project.mapLayers().items():
        item = {
            "id": lid,
            "name": layer.name(),
            "source": layer.source(),
            "crs": layer.crs().authid() if layer.crs() else None,
        }
        if isinstance(layer, QgsVectorLayer):
            item["type"] = "vector"
            item["geometry"] = QgsWkbTypes.displayString(layer.wkbType())
            item["feature_count"] = layer.featureCount()
            item["fields"] = [f.name() for f in layer.fields()]
        else:
            item["type"] = layer.__class__.__name__
        out.append(item)
    return out


def project_info():
    project = QgsProject.instance()
    rect = project.extent() if project.fileName() else None
    return {
        "file": project.fileName() or None,
        "title": project.title(),
        "crs": project.crs().authid() if project.crs() else None,
        "extent": list(rect.toRectF()) if rect and not rect.isEmpty() else None,
        "layers": layer_list(),
    }


def main():
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print("=" * 60)
    print("QGISAgent Server v%s  |  QGIS %s" % (VERSION, QGIS_APP.applicationVersion() if callable(getattr(QGIS_APP, "applicationVersion", None)) else ""))
    print("监听: http://127.0.0.1:%d   算法总数: %d" % (PORT, len(REGISTRY.algorithms())))
    print("路径白名单: %s" % (ALLOWED_PATHS or "未设置（允许任意路径）"))
    print("PyQGIS 代码执行: %s" % ("开启" if PYQGIS_EXEC_ENABLED else "关闭"))
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[qgis-agent] shutting down")
        QGIS_APP.exitQgis()


if __name__ == "__main__":
    main()
