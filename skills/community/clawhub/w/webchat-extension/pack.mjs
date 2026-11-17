#!/usr/bin/env node
// pack.mjs — 一键打包分享用干净 zip（自动按 .gitignore 排除 node_modules/.env/私钥等）
// 用法：在 webchat-extension/ 目录下执行 `node pack.mjs`
// 输出：父目录下的 webchat-extension-share-YYYYMMDD.zip
// 内容（SKILL.md 直接位于 webchat-extension/ 根，满足「技能文件在根目录或一级目录」规则）：
//   webchat-extension/        ← 既是手动安装版（extension/ + backend/ + 文档 + 本脚本）
//                              ← 也是 agent 技能版（SKILL.md + scripts/ + references/ + assets/）
//   用 WorkBuddy：把整个 webchat-extension/ 复制到 ~/.workbuddy/skills/webchat-extension/
// 纯 Node 实现，零依赖，跨平台（Windows / macOS / Linux）。

import {
  readFileSync, writeFileSync, statSync, readdirSync, existsSync,
} from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { homedir } from 'node:os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = __dirname;                       // webchat-extension/ 本身
const TOP = ROOT.split(/[\\/]/).pop();        // 归档内顶层文件夹名
const OUT = join(
  dirname(ROOT),
  `webchat-extension-share-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}-clean.zip`,
);

// ---------- 解析 .gitignore ----------
function parseGitignore(p) {
  if (!existsSync(p)) return [];
  return readFileSync(p, 'utf8')
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith('#'));
}
const patterns = parseGitignore(join(ROOT, '.gitignore'));

function matchPattern(relPath, pattern) {
  const isDir = pattern.endsWith('/');
  const clean = pattern.replace(/\/+$/, '');
  if (isDir) {
    // 目录模式：任意路径段等于该名即排除（如 node_modules/）
    return relPath.split('/').includes(clean);
  }
  // glob → 正则（* 匹配非斜杠任意字符，? 单字符，. 等转义）
  const reSrc = clean
    .replace(/[.+^${}()|[\]\\]/g, '\\$&')
    .replace(/\*/g, '[^/]*')
    .replace(/\?/g, '[^/]');
  const reBase = new RegExp('^' + reSrc + '$');
  const base = relPath.split('/').pop();
  return reBase.test(base) || reBase.test(relPath);
}

function isIgnored(relPath) {
  const p = relPath.split('\\').join('/');
  for (const pat of patterns) {
    if (matchPattern(p, pat)) return true;
  }
  return false;
}

// skill 目录额外的硬过滤（不依赖 .gitignore，防泄露/体积）
function isSkillSensitive(relPath) {
  const segs = relPath.split('/');
  const base = segs[segs.length - 1];
  if (base === '.env') return true;                 // 仅允许 .env.example
  if (base.endsWith('.pem')) return true;
  if (base.includes('.bak')) return true;
  if (segs.includes('node_modules')) return true;
  if (base.endsWith('.log')) return true;
  return false;
}

// 一律禁止进入分享包的文件（独立于 .gitignore，显式硬性排除）
// 图标（*.png）不进包：extension/icons 由 agent 在部署时（deploy.mjs / gen-icons.mjs）自动生成，
// 既减小体积又避免二进制 png 进分享包。
const FORBIDDEN = [
  '.gitignore',                  // 内部版本控制配置，非分享产物
  'launcher.vbs',                // 本地启动器，收件人用 npm start 即可（由 deploy.mjs 部署时内联生成）
  '.launcher.vbs',               // 兼容可能的笔误命名
  'webchat-protocol.reg.example', // 协议注册表模板，改用 README 指引手动创建
  'extension.crx',               // 打包扩展二进制：浏览器禁本地安装 + 分享不需要
  'extension.pem',               // 签名私钥：绝不可进共享包（安全 + 体积）
  '_meta.json',                  // 安装元数据，非源
  '_skillhub_meta.json',
];
function isForbidden(relPath) {
  const norm = relPath.replace(/\\/g, '/');
  const base = norm.split('/').pop();
  if (base.toLowerCase().endsWith('.png')) return true;   // 图标由 agent 部署时生成，不进包
  return FORBIDDEN.includes(base) || FORBIDDEN.includes(norm);
}

// ---------- 收集文件 ----------
const files = [];
function walk(dir, rel, sensitive) {
  for (const entry of readdirSync(dir)) {
    if (entry === '.' || entry === '..') continue;
    const abs = join(dir, entry);
    const relPath = rel ? rel + '/' + entry : entry;
    const st = statSync(abs);
    if (st.isDirectory()) {
      if (isIgnored(relPath + '/')) continue;       // 跳过被忽略的目录（如 node_modules/）
      if (sensitive && sensitive(relPath + '/')) continue;
      walk(abs, relPath, sensitive);
    } else {
      if (isIgnored(relPath)) continue;
      if (isForbidden(relPath)) continue;
      if (sensitive && sensitive(relPath)) continue;
      files.push({ abs, rel: relPath.split('\\').join('/') });
    }
  }
}

