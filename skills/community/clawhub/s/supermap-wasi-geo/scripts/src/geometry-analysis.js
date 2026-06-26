/**
 * 几何分析模块
 * 封装 WASM 的所有几何分析功能
 */

const { initWasm } = require('./wasm-adapter');
const {
  parseGeoJSON,
  geojsonCoordsToPoint2Ds,
  geojsonCoords2UGDoubleArray,
  geojson2UGGeometry,
  ugGeometry2Geojson
} = require('./geojson');

// ==================== 几何分析函数 ====================

/**
 * 缓冲区分析
 */
async function buffer(input, radius) {
  const parsedInput = typeof input === 'string' ? JSON.parse(input) : input;
  const Module = await initWasm();
  const ugGeom = geojson2UGGeometry(Module, parsedInput);
  const result = Module._UGCWasm_Geometrist_Buffer(ugGeom, radius);
  const geometry = ugGeometry2Geojson(Module, result);
  return { type: 'Feature', geometry, properties: { bufferRadius: radius } };
}

/**
 * 凸多边形计算
 */
async function computeConvexHull(input) {
  const parsedInput = typeof input === 'string' ? JSON.parse(input) : input;
  const { type, coordinates } = parseGeoJSON(parsedInput);
  const Module = await initWasm();

  // 提取扁平的点坐标数组
  let points;
  switch (type) {
    case 'Point':
      points = [coordinates];
      break;
    case 'MultiPoint':
    case 'LineString':
      points = coordinates;
      break;
    case 'MultiLineString':
    case 'Polygon':
      points = coordinates.flat();
      break;
    case 'MultiPolygon':
      points = coordinates.flat(2);
      break;
    default:
      points = coordinates;
  }

  const ugPoints = geojsonCoordsToPoint2Ds(Module, points);
  const result = Module._UGCWasm_Geometrist_ComputeConvexHull(ugPoints, points.length);
  const geometry = ugGeometry2Geojson(Module, result);
  return { type: 'Feature', geometry, properties: {} };
}

/**
 * 重采样分析
 */
async function resample(input, tolerance) {
  const parsedInput = typeof input === 'string' ? JSON.parse(input) : input;
  const Module = await initWasm();
  const ugFeature = geojson2UGGeometry(Module, parsedInput);
  const result = Module._UGCWasm_Geometrist_Resample(ugFeature, tolerance);
  const geometry = ugGeometry2Geojson(Module, result);
  return { type: 'Feature', geometry, properties: { tolerance } };
}

/**
 * 线要素光滑分析
 */
async function smooth(input, smoothness) {
  const parsedInput = typeof input === 'string' ? JSON.parse(input) : input;
  const Module = await initWasm();
  const ugFeature = geojson2UGGeometry(Module, parsedInput);
  const result = Module._UGCWasm_Geometrist_Smooth(ugFeature, smoothness);
  const geometry = ugGeometry2Geojson(Module, result);
  return { type: 'Feature', geometry, properties: { smoothness } };
}

/**
 * 计算测地线距离
 */
async function computeGeodesicDistance(input, majorAxis = 6378137, flatten = 0.003352810664) {
  const parsedInput = typeof input === 'string' ? JSON.parse(input) : input;
  const { type, coordinates } = parseGeoJSON(parsedInput);
  const Module = await initWasm();

  // 提取点坐标并分离 x/y 数组
  let points;
  switch (type) {
    case 'Point':
      points = [coordinates];
      break;
    case 'MultiPoint':
    case 'LineString':
      points = coordinates;
      break;
    default:
      points = Array.isArray(coordinates[0]) && Array.isArray(coordinates[0][0])
        ? coordinates.flat()
        : coordinates;
  }

  const xArray = points.map(p => p[0]);
  const yArray = points.map(p => p[1]);
  const pXArray = geojsonCoords2UGDoubleArray(Module, xArray);
  const pYArray = geojsonCoords2UGDoubleArray(Module, yArray);
  const distance = Module._UGCWasm_Geometrist_ComputeGeodesicDistance(pXArray, pYArray, majorAxis, flatten);
  return { type: 'Result', distance, unit: 'meters', properties: {} };
}

/**
 * 计算测地线面积
 */
async function computeGeodesicArea(input, majorAxis = 6378137, flatten = 0.003352810664) {
  const parsedInput = typeof input === 'string' ? JSON.parse(input) : input;
  const Module = await initWasm();
  const ugFeature = geojson2UGGeometry(Module, parsedInput);
  const prjCoordSys = Module._UGCWasm_Geometry_NewUGPrjCoordSys(4326);
  const area = Module._UGCWasm_Geometrist_ComputeGeodesicArea(ugFeature, prjCoordSys);
  return { type: 'Result', area, unit: 'square_meters', properties: {} };
}

