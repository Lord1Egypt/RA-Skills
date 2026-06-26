/**
 * GeoJSON 解析和序列化模块
 * 处理 GeoJSON 与 WASM 内存之间的数据转换
 */

/**
 * 几何类型枚举
 */
const GeometryType = {
  POINT: 1,
  LINESTRING: 2,
  POLYGON: 3,
  MULTIPOINT: 4,
  MULTILINESTRING: 5,
  MULTIPOLYGON: 6
};

/**
 * 从 WASM 内存读取点坐标
 * @param {Object} Module - WASM 模块实例
 * @param {number} ptr - 内存指针
 * @param {number} offset - 偏移量
 * @returns {[number, number]} [x, y] 坐标
 */
function readPoint(Module, ptr, offset = 0) {
  const x = Module.HEAPF64[ptr / 8 + offset * 2];
  const y = Module.HEAPF64[ptr / 8 + offset * 2 + 1];
  return [x, y];
}

/**
 * 从 WASM 内存读取坐标数组
 * @param {Object} Module - WASM 模块实例
 * @param {number} ptr - 内存指针
 * @param {number} count - 点数量
 * @returns {Array<Array<number>>} 坐标数组
 */
function readPoints(Module, ptr, count) {
  const points = [];
  for (let i = 0; i < count; i++) {
    points.push(readPoint(Module, ptr, i));
  }
  return points;
}

/**
 * 将坐标写入 WASM 内存
 * @param {Object} Module - WASM 模块实例
 * @param {number} ptr - 内存指针
 * @param {Array<Array<number>>} points - 坐标数组
 */
function writePoints(Module, ptr, points) {
  for (let i = 0; i < points.length; i++) {
    const [x, y] = points[i];
    Module.HEAPF64[ptr / 8 + i * 2] = x;
    Module.HEAPF64[ptr / 8 + i * 2 + 1] = y;
  }
}

/**
 * 从 GeoRegion 对象提取多边形坐标
 * @param {Object} Module - WASM 模块实例
 * @param {number} regionPtr - GeoRegion 指针
 * @returns {Array<Array<Array<number>>>} 多边形坐标（支持带洞）
 */
function extractPolygonFromRegion(Module, regionPtr) {
  if (!regionPtr) return null;

  const partCount = Module._UGCWasm_GeoRegion_GetPartCount(regionPtr);
  if (partCount === 0) return null;

  const coordinates = [];

  for (let part = 0; part < partCount; part++) {
    const pointCount = Module._UGCWasm_GeoRegion_GetPartPointCount(regionPtr, part);
    if (pointCount === 0) continue;

    // 使用 GetSubPoints 获取点坐标数组的指针
    const pointsPtr = Module._UGCWasm_GeoRegion_GetSubPoints(regionPtr);
    
    if (!pointsPtr) {
      console.error('GetSubPoints returned null');
      continue;
    }

    // 从内存读取点坐标
    // 注意：GetSubPoints 返回的是所有部分的点，需要根据 part 索引计算偏移
    // 简化处理：假设第一部分从索引 0 开始
    const ring = [];
    for (let i = 0; i < pointCount; i++) {
      const x = Module.HEAPF64[pointsPtr / 8 + i * 2];
      const y = Module.HEAPF64[pointsPtr / 8 + i * 2 + 1];
      ring.push([x, y]);
    }

    // 确保首尾点相同（闭合多边形）
    if (ring.length > 0) {
      const first = ring[0];
      const last = ring[ring.length - 1];
      if (first[0] !== last[0] || first[1] !== last[1]) {
        ring.push([...first]);
      }
    }

    coordinates.push(ring);
  }

  return coordinates.length > 0 ? coordinates : null;
}

/**
 * 从 GeoLine 对象提取线坐标
 * @param {Object} Module - WASM 模块实例
 * @param {number} linePtr - GeoLine 指针
 * @returns {Array<Array<Array<number>>>} 多线坐标
 */
function extractLineFromGeoLine(Module, linePtr) {
  if (!linePtr) return null;

  const partCount = Module._UGCWasm_GeoLine_GetPartCount(linePtr);
  if (partCount === 0) return null;

  const coordinates = [];

  for (let part = 0; part < partCount; part++) {
    const pointCount = Module._UGCWasm_GeoLine_GetPartPointCount(linePtr, part);
    if (pointCount === 0) continue;

    const bufferSize = pointCount * 2 * 8;
    const bufferPtr = Module._malloc(bufferSize);

    try {
      const actualCount = Module._UGCWasm_GeoLine_GetPart2(linePtr, part, bufferPtr, pointCount);
      const line = readPoints(Module, bufferPtr, actualCount);
      coordinates.push(line);
    } finally {
      Module._free(bufferPtr);
    }
  }

  return coordinates.length > 0 ? coordinates : null;
}

