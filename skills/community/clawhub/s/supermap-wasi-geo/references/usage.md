# SuperMap WASI Geometry 详细使用说明

## 安装与配置

### 环境要求

- Node.js 14.0 或更高版本
- 支持 SuperMap WebAssembly 的运行环境

### 验证安装

```bash
# 检查 Node.js 版本
node --version

# 测试 CLI
node scripts/bin/supermap-wasi-geo.js --help
```

## 支持的操作

### 单几何操作

| 操作 | 说明 | 参数 |
|------|------|------|
| `buffer` | 缓冲区分析 | `--input`, `--radius` |
| `convex-hull` | 凸包计算 | `--input` |
| `resample` | 重采样分析 | `--input`, `--tolerance` |
| `smooth` | 线要素光滑 | `--input`, `--smoothness` |
| `geodesic-distance` | 测地线距离 | `--input`, `[--major-axis]`, `[--flatten]` |
| `geodesic-area` | 测地线面积 | `--input`, `[--major-axis]`, `[--flatten]` |
| `parallel` | 计算平行线 | `--input`, `--distance` |

### 双几何操作

| 操作 | 说明 | 参数 |
|------|------|------|
| `intersect` | 相交分析 | `--input1`, `--input2` |
| `union` | 合并分析 | `--input1`, `--input2` |
| `erase` | 擦除分析 | `--input1`, `--input2` |
| `xor` | 异或分析 | `--input1`, `--input2` |
| `clip` | 裁剪分析 | `--input1`, `--input2` |
| `has-intersection` | 判断是否相交 | `--input1`, `--input2`, `[--tolerance]` |
| `has-touch` | 判断边界是否接触 | `--input1`, `--input2`, `[--tolerance]` |
| `is-identical` | 判断是否相等 | `--input1`, `--input2`, `[--tolerance]` |
| `distance` | 计算两几何距离 | `--input1`, `--input2` |

### 点线关系分析

| 操作 | 说明 | 参数 |
|------|------|------|
| `is-left` | 点是否在线左侧 | `--point`, `--line-start`, `--line-end` |
| `is-right` | 点是否在线右侧 | `--point`, `--line-start`, `--line-end` |
| `is-point-on-line` | 点是否在线段上 | `--point`, `--line-start`, `--line-end`, `[--extended]` |
| `is-parallel` | 两线是否平行 | `--line1-start`, `--line1-end`, `--line2-start`, `--line2-end` |
| `distance-to-line` | 点到线段距离 | `--point`, `--line-start`, `--line-end` |

## 完整 API 参考

### CLI 命令

```
node scripts/bin/supermap-wasi-geo.js <operation> [options]
```

### 通用选项

| 选项 | 简写 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `--input` | | string | 二选一 | - | GeoJSON 字符串 |
| `--input-file` | | path | 二选一 | - | 输入文件路径 |
| `--output` | | path | 否 | stdout | 输出文件路径 |
| `--pretty` | | boolean | 否 | false | 美化 JSON 输出 |
| `--help` | `-h` | | 否 | | 显示帮助 |
| `--version` | `-v` | | 否 | | 显示版本 |

### 操作特定参数

| 参数 | 适用操作 | 说明 |
|------|----------|------|
| `--radius` | buffer | 缓冲区半径 |
| `--tolerance` | resample, has-intersection, has-touch, is-identical | 容差值 |
| `--smoothness` | smooth | 光滑度（整数） |
| `--distance` | parallel | 平行线距离 |
| `--major-axis` | geodesic-distance, geodesic-area | 椭球长半轴（默认 6378137） |
| `--flatten` | geodesic-distance, geodesic-area | 椭球扁率（默认 0.003352810664） |
| `--extended` | is-point-on-line | 是否延长线段 |

### 输入格式

支持以下 GeoJSON 格式：

#### 1. Geometry 直接输入

```json
{"type": "Point", "coordinates": [120, 30]}
```

#### 2. Feature 输入

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [120, 30]
  },
  "properties": {
    "name": "示例点"
  }
}
```

#### 3. 支持的几何类型

- `Point` - 点
- `LineString` - 线
- `Polygon` - 多边形
- `MultiPoint` - 多点
- `MultiLineString` - 多线
- `MultiPolygon` - 多多边形

### 输出格式

#### 几何操作输出

返回 GeoJSON Feature：

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [[x1, y1], [x2, y2], ..., [x1, y1]]
    ]
  },
  "properties": {
    "bufferRadius": <radius>,
    "...": "其他原始属性"
  }
}
```

#### 判断操作输出

返回结果对象：

```json
{
  "type": "Result",
  "hasIntersection": true
}
```

#### 计算操作输出

返回结果对象：

```json
{
  "type": "Result",
  "distance": 5,
  "unit": "meters"
}
```

## 使用场景

### 场景 1: 缓冲区分析

分析城市中心 50km 范围内的区域：

```bash
node scripts/bin/supermap-wasi-geo.js buffer --input '{"type":"Point","coordinates":[116.4,39.9]}' --radius 0.5 --pretty
```

> 注意：经纬度坐标系下，1度约等于 111km

### 场景 2: 距离计算

计算两点之间的欧氏距离：

