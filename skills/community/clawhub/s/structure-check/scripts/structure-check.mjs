#!/usr/bin/env node
/**
 * structure-check —— 代码结构实现核对器（退出码裁决，模型只转述无权改判）。
 *
 * 职能划分：回归守卫管「改完后的行为验证」，TDD 守卫管「开发顺序合规」，
 * 本工具管「要求的东西在不在、接没接上」——机械结构核对，不做语义分析。
 *
 * 用法（项目根目录执行）:
 *   node structure-check.mjs <checklist.json>
 *
 * checklist 格式:
 *   {
 *     "task": "任务描述（可选）",
 *     "requirements": [
 *       { "desc": "Cart 类已定义",       "type": "exists",   "file": "src/cart.js",  "symbol": "Cart" },
 *       { "desc": "Cart 已导出",         "type": "exported", "file": "src/cart.js",  "symbol": "Cart" },
 *       { "desc": "addItem 已被调用",    "type": "called",   "file": "src/index.js", "symbol": "addItem" },
 *       { "desc": "computeTotal 非空壳", "type": "notStub",  "file": "src/cart.js",  "symbol": "computeTotal" }
 *     ]
 *   }
 *
 * 检查类型:
 *   exists   符号在本文件有定义（function/class/const|let|var/interface/type/enum/方法简写/def）
 *   exported 符号已导出（export ... / export default / module.exports / exports.x）
 *   called   符号在本文件存在调用点（排除定义行本身；new X() 也算调用）
 *   notStub  符号非空壳：去注释后空体、裸 return、TODO/未实现抛错、pass/... 均为 FAIL
 *
 * 退出码（唯一裁决依据）:
 *   0 = 全部要求 PASS
 *   1 = FAIL —— 清单本身合法，但至少一条要求未实现
 *   2 = UNVERIFIED —— 无法裁决（用法错误 / 清单缺失字段 / 非法 JSON / 未知检查类型）
 *
 * 说明: file 相对当前工作目录解析；文件不存在按该条 FAIL（不豁免）。
 *       以 JS/TS 为主；Python 支持 exists/notStub；exported/called 为 JS/TS 形态。
 */

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

