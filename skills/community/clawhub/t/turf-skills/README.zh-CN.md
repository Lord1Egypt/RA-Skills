# turf-skills

基于 [Turf.js](https://turfjs.org/) 的空间分析 Claude Code 技能。

[English](./README.md)

## 安装

### 作为 Claude Code 技能

```bash
# npm 全局安装
npm install -g turf-skills

# 或克隆并链接
git clone https://github.com/zhyt1985/turf-skills.git
cd turf-skills && npm install && npm link

# 安装为技能
mkdir -p ~/.claude/skills/turf-skills
ln -s $(which turf-skills) ~/.claude/skills/turf-skills/
cp SKILL.md ~/.claude/skills/turf-skills/
```

### 作为命令行工具

```bash
npm install -g turf-skills
turf-skills --action distance --input '{"type":"Point","coordinates":[120,30]}' --input2 '{"type":"Point","coordinates":[121,31]}'
```

## 功能

| 分类      | 操作                                                                                                                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 测量      | distance, area, length, bearing, destination, midpoint, center, centroid, centerOfMass, along, bbox, bboxPolygon, envelope                                                                 |
| 空间查询  | booleanPointInPolygon, booleanContains, booleanCrosses, booleanDisjoint, booleanEqual, booleanIntersects, booleanOverlap, booleanWithin, booleanParallel, booleanPointOnLine, nearestPoint |
| 变换      | buffer, union, intersect, difference, simplify, convex, concave, dissolve, voronoi, tin, bezierSpline, transformRotate, transformScale, transformTranslate                                 |
| 创建      | point, lineString, polygon, multiPoint, multiLineString, multiPolygon, featureCollection, randomPoint, randomLineString, randomPolygon                                                     |
| 插值/网格 | interpolate, isobands, isolines, hexGrid, pointGrid, squareGrid, triangleGrid                                                                                                              |
| 聚类      | clustersKmeans, clustersDbscan                                                                                                                                                             |

## 示例

### 基本用法

```bash
# 计算两点距离
turf-skills --action distance \
  --input '{"type":"Point","coordinates":[120,30]}' \
  --input2 '{"type":"Point","coordinates":[121,31]}'

# 判断点是否在多边形内
turf-skills --action booleanPointInPolygon \
  --input '{"type":"Point","coordinates":[120.5,30.5]}' \
  --input2 '{"type":"Polygon","coordinates":[[[120,30],[121,30],[121,31],[120,31],[120,30]]]}'

# 创建缓冲区
turf-skills --action buffer \
  --input '{"type":"Point","coordinates":[120,30]}' \
  --radius 5 --units kilometers

# 从文件读取
turf-skills --action area --file polygon.geojson

# 六边形网格
turf-skills --action hexGrid --bbox '[120,30,121,31]' --cellSide 5

# K均值聚类
turf-skills --action clustersKmeans --file points.geojson --numberOfClusters 5
```

### 实际场景

```bash
# 北京到上海的距离 → 1068 公里
turf-skills --action distance \
  --input '{"type":"Point","coordinates":[116.397428,39.90923]}' \
  --input2 '{"type":"Point","coordinates":[121.473701,31.230416]}' \
  --units kilometers

# 天安门是否在北京五环内？ → true
turf-skills --action booleanPointInPolygon \
  --input '{"type":"Point","coordinates":[116.397428,39.90923]}' \
  --input2 '{"type":"Polygon","coordinates":[[[116.1,39.7],[116.8,39.7],[116.8,40.1],[116.1,40.1],[116.1,39.7]]]}'

# 给天安门创建 5 公里缓冲区
turf-skills --action buffer \
  --input '{"type":"Point","coordinates":[116.397428,39.90923]}' \
  --radius 5 --units kilometers

# 两个多边形求并集
turf-skills --action union \
  --input '{"type":"Polygon","coordinates":[[[120,30],[121,30],[121,31],[120,31],[120,30]]]}' \
  --input2 '{"type":"Polygon","coordinates":[[[120.5,30.5],[121.5,30.5],[121.5,31.5],[120.5,31.5],[120.5,30.5]]]}'

# 生成区域六边形网格（28 个六边形）
turf-skills --action hexGrid --bbox '[116,39,117,40]' --cellSide 10 --units kilometers

# K均值聚类分为 3 组
turf-skills --action clustersKmeans --file points.geojson --numberOfClusters 3

# 创建带属性的点
turf-skills --action point \
  --coordinates '[116.397428,39.90923]' \
  --properties '{"name":"天安门"}'

# 求点集的凸包
turf-skills --action convex --file points.geojson

# 查找最近点
turf-skills --action nearestPoint \
  --input '{"type":"Point","coordinates":[120.3,30.3]}' \
  --file2 points-collection.geojson

# 计算线段长度（公里）
turf-skills --action length --file line.geojson --units kilometers

# 输出结果到文件
turf-skills --action buffer --file point.geojson --radius 10 --output result.geojson
```

## 参数

| 参数                   | 说明                   |
| ---------------------- | ---------------------- |
| `--action <name>`      | Turf 函数名（必填）    |
| `--input <geojson>`    | 第一个 GeoJSON 输入    |
| `--input2 <geojson>`   | 第二个 GeoJSON 输入    |
| `--file <path>`        | 从文件读取第一个输入   |
| `--file2 <path>`       | 从文件读取第二个输入   |
| `--output <path>`      | 输出到文件             |
| `--units <km\|mi\|m>`  | 距离单位               |
| `--radius <n>`         | 缓冲区半径             |
| `--bbox <json>`        | 边界框                 |
| `--cellSide <n>`       | 网格单元大小           |
| `--coordinates <json>` | 坐标数组（创建几何用） |
| `--properties <json>`  | 属性对象（创建几何用） |
| `--list`               | 列出所有操作           |
| `--help`               | 显示帮助               |

## 在 Claude Code 中用自然语言调用

安装为 Claude Code 技能后，可以直接用自然语言描述需求，Claude 会自动转换为对应的 turf-skills 命令。

| 你说                                                        | Claude 执行                                                                                                                                                                        |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "计算北京到上海的距离"                                      | `turf-skills --action distance --input '{"type":"Point","coordinates":[116.397428,39.90923]}' --input2 '{"type":"Point","coordinates":[121.473701,31.230416]}' --units kilometers` |
| "天安门是否在这个多边形内？"                                | `turf-skills --action booleanPointInPolygon --input '...' --input2 '...'`                                                                                                          |
| "给这个点创建 5 公里缓冲区"                                 | `turf-skills --action buffer --input '...' --radius 5 --units kilometers`                                                                                                          |
| "对 points.geojson 中的点集计算凸包，保存到 result.geojson" | `turf-skills --action convex --file points.geojson --output result.geojson`                                                                                                        |
| "计算 polygon.geojson 的面积"                               | `turf-skills --action area --file polygon.geojson`                                                                                                                                 |
| "生成北京区域的六边形网格"                                  | `turf-skills --action hexGrid --bbox '[116,39,117,40]' --cellSide 10 --units kilometers`                                                                                           |
| "把这些点聚类成 3 组"                                       | `turf-skills --action clustersKmeans --file points.geojson --numberOfClusters 3`                                                                                                   |
| "查找离 [120.3, 30.3] 最近的点"                             | `turf-skills --action nearestPoint --input '...' --file2 points.geojson`                                                                                                           |
| "合并这两个多边形"                                          | `turf-skills --action union --input '...' --input2 '...'`                                                                                                                          |
| "这条线有多长（公里）？"                                    | `turf-skills --action length --file line.geojson --units kilometers`                                                                                                               |

## 许可证

MIT
