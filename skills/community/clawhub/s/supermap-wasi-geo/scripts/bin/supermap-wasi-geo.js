#!/usr/bin/env node

/**
 * SuperMap WASI Geometry CLI
 * 基于 SuperMap WASM 的几何分析命令行工具
 * 支持23种几何分析操作
 */

const fs = require('fs');
const path = require('path');
const GeometryAnalysis = require('../src/geometry-analysis');

// 版本信息
const VERSION = require('../../package.json').version;

// 操作定义
const OPERATIONS = {
  // 单几何操作
  'buffer': {
    description: '缓冲区分析',
    params: ['input', 'radius'],
    optionalParams: [],
    example: 'wasi-geo buffer --input \'{"type":"Point","coordinates":[120,30]}\' --radius 2'
  },
  'convex-hull': {
    description: '凸包计算',
    params: ['input'],
    optionalParams: [],
    example: 'wasi-geo convex-hull --input \'{"type":"MultiPoint","coordinates":[[0,0],[1,1],[1,0],[0,1]]}\''
  },
  'resample': {
    description: '重采样分析',
    params: ['input', 'tolerance'],
    optionalParams: [],
    example: 'wasi-geo resample --input \'{"type":"LineString","coordinates":[[0,0],[1,1],[2,0]]}\' --tolerance 0.5'
  },
  'smooth': {
    description: '线要素光滑分析',
    params: ['input', 'smoothness'],
    optionalParams: [],
    example: 'wasi-geo smooth --input \'{"type":"LineString","coordinates":[[0,0],[1,1],[2,0]]}\' --smoothness 3'
  },
  'geodesic-distance': {
    description: '计算测地线距离',
    params: ['input'],
    optionalParams: ['major-axis', 'flatten'],
    example: 'wasi-geo geodesic-distance --input \'{"type":"LineString","coordinates":[[0,0],[1,1]]}\''
  },
  'geodesic-area': {
    description: '计算测地线面积',
    params: ['input'],
    optionalParams: ['major-axis', 'flatten'],
    example: 'wasi-geo geodesic-area --input \'{"type":"Polygon","coordinates":[[[0,0],[1,0],[1,1],[0,1],[0,0]]]}\''
  },
  'parallel': {
    description: '计算平行线',
    params: ['input', 'distance'],
    optionalParams: [],
    example: 'wasi-geo parallel --input \'{"type":"LineString","coordinates":[[0,0],[1,1]]}\' --distance 0.5'
  },

  // 双几何操作
  'intersect': {
    description: '相交分析',
    params: ['input1', 'input2'],
    optionalParams: [],
    example: 'wasi-geo intersect --input1 \'{"type":"Polygon",...}\' --input2 \'{"type":"Polygon",...}\''
  },
  'union': {
    description: '合并分析',
    params: ['input1', 'input2'],
    optionalParams: [],
    example: 'wasi-geo union --input1 \'{"type":"Polygon",...}\' --input2 \'{"type":"Polygon",...}\''
  },
  'erase': {
    description: '擦除分析',
    params: ['input1', 'input2'],
    optionalParams: [],
    example: 'wasi-geo erase --input1 \'{"type":"Polygon",...}\' --input2 \'{"type":"Polygon",...}\''
  },
  'xor': {
    description: '异或分析',
    params: ['input1', 'input2'],
    optionalParams: [],
    example: 'wasi-geo xor --input1 \'{"type":"Polygon",...}\' --input2 \'{"type":"Polygon",...}\''
  },
  'clip': {
    description: '裁剪分析',
    params: ['input1', 'input2'],
    optionalParams: [],
    example: 'wasi-geo clip --input1 \'{"type":"Polygon",...}\' --input2 \'{"type":"Polygon",...}\''
  },
  'has-intersection': {
    description: '判断是否相交',
    params: ['input1', 'input2'],
    optionalParams: ['tolerance'],
    example: 'wasi-geo has-intersection --input1 \'{"type":"Point","coordinates":[0,0]}\' --input2 \'{"type":"Point","coordinates":[1,1]}\''
  },
  'has-touch': {
    description: '判断边界是否接触',
    params: ['input1', 'input2'],
    optionalParams: ['tolerance'],
    example: 'wasi-geo has-touch --input1 \'{"type":"Polygon",...}\' --input2 \'{"type":"Polygon",...}\''
  },
  'is-identical': {
    description: '判断是否相等',
    params: ['input1', 'input2'],
    optionalParams: ['tolerance'],
    example: 'wasi-geo is-identical --input1 \'{"type":"Point","coordinates":[0,0]}\' --input2 \'{"type":"Point","coordinates":[0,0]}\''
  },
  'distance': {
    description: '计算两几何对象距离',
    params: ['input1', 'input2'],
    optionalParams: [],
    example: 'wasi-geo distance --input1 \'{"type":"Point","coordinates":[0,0]}\' --input2 \'{"type":"Point","coordinates":[1,1]}\''
  },

  // 点线关系
  'is-left': {
    description: '判断点是否在线的左侧',
    params: ['point', 'line-start', 'line-end'],
    optionalParams: [],
    example: 'wasi-geo is-left --point "[0,1]" --line-start "[0,0]" --line-end "[1,0]"'
  },
  'is-right': {
    description: '判断点是否在线的右侧',
    params: ['point', 'line-start', 'line-end'],
    optionalParams: [],
    example: 'wasi-geo is-right --point "[1,1]" --line-start "[0,0]" --line-end "[1,0]"'
  },
  'is-point-on-line': {
    description: '判断点是否在线段上',
    params: ['point', 'line-start', 'line-end'],
    optionalParams: ['extended'],
    example: 'wasi-geo is-point-on-line --point "[0.5,0]" --line-start "[0,0]" --line-end "[1,0]"'
  },
  'is-parallel': {
    description: '判断两线是否平行',
    params: ['line1-start', 'line1-end', 'line2-start', 'line2-end'],
    optionalParams: [],
    example: 'wasi-geo is-parallel --line1-start "[0,0]" --line1-end "[1,1]" --line2-start "[0,1]" --line2-end "[1,2]"'
  },
  'distance-to-line': {
    description: '计算点到线段的距离',
    params: ['point', 'line-start', 'line-end'],
    optionalParams: [],
    example: 'wasi-geo distance-to-line --point "[0,1]" --line-start "[0,0]" --line-end "[1,0]"'
  }
};

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
wasi-geo v${VERSION} - WASM 几何分析工具

