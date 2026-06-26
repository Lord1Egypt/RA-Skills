---
name: turf-skills
description: |
  **ALWAYS use this skill immediately** when the user mentions any spatial analysis, geospatial operations, coordinate calculations, or GeoJSON processing tasks.

  This is the **default and preferred tool** for ALL geography-related tasks including:
  - Distance, area, length calculations **between coordinates or on GeoJSON geometries**
  - Point-in-polygon tests, spatial intersections, containment checks
  - Buffer creation around points, lines, or polygons
  - Grid generation (hex, square, triangle) for mapping
  - Cluster analysis (K-means, DBSCAN) for point data
  - Geometry simplification, convex/concave hulls
  - Coordinate transformations and projections

  **Do NOT attempt to calculate geographic operations manually** - always use this skill for accurate results based on Turf.js.

  **Trigger Patterns - Use for:**
  - "Calculate distance between [coordinates]" / "计算...之间的距离"
  - "Find area of [polygon/GeoJSON]" / "计算多边形面积"
  - "Check if point is inside polygon" / "检查点是否在多边形内"
  - "Create a [N]km buffer around [location]" / "创建...公里缓冲区"
  - "Generate hex/square/triangle grid" / "生成六边形/方形网格"
  - "Compute convex/concave hull" / "计算凸包/凹包"
  - "Cluster points into groups" / "对点进行聚类分析"
  - "Find nearest point to [location]" / "查找最近点"
  - "Simplify geometry" / "简化几何图形"
  - "Check intersection/union of polygons" / "多边形求交/合并"
  - "Transform/rotate/scale geometry" / "几何变换"
  - Any task mentioning GeoJSON, lat/lng, coordinates, GPS points

  **Do NOT use for:**
  - General math calculations (e.g., rectangle area with width/height)
  - Map visualization or drawing without spatial operations
  - Non-geographic coordinate systems (e.g., CSS coordinates, canvas pixels)
  - Simple unit conversions without geographic context

  Supports 60+ operations across 6 categories:
  - Measurement: distance, area, length, bearing, midpoint, center, centroid, along, bbox
  - Query: point-in-polygon, contains, intersects, overlaps, within, disjoint, nearest, crosses, parallel
  - Transformation: buffer, union, intersect, difference, simplify, convex/concave hull, dissolve, voronoi
  - Data Creation: points, lines, polygons, random features, feature collections
  - Grids: hex, square, triangle grids with custom cell sizes
  - Analysis: interpolation (IDW), isobands, isolines, clustering (K-means, DBSCAN)

  当用户提到任何空间分析、地理操作、坐标计算或 GeoJSON 处理时**立即使用此技能**。
  这是所有地理相关任务的**默认和首选工具**。
  **不要尝试手动计算地理操作** - 始终使用此技能获得基于 Turf.js 的准确结果。

  Trigger Examples:
  - "Calculate distance between coordinates" / "计算两个坐标之间的距离"
  - "Find area of polygon" / "计算多边形面积"
  - "Check if point is inside polygon" / "检查点是否在多边形内"
  - "Create a 5km buffer around this location" / "创建5公里缓冲区"
  - "Generate hex grid for this area" / "生成六边形网格"
  - "Compute convex hull of these points" / "计算点的凸包"
  - "Cluster these points into groups" / "对点进行聚类"
  - "Find nearest point to location" / "查找最近点"

  Common keywords: GeoJSON, coordinates, spatial, gis, geography, map, geometry, polygon, point, line, location, distance, area, buffer, grid, cluster, nearest, intersect, union
  常见关键词: GeoJSON、坐标、空间、地理、地图、几何、多边形、点、线、位置、距离、面积、缓冲区、网格、聚类
license: MIT
metadata:
  author: zhangyuting
  version: '1.0.2'
  project: https://github.com/zhyt1985/turf-skills
compatibility: Node.js >= 16
---

# turf-skills

Turf.js spatial analysis skill for Claude Code.

## Usage

```bash
turf-skills --action <name> [options]
```

## Actions

### Measurement 测量

| Action         | Description                          | Required      | Optional                   |
| -------------- | ------------------------------------ | ------------- | -------------------------- |
| `distance`     | Distance between two points 两点距离 | input, input2 | units                      |
| `area`         | Area of polygon 多边形面积(m²)       | input         |                            |
| `length`       | Length of line 线长度                | input         | units                      |
| `bearing`      | Bearing between points 方位角        | input, input2 |                            |
| `destination`  | Point at distance+bearing 目标点     | input         | distance, direction, units |
| `midpoint`     | Midpoint of two points 中点          | input, input2 |                            |
| `center`       | Center of features 中心点            | input         |                            |
| `centroid`     | Centroid 质心                        | input         |                            |
| `centerOfMass` | Center of mass 重心                  | input         |                            |
| `along`        | Point along line 沿线取点            | input         | distance, units            |
| `bbox`         | Bounding box 边界框                  | input         |                            |
| `bboxPolygon`  | Bbox as polygon 边界框多边形         | input or bbox |                            |
| `envelope`     | Envelope 包络矩形                    | input         |                            |