/**
 * 几何对象是否相交
 */
async function hasIntersection(input1, input2, tolerance = 0) {
  const parsed1 = typeof input1 === 'string' ? JSON.parse(input1) : input1;
  const parsed2 = typeof input2 === 'string' ? JSON.parse(input2) : input2;
  const Module = await initWasm();
  const ugFeature1 = geojson2UGGeometry(Module, parsed1);
  const ugFeature2 = geojson2UGGeometry(Module, parsed2);
  const result = Module._UGCWasm_Geometrist_HasIntersection(ugFeature1, ugFeature2, tolerance);
  return { type: 'Result', hasIntersection: result === 1 };
}

/**
 * 几何对象边界是否接触
 */
async function hasTouch(input1, input2, tolerance = 0) {
  const parsed1 = typeof input1 === 'string' ? JSON.parse(input1) : input1;
  const parsed2 = typeof input2 === 'string' ? JSON.parse(input2) : input2;
  const Module = await initWasm();
  const ugFeature1 = geojson2UGGeometry(Module, parsed1);
  const ugFeature2 = geojson2UGGeometry(Module, parsed2);
  const result = Module._UGCWasm_Geometrist_HasTouch(ugFeature1, ugFeature2, tolerance);
  return { type: 'Result', hasTouch: result === 1 };
}

/**
 * 几何对象相等分析
 */
async function isIdentical(input1, input2, tolerance = 0) {
  const parsed1 = typeof input1 === 'string' ? JSON.parse(input1) : input1;
  const parsed2 = typeof input2 === 'string' ? JSON.parse(input2) : input2;
  const Module = await initWasm();
  const ugFeature1 = geojson2UGGeometry(Module, parsed1);
  const ugFeature2 = geojson2UGGeometry(Module, parsed2);
  const result = Module._UGCWasm_Geometrist_IsIdentical(ugFeature1, ugFeature2, tolerance);
  return { type: 'Result', isIdentical: result === 1 };
}

/**
 * 相交分析
 */
async function intersect(input1, input2) {
  const parsed1 = typeof input1 === 'string' ? JSON.parse(input1) : input1;
  const parsed2 = typeof input2 === 'string' ? JSON.parse(input2) : input2;
  const Module = await initWasm();
  const ugFeature1 = geojson2UGGeometry(Module, parsed1);
  const ugFeature2 = geojson2UGGeometry(Module, parsed2);
  const resultPtr = Module._UGCWasm_Geometrist_Intersect(ugFeature1, ugFeature2);
  if (!resultPtr) return null;
  const geometry = ugGeometry2Geojson(Module, resultPtr);
  return { type: 'Feature', geometry, properties: {} };
}

/**
 * 合并分析
 */
async function union(input1, input2) {
  const parsed1 = typeof input1 === 'string' ? JSON.parse(input1) : input1;
  const parsed2 = typeof input2 === 'string' ? JSON.parse(input2) : input2;
  const Module = await initWasm();
  const ugFeature1 = geojson2UGGeometry(Module, parsed1);
  const ugFeature2 = geojson2UGGeometry(Module, parsed2);
  const resultPtr = Module._UGCWasm_Geometrist_Union(ugFeature1, ugFeature2);
  if (!resultPtr) return null;
  const geometry = ugGeometry2Geojson(Module, resultPtr);
  return { type: 'Feature', geometry, properties: {} };
}

/**
 * 擦除分析
 */
async function erase(input1, input2) {
  const parsed1 = typeof input1 === 'string' ? JSON.parse(input1) : input1;
  const parsed2 = typeof input2 === 'string' ? JSON.parse(input2) : input2;
  const Module = await initWasm();
  const ugFeature1 = geojson2UGGeometry(Module, parsed1);
  const ugFeature2 = geojson2UGGeometry(Module, parsed2);
  const resultPtr = Module._UGCWasm_Geometrist_Erase(ugFeature1, ugFeature2);
  if (!resultPtr) return null;
  const geometry = ugGeometry2Geojson(Module, resultPtr);
  return { type: 'Feature', geometry, properties: {} };
}

/**
 * 异或分析
 */
async function xor(input1, input2) {
  const parsed1 = typeof input1 === 'string' ? JSON.parse(input1) : input1;
  const parsed2 = typeof input2 === 'string' ? JSON.parse(input2) : input2;
  const Module = await initWasm();
  const ugFeature1 = geojson2UGGeometry(Module, parsed1);
  const ugFeature2 = geojson2UGGeometry(Module, parsed2);
  const resultPtr = Module._UGCWasm_Geometrist_XOR(ugFeature1, ugFeature2);
  if (!resultPtr) return null;
  const geometry = ugGeometry2Geojson(Module, resultPtr);
  return { type: 'Feature', geometry, properties: {} };
}