用法:
  wasi-geo <operation> [options]

操作:
  单几何操作:
    buffer              缓冲区分析
    convex-hull         凸包计算
    resample            重采样分析
    smooth              线要素光滑分析
    geodesic-distance   计算测地线距离
    geodesic-area       计算测地线面积
    parallel            计算平行线

  双几何操作:
    intersect           相交分析
    union               合并分析
    erase               擦除分析
    xor                 异或分析
    clip                裁剪分析
    has-intersection    判断是否相交
    has-touch           判断边界是否接触
    is-identical        判断是否相等
    distance            计算两几何对象距离

  点线关系:
    is-left             判断点是否在线的左侧
    is-right            判断点是否在线的右侧
    is-point-on-line    判断点是否在线段上
    is-parallel         判断两线是否平行
    distance-to-line    计算点到线段的距离

通用选项:
  --input <json>        直接传入 GeoJSON 字符串
  --input-file <path>   从文件读取 GeoJSON
  --output <path>       输出到文件（默认 stdout）
  --pretty              美化 JSON 输出
  --help, -h            显示帮助信息
  --version, -v         显示版本信息

查看具体操作帮助:
  wasi-geo <operation> --help

示例:
  # 缓冲区分析
  wasi-geo buffer --input '{"type":"Point","coordinates":[120,30]}' --radius 2

  # 凸包计算
  wasi-geo convex-hull --input '{"type":"MultiPoint","coordinates":[[0,0],[1,1],[1,0],[0,1]]}'

  # Windows CMD 示例（注意转义引号）
  wasi-geo buffer --input "{\\"type\\":\\"Point\\",\\"coordinates\\":[120,30]}" --radius 2
`);
}

/**
 * 显示操作帮助信息
 */
function showOperationHelp(operation) {
  const op = OPERATIONS[operation];
  if (!op) {
    console.error(`错误: 未知操作 "${operation}"`);
    process.exit(1);
  }

  console.log(`
wasi-geo ${operation} - ${op.description}