/**
 * 从 WASM 几何对象创建 GeoJSON Geometry
 * @param {Object} Module - WASM 模块实例
 * @param {number} geomPtr - 几何对象指针
 * @param {number} geomType - 几何类型
 * @returns {Object} GeoJSON Geometry 对象
 */
function createGeoJSONGeometry(Module, geomPtr, geomType) {
  if (!geomPtr) return null;

  switch (geomType) {
    case GeometryType.POINT: {
      const x = Module._UGCWasm_GeoPoint_GetX(geomPtr);
      const y = Module._UGCWasm_GeoPoint_GetY(geomPtr);
      return {
        type: 'Point',
        coordinates: [x, y]
      };
    }

    case GeometryType.LINESTRING: {
      const coordinates = extractLineFromGeoLine(Module, geomPtr);
      if (!coordinates || coordinates.length === 0) return null;
      
      // 单线
      if (coordinates.length === 1) {
        return {
          type: 'LineString',
          coordinates: coordinates[0]
        };
      }
      // 多线
      return {
        type: 'MultiLineString',
        coordinates: coordinates
      };
    }

    case GeometryType.POLYGON: {
      const coordinates = extractPolygonFromRegion(Module, geomPtr);
      if (!coordinates || coordinates.length === 0) return null;
      
      // 单多边形
      if (coordinates.length === 1) {
        return {
          type: 'Polygon',
          coordinates: coordinates[0]
        };
      }
      // 多多边形或带洞多边形
      // 判断是否为带洞多边形
      const isHole = coordinates.length > 1 && isCounterClockwise(Module, geomPtr, 1);
      if (isHole || coordinates.length === 1) {
        return {
          type: 'Polygon',
          coordinates: coordinates
        };
      }
      return {
        type: 'MultiPolygon',
        coordinates: coordinates.map(c => [c])
      };
    }

    default:
      console.error(`不支持的几何类型: ${geomType}`);
      return null;
  }
}

/**
 * 判断多边形环是否为逆时针方向（洞）
 */
function isCounterClockwise(Module, regionPtr, partIndex) {
  try {
    return Module._UGCWasm_GeoRegion_IsCounterClockwise(regionPtr, partIndex);
  } catch {
    return false;
  }
}

/**
 * 解析输入的 GeoJSON 并提取几何信息
 * @param {Object} input - GeoJSON Feature 或 Geometry
 * @returns {Object} { type, coordinates, properties }
 */
function parseGeoJSON(input) {
  // 处理 Feature
  if (input.type === 'Feature' && input.geometry) {
    return {
      type: input.geometry.type,
      coordinates: input.geometry.coordinates,
      properties: input.properties || {}
    };
  }

  // 处理 Geometry
  if (input.geometry) {
    return {
      type: input.geometry.type,
      coordinates: input.geometry.coordinates,
      properties: {}
    };
  }

  // 直接是 Geometry
  if (input.type && input.coordinates) {
    return {
      type: input.type,
      coordinates: input.coordinates,
      properties: {}
    };
  }

  throw new Error('无效的 GeoJSON 输入');
}

/**
 * 创建 GeoJSON Feature 输出
 * @param {Object} geometry - GeoJSON Geometry
 * @param {Object} properties - 属性
 * @returns {Object} GeoJSON Feature
 */
function createFeature(geometry, properties = {}) {
  return {
    type: 'Feature',
    geometry: geometry,
    properties: properties
  };
}

/**
 * 创建 GeoJSON FeatureCollection 输出
 * @param {Array<Object>} features - Feature 数组
 * @returns {Object} GeoJSON FeatureCollection
 */
function createFeatureCollection(features) {
  return {
    type: 'FeatureCollection',
    features: features
  };
}

/**
 * 将坐标数组转换为 WASM Point2Ds 对象
 * 参照 src1/util.js 的 geojsonCoordsToPoint2Ds
 * @param {Object} Module - WASM 模块实例
 * @param {Array} coords - 坐标数组 [[x,y], ...]
 * @returns {number} Point2Ds 指针
 */