// 1) 项目本体（手动安装版）—— 同样套用敏感过滤，根目录残留的 .env/.pem 也会被排除
walk(ROOT, '', isSkillSensitive);

// 2) agent 技能版（可选）：默认 ~/.workbuddy/skills/webchat-extension，可用 SKILL_DIR 覆盖
//    扁平化进归档根：SKILL.md 直接落在 webchat-extension/ 下（根目录），
//    并排除 assets/root（与项目根文档重复，避免 zip 同名冲突、且 deploy.mjs 已容错缺失）。
const SKILL_SRC = process.env.SKILL_DIR
  || join(homedir(), '.workbuddy/skills/webchat-extension');
if (existsSync(SKILL_SRC)) {
  walk(
    SKILL_SRC,
    '',
    (rel) => isSkillSensitive(rel) || rel.replace(/\\/g, '/').startsWith('assets/root'),
  );
} else {
  console.log(`  (未找到 skill 目录 ${SKILL_SRC}，跳过技能版)`);
}

// ---------- 纯 JS ZIP 写入（stored，无压缩，零依赖） ----------
const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    t[n] = c >>> 0;
  }
  return t;
})();
function crc32(buf) {
  let c = 0xFFFFFFFF;
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xFF] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}
function dosTime(d) { return ((d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() >> 1)) & 0xFFFF; }
function dosDate(d) { return (((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate()) & 0xFFFF; }

const enc = new TextEncoder();
const localParts = [];
const central = [];
let offset = 0;
const seen = new Set();   // 防同名重复条目（项目根与技能 assets/root 可能撞名）

for (const f of files) {
  const zipName = TOP + '/' + f.rel;
  if (seen.has(zipName)) continue;
  seen.add(zipName);
  const data = readFileSync(f.abs);
  const name = TOP + '/' + f.rel;
  const nameBuf = enc.encode(name);
  const crc = crc32(data);
  const size = data.length;
  const now = new Date();

  const lh = Buffer.alloc(30);
  lh.writeUInt32LE(0x04034b50, 0);
  lh.writeUInt16LE(20, 4);
  lh.writeUInt16LE(0, 6);
  lh.writeUInt16LE(0, 8);            // method 0 = stored
  lh.writeUInt16LE(dosTime(now), 10);
  lh.writeUInt16LE(dosDate(now), 12);
  lh.writeUInt32LE(crc, 14);
  lh.writeUInt32LE(size, 18);
  lh.writeUInt32LE(size, 22);
  lh.writeUInt16LE(nameBuf.length, 26);
  lh.writeUInt16LE(0, 28);
  localParts.push(lh, nameBuf, data);

  const ch = Buffer.alloc(46);
  ch.writeUInt32LE(0x02014b50, 0);
  ch.writeUInt16LE(20, 4);
  ch.writeUInt16LE(20, 6);
  ch.writeUInt16LE(0, 8);
  ch.writeUInt16LE(0, 10);
  ch.writeUInt16LE(dosTime(now), 12);
  ch.writeUInt16LE(dosDate(now), 14);
  ch.writeUInt32LE(crc, 16);
  ch.writeUInt32LE(size, 20);
  ch.writeUInt32LE(size, 24);
  ch.writeUInt16LE(nameBuf.length, 28);
  ch.writeUInt16LE(0, 30);
  ch.writeUInt16LE(0, 32);
  ch.writeUInt16LE(0, 34);
  ch.writeUInt16LE(0, 36);
  ch.writeUInt32LE(0, 38);
  ch.writeUInt32LE(offset, 42);
  central.push(ch, nameBuf);

  offset += 30 + nameBuf.length + size;
}

const localBuf = Buffer.concat(localParts);
const centralBuf = Buffer.concat(central);
const eocd = Buffer.alloc(22);
eocd.writeUInt32LE(0x06054b50, 0);
eocd.writeUInt16LE(0, 4);
eocd.writeUInt16LE(0, 6);
eocd.writeUInt16LE(files.length, 8);
eocd.writeUInt16LE(files.length, 10);
eocd.writeUInt32LE(centralBuf.length, 12);
eocd.writeUInt32LE(localBuf.length, 16);
eocd.writeUInt16LE(0, 20);

writeFileSync(OUT, Buffer.concat([localBuf, centralBuf, eocd]));

console.log(`\u2713 已打包 ${files.length} 个文件`);
console.log(`  输出: ${OUT}`);
console.log(`  大小: ${(statSync(OUT).size / 1024).toFixed(1)} KB`);
console.log(`  按 .gitignore 排除: ${patterns.join(', ')}`);