// ── 基础工具 ───────────────────────────────────────────────
function esc(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
function stripJsComments(s) {
  return s.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/(^|[^:])\/\/[^\n]*/gm, '$1');
}
function stripHashComments(s) {
  return s.replace(/#[^\n]*/g, '');
}
function collapse(s) {
  return s.replace(/\s+/g, ' ').trim();
}
function truncate(s, n) {
  return s.length > n ? s.slice(0, n) + '…' : s;
}

// ── 输出 ───────────────────────────────────────────────────
function emit(result, fields, itemLines) {
  console.log('=== STRUCTURE CHECK ===');
  for (const [k, v] of Object.entries(fields)) console.log(`${k}: ${v}`);
  for (const l of itemLines || []) console.log(l);
  console.log(`result: ${result}`);
  console.log('=== END STRUCTURE CHECK ===');
}
function bail(result, fields) {
  emit(result, fields);
  process.exit(2);
}

// ── 定义定位 ───────────────────────────────────────────────
function findDef(src, sym) {
  const s = esc(sym);
  const pats = [
    ['function', new RegExp('\\b(?:async\\s+)?function\\s*\\*?\\s*' + s + '\\b')],
    ['class', new RegExp('\\bclass\\s+' + s + '\\b')],
    ['const', new RegExp('\\b(?:const|let|var)\\s+' + s + '\\b')],
    ['method', new RegExp('^\\s*(?:async\\s+)?(?:get\\s+|set\\s+)?' + s + '\\s*\\([^)]*\\)\\s*\\{', 'm')],
    ['def', new RegExp('^\\s*def\\s+' + s + '\\b', 'm')],
    ['tsdecl', new RegExp('\\b(?:interface|type|enum|namespace)\\s+' + s + '\\b')],
  ];
  let best = null;
  for (const [kind, re] of pats) {
    const m = re.exec(src);
    if (m && (best === null || m.index < best.index)) best = { kind, index: m.index };
  }
  return best;
}

function braceBody(src, fromIdx) {
  const open = src.indexOf('{', fromIdx);
  if (open === -1) return null;
  let d = 0;
  for (let i = open; i < src.length; i++) {
    if (src[i] === '{') d++;
    else if (src[i] === '}') {
      d--;
      if (d === 0) return src.slice(open + 1, i);
    }
  }
  return null;
}

// ── notStub ────────────────────────────────────────────────
// 去注释、折叠空白后的函数体，若只匹配这些形态即判空壳
const JS_STUB = new RegExp(
  '^(?:' +
    'return\\s*;?' +
    "|return\\s+(?:undefined|null|void\\s*0|\\{\\}|\\[\\]|''|\"\"|``)\\s*;?" +
    '|throw\\s+new\\s+Error\\s*\\([^)]*(?:not\\s*implemented|未实现|未完成|todo)[^)]*\\)\\s*;?' +
  ')$',
  'i'
);
const PY_STUB = /^(?:pass|\.\.\.|return(?:\s+None)?|raise\s+NotImplementedError.*)$/;
const EMPTY_VALUE = /^(?:undefined|null|\{\}|\[\]|(['"`])\1)\s*;?$/;

function ok(reason) {
  return { verdict: 'PASS', reason };
}
function no(reason) {
  return { verdict: 'FAIL', reason };
}

function judgeBrace(body, sym) {
  if (body === null) return no('无法定位函数体（无花括号体或不平衡）');
  const b = collapse(stripJsComments(body));
  if (b === '') return no(`空壳：${sym} 函数体为空（去注释后无代码）`);
  if (JS_STUB.test(b)) return no(`空壳：函数体只有固定返回/未实现抛错 —— ${truncate(b, 60)}`);
  return ok(`函数体非空（${b.length} 字符）`);
}

function judgeExpr(expr, sym) {
  const e = collapse(stripJsComments(expr)).replace(/;\s*$/, '');
  if (e === '' || EMPTY_VALUE.test(e)) return no(`空壳：箭头函数体只有 ${e || '空表达式'}`);
  return ok(`箭头函数有实现：${truncate(e, 40)}`);
}

function checkPyBody(src, defIdx, sym) {
  const lines = src.split('\n');
  const li = src.slice(0, defIdx).split('\n').length - 1;
  const indent = lines[li].match(/^\s*/)[0].length;
  const bodyLines = [];
  for (let j = li + 1; j < lines.length; j++) {
    const L = lines[j];
    if (L.trim() === '') {
      bodyLines.push('');
      continue;
    }
    if (L.match(/^\s*/)[0].length <= indent) break;
    bodyLines.push(L);
  }
  const b = collapse(stripHashComments(bodyLines.join('\n')));
  if (b === '' || PY_STUB.test(b)) return no(`空壳：函数体只有 ${truncate(b, 40) || '空'}`);
  return ok(`函数体非空（${b.length} 字符）`);
}

function checkNotStub(src, sym) {
  const d = findDef(src, sym);
  if (!d) return no('未找到定义，无法核实是否空壳');
  if (d.kind === 'def') return checkPyBody(src, d.index, sym);
  if (d.kind === 'const') {
    const eq = src.indexOf('=', d.index);
    if (eq === -1) return no('找到声明但无法定位赋值');
    const lineEnd = src.indexOf('\n', eq);
    const rhs = src.slice(eq + 1, lineEnd === -1 ? undefined : lineEnd).trim();
    const am = /^(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>\s*([\s\S]*)$/.exec(rhs);
    if (!am) {
      const v = rhs.replace(/;\s*$/, '').trim();
      if (EMPTY_VALUE.test(v)) return no(`空壳：赋值只有 ${v}`);
      return ok(`已赋值：${truncate(v, 40)}`);
    }
    const ab = am[1].trim();
    if (ab.startsWith('{')) return judgeBrace(braceBody(ab, 0), sym);
    return judgeExpr(ab, sym);
  }
  return judgeBrace(braceBody(src, d.index), sym);
}

// ── called ────────────────────────────────────────────────
function checkCalled(src, sym) {
  const s = esc(sym);
  const callRe = new RegExp('\\b' + s + '\\s*\\(');
  const constDef = new RegExp('\\b(?:const|let|var)\\s+' + s + '\\s*=');
  const fnDef = new RegExp('\\b(?:async\\s+)?function\\s*\\*?\\s*' + s + '\\b');
  const pyDef = new RegExp('\\bdef\\s+' + s + '\\b');
  const kwDef = new RegExp('\\b(?:class|interface|enum)\\s+' + s + '\\b');
  const methodDef = new RegExp('^\\s*(?:async\\s+)?' + s + '\\s*\\([^)]*\\)\\s*\\{\\s*$');
  for (const ln of src.split('\n')) {
    const m = callRe.exec(ln);
    if (!m) continue;
    if (constDef.test(ln) && ln.indexOf('=') !== -1 && ln.indexOf('=') < m.index) continue;
    if (fnDef.test(ln) || pyDef.test(ln) || kwDef.test(ln)) continue;
    if (methodDef.test(ln)) continue;
    return true;
  }
  return false;
}

// ── exported ───────────────────────────────────────────────
function checkExported(src, sym) {
  const s = esc(sym);
  const pats = [
    new RegExp('\\bexport\\s+(?:declare\\s+)?(?:default\\s+)?(?:async\\s+)?(?:const|let|var|function\\*?|class|interface|type|enum)\\s+' + s + '\\b'),
    new RegExp('\\bexport\\s*\\{[^}]*\\b' + s + '\\b[^}]*\\}'),
    new RegExp('\\bexport\\s+default\\s+' + s + '\\b'),
    new RegExp('\\bmodule\\.exports[^\\n=]*=[^\\n]*\\b' + s + '\\b'),
    new RegExp('\\bmodule\\.exports\\s*\\.\\s*' + s + '\\b'),
    new RegExp('\\bexports\\s*\\.\\s*' + s + '\\b'),
  ];
  return pats.some((p) => p.test(src));
}

// ── 主流程 ─────────────────────────────────────────────────
const listArg = process.argv[2];

if (!listArg) {
  bail('UNVERIFIED', { reason: '缺少清单参数。用法: node structure-check.mjs <checklist.json>' });
}

let raw;
try {
  raw = readFileSync(resolve(listArg), 'utf8');
} catch (e) {
  bail('UNVERIFIED', { checklist: listArg, reason: '清单文件无法读取: ' + e.message });
}

let cl;
try {
  cl = JSON.parse(raw);
} catch (e) {
  bail('UNVERIFIED', { checklist: listArg, reason: '清单不是合法 JSON: ' + e.message });
}

const reqs = cl && cl.requirements;
if (!Array.isArray(reqs) || reqs.length === 0) {
  bail('UNVERIFIED', { checklist: listArg, reason: '清单缺少非空 requirements 数组' });
}

const VALID = ['exists', 'exported', 'called', 'notStub'];
for (let i = 0; i < reqs.length; i++) {
  const r = reqs[i] || {};
  const bad =
    !VALID.includes(r.type)
      ? `type 非法（须为 ${VALID.join(' / ')}）`
      : typeof r.file !== 'string' || !r.file.trim()
        ? '缺少 file'
        : typeof r.symbol !== 'string' || !r.symbol.trim()
          ? '缺少 symbol'
          : null;
  if (bad) bail('UNVERIFIED', { checklist: listArg, requirement: `#${i + 1}`, reason: bad });
}

const fields = { checklist: listArg, requirements: String(reqs.length) };
if (cl.task) fields.task = cl.task;

const itemLines = [];
let passCount = 0;
let failCount = 0;

for (let i = 0; i < reqs.length; i++) {
  const r = reqs[i];
  let verdict = 'FAIL';
  let reason = '';
  let src = null;
  try {
    src = readFileSync(resolve(r.file), 'utf8');
    // 先去注释，避免「注释里的代码」造成假阳性；Python 文件额外去 # 注释
    src = stripJsComments(src);
    if (/\.py$/i.test(r.file)) src = stripHashComments(src);
  } catch {
    verdict = 'FAIL';
    reason = '文件不存在或不可读';
  }
  if (src !== null) {
    if (r.type === 'exists') {
      const d = findDef(src, r.symbol);
      verdict = d ? 'PASS' : 'FAIL';
      reason = d ? `已找到定义（${d.kind}）` : '未找到定义';
    } else if (r.type === 'exported') {
      if (!findDef(src, r.symbol)) {
        verdict = 'FAIL';
        reason = '未找到定义（无从导出）';
      } else if (checkExported(src, r.symbol)) {
        verdict = 'PASS';
        reason = '已导出';
      } else {
        verdict = 'FAIL';
        reason = '已定义但未导出（无 export / module.exports / exports.x）';
      }
    } else if (r.type === 'called') {
      verdict = checkCalled(src, r.symbol) ? 'PASS' : 'FAIL';
      reason = verdict === 'PASS' ? '存在调用点' : '未发现调用点（仅声明/导出不算调用）';
    } else if (r.type === 'notStub') {
      ({ verdict, reason } = checkNotStub(src, r.symbol));
    }
  }
  const desc = r.desc ? `（${r.desc}）` : '';
  itemLines.push(`[${i + 1}/${reqs.length}] ${verdict} ${r.type} ${r.symbol} @ ${r.file} —— ${reason}${desc}`);
  if (verdict === 'PASS') passCount++;
  else failCount++;
}

fields.summary = `passed ${passCount}, failed ${failCount}`;
emit(failCount > 0 ? 'FAIL' : 'PASS', fields, itemLines);
process.exit(failCount > 0 ? 1 : 0);