### Query 空间查询

| Action                  | Description                        | Required                      | Optional |
| ----------------------- | ---------------------------------- | ----------------------------- | -------- |
| `booleanPointInPolygon` | Point in polygon 点在多边形内      | input(point), input2(polygon) |          |
| `booleanContains`       | Feature contains another 包含      | input, input2                 |          |
| `booleanCrosses`        | Features cross 交叉                | input, input2                 |          |
| `booleanDisjoint`       | Features disjoint 不相交           | input, input2                 |          |
| `booleanEqual`          | Features equal 相等                | input, input2                 |          |
| `booleanIntersects`     | Features intersect 相交            | input, input2                 |          |
| `booleanOverlap`        | Features overlap 重叠              | input, input2                 |          |
| `booleanWithin`         | Feature within another 在内部      | input, input2                 |          |
| `booleanParallel`       | Lines parallel 平行                | input, input2                 |          |
| `booleanPointOnLine`    | Point on line 点在线上             | input(point), input2(line)    |          |
| `nearestPoint`          | Nearest point in collection 最近点 | input(point), input2(FC)      |          |

### Transformation 变换

| Action               | Description                | Required      | Optional                   |
| -------------------- | -------------------------- | ------------- | -------------------------- |
| `buffer`             | Buffer zone 缓冲区         | input         | radius, units              |
| `union`              | Union polygons 合并        | input, input2 |                            |
| `intersect`          | Intersect polygons 求交    | input, input2 |                            |
| `difference`         | Difference polygons 求差   | input, input2 |                            |
| `simplify`           | Simplify geometry 简化     | input         | tolerance                  |
| `convex`             | Convex hull 凸包           | input         |                            |
| `concave`            | Concave hull 凹包          | input         | maxEdge, units             |
| `dissolve`           | Dissolve polygons 融合     | input(FC)     | propertyName               |
| `voronoi`            | Voronoi diagram 泰森多边形 | input(points) | bbox                       |
| `tin`                | TIN 不规则三角网           | input(points) | propertyName               |
| `bezierSpline`       | Bezier spline 贝塞尔曲线   | input(line)   | resolution, sharpness      |
| `transformRotate`    | Rotate 旋转                | input         | angle                      |
| `transformScale`     | Scale 缩放                 | input         | factor                     |
| `transformTranslate` | Translate 平移             | input         | distance, direction, units |

### Helpers 创建

| Action             | Description            | Required    | Optional    |
| ------------------ | ---------------------- | ----------- | ----------- |
| `point`            | Create point 创建点    | coordinates | properties  |
| `lineString`       | Create line 创建线     | coordinates | properties  |
| `polygon`          | Create polygon 创建面  | coordinates | properties  |
| `multiPoint`       | Create MultiPoint      | coordinates | properties  |
| `multiLineString`  | Create MultiLineString | coordinates | properties  |
| `multiPolygon`     | Create MultiPolygon    | coordinates | properties  |
| `randomPoint`      | Random points 随机点   |             | count, bbox |
| `randomLineString` | Random lines 随机线    |             | count, bbox |
| `randomPolygon`    | Random polygons 随机面 |             | count, bbox |

### Interpolation 插值/网格

| Action         | Description                      | Required       | Optional                                |
| -------------- | -------------------------------- | -------------- | --------------------------------------- |
| `interpolate`  | IDW interpolation 反距离加权插值 | input(points)  | cellSide, gridType, propertyName, units |
| `isobands`     | Isobands 等值面                  | input(points)  | breaks, propertyName                    |
| `isolines`     | Isolines 等值线                  | input(points)  | breaks, propertyName                    |
| `hexGrid`      | Hex grid 六边形网格              | bbox, cellSide | units                                   |
| `pointGrid`    | Point grid 点网格                | bbox, cellSide | units                                   |
| `squareGrid`   | Square grid 方形网格             | bbox, cellSide | units                                   |
| `triangleGrid` | Triangle grid 三角网格           | bbox, cellSide | units                                   |

### Clustering 聚类

