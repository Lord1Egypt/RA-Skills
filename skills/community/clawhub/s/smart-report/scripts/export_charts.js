// export_charts.js —— 批量把 chartOption 序列化为 SVG 文件，供 docx/pptx 静态嵌入。
//
// 用法：
//   node export_charts.js <manifest.json> <out_dir>
// manifest.json: [
//   { "id": "s1", "option_js": "<object literal>", "width": 900, "height": 560,
//     "plugins": ["wordcloud"|"liquidfill"|...], "background": "#FFFFFF" }
// ]
//
// 环境前置（调用方负责）：NODE_PATH 必须包含脚本所在目录（scripts/），
// 让 wordcloud/liquidfill 插件的 require('echarts') 解析到同目录的 echarts.js shim。
//
// 关键技术点：
//   1. Node 21+ 自带全局 navigator，会让内置 echarts 走浏览器分支 → 报 document 未定义；
//      通过 Object.defineProperty 强制覆盖为 undefined，让 echarts 进入 node 分支
//      （svgSupported=true），不需要 document/window shim。
//   2. SSR 渲染前统一改写 option：animation=false / 禁 dataZoom / 宽度自适应 / 白底，
//      否则静态版可能动画残留、缩放丢失或暗色主题文字在白纸上隐形。
//   3. option_js 是 chartOption 的对象字面量字符串（含 formatter 函数），
//      通过 eval 在隔离作用域里构造对象；不引入 eval 攻击面（manifest 由本地 Python 生成）。

'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const SKILL_ROOT = path.resolve(__dirname, '..');
const ASSETS_DIR = path.join(SKILL_ROOT, 'assets');

// === echarts 环境前置：navigator 置空，让内置构建走 node 分支 ===
try {
  Object.defineProperty(globalThis, 'navigator', {
    get() { return undefined; }, configurable: true, enumerable: false,
  });
} catch (e) {
  // 旧版 Node（<21）可能可写，赋值兜底
  try { globalThis.navigator = undefined; } catch (_) {}
}
globalThis.window = globalThis; // 兜底：避免偶发 window 引用
globalThis.self = globalThis; // 插件 UMD 头以 self 作为全局引用（liquidfill 需要；wordcloud 另需 canvas）

const echarts = require(path.join(ASSETS_DIR, 'echarts.min.js'));

// 插件：wordcloud / liquidfill 通过 require('echarts') 解析到 shim
function _loadPlugins(names) {
  const loaded = {};
  if (!Array.isArray(names)) return loaded;
  for (const n of names) {
    try {
      if (n === 'wordcloud') {
        require('echarts-wordcloud');
        loaded.wordcloud = true;
      } else if (n === 'liquidfill') {
        require('echarts-liquidfill');
        loaded.liquidfill = true;
      }
    } catch (e) {
      loaded[n] = String((e && e.message) || e).slice(0, 120);
    }
  }
  return loaded;
}

function _adaptOption(option, opts) {
  // 动画关闭（SSR 必须）
  option.animation = false;
  option.animationDuration = 0;
  option.animationDurationUpdate = 0;
  // 白底（避免深色主题文字在白纸上隐形）
  option.backgroundColor = opts.background || '#FFFFFF';
  // dataZoom 禁掉（静态版没机会滑动）+ 宽度按数据点数自适应
  const xDataLen = (option.xAxis && Array.isArray(option.xAxis.data)) ? option.xAxis.data.length : 0;
  if (xDataLen > 15) {
    delete option.dataZoom;
    opts.width = Math.min(Math.max(opts.width || 900, 80 * xDataLen), 2400);
  }
  // 移除 toolbox（saveAsImage 等静态无用，且 SVG 中会渲染为按钮）
  if (option.toolbox) {
    delete option.toolbox;
  }
  // liquidfill 水波图：插件用 CSS d:path() 定义波浪 clip，让 label 呈现
  // "水面下方主色、水面上方白色"；但 resvg 不支持 SVG2 的 CSS d 属性，
  // 白色 label 副本会被空 clipPath 全部裁掉，只剩主色副本与波浪同色 → 水球内
  // 数字不可见。静态导出时把 label 颜色统一为白色并加主色描边，保证数字清晰。
  if (option.series && Array.isArray(option.series)) {
    for (const s of option.series) {
      if (s && s.type === 'liquidFill' && s.label) {
        const mainColor = Array.isArray(s.color) ? s.color[0] : (s.color || '#000000');
        s.label.color = '#ffffff';
        s.label.insideColor = '#ffffff';
        s.label.textBorderColor = mainColor;
        s.label.textBorderWidth = 3;
      }
    }
  }
  // wordcloud 词云：echarts-wordcloud 插件仅支持 canvas renderer，在 SVG SSR
  // （renderer:'svg'）下无法初始化（报 "Cannot set properties of undefined (setting 'ondraw')"），
  // 会导致整图导出失败。静态导出时降级为横向柱状图（按词频降序），保证 docx/pptx
  // 仍有词频数据可读；浏览器 HTML 报告不受影响（走 template.py 内联 JS）。
  if (option.series && Array.isArray(option.series)) {
    const wcIdx = option.series.findIndex((s) => s && s.type === 'wordCloud');
    if (wcIdx >= 0) {
      const wc = option.series[wcIdx];
      const data = (wc.data || []).slice().sort((a, b) => (b.value || 0) - (a.value || 0));
      option.xAxis = { type: 'value' };
      option.yAxis = { type: 'category', data: data.map((d) => d.name) };
      option.series = [{ type: 'bar', name: wc.name, data: data.map((d) => d.value) }];
    }
  }
  return option;
}

