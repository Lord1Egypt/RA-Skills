---
name: supermap-wasi-geo
description: 使用SuperMap WebAssembly 进行几何分析，支持缓冲区、凸包、相交、合并、擦除、裁剪等 20+ 种几何操作
version: 1.0.0
author: NestOne
tags:
  - gis
  - geometry
  - buffer
  - convex-hull
  - intersection
  - union
  - spatial-analysis
  - wasm
  - geojson
---

# SuperMap WASI Geometry Skill

基于 SuperMap WebAssembly 的高性能几何分析工具。支持 20+ 种几何分析操作，包括缓冲区分析、拓扑运算、距离计算等。

## 安装

```bash
# 进入项目目录
cd C:\supermap-wasi-geo

# 安装为全局命令（可选）
npm link
```

安装后可以直接使用 `wasi-geo` 命令，否则需要使用 `node bin/supermap-wasi-geo.js`。

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

## 使用方式

### Windows 命令行 (CMD)

```cmd
# 基本用法：操作名 + 参数
node bin\supermap-wasi-geo.js buffer --input "{\"type\":\"Point\",\"coordinates\":[120,30]}" --radius 2

# 显示帮助
node bin\supermap-wasi-geo.js --help

# 显示特定操作帮助
node bin\supermap-wasi-geo.js buffer --help
```

### Windows PowerShell

```powershell
# 基本用法（使用单引号包裹）
node bin/supermap-wasi-geo.js buffer --input '{"type":"Point","coordinates":[120,30]}' --radius 2

# 管道输入
echo '{"type":"Point","coordinates":[120,30]}' | node bin/supermap-wasi-geo.js buffer --radius 2
```

### 通用参数

| 参数 | 说明 |
|------|------|
| `--input <json>` | GeoJSON 字符串输入 |
| `--input-file <path>` | 从文件读取 GeoJSON |
| `--output <path>` | 输出到文件（默认 stdout） |
| `--pretty` | 美化 JSON 输出 |
| `--help, -h` | 显示帮助信息 |
| `--version, -v` | 显示版本信息 |

## 示例

### 1. 缓冲区分析 (Windows CMD)

```cmd
rem 点缓冲区
node bin\supermap-wasi-geo.js buffer --input "{\"type\":\"Point\",\"coordinates\":[120,30]}" --radius 2 --pretty

rem 线缓冲区
node bin\supermap-wasi-geo.js buffer --input "{\"type\":\"LineString\",\"coordinates\":[[0,0],[10,0]]}" --radius 0.5 --pretty

rem 多边形缓冲区
node bin\supermap-wasi-geo.js buffer --input "{\"type\":\"Polygon\",\"coordinates\":[[[0,0],[1,0],[1,1],[0,1],[0,0]]]}" --radius 0.1 --pretty
```

### 2. 距离计算 (Windows CMD)

```cmd
rem 两点距离
node bin\supermap-wasi-geo.js distance --input1 "{\"type\":\"Point\",\"coordinates\":[0,0]}" --input2 "{\"type\":\"Point\",\"coordinates\":[3,4]}"

rem 输出: {"type":"Result","distance":5}
```

### 3. 相交判断 (Windows CMD)

```cmd
node bin\supermap-wasi-geo.js has-intersection --input1 "{\"type\":\"Point\",\"coordinates\":[0,0]}" --input2 "{\"type\":\"Point\",\"coordinates\":[1,1]}"

rem 输出: {"type":"Result","hasIntersection":false}
```

### 4. 点线关系 (Windows CMD)

```cmd
rem 判断点是否在线左侧
node bin\supermap-wasi-geo.js is-left --point "[0,1]" --line-start "[0,0]" --line-end "[1,0]"

rem 判断点是否在线段上
node bin\supermap-wasi-geo.js is-point-on-line --point "[0.5,0]" --line-start "[0,0]" --line-end "[1,0]"

rem 计算点到线段距离
node bin\supermap-wasi-geo.js distance-to-line --point "[0,1]" --line-start "[0,0]" --line-end "[1,0]"
```

### 5. 测地线计算 (Windows CMD)

```cmd
rem 测地线距离（单位：米）
node bin\supermap-wasi-geo.js geodesic-distance --input "{\"type\":\"LineString\",\"coordinates\":[[0,0],[1,1]]}"

rem 测地线面积（单位：平方米）
node bin\supermap-wasi-geo.js geodesic-area --input "{\"type\":\"Polygon\",\"coordinates\":[[[0,0],[1,0],[1,1],[0,1],[0,0]]]}"
```

### 6. 文件输入输出

```cmd
rem 从文件读取，输出到文件
node bin\supermap-wasi-geo.js buffer --input-file input.geojson --radius 2 --output buffer.geojson

rem 双几何操作
node bin\supermap-wasi-geo.js intersect --input1-file polygon1.geojson --input2-file polygon2.geojson --output intersect.geojson
```

### 7. PowerShell 示例

