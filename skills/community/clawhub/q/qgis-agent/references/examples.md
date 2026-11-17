# QGIS Agent 调用示例集

所有示例假设服务已运行在 `http://127.0.0.1:8767`。
示例数据路径请替换为你的实际路径（受 `QGIS_ALLOWED_PATHS` 白名单约束）。

## 1. 矢量地理处理

### 缓冲区
```bash
curl -s -X POST http://127.0.0.1:8767/call -H "Content-Type: application/json" -d '{
  "name": "native:buffer",
  "arguments": {"INPUT":"D:/data/roads.shp","DISTANCE":500,"SEGMENTS":5,
                "END_CAP_STYLE":0,"JOIN_STYLE":0,"OUTPUT":"D:/out/roads_buf_500m.gpkg"}
}'
```

### 裁剪（用行政边界裁剪路网）
```bash
curl -s -X POST http://127.0.0.1:8767/call -H "Content-Type: application/json" -d '{
  "name": "native:clip",
  "arguments": {"INPUT":"D:/data/roads.gpkg","OVERLAY":"D:/data/boundary.shp",
                "OUTPUT":"D:/out/roads_clipped.gpkg"}
}'
```

### 相交 / 联合 / 融合
```bash
# 相交
{"name":"native:intersection","arguments":{"INPUT":"A.gpkg","OVERLAY":"B.gpkg","OUTPUT":"out.gpkg"}}
# 联合
{"name":"native:union","arguments":{"INPUT":"A.gpkg","OVERLAY":"B.gpkg","OUTPUT":"out.gpkg"}}
# 按字段融合（如按行政区合并地块）
{"name":"native:dissolve","arguments":{"INPUT":"plots.gpkg","FIELD":["district"],"OUTPUT":"merged.gpkg"}}
```

## 2. 属性与统计

### 字段计算（新建字段：面积平方公里）
```bash
curl -s -X POST http://127.0.0.1:8767/call -H "Content-Type: application/json" -d '{
  "name": "native:fieldcalculator",
  "arguments": {"INPUT":"D:/data/districts.gpkg","FIELD_NAME":"area_km2",
                "FIELD_TYPE":0,"FIELD_LENGTH":10,"FIELD_PRECISION":3,
                "FORMULA":"$area / 1000000","OUTPUT":"D:/out/districts_area.gpkg"}
}'
```
> FIELD_TYPE: 0=Float 1=Integer 2=String 4=Date

### 按表达式筛选要素
```bash
{"name":"native:extractbyexpression",
 "arguments":{"INPUT":"cities.gpkg","EXPRESSION":"\"population\" > 1000000","OUTPUT":"big_cities.gpkg"}}
```

### 按位置选择（点落在多边形内）
```bash
{"name":"native:extractbylocation",
 "arguments":{"INPUT":"stations.gpkg","PREDICATE":[0],"INTERSECT":"districts.gpkg","OUTPUT":"stations_in.gpkg"}}
```

### 空间连接（把行政区属性挂到 POI 上）
```bash
{"name":"native:joinattributesbylocation",
 "arguments":{"INPUT":"poi.gpkg","JOIN":"districts.gpkg","PREDICATE":[0],
              "JOIN_FIELDS":["district_name"],"OUTPUT":"poi_with_district.gpkg"}}
```

## 3. 栅格与地形分析

### DEM 求坡度 / 坡向 / 山体阴影
```bash
{"name":"native:slope","arguments":{"INPUT":"D:/data/dem.tif","OUTPUT":"D:/out/slope.tif"}}
{"name":"native:aspect","arguments":{"INPUT":"D:/data/dem.tif","OUTPUT":"D:/out/aspect.tif"}}
{"name":"native:hillshade","arguments":{"INPUT":"D:/data/dem.tif","OUTPUT":"D:/out/hillshade.tif"}}
```
> 部分版本地形算法挂在 `native:slope` 等 ID 下，先用 /search?q=slope 确认。

### 重分类（按查找表）
```bash
{"name":"qgis:reclassifybytable",
 "arguments":{"INPUT":"slope.tif","RASTER_BAND":1,
              "TABLE":[0,5,1,5,15,2,15,90,3],"RANGE_BOUNDARIES":0,"OUTPUT":"slope_class.tif"}}
```
> TABLE 为一维数值序列，每 3 个值一组：下限, 上限, 新值。

### 栅格计算器
```bash
{"name":"qgis:rastercalculator",
 "arguments":{"LAYERS":["ndvi.tif"],"EXPRESSION":"ndvi@1 * 0.001","OUTPUT":"ndvi_scaled.tif"}}
```

### 等值线（DEM → 等高线）
```bash
{"name":"gdal:contour",
 "arguments":{"INPUT":"dem.tif","BAND":1,"INTERVAL":50,"OUTPUT":"contours.gpkg"}}
```

## 4. 插值与点分析

### IDW / TIN 插值（高程点 → DEM）
```bash
{"name":"qgis:idwinterpolation",
 "arguments":{"INTERPOLATION_DATA":"points.gpkg::~::0::~::elevation::~::0",
              "EXTENT":"dem_extent.tif","PIXEL_SIZE":30,"OUTPUT":"dem_idw.tif"}}
```

### 多边形内点数统计
```bash
{"name":"qgis:countpointsinpolygon",
 "arguments":{"POLYGONS":"districts.gpkg","POINTS":"stations.gpkg","OUTPUT":"districts_count.gpkg"}}
```