```bash
node scripts/bin/supermap-wasi-geo.js distance --input1 '{"type":"Point","coordinates":[0,0]}' --input2 '{"type":"Point","coordinates":[3,4]}'
# 输出: {"type":"Result","distance":5}
```

### 场景 3: 相交判断

判断两个几何对象是否相交：

```bash
node scripts/bin/supermap-wasi-geo.js has-intersection --input1 '{"type":"Point","coordinates":[0,0]}' --input2 '{"type":"Point","coordinates":[1,1]}'
# 输出: {"type":"Result","hasIntersection":false}
```

### 场景 4: 点线关系

判断点是否在线段上：

```bash
node scripts/bin/supermap-wasi-geo.js is-point-on-line --point "[0.5,0]" --line-start "[0,0]" --line-end "[1,0]"
# 输出: {"type":"Result","isPointOnLine":true}
```

### 场景 5: 测地线计算

计算线段的测地线距离（单位：米）：

```bash
node scripts/bin/supermap-wasi-geo.js geodesic-distance --input '{"type":"LineString","coordinates":[[0,0],[1,1]]}'
```

### 场景 6: 批量处理

使用脚本批量处理多个文件：

```bash
# Windows PowerShell
Get-ChildItem *.geojson | ForEach-Object {
    node scripts/bin/supermap-wasi-geo.js buffer --input-file $_.Name --radius 1 --output "buffer_$($_.Name)"
}
```

## Node.js 模块 API

### 引入模块

```javascript
const GeometryAnalysis = require('./scripts/src/geometry-analysis.js');
```

### 单几何操作

```javascript
// 缓冲区分析
const buffer = await GeometryAnalysis.buffer(input, radius);

// 凸包计算
const hull = await GeometryAnalysis.computeConvexHull(input);

// 重采样
const resampled = await GeometryAnalysis.resample(input, tolerance);

// 光滑
const smoothed = await GeometryAnalysis.smooth(input, smoothness);

// 测地线距离
const geoDist = await GeometryAnalysis.computeGeodesicDistance(input, majorAxis?, flatten?);

// 测地线面积
const geoArea = await GeometryAnalysis.computeGeodesicArea(input, majorAxis?, flatten?);

// 平行线
const parallel = await GeometryAnalysis.computeParallel(input, distance);
```

### 双几何操作

```javascript
// 相交
const intersect = await GeometryAnalysis.intersect(input1, input2);

// 合并
const union = await GeometryAnalysis.union(input1, input2);

// 擦除
const erased = await GeometryAnalysis.erase(input1, input2);

// 异或
const xored = await GeometryAnalysis.xor(input1, input2);

// 裁剪
const clipped = await GeometryAnalysis.clip(input1, input2);

// 判断相交
const hasInt = await GeometryAnalysis.hasIntersection(input1, input2, tolerance?);

// 判断接触
const hasTch = await GeometryAnalysis.hasTouch(input1, input2, tolerance?);

// 判断相等
const isId = await GeometryAnalysis.isIdentical(input1, input2, tolerance?);

// 计算距离
const dist = await GeometryAnalysis.distance(input1, input2);
```

### 点线关系

```javascript
// 点是否在线左侧
const left = await GeometryAnalysis.isLeft(point, lineStart, lineEnd);

// 点是否在线右侧
const right = await GeometryAnalysis.isRight(point, lineStart, lineEnd);

// 点是否在线段上
const onLine = await GeometryAnalysis.isPointOnLine(point, lineStart, lineEnd, extended?);

// 两线是否平行
const parallel = await GeometryAnalysis.isParallel(line1Start, line1End, line2Start, line2End);

// 点到线段距离
const dist = await GeometryAnalysis.distanceToLineSegment(point, lineStart, lineEnd);
```

## 常见问题

### Q: 缓冲区结果不正确？

A: 检查以下几点：
1. 坐标单位是否正确（经纬度用度，投影坐标用米）
2. 半径是否为正数
3. GeoJSON 格式是否正确

### Q: Windows CMD 中引号问题？

A: Windows CMD 使用双引号，内部双引号需要转义：

```cmd
node scripts\bin\supermap-wasi-geo.js buffer --input "{\"type\":\"Point\",\"coordinates\":[120,30]}" --radius 2
```

### Q: 首次运行很慢？

A: 首次运行需要初始化 WASM 模块（约 1-2 秒），后续调用会更快。

### Q: 如何在其他目录使用？

A: 使用绝对路径或先 cd 到 skill 目录：

```bash
cd /path/to/wasi-buffer-skill
node scripts/bin/supermap-wasi-geo.js buffer --input '...' --radius 1
```

## 性能优化

1. **批量处理**：使用文件输入/输出减少命令行参数解析开销
2. **管道操作**：使用 stdin/stdout 进行链式处理
3. **避免重复初始化**：在脚本中复用模块实例

## 技术细节

### WASM 模块

- 文件：`scripts/wasm/UGCWasmAll.js`
- 大小：约 1.6 MB（包含内嵌 WASM 二进制）
- 来源：SuperMap UGC Wasm

### 内存管理

WASM 模块使用 Emscripten 运行时，自动管理内存。大几何对象可能需要更多内存。

### 坐标系

默认假设输入为 WGS84 经纬度坐标。使用其他坐标系时，注意半径单位匹配。