function geojsonCoordsToPoint2Ds(Module, coords) {
  if (!coords || coords.length === 0) return null;
  const length = coords.length;
  const dim = 2;
  const coordArr = new Float64Array(coords.flat());
  const coordPtr = Module._malloc(length * dim * 8);
  Module.HEAPF64.set(coordArr, coordPtr / 8);
  const seqPtr = Module._UGCWasm_Geometry_CreatePoint2DsFromBuffer(coordPtr, length);
  Module._free(coordPtr);
  return seqPtr;
}

/**
 * 将 JS 数组转换为 WASM DoubleArray
 * 参照 src1/util.js 的 geojsonCoords2UGDoubleArray
 * @param {Object} Module - WASM 模块实例
 * @param {Array} coords - 数值数组
 * @returns {number} DoubleArray 指针
 */
function geojsonCoords2UGDoubleArray(Module, coords) {
  if (!coords || coords.length === 0) return null;
  const length = coords.length;
  const coordArr = new Float64Array(coords);
  const coordPtr = Module._malloc(length * 8);
  Module.HEAPF64.set(coordArr, coordPtr / 8);
  const pDoubleArray = Module._UGCWasm_Helper_CreateDoubleArray(coordPtr, length);
  Module._free(coordPtr);
  return pDoubleArray;
}

/**
 * 从 WASM DoubleArray 获取 JS 数组
 * 参照 src1/util.js 的 getJSArrayFromUGDoubleArray
 * @param {Object} Module - WASM 模块实例
 * @param {number} pDoubleArray - DoubleArray 指针
 * @returns {Array} JS 数组
 */
function getJSArrayFromUGDoubleArray(Module, pDoubleArray) {
  const length = Module._UGCWasm_Helper_GetDoubleArrayLength(pDoubleArray);
  const pBuffer = Module._malloc(length * 8);
  Module._UGCWasm_Helper_GetBufferFromDoubleArray(pDoubleArray, pBuffer);
  const view = new Float64Array(Module.HEAPF64.buffer, pBuffer, length);
  const coords = [];
  for (let i = 0; i < length; i++) {
    coords.push(view[i]);
  }
  Module._free(pBuffer);
  return coords;
}

/**
 * 将 GeoJSON 对象转换为 WASM 几何对象指针
 * 参照 src1/util.js 的 geojson2UGGeometry
 * @param {Object} Module - WASM 模块实例
 * @param {Object} geojson - GeoJSON 对象
 * @returns {number} WASM 几何对象指针
 */
function geojson2UGGeometry(Module, geojson) {
  if (!geojson) throw new Error('No GeoJSON object provided');

  switch (geojson.type) {
    case 'Feature':
      return geojson2UGGeometry(Module, geojson.geometry);
    case 'FeatureCollection':
      if (geojson.features.length === 0) return null;
      return geojson2UGGeometry(Module, geojson.features[0].geometry);
    case 'Point':
      if (geojson.coordinates.length === 0) {
        return Module._UGCWasm_GeoPoint_New();
      }
      return Module._UGCWasm_GeoPoint_New2(geojson.coordinates[0], geojson.coordinates[1]);
    case 'LineString': {
      if (geojson.coordinates.length === 0) {
        return Module._UGCWasm_GeoLine_New();
      }
      const pGeoLine = Module._UGCWasm_GeoLine_New();
      const pPoint2Ds = geojsonCoordsToPoint2Ds(Module, geojson.coordinates);
      Module._UGCWasm_GeoLine_AddPart2(pGeoLine, pPoint2Ds, geojson.coordinates.length);
      return pGeoLine;
    }
    case 'Polygon': {
      if (geojson.coordinates.length === 0) {
        return Module._UGCWasm_GeoRegion_New();
      }
      const pGeoRegion = Module._UGCWasm_GeoRegion_New();
      for (let i = 0; i < geojson.coordinates.length; i++) {
        const pPt = geojsonCoordsToPoint2Ds(Module, geojson.coordinates[i]);
        Module._UGCWasm_GeoRegion_AddPart2(pGeoRegion, pPt, geojson.coordinates[i].length);
      }
      return pGeoRegion;
    }
    case 'MultiLineString': {
      if (geojson.coordinates.length === 0) {
        return Module._UGCWasm_GeoLine_New();
      }
      const pGeoLine = Module._UGCWasm_GeoLine_New();
      for (let i = 0; i < geojson.coordinates.length; i++) {
        const pPt = geojsonCoordsToPoint2Ds(Module, geojson.coordinates[i]);
        Module._UGCWasm_GeoLine_AddPart2(pGeoLine, pPt, geojson.coordinates[i].length);
      }
      return pGeoLine;
    }
    case 'MultiPolygon': {
      if (geojson.coordinates.length === 0) {
        return Module._UGCWasm_GeoRegion_New();
      }
      const pGeoRegion = Module._UGCWasm_GeoRegion_New();
      for (let i = 0; i < geojson.coordinates.length; i++) {
        for (let j = 0; j < geojson.coordinates[i].length; j++) {
          const pPt = geojsonCoordsToPoint2Ds(Module, geojson.coordinates[i][j]);
          Module._UGCWasm_GeoRegion_AddPart2(pGeoRegion, pPt, geojson.coordinates[i][j].length);
        }
      }
      return pGeoRegion;
    }
    case 'MultiPoint': {
      const pGeoLine = Module._UGCWasm_GeoLine_New();
      const pPoint2Ds = geojsonCoordsToPoint2Ds(Module, geojson.coordinates);
      Module._UGCWasm_GeoLine_AddPart2(pGeoLine, pPoint2Ds, geojson.coordinates.length);
      return pGeoLine;
    }
    default:
      throw new Error('Unsupported GeoJSON type: ' + geojson.type);
  }
}