/**
 * 裁剪分析
 */
async function clip(input1, input2) {
  const parsed1 = typeof input1 === 'string' ? JSON.parse(input1) : input1;
  const parsed2 = typeof input2 === 'string' ? JSON.parse(input2) : input2;
  const Module = await initWasm();
  const ugFeature1 = geojson2UGGeometry(Module, parsed1);
  const ugFeature2 = geojson2UGGeometry(Module, parsed2);
  const resultPtr = Module._UGCWasm_Geometrist_Clip(ugFeature1, ugFeature2);
  if (!resultPtr) return null;
  const geometry = ugGeometry2Geojson(Module, resultPtr);
  return { type: 'Feature', geometry, properties: {} };
}

/**
 * 计算距离
 */
async function distance(input1, input2) {
  const parsed1 = typeof input1 === 'string' ? JSON.parse(input1) : input1;
  const parsed2 = typeof input2 === 'string' ? JSON.parse(input2) : input2;
  const Module = await initWasm();
  const ugFeature1 = geojson2UGGeometry(Module, parsed1);
  const ugFeature2 = geojson2UGGeometry(Module, parsed2);
  const dist = Module._UGCWasm_Geometrist_Distance(ugFeature1, ugFeature2);
  return { type: 'Result', distance: dist };
}

/**
 * 点是否在线的左侧
 */
async function isLeft(point, lineStart, lineEnd) {
  const Module = await initWasm();
  const result = Module._UGCWasm_Geometrist_IsLeft(
    point[0], point[1],
    lineStart[0], lineStart[1],
    lineEnd[0], lineEnd[1]
  );
  return { type: 'Result', isLeft: result === 1 };
}

/**
 * 点是否在线的右侧
 */
async function isRight(point, lineStart, lineEnd) {
  const Module = await initWasm();
  const result = Module._UGCWasm_Geometrist_IsRight(
    point[0], point[1],
    lineStart[0], lineStart[1],
    lineEnd[0], lineEnd[1]
  );
  return { type: 'Result', isRight: result === 1 };
}

/**
 * 点是否在线段上
 */
async function isPointOnLine(point, lineStart, lineEnd, extended = false) {
  const Module = await initWasm();
  const result = Module._UGCWasm_Geometrist_IsPointOnLine(
    point[0], point[1],
    lineStart[0], lineStart[1],
    lineEnd[0], lineEnd[1],
    extended ? 1 : 0
  );
  return { type: 'Result', isPointOnLine: result === 1 };
}

/**
 * 线平行分析
 */
async function isParallel(line1Start, line1End, line2Start, line2End) {
  const Module = await initWasm();
  const result = Module._UGCWasm_Geometrist_IsParallel(
    line1Start[0], line1Start[1], line1End[0], line1End[1],
    line2Start[0], line2Start[1], line2End[0], line2End[1]
  );
  return { type: 'Result', isParallel: result === 1 };
}

/**
 * 计算点到线段的距离
 */
async function distanceToLineSegment(point, lineStart, lineEnd) {
  const Module = await initWasm();
  const dist = Module._UGCWasm_Geometrist_DistanceToLineSegment(
    point[0], point[1],
    lineStart[0], lineStart[1],
    lineEnd[0], lineEnd[1]
  );
  return { type: 'Result', distance: dist };
}

/**
 * 计算平行线
 */
async function computeParallel(input, distance) {
  const parsedInput = typeof input === 'string' ? JSON.parse(input) : input;
  const Module = await initWasm();
  const ugFeature = geojson2UGGeometry(Module, parsedInput);
  const result = Module._UGCWasm_Geometrist_ComputeParallel(ugFeature, distance);
  const geometry = ugGeometry2Geojson(Module, result);
  return { type: 'Feature', geometry, properties: { distance } };
}

// 导出所有函数
module.exports = {
  // 单几何操作
  buffer,
  computeConvexHull,
  resample,
  smooth,
  computeGeodesicDistance,
  computeGeodesicArea,
  computeParallel,
  
  // 双几何操作
  hasIntersection,
  hasTouch,
  isIdentical,
  intersect,
  union,
  erase,
  xor,
  clip,
  distance,
  
  // 点线关系
  isLeft,
  isRight,
  isPointOnLine,
  isParallel,
  distanceToLineSegment
};