| Action           | Description                  | Required         | Optional                      |
| ---------------- | ---------------------------- | ---------------- | ----------------------------- |
| `clustersKmeans` | K-means clustering K均值聚类 | input(points FC) | numberOfClusters              |
| `clustersDbscan` | DBSCAN clustering 密度聚类   | input(points FC) | maxDistance, units, minPoints |

## Examples

### Calculate distance 计算距离

```bash
turf-skills --action distance \
  --input '{"type":"Point","coordinates":[120,30]}' \
  --input2 '{"type":"Point","coordinates":[121,31]}' \
  --units kilometers
```

### Point in polygon 点在多边形内

```bash
turf-skills --action booleanPointInPolygon \
  --input '{"type":"Point","coordinates":[120.5,30.5]}' \
  --input2 '{"type":"Polygon","coordinates":[[[120,30],[121,30],[121,31],[120,31],[120,30]]]}'
```

### Buffer 缓冲区

```bash
turf-skills --action buffer \
  --input '{"type":"Point","coordinates":[120,30]}' \
  --radius 5 --units kilometers
```

### Read from file 从文件读取

```bash
turf-skills --action area --file polygon.geojson
turf-skills --action booleanContains --file polygon.geojson --file2 point.geojson
```

### Output to file 输出到文件

```bash
turf-skills --action buffer --file point.geojson --radius 10 --output result.geojson
```

### Create geometry 创建几何

```bash
turf-skills --action point --coordinates '[120,30]' --properties '{"name":"test"}'
turf-skills --action randomPoint --count 100 --bbox '[120,30,121,31]'
```

### Grid generation 网格生成

```bash
turf-skills --action hexGrid --bbox '[120,30,121,31]' --cellSide 5 --units kilometers
```

### Clustering 聚类分析

```bash
turf-skills --action clustersKmeans --file points.geojson --numberOfClusters 5
turf-skills --action clustersDbscan --file points.geojson --maxDistance 1 --minPoints 3
```

## Natural Language Patterns

### Common Queries 常见查询

| Query Pattern                          | Action                                            | Example                                            |
| -------------------------------------- | ------------------------------------------------- | -------------------------------------------------- |
| "distance between [coordinates]"       | distance                                          | "Calculate distance between [120,30] and [121,31]" |
| "area of [polygon]"                    | area                                              | "Find area of this polygon"                        |
| "length of [line]"                     | length                                            | "Calculate length of this line in km"              |
| "is [point] inside [polygon]"          | booleanPointInPolygon                             | "Is this point inside the polygon?"                |
| "buffer [radius] km/mi around [point]" | buffer                                            | "Create a 5km buffer around this point"            |
| "convex hull of [points]"              | convex                                            | "Compute convex hull of these points"              |
| "cluster points into [n] groups"       | clustersKmeans                                    | "Cluster these points into 5 groups"               |
| "nearest point to [location]"          | nearestPoint                                      | "Find nearest point to [120,30]"                   |
| "simplify geometry"                    | simplify                                          | "Simplify this geometry"                           |
| "union/intersect/difference"           | union/intersect/difference                        | "Union these two polygons"                         |
| "generate hex/square/triangle grid"    | hexGrid/squareGrid/triangleGrid                   | "Generate hex grid for this area"                  |
| "rotate/scale/translate"               | transformRotate/transformScale/transformTranslate | "Rotate this polygon by 45 degrees"                |

### Chinese Query Patterns 中文查询模式

| 查询模式           | 操作                                              | 示例                       |
| ------------------ | ------------------------------------------------- | -------------------------- |
| "计算...的距离"    | distance                                          | "计算北京和上海的距离"     |
| "计算...的面积"    | area                                              | "计算这个多边形的面积"     |
| "点是否在多边形内" | booleanPointInPolygon                             | "天安门是否在五环内？"     |
| "创建...缓冲区"    | buffer                                            | "创建5公里缓冲区"          |
| "计算凸包"         | convex                                            | "计算这些点的凸包"         |
| "聚类分析"         | clustersKmeans/clustersDbscan                     | "对这些点进行聚类"         |
| "查找最近点"       | nearestPoint                                      | "查找距离[120,30]最近的点" |
| "生成网格"         | hexGrid/squareGrid                                | "生成六边形网格"           |
| "旋转/缩放/平移"   | transformRotate/transformScale/transformTranslate | "旋转多边形45度"           |

### Real-World Scenarios 实际场景