用法:
  wasi-geo ${operation} ${op.params.map(p => `--${p} <value>`).join(' ')} [options]

参数:
${op.params.map(p => `  --${p} <value>    必需参数`).join('\n')}
${op.optionalParams.map(p => `  --${p} <value>    可选参数`).join('\n')}

示例:
  ${op.example}
`);
}

/**
 * 解析命令行参数
 */
function parseArgs(args) {
  const result = {
    operation: null,
    input: null,
    inputFile: null,
    input1: null,
    input1File: null,
    input2: null,
    input2File: null,
    output: null,
    pretty: false,
    // 操作特定参数
    radius: null,
    tolerance: null,
    smoothness: null,
    distance: null,
    majorAxis: 6378137,
    flatten: 0.003352810664,
    extended: false,
    // 点线关系参数
    point: null,
    lineStart: null,
    lineEnd: null,
    line1Start: null,
    line1End: null,
    line2Start: null,
    line2End: null
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    switch (arg) {
      case '-h':
      case '--help':
        result.help = true;
        break;

      case '-v':
      case '--version':
        result.version = true;
        break;

      case '--input':
        result.input = args[++i];
        break;

      case '--input-file':
        result.inputFile = args[++i];
        break;

      case '--input1':
        result.input1 = args[++i];
        break;

      case '--input1-file':
        result.input1File = args[++i];
        break;

      case '--input2':
        result.input2 = args[++i];
        break;

      case '--input2-file':
        result.input2File = args[++i];
        break;

      case '--output':
        result.output = args[++i];
        break;

      case '--pretty':
        result.pretty = true;
        break;

      case '--radius':
        result.radius = parseFloat(args[++i]);
        break;

      case '--tolerance':
        result.tolerance = parseFloat(args[++i]);
        break;

      case '--smoothness':
        result.smoothness = parseInt(args[++i], 10);
        break;

      case '--distance':
        result.distance = parseFloat(args[++i]);
        break;

      case '--major-axis':
        result.majorAxis = parseFloat(args[++i]);
        break;

      case '--flatten':
        result.flatten = parseFloat(args[++i]);
        break;

      case '--extended':
        result.extended = true;
        break;

      case '--point':
        result.point = args[++i];
        break;

      case '--line-start':
        result.lineStart = args[++i];
        break;

      case '--line-end':
        result.lineEnd = args[++i];
        break;

      case '--line1-start':
        result.line1Start = args[++i];
        break;

      case '--line1-end':
        result.line1End = args[++i];
        break;

      case '--line2-start':
        result.line2Start = args[++i];
        break;

      case '--line2-end':
        result.line2End = args[++i];
        break;

      default:
        // 第一个非选项参数是操作名
        if (!arg.startsWith('-') && !result.operation) {
          result.operation = arg;
        }
        break;
    }
  }

  return result;
}

/**
 * 从 stdin 读取数据
 */
function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';

    process.stdin.setEncoding('utf8');

    process.stdin.on('readable', () => {
      let chunk;
      while ((chunk = process.stdin.read()) !== null) {
        data += chunk;
      }
    });

    process.stdin.on('end', () => {
      resolve(data.trim());
    });

    process.stdin.on('error', reject);
  });
}

/**
 * 获取输入数据
 */
async function getInputData(args) {
  if (args.input) {
    return args.input;
  } else if (args.inputFile) {
    if (!fs.existsSync(args.inputFile)) {
      throw new Error(`文件不存在: ${args.inputFile}`);
    }
    return fs.readFileSync(args.inputFile, 'utf-8');
  } else if (!process.stdin.isTTY) {
    return await readStdin();
  }
  return null;
}

/**
 * 解析坐标数组
 */
function parseCoordinates(str) {
  try {
    const arr = JSON.parse(str);
    if (Array.isArray(arr) && arr.length >= 2) {
      return arr;
    }
    throw new Error('无效的坐标格式');
  } catch (e) {
    throw new Error(`坐标解析失败: ${e.message}`);
  }
}

/**
 * 执行操作
 */
async function executeOperation(args) {
  const op = OPERATIONS[args.operation];
  if (!op) {
    throw new Error(`未知操作: ${args.operation}`);
  }

  let result;

  switch (args.operation) {
    // 单几何操作
    case 'buffer': {
      const input = await getInputData(args);
      if (!input) throw new Error('缺少输入数据');
      if (args.radius === null) throw new Error('缺少 --radius 参数');
      result = await GeometryAnalysis.buffer(input, args.radius);
      break;
    }

    case 'convex-hull': {
      const input = await getInputData(args);
      if (!input) throw new Error('缺少输入数据');
      result = await GeometryAnalysis.computeConvexHull(input);
      break;
    }

    case 'resample': {
      const input = await getInputData(args);
      if (!input) throw new Error('缺少输入数据');
      if (args.tolerance === null) throw new Error('缺少 --tolerance 参数');
      result = await GeometryAnalysis.resample(input, args.tolerance);
      break;
    }

    case 'smooth': {
      const input = await getInputData(args);
      if (!input) throw new Error('缺少输入数据');
      if (args.smoothness === null) throw new Error('缺少 --smoothness 参数');
      result = await GeometryAnalysis.smooth(input, args.smoothness);
      break;
    }

    case 'geodesic-distance': {
      const input = await getInputData(args);
      if (!input) throw new Error('缺少输入数据');
      result = await GeometryAnalysis.computeGeodesicDistance(input, args.majorAxis, args.flatten);
      break;
    }

    case 'geodesic-area': {
      const input = await getInputData(args);
      if (!input) throw new Error('缺少输入数据');
      result = await GeometryAnalysis.computeGeodesicArea(input, args.majorAxis, args.flatten);
      break;
    }

    case 'parallel': {
      const input = await getInputData(args);
      if (!input) throw new Error('缺少输入数据');
      if (args.distance === null) throw new Error('缺少 --distance 参数');
      result = await GeometryAnalysis.computeParallel(input, args.distance);
      break;
    }

    // 双几何操作
    case 'intersect': {
      if (!args.input1 && !args.input1File) throw new Error('缺少第一个输入数据');
      if (!args.input2 && !args.input2File) throw new Error('缺少第二个输入数据');

      let input1 = args.input1;
      let input2 = args.input2;

      if (args.input1File) {
        if (!fs.existsSync(args.input1File)) throw new Error(`文件不存在: ${args.input1File}`);
        input1 = fs.readFileSync(args.input1File, 'utf-8');
      }
      if (args.input2File) {
        if (!fs.existsSync(args.input2File)) throw new Error(`文件不存在: ${args.input2File}`);
        input2 = fs.readFileSync(args.input2File, 'utf-8');
      }

      result = await GeometryAnalysis.intersect(input1, input2);
      break;
    }

    case 'union': {
      if (!args.input1 && !args.input1File) throw new Error('缺少第一个输入数据');
      if (!args.input2 && !args.input2File) throw new Error('缺少第二个输入数据');

      let input1 = args.input1;
      let input2 = args.input2;

      if (args.input1File) {
        if (!fs.existsSync(args.input1File)) throw new Error(`文件不存在: ${args.input1File}`);
        input1 = fs.readFileSync(args.input1File, 'utf-8');
      }
      if (args.input2File) {
        if (!fs.existsSync(args.input2File)) throw new Error(`文件不存在: ${args.input2File}`);
        input2 = fs.readFileSync(args.input2File, 'utf-8');
      }

      result = await GeometryAnalysis.union(input1, input2);
      break;
    }

    case 'erase': {
      if (!args.input1 && !args.input1File) throw new Error('缺少第一个输入数据');
      if (!args.input2 && !args.input2File) throw new Error('缺少第二个输入数据');

      let input1 = args.input1;
      let input2 = args.input2;

      if (args.input1File) {
        if (!fs.existsSync(args.input1File)) throw new Error(`文件不存在: ${args.input1File}`);
        input1 = fs.readFileSync(args.input1File, 'utf-8');
      }
      if (args.input2File) {
        if (!fs.existsSync(args.input2File)) throw new Error(`文件不存在: ${args.input2File}`);
        input2 = fs.readFileSync(args.input2File, 'utf-8');
      }

      result = await GeometryAnalysis.erase(input1, input2);
      break;
    }

    case 'xor': {
      if (!args.input1 && !args.input1File) throw new Error('缺少第一个输入数据');
      if (!args.input2 && !args.input2File) throw new Error('缺少第二个输入数据');

      let input1 = args.input1;
      let input2 = args.input2;

      if (args.input1File) {
        if (!fs.existsSync(args.input1File)) throw new Error(`文件不存在: ${args.input1File}`);
        input1 = fs.readFileSync(args.input1File, 'utf-8');
      }
      if (args.input2File) {
        if (!fs.existsSync(args.input2File)) throw new Error(`文件不存在: ${args.input2File}`);
        input2 = fs.readFileSync(args.input2File, 'utf-8');
      }

      result = await GeometryAnalysis.xor(input1, input2);
      break;
    }

    case 'clip': {
      if (!args.input1 && !args.input1File) throw new Error('缺少第一个输入数据');
      if (!args.input2 && !args.input2File) throw new Error('缺少第二个输入数据');

      let input1 = args.input1;
      let input2 = args.input2;

      if (args.input1File) {
        if (!fs.existsSync(args.input1File)) throw new Error(`文件不存在: ${args.input1File}`);
        input1 = fs.readFileSync(args.input1File, 'utf-8');
      }
      if (args.input2File) {
        if (!fs.existsSync(args.input2File)) throw new Error(`文件不存在: ${args.input2File}`);
        input2 = fs.readFileSync(args.input2File, 'utf-8');
      }

      result = await GeometryAnalysis.clip(input1, input2);
      break;
    }

    case 'has-intersection': {
      if (!args.input1 && !args.input1File) throw new Error('缺少第一个输入数据');
      if (!args.input2 && !args.input2File) throw new Error('缺少第二个输入数据');

      let input1 = args.input1;
      let input2 = args.input2;

      if (args.input1File) {
        if (!fs.existsSync(args.input1File)) throw new Error(`文件不存在: ${args.input1File}`);
        input1 = fs.readFileSync(args.input1File, 'utf-8');
      }
      if (args.input2File) {
        if (!fs.existsSync(args.input2File)) throw new Error(`文件不存在: ${args.input2File}`);
        input2 = fs.readFileSync(args.input2File, 'utf-8');
      }

      result = await GeometryAnalysis.hasIntersection(input1, input2, args.tolerance || 0);
      break;
    }

    case 'has-touch': {
      if (!args.input1 && !args.input1File) throw new Error('缺少第一个输入数据');
      if (!args.input2 && !args.input2File) throw new Error('缺少第二个输入数据');

      let input1 = args.input1;
      let input2 = args.input2;

      if (args.input1File) {
        if (!fs.existsSync(args.input1File)) throw new Error(`文件不存在: ${args.input1File}`);
        input1 = fs.readFileSync(args.input1File, 'utf-8');
      }
      if (args.input2File) {
        if (!fs.existsSync(args.input2File)) throw new Error(`文件不存在: ${args.input2File}`);
        input2 = fs.readFileSync(args.input2File, 'utf-8');
      }

      result = await GeometryAnalysis.hasTouch(input1, input2, args.tolerance || 0);
      break;
    }

    case 'is-identical': {
      if (!args.input1 && !args.input1File) throw new Error('缺少第一个输入数据');
      if (!args.input2 && !args.input2File) throw new Error('缺少第二个输入数据');

      let input1 = args.input1;
      let input2 = args.input2;

      if (args.input1File) {
        if (!fs.existsSync(args.input1File)) throw new Error(`文件不存在: ${args.input1File}`);
        input1 = fs.readFileSync(args.input1File, 'utf-8');
      }
      if (args.input2File) {
        if (!fs.existsSync(args.input2File)) throw new Error(`文件不存在: ${args.input2File}`);
        input2 = fs.readFileSync(args.input2File, 'utf-8');
      }

      result = await GeometryAnalysis.isIdentical(input1, input2, args.tolerance || 0);
      break;
    }

    case 'distance': {
      if (!args.input1 && !args.input1File) throw new Error('缺少第一个输入数据');
      if (!args.input2 && !args.input2File) throw new Error('缺少第二个输入数据');

      let input1 = args.input1;
      let input2 = args.input2;

      if (args.input1File) {
        if (!fs.existsSync(args.input1File)) throw new Error(`文件不存在: ${args.input1File}`);
        input1 = fs.readFileSync(args.input1File, 'utf-8');
      }
      if (args.input2File) {
        if (!fs.existsSync(args.input2File)) throw new Error(`文件不存在: ${args.input2File}`);
        input2 = fs.readFileSync(args.input2File, 'utf-8');
      }

      result = await GeometryAnalysis.distance(input1, input2);
      break;
    }

    // 点线关系
    case 'is-left': {
      if (!args.point) throw new Error('缺少 --point 参数');
      if (!args.lineStart) throw new Error('缺少 --line-start 参数');
      if (!args.lineEnd) throw new Error('缺少 --line-end 参数');

      const point = parseCoordinates(args.point);
      const lineStart = parseCoordinates(args.lineStart);
      const lineEnd = parseCoordinates(args.lineEnd);

      result = await GeometryAnalysis.isLeft(point, lineStart, lineEnd);
      break;
    }

    case 'is-right': {
      if (!args.point) throw new Error('缺少 --point 参数');
      if (!args.lineStart) throw new Error('缺少 --line-start 参数');
      if (!args.lineEnd) throw new Error('缺少 --line-end 参数');

      const point = parseCoordinates(args.point);
      const lineStart = parseCoordinates(args.lineStart);
      const lineEnd = parseCoordinates(args.lineEnd);

      result = await GeometryAnalysis.isRight(point, lineStart, lineEnd);
      break;
    }

    case 'is-point-on-line': {
      if (!args.point) throw new Error('缺少 --point 参数');
      if (!args.lineStart) throw new Error('缺少 --line-start 参数');
      if (!args.lineEnd) throw new Error('缺少 --line-end 参数');

      const point = parseCoordinates(args.point);
      const lineStart = parseCoordinates(args.lineStart);
      const lineEnd = parseCoordinates(args.lineEnd);

      result = await GeometryAnalysis.isPointOnLine(point, lineStart, lineEnd, args.extended);
      break;
    }

    case 'is-parallel': {
      if (!args.line1Start) throw new Error('缺少 --line1-start 参数');
      if (!args.line1End) throw new Error('缺少 --line1-end 参数');
      if (!args.line2Start) throw new Error('缺少 --line2-start 参数');
      if (!args.line2End) throw new Error('缺少 --line2-end 参数');

      const line1Start = parseCoordinates(args.line1Start);
      const line1End = parseCoordinates(args.line1End);
      const line2Start = parseCoordinates(args.line2Start);
      const line2End = parseCoordinates(args.line2End);

      result = await GeometryAnalysis.isParallel(line1Start, line1End, line2Start, line2End);
      break;
    }

    case 'distance-to-line': {
      if (!args.point) throw new Error('缺少 --point 参数');
      if (!args.lineStart) throw new Error('缺少 --line-start 参数');
      if (!args.lineEnd) throw new Error('缺少 --line-end 参数');

      const point = parseCoordinates(args.point);
      const lineStart = parseCoordinates(args.lineStart);
      const lineEnd = parseCoordinates(args.lineEnd);

      result = await GeometryAnalysis.distanceToLineSegment(point, lineStart, lineEnd);
      break;
    }

    default:
      throw new Error(`未实现的操作: ${args.operation}`);
  }

  return result;
}

/**
 * 主函数
 */
async function main() {
  const args = parseArgs(process.argv.slice(2));

  // 显示帮助
  if (args.help) {
    if (args.operation) {
      showOperationHelp(args.operation);
    } else {
      showHelp();
    }
    process.exit(0);
  }

  // 显示版本
  if (args.version) {
    console.log(`wasi-geo v${VERSION}`);
    process.exit(0);
  }

  // 检查操作
  if (!args.operation) {
    console.error('错误: 请指定操作');
    console.error('使用 --help 查看帮助信息');
    process.exit(1);
  }

  try {
    const result = await executeOperation(args);

    // 格式化输出
    const output = args.pretty
      ? JSON.stringify(result, null, 2)
      : JSON.stringify(result);

    // 输出结果
    if (args.output) {
      fs.writeFileSync(args.output, output + '\n');
      console.error(`结果已写入: ${args.output}`);
    } else {
      console.log(output);
    }

  } catch (error) {
    console.error(`错误: ${error.message}`);
    if (process.env.DEBUG) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}

// 运行主函数
main();