```powershell
# 缓冲区分析
node bin/supermap-wasi-geo.js buffer --input '{"type":"Point","coordinates":[120,30]}' --radius 2 --pretty

# 距离计算
node bin/supermap-wasi-geo.js distance --input1 '{"type":"Point","coordinates":[0,0]}' --input2 '{"type":"Point","coordinates":[3,4]}'

# 管道操作
echo '{"type":"Point","coordinates":[0,0]}' | node bin/supermap-wasi-geo.js buffer --radius 1
```

## 支持的几何类型

- **Point** - 点
- **LineString** - 线
- **Polygon** - 多边形
- **MultiPoint** - 多点
- **MultiLineString** - 多线
- **MultiPolygon** - 多多边形

## 快速测试

```cmd
cd e:\wasi_test

rem 显示帮助
node bin\supermap-wasi-geo.js --help

rem 测试缓冲区
node bin\supermap-wasi-geo.js buffer --input "{\"type\":\"Point\",\"coordinates\":[120,30]}" --radius 2 --pretty

rem 测试距离
node bin\supermap-wasi-geo.js distance --input1 "{\"type\":\"Point\",\"coordinates\":[0,0]}" --input2 "{\"type\":\"Point\",\"coordinates\":[3,4]}"

rem 测试点线关系
node bin\supermap-wasi-geo.js is-left --point "[0,1]" --line-start "[0,0]" --line-end "[1,0]"
```

## Node.js 模块调用

也可以作为 Node.js 模块使用：

```javascript
const GeometryAnalysis = require('./src/geometry-analysis.js');

async function main() {
  // 缓冲区分析
  const buffer = await GeometryAnalysis.buffer(
    { type: 'Point', coordinates: [120, 30] },
    2
  );
  console.log('Buffer:', buffer);

  // 距离计算
  const dist = await GeometryAnalysis.distance(
    { type: 'Point', coordinates: [0, 0] },
    { type: 'Point', coordinates: [3, 4] }
  );
  console.log('Distance:', dist);

  // 点线关系
  const isLeft = await GeometryAnalysis.isLeft([0, 1], [0, 0], [1, 0]);
  console.log('Is Left:', isLeft);
}

main();
```

## 注意事项

1. **坐标单位**：
   - 缓冲区半径的单位与输入坐标系一致
   - 经纬度坐标：单位为度
   - 投影坐标：单位为米或其他投影单位

2. **性能**：首次调用需要初始化 WASM 模块，约需 1-2 秒

3. **Windows 引号问题**：
   - CMD: 使用双引号 `"`，内部双引号用 `\"` 转义
   - PowerShell: 使用单引号 `'` 包裹，内部使用双引号

4. **路径分隔符**：
   - CMD: 使用反斜杠 `\` 或正斜杠 `/`
   - PowerShell: 推荐使用正斜杠 `/`

## 错误处理

CLI 在出错时会返回非零退出码：

```cmd
rem 测试错误情况
node bin\supermap-wasi-geo.js buffer --input "invalid" --radius 2

rem 检查退出码 (CMD)
echo %ERRORLEVEL%
```

## API 参考

### 单几何操作

```javascript
// 缓冲区分析
await GeometryAnalysis.buffer(input, radius);

// 凸包计算
await GeometryAnalysis.computeConvexHull(input);

// 重采样
await GeometryAnalysis.resample(input, tolerance);

// 光滑
await GeometryAnalysis.smooth(input, smoothness);

// 测地线距离
await GeometryAnalysis.computeGeodesicDistance(input, majorAxis?, flatten?);

// 测地线面积
await GeometryAnalysis.computeGeodesicArea(input, majorAxis?, flatten?);

// 平行线
await GeometryAnalysis.computeParallel(input, distance);
```

### 双几何操作

```javascript
// 相交
await GeometryAnalysis.intersect(input1, input2);

// 合并
await GeometryAnalysis.union(input1, input2);

// 擦除
await GeometryAnalysis.erase(input1, input2);

// 异或
await GeometryAnalysis.xor(input1, input2);

// 裁剪
await GeometryAnalysis.clip(input1, input2);

// 判断相交
await GeometryAnalysis.hasIntersection(input1, input2, tolerance?);

// 判断接触
await GeometryAnalysis.hasTouch(input1, input2, tolerance?);

// 判断相等
await GeometryAnalysis.isIdentical(input1, input2, tolerance?);

// 计算距离
await GeometryAnalysis.distance(input1, input2);
```

### 点线关系

```javascript
// 点是否在线左侧
await GeometryAnalysis.isLeft(point, lineStart, lineEnd);

// 点是否在线右侧
await GeometryAnalysis.isRight(point, lineStart, lineEnd);

// 点是否在线段上
await GeometryAnalysis.isPointOnLine(point, lineStart, lineEnd, extended?);

// 两线是否平行
await GeometryAnalysis.isParallel(line1Start, line1End, line2Start, line2End);

// 点到线段距离
await GeometryAnalysis.distanceToLineSegment(point, lineStart, lineEnd);
```