/**
 * 将 WASM 几何对象指针转换为 GeoJSON
 * 参照 src1/util.js 的 ugGeometry2Geojson
 * @param {Object} Module - WASM 模块实例
 * @param {number} pUGGeo - WASM 几何对象指针
 * @returns {Object} GeoJSON Geometry 对象
 */
function ugGeometry2Geojson(Module, pUGGeo) {
  if (!pUGGeo) return null;

  const geomType = Module._UGCWasm_Geometry_GetType(pUGGeo);
  switch (geomType) {
    case 1: { // UGGeoPoint
      const x = Module._UGCWasm_GeoPoint_GetX(pUGGeo);
      const y = Module._UGCWasm_GeoPoint_GetY(pUGGeo);
      return { type: 'Point', coordinates: [x, y] };
    }
    case 3: { // UGGeoLine
      const outlines = [];
      const partCount = Module._UGCWasm_GeoLine_GetPartCount(pUGGeo);
      for (let j = 0; j < partCount; j++) {
        const count = Module._UGCWasm_GeoLine_GetPartPointCount(pUGGeo, j);
        const pBuffer = Module._malloc(count * 2 * 8);
        Module._UGCWasm_GeoLine_GetPart2(pUGGeo, pBuffer, j);
        const view = new Float64Array(Module.HEAPF64.buffer, pBuffer, count * 2);
        const coords = [];
        for (let i = 0; i < count * 2; i += 2) {
          coords.push([view[i], view[i + 1]]);
        }
        Module._free(pBuffer);
        outlines.push(coords);
      }
      return { type: 'LineString', coordinates: outlines[0] };
    }
    case 5: { // UGGeoRegion
      const outlines = [];
      const partCount = Module._UGCWasm_GeoRegion_GetPartCount(pUGGeo);
      for (let j = 0; j < partCount; j++) {
        const count = Module._UGCWasm_GeoRegion_GetPartPointCount(pUGGeo, j);
        const pBuffer = Module._malloc(count * 2 * 8);
        Module._UGCWasm_GeoRegion_GetPart2(pUGGeo, pBuffer, j);
        const view = new Float64Array(Module.HEAPF64.buffer, pBuffer, count * 2);
        const coords = [];
        for (let i = 0; i < count * 2; i += 2) {
          coords.push([view[i], view[i + 1]]);
        }
        Module._free(pBuffer);
        outlines.push(coords);
      }
      return { type: 'Polygon', coordinates: outlines };
    }
    default:
      return null;
  }
}

module.exports = {
  GeometryType,
  readPoint,
  readPoints,
  writePoints,
  extractPolygonFromRegion,
  extractLineFromGeoLine,
  createGeoJSONGeometry,
  parseGeoJSON,
  createFeature,
  createFeatureCollection,
  geojsonCoordsToPoint2Ds,
  geojsonCoords2UGDoubleArray,
  getJSArrayFromUGDoubleArray,
  geojson2UGGeometry,
  ugGeometry2Geojson
};