## 5. 矢量创建与转换

### 泰森多边形 / 创建网格 / 随机点
```bash
{"name":"qgis:voronoipolygons","arguments":{"INPUT":"stations.gpkg","OUTPUT":"voronoi.gpkg"}}
{"name":"native:creategrid","arguments":{"TYPE":2,"EXTENT":"483000,513000,4407000,4437000 [EPSG:32650]","HSPACING":2000,"VSPACING":2000,"CRS":"EPSG:32650","OUTPUT":"grid.gpkg"}}
{"name":"qgis:randompointsinpolygons","arguments":{"POLYGONS":"districts.gpkg","POINTS_NUMBER":100,"OUTPUT":"random_pts.gpkg"}}
```

### 格式转换（GDAL，Shapefile ↔ GeoPackage ↔ GeoJSON）
```bash
{"name":"gdal:convertformat","arguments":{"INPUT":"roads.shp","CONVERT":"GPKG","OPTIONS":"", "OUTPUT":"roads.gpkg"}}
{"name":"gdal:vectortranslate","arguments":{"INPUT":"roads.gpkg","FORMAT":"GeoJSON","OUTPUT":"roads.geojson"}}
```

### 投影变换
```bash
{"name":"gdal:warpreproject",
 "arguments":{"INPUT":"dem.tif","SOURCE_CRS":"EPSG:4326","TARGET_CRS":"EPSG:4549",
              "RESAMPLING":1,"OUTPUT":"dem_4549.tif"}}
```
> 常用中国投影：CGCS2000 / EPSG:4490（经纬度）、EPSG:4526~4549（3 度带）。

## 6. 渲染出图

```bash
# 打开工程 → 渲染为 PNG
curl -s -X POST http://127.0.0.1:8767/project/open -H "Content-Type: application/json" \
  -d '{"path":"D:/maps/city_map.qgz"}'
curl -s -X POST http://127.0.0.1:8767/render -H "Content-Type: application/json" \
  -d '{"output":"D:/out/city_map.png","width":1920,"height":1080}'

# 只渲染指定图层、指定范围（minx,miny,maxx,maxy）
curl -s -X POST http://127.0.0.1:8767/render -H "Content-Type: application/json" \
  -d '{"output":"D:/out/zoom.png","layers":["roads_20240101_abcdef"],"extent":[116.3,39.8,116.6,40.1]}'
```

## 7. 复合工作流示例：工厂选址

需求：距高速公路 > 2km，位于坡度 < 8° 区域，且在 A 区界内。

```bash
# 1) 高速公路缓冲 2000m
curl -s -X POST http://127.0.0.1:8767/call -H "Content-Type: application/json" \
  -d '{"name":"native:buffer","arguments":{"INPUT":"highway.gpkg","DISTANCE":2000,"OUTPUT":"D:/tmp/hw_buf.gpkg"}}'

# 2) DEM 反向缓冲效果：求坡度并重分类（1 = 平缓区）
curl -s -X POST http://127.0.0.1:8767/call -H "Content-Type: application/json" \
  -d '{"name":"native:slope","arguments":{"INPUT":"dem.tif","OUTPUT":"D:/tmp/slope.tif"}}'
curl -s -X POST http://127.0.0.1:8767/call -H "Content-Type: application/json" \
  -d '{"name":"qgis:reclassifybytable","arguments":{"INPUT":"D:/tmp/slope.tif","RASTER_BAND":1,
        "TABLE":[0,8,1,8,999,0],"OUTPUT":"D:/tmp/slope_ok.tif"}}'

# 3) 栅格转面
curl -s -X POST http://127.0.0.1:8767/call -H "Content-Type: application/json" \
  -d '{"name":"qgis:pixelstopolygons","arguments":{"INPUT":"D:/tmp/slope_ok.tif","FIELD":"DN","OUTPUT":"D:/tmp/slope_ok_poly.gpkg"}}'

# 4) 依次擦除高速缓冲区、裁剪 A 区界
curl -s -X POST http://127.0.0.1:8767/call -H "Content-Type: application/json" \
  -d '{"name":"native:difference","arguments":{"INPUT":"D:/tmp/slope_ok_poly.gpkg","OVERLAY":"D:/tmp/hw_buf.gpkg","OUTPUT":"D:/tmp/step1.gpkg"}}'
curl -s -X POST http://127.0.0.1:8767/call -H "Content-Type: application/json" \
  -d '{"name":"native:clip","arguments":{"INPUT":"D:/tmp/step1.gpkg","OVERLAY":"zone_A.gpkg","OUTPUT":"D:/out/site_candidates.gpkg"}}'
```

## 8. 常用参数类型速记

| QGIS 参数 | 传值方式 |
|---|---|
| 矢量图层 | 文件路径字符串，或工程内图层名/ID |
| 栅格图层 | 文件路径字符串 |
| 多选字段 | `["field1","field2"]` |
| 枚举(int) | 查 `/tool/{id}` 中的 description（如 END_CAP_STYLE: 0=平头 1=圆头 2=方形）|
| 表格参数 | 扁平一维数组 |
| 范围 | `"minx,miny,maxx,maxy [EPSG:xxxx]"` 字符串 |
| 输出 | 文件路径；`.gpkg` 推荐（单文件、无编码问题）|
| 临时输出 | `"TEMPORARY_OUTPUT"` |