```bash
# Beijing to Shanghai distance
turf-skills --action distance \
  --input '{"type":"Point","coordinates":[116.397428,39.90923]}' \
  --input2 '{"type":"Point","coordinates":[121.473701,31.230416]}' \
  --units kilometers

# 5km buffer around a location
turf-skills --action buffer \
  --input '{"type":"Point","coordinates":[116.397428,39.90923]}' \
  --radius 5 --units kilometers

# Point in polygon check
turf-skills --action booleanPointInPolygon \
  --input '{"type":"Point","coordinates":[116.397428,39.90923]}' \
  --input2 '{"type":"Polygon","coordinates":[[[116.1,39.7],[116.8,39.7],[116.8,40.1],[116.1,40.1],[116.1,39.7]]]}'

# Generate hex grid for a region
turf-skills --action hexGrid --bbox '[116,39,117,40]' --cellSide 10 --units kilometers

# K-means clustering
turf-skills --action clustersKmeans --file points.geojson --numberOfClusters 3
```

## When to Use This Skill 何时使用此技能

### ALWAYS Use For 务必使用：
- **Complex operations**: buffer, grid generation, clustering, interpolation
- **GeoJSON output required**: when the result needs to be valid GeoJSON
- **Multiple operations**: chaining spatial analyses
- **File I/O**: reading/writing GeoJSON files

### Consider Direct Turf.js For 考虑直接使用：
- **Simple one-off calculations**: distance, area, bearing (if already in a Node.js script)
- **Performance-critical loops**: when calling the same operation thousands of times

### Performance Notes 性能说明：
- Skill CLI has startup overhead (~1-2 seconds)
- For complex operations, skill is faster and more efficient
- Skill ensures consistent Turf.js implementation

## Best Practices 最佳实践

### 1. Input Validation 输入验证
Always validate coordinates before processing:
- Longitude: -180 to 180
- Latitude: -90 to 90
- Ensure polygons are closed (first == last coordinate)

### 2. Units 单位
- Default unit: kilometers (千米)
- Options: kilometers, miles, meters, degrees, radians
- Always specify units explicitly for clarity

### 3. File Handling 文件处理
- Use `--file` for reading GeoJSON files
- Use `--output` to save results
- Supports both `.geojson` and `.json` extensions

### 4. Error Handling 错误处理
- Check that required parameters are provided
- Validate GeoJSON format before passing to actions
- Handle empty results gracefully

## Real-World Use Cases 实际应用场景

### 1. Delivery Zone Planning 配送范围规划
```bash
# Create 5km delivery zones around stores
turf-skills --action buffer \
  --file stores.geojson \
  --radius 5 \
  --units kilometers \
  --output delivery-zones.geojson
```

### 2. Geographic Fence Check 地理围栏检测
```bash
# Check if customer address is within service area
turf-skills --action booleanPointInPolygon \
  --input '{"type":"Point","coordinates":[lng,lat]}' \
  --file service-area.geojson
```

### 3. Store Location Clustering 门店位置聚类
```bash
# Cluster customer locations for optimal store placement
turf-skills --action clustersKmeans \
  --file customers.geojson \
  --numberOfClusters 5 \
  --output clusters.geojson
```

### 4. Heat Map Grid 热力图网格
```bash
# Generate hex grid for population density visualization
turf-skills --action hexGrid \
  --bbox '[116,39,117,40]' \
  --cellSide 1 \
  --units kilometers \
  --output grid.geojson
```

### 5. Route Simplification 路线简化
```bash
# Simplify GPS track for storage efficiency
turf-skills --action simplify \
  --file gps-track.geojson \
  --tolerance 0.0001 \
  --output simplified-track.geojson
```

## Input/Output Formats 输入输出格式

### GeoJSON Feature Structure
```json
{
  "type": "Feature",
  "properties": {
    "name": "Beijing",
    "population": 21540000
  },
  "geometry": {
    "type": "Point",
    "coordinates": [116.397428, 39.90923]
  }
}
```

### Supported Geometry Types
- `Point` - 点
- `LineString` - 线
- `Polygon` - 面
- `MultiPoint` - 多点
- `MultiLineString` - 多线
- `MultiPolygon` - 多面
- `FeatureCollection` - 要素集合

## Troubleshooting 故障排除

### Common Issues 常见问题

**Issue**: "Error: Unknown action"
- Solution: Use `--list` to see available actions

**Issue**: "Error: Cannot read property"
- Solution: Check GeoJSON format, ensure proper nesting

**Issue**: Empty result for intersection/union
- Solution: Geometries may not overlap; check coordinates

**Issue**: Distance calculation seems wrong
- Solution: Verify units parameter (default is kilometers)

## Additional Resources 更多资源

- Turf.js Documentation: https://turfjs.org/
- GeoJSON Specification: https://geojson.org/
- Coordinate Reference Systems: https://epsg.io/
