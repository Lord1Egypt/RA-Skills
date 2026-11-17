# QGIS Agent API 详细说明

所有请求与响应均为 JSON（UTF-8）。服务仅监听 `127.0.0.1`，默认端口 `8767`。

## GET /health

```json
{
  "status": "ok",
  "server": "qgis-agent-server",
  "version": "1.0",
  "algorithms": 1013,
  "providers": 6,
  "project": "city_map.qgz"
}
```

## GET /modules

返回当前安装的全部算法提供器：

```json
{
  "status": "ok",
  "modules": {
    "native": {"name": "QGIS (native c++)", "algorithms": 173},
    "qgis":   {"name": "QGIS algorithms",    "algorithms": 160},
    "gdal":   {"name": "GDAL",               "algorithms": 74},
    "grass7": {"name": "GRASS",              "algorithms": 82},
    "saga":   {"name": "SAGA",               "algorithms": 439},
    "3d":     {"name": "QGIS (3D)",          "algorithms": 4}
  },
  "total": 932
}
```

## GET /module/{provider}

```json
{
  "status": "ok",
  "provider": "qgis",
  "count": 160,
  "algorithms": [
    {"id": "qgis:aspect", "name": "Aspect", "group": "Raster terrain analysis"},
    ...
  ]
}
```

## GET /search?q=关键词

大小写不敏感，匹配算法 ID、名称与分组，最多返回 50 条。

## GET /tool/{algorithm_id}

返回算法完整签名（参数名、类型、默认值、输出定义）。**执行前建议先查签名**。

## POST /call

请求：

```json
{
  "name": "native:buffer",
  "arguments": {
    "INPUT": "C:/data/roads.shp",
    "DISTANCE": 500,
    "OUTPUT": "C:/out/roads_buf.gpkg"
  }
}
```

成功响应：

```json
{
  "status": "ok",
  "tool": "native:buffer",
  "elapsed_sec": 1.23,
  "result": {
    "OUTPUT": {
      "path": "C:/out/roads_buf.gpkg",
      "size_mb": 0.42,
      "feature_count": 356,
      "geometry_type": "MultiPolygon"
    }
  }
}
```

说明：
- 输出参数传 `"TEMPORARY_OUTPUT"` 可生成临时图层
- 矢量输出会自动附 `feature_count` / `geometry_type` / `size_mb`

## POST /render

| 参数 | 类型 | 说明 |
|---|---|---|
| output | str, 必填 | PNG 输出路径 |
| width / height | int | 像素尺寸，默认 1024×768 |
| layers | array, 可选 | 图层 ID 列表，缺省渲染全部图层 |
| extent | array, 可选 | `[minx, miny, maxx, maxy]`，缺省取图层总范围 |

## POST /pyqgis

默认 403。启动服务前设置 `PYQGIS_ENABLE_EXEC=1` 开启。
预置可用对象：`QgsProject`、`QgsVectorLayer`、`QgsApplication`、`processing`、`registry`（Processing 注册表）。
`print()` 输出会收集在响应的 `stdout` 字段中。

## 错误格式

```json
{
  "status": "error",
  "message": "algorithm not found: native:buff",
  "suggestion": "use GET /search?q= to find the correct id"
}
```

HTTP 状态码：200 成功；400 参数缺失；403 路径白名单拦截；404 算法/端点不存在。
