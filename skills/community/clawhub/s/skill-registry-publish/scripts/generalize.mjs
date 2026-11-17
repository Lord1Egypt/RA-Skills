#!/usr/bin/env node
// 泛化检查：把一个自用 skill 里带个人痕迹的地方挑出来，判断哪些会挡住别人。
//
//   node generalize.mjs <skill 目录或仓库根> [--json]
//
// 分三级：
//   block  别人跑不起来或会看到错误指引，必须改
//   warn   能用但会让人困惑，建议改成通用表述
//   info   刻意保留的（比如 README 里的真实安装命令），确认即可
//
// 只做文本扫描，判不出「逻辑上假设了某台机器」这类问题，那部分要靠人读代码。

import { readdirSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { t } from './lib-i18n.mjs';

const argv = process.argv.slice(2);
const target = argv.find((a) => !a.startsWith('--'));
const asJson = argv.includes('--json');

if (!target) {
  console.error('用法：node generalize.mjs <skill 目录或仓库根> [--json]');
  process.exit(2);
}

const C = {
  block: (s) => `\x1b[31m✗\x1b[0m ${s}`,
  warn: (s) => `\x1b[33m!\x1b[0m ${s}`,
  info: (s) => `\x1b[2m·\x1b[0m ${s}`,
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
  bold: (s) => `\x1b[1m${s}\x1b[0m`,
};

const TEXT_EXT = /\.(mjs|js|cjs|ts|md|json|ya?ml|sh|ps1|py|txt)$/i;
const SKIP_DIR = /^(node_modules|\.git|\.github|dist|build)$/;

// 规则：before 是给人看的说明，test 命中即报告
const RULES = [
  {
    level: 'block',
    label: '绝对路径',
    why: '别人机器上没有这个路径，报错信息会指错方向',
    // 排除 URL 里的路径和正则里的转义
    // 用 [^\w] 而不是列一串标点，字符类里混进 [ 会让整个正则失效
    test: /(?:^|[^\w])([A-Za-z]:[\\/](?:Users|home|01-project|projects|work|data)\S*|\/Users\/\w+\S*|\/home\/\w+\S*)/,
  },
  {
    level: 'block',
    label: '内网地址',
    why: '内部服务地址对外无意义，也可能泄露拓扑',
    test: /\b(?:10\.\d{1,3}|192\.168\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3})\.\d{1,3}\b|localhost:\d{4,5}/,
  },
  {
    level: 'block',
    label: '密钥形态',
    why: '任何看起来像凭据的字符串都不该进公开仓库',
    test: /\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16})/,
  },
  {
    level: 'warn',
    label: '个人用户名',
    why: '示例或注释里出现的具体用户名，换成占位符更通用',
    test: /\bLyq\b|\bLYQ\b|\/c\/Users\/[a-z]+/,
  },
  {
    level: 'warn',
    label: '私有或特定项目名',
    why: '具体项目名对他人无意义，示例里用通用名字',
    test: /光润|某项目|内部系统|公司内部/,
  },
  {
    level: 'warn',
    label: '写死的量级数字',
    why: '下载量、星数这类数字会过期，写进文档一个月后就错了',
    test: /\d+\s*次下载|\d+\s*stars?|★\s*\d+/i,
  },
  {
    level: 'info',
    label: '安装命令含账号',
    why: 'README 里的安装命令本来就该是你的账号，保留',
    test: /npx skills add \w[\w-]*\//,
  },
];

function* walk(dir) {
  let entries;
  try {
    entries = readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const e of entries) {
    if (SKIP_DIR.test(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else if (TEXT_EXT.test(e.name)) yield p;
  }
}

// target 可能是单个文件，这时 walk 读目录会返回空，要单独处理
const root = path.resolve(target);
let isFile = false;
try {
  isFile = statSync(root).isFile();
} catch {
  /* 路径不存在，交给 walk 返回空 */
}
const files = isFile ? [root] : [...walk(root)];

const findings = [];
for (const file of files) {
  // 规则定义本身含示例词，扫自己会一直报
  if (path.basename(file) === 'generalize.mjs') continue;
  let text;
  try {
    text = readFileSync(file, 'utf8');
  } catch {
    continue;
  }
  const lines = text.split('\n');
  for (const rule of RULES) {
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      // 跳过明显的注释掉的正则定义，避免规则自己命中自己
      if (/^\s*\/\/.*\btest:/.test(line)) continue;
      if (rule.test.test(line)) {
        const m = line.match(rule.test);
        // 文档里的绝对路径多半是示例，降一级；代码里的才是真问题
        const level = rule.level === 'block' && /\.(md|txt)$/i.test(file) ? 'warn' : rule.level;
        findings.push({
          level,
          label: rule.label,
          why: rule.why,
          file: path.relative(process.cwd(), file),
          line: i + 1,
          sample: (m ? m[0] : line.trim()).slice(0, 90),
        });
      }
    }
  }
}

const groups = { block: [], warn: [], info: [] };
for (const f of findings) groups[f.level].push(f);

if (asJson) {
  console.log(JSON.stringify(groups, null, 2));
} else {
  const titles = {
    block: t('必须改（别人跑不起来或看到错误指引）', 'Must fix (blocks others from running it)'),
    warn: t('建议改（能用，但表述不通用）', 'Should fix (works, but text is not generic)'),
    info: t('确认即可（通常是刻意保留的）', 'Confirm only (usually intentional)'),
  };
  let total = 0;
  for (const level of ['block', 'warn', 'info']) {
    const list = groups[level];
    if (!list.length) continue;
    total += list.length;
    console.log(`\n${C.bold('=== ' + titles[level] + ' ===')}`);
    const shown = level === 'info' ? list.slice(0, 3) : list;
    for (const f of shown) {
      const head = level === 'block' ? C.block(f.label) : level === 'warn' ? C.warn(f.label) : C.info(f.label);
      console.log(`${head}  ${f.file}:${f.line}`);
      console.log(C.dim(`    ${f.sample}`));
      if (level !== 'info') console.log(C.dim(`    为什么：${f.why}`));
    }
    if (level === 'info' && list.length > shown.length) {
      console.log(C.dim(`    …另有 ${list.length - shown.length} 处`));
    }
  }
  if (!total) console.log(t('\n没有发现个人痕迹。\n', '\nNo personal traces found.\n'));
  else {
    console.log(`\n共 ${total} 处。block 项清零才能发，warn 项逐条确认。`);
    console.log(C.dim('这个脚本只扫文本。逻辑上假设了某台机器（例如默认某个端口已被占用、依赖某个特定工具已装）要靠人读代码判断。\n'));
  }
}

process.exit(groups.block.length ? 1 : 0);
