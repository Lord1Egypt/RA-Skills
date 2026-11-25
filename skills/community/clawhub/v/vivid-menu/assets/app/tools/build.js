/**
 * tools/build.js — 把 ES 模块合成一个普通脚本
 *
 * 为什么需要：浏览器在 file:// 协议下会以 CORS 为由拒绝加载 type="module"，
 * 所以「双击 index.html 就能用」必须走单文件包。
 *
 * 做法：按依赖顺序拼接，剥掉 import / export 语句，整体套一层 IIFE。
 * 前提：各模块顶层标识符不重名（当前已满足，新增模块时请沿用此约定）。
 */

import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');

// 拓扑顺序：被依赖的在前
const ORDER = [
  'art/pen.js',
  'art/kinds.js',
  'art/index.js',
  'measure.js',
  'model.js',
  'layout.js',
  'render.js',
  'inspect.js',
  'parse.js',
  'store.js',
  'protocol.js',
  'driver.js',
  'photo.js',
  'export.js',
  'main.js',
];

const strip = (src) => src
  // 去掉 import（含多行花括号）
  .replace(/import\s+(?:\{[^}]*\}|\*\s+as\s+\w+|\w+)\s+from\s+['"][^'"]+['"];?/g, '')
  // 去掉 export 关键字，保留声明
  .replace(/\bexport\s+(?=(const|let|var|function|async|class)\b)/g, '')
  // 去掉纯再导出语句
  .replace(/^[ \t]*export\s*\{[^}]*\};?[ \t]*$/gm, '');

let bundle = '';
const seen = new Set();

for (const rel of ORDER) {
  const file = path.join(ROOT, 'js', rel);
  if (!fs.existsSync(file)) {
    console.error(`缺少文件：js/${rel}`);
    process.exitCode = 1;
    continue;
  }
  const code = strip(fs.readFileSync(file, 'utf8'));
  bundle += `\n/* ==================== js/${rel} ==================== */\n${code}\n`;

  // 粗查顶层重名，早发现比运行时炸好
  for (const m of code.matchAll(/^(?:const|let|var|function|async function)\s+([A-Za-z_$][\w$]*)/gm)) {
    const name = m[1];
    if (seen.has(name)) console.warn(`  ⚠ 顶层标识符重复：${name}（在 js/${rel}）`);
    seen.add(name);
  }
}

const out = `/* 生动菜单 · 单文件包
 * 由 tools/build.js 生成，请勿直接修改。
 * 改源码请编辑 js/ 下的模块，然后执行：npm run build
 */
(function () {
'use strict';
${bundle}
})();
`;

// 语法自检：让 node 解析一遍
try {
  new Function(out);
} catch (e) {
  console.error('打包结果有语法错误：', e.message);
  process.exitCode = 1;
}

fs.writeFileSync(path.join(ROOT, 'app.bundle.js'), out);
const kb = (Buffer.byteLength(out, 'utf8') / 1024).toFixed(1);
console.log(`✓ app.bundle.js  ${kb} KB  （${ORDER.length} 个模块，${seen.size} 个顶层标识符）`);