function _renderOne(item, outDir) {
  const id = item.id;
  const width = item.width || 900;
  const height = item.height || 560;
  const background = item.background || '#FFFFFF';
  // 在独立 vm 作用域里 eval，避免与全局变量冲突
  const sandbox = {};
  vm.createContext(sandbox);
  let option;
  try {
    vm.runInContext(`var __opt = ( ${item.option_js} );`, sandbox);
    option = sandbox.__opt;
  } catch (e) {
    return { id, success: false, error: 'option_eval_failed', message: String((e && e.message) || e).slice(0, 300) };
  }

  const plugins = _loadPlugins(item.plugins || []);
  // 即使插件 require 失败，已 require 成功的会保留；未成功的下面绘图时若用到会报缺插件错误
  let chart;
  try {
    chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width, height });
  } catch (e) {
    return { id, success: false, error: 'init_failed', message: String((e && e.message) || e).slice(0, 200) };
  }

  try {
    _adaptOption(option, { width, height, background });
    chart.setOption(option);
    const svg = chart.renderToSVGString();
    // SSR SVG 默认 width="900" height="560"，无 xmlns 头；补充 namespace 与尺寸
    const finalSvg = _normalizeSvg(svg, width, height);
    const outPath = path.join(outDir, `${id}.svg`);
    fs.writeFileSync(outPath, finalSvg, 'utf8');
    return { id, success: true, path: outPath, width, height, plugins };
  } catch (e) {
    return { id, success: false, error: 'render_failed', message: String((e && e.message) || e).slice(0, 300) };
  } finally {
    try { chart.dispose && chart.dispose(); } catch (_) {}
  }
}

function _normalizeSvg(svg, width, height) {
  if (svg.startsWith('<?xml')) {
    // 已有 XML 头：去掉再重组，避免 xmlns 重复
    svg = svg.replace(/^<\?xml[^>]*\?>\s*/, '');
  }
  if (!svg.includes('xmlns=')) {
    svg = svg.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ');
  }
  // 确保有显式 width/height（一些 resvg/svg 渲染器需要）
  if (!/width=/.test(svg.split('>', 1)[0])) {
    svg = svg.replace('<svg ', `<svg width="${width}" height="${height}" `);
  }
  return svg;
}

function main() {
  const manifestPath = process.argv[2];
  const outDir = process.argv[3];
  if (!manifestPath || !outDir) {
    console.error('usage: node export_charts.js <manifest.json> <out_dir>');
    process.exit(2);
  }
  fs.mkdirSync(outDir, { recursive: true });

  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  } catch (e) {
    console.error(JSON.stringify({ success: false, error: 'manifest_unreadable', message: String(e.message) }));
    process.exit(1);
  }
  if (!Array.isArray(manifest)) {
    console.error(JSON.stringify({ success: false, error: 'manifest_not_array' }));
    process.exit(1);
  }

  const items = [];
  for (const item of manifest) {
    if (!item || !item.id || typeof item.option_js !== 'string') {
      items.push({ id: item && item.id, success: false, error: 'manifest_item_invalid' });
      continue;
    }
    items.push(_renderOne(item, outDir));
  }

  const summary = {
    total: items.length,
    succeeded: items.filter((x) => x.success).length,
    failed: items.filter((x) => !x.success).length,
  };
  process.stdout.write(JSON.stringify({ charts: items, summary }, null, 2) + '\n');
  // 显式退出，避免 echarts 内部 timer 导致进程挂起
  process.exit(summary.failed === summary.total && summary.total > 0 ? 1 : 0);
}

main();