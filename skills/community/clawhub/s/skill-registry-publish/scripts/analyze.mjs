#!/usr/bin/env node
// 赛道分析：拉同类 skill 的 SKILL.md，从它们的章节标题里自下而上提炼能力维度。
//
//   node analyze.mjs "<关键词>" [--top 6] [--json]
//
// 不预设任何维度。不同赛道的能力完全不同，预设一套维度只能分析一个赛道。
// 做法是把每个 SKILL.md 的二级三级标题抽出来归一化，统计哪些在多数同类里重复出现、
// 哪些只有一两个有。重复出现的是这个赛道的标配，少数的位置是差异化空间。
import { t } from './lib-i18n.mjs';

const argv = process.argv.slice(2);
let keyword = '';
let top = 6;
let json = false;
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--top') top = Number(argv[++i]) || 6;
  else if (argv[i] === '--json') json = true;
  else if (!keyword) keyword = argv[i];
}

if (!keyword) {
  console.error(t('用法：node analyze.mjs "<关键词>" [--top 6] [--json]', 'Usage: node analyze.mjs "<keyword>" [--top 6] [--json]'));
  process.exit(2);
}

const C = {
  ok: (s) => `\x1b[32m✓\x1b[0m ${s}`,
  warn: (s) => `\x1b[33m!\x1b[0m ${s}`,
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
  bold: (s) => `\x1b[1m${s}\x1b[0m`,
};

// 文档结构型标题，不算能力。几乎每个 skill 都有，单列出来不参与能力统计
const STRUCTURAL =
  /^(usage|install|installation|quick ?start|example|examples|setup|requirements?|license|overview|intro|introduction|about|when to use|用法|安装|示例|快速开始|概览|简介|许可|前置条件)$/i;

// 归一化：去编号、标点、括号注、常见修饰
const SYNONYMS = [
  [/^(step|phase|stage)\s*\d+/i, 'step'],
  [/\b(optional|advanced|basic|simple|full|complete)\b/gi, ''],
];

function normHeading(h) {
  let s = String(h)
    .replace(/^\d+[.)]\s*/, '')
    .replace(/[*`_~]/g, '')
    .replace(/^[^\p{L}\p{N}]+/u, '')
    .trim()
    .toLowerCase();
  for (const [re, rep] of SYNONYMS) s = s.replace(re, rep);
  return s.replace(/\s+/g, ' ').trim();
}

// 聚到「能力」级别，不聚到具体功能。
// 英文取首个词：extract text / extract images / extract pages 合成 extract 一组，
// 这样看到的才是「提取」这项能力，而不是三个零散功能。
// 中文没有词边界，取前两个字。
function clusterKey(s) {
  if (!s) return '';
  if (/[\u4e00-\u9fa5]/.test(s)) return s.slice(0, 2);
  return s.split(' ')[0].replace(/[^a-z0-9-]/g, '');
}

function extractHeadings(md) {
  const out = [];
  for (const line of md.split('\n')) {
    const m = line.match(/^(#{2,3})\s+(.+?)\s*$/);
    if (m) out.push(m[2]);
  }
  return out;
}

function parseId(id) {
  const parts = String(id).split('/');
  if (parts.length < 3) return null;
  return { owner: parts[0], repo: parts[1], skill: parts.slice(2).join('/') };
}

async function fetchSkillMd({ owner, repo, skill }) {
  const paths = [`skills/${skill}/SKILL.md`, `${skill}/SKILL.md`, 'SKILL.md', `skills/${repo}/SKILL.md`];
  for (const p of paths) {
    for (const branch of ['main', 'master']) {
      try {
        const r = await fetch(`https://raw.githubusercontent.com/${owner}/${repo}/${branch}/${p}`, {
          signal: AbortSignal.timeout(8000),
        });
        if (r.ok) return await r.text();
      } catch {
        /* 试下一个 */
      }
    }
  }
  return '';
}

async function search(q) {
  const r = await fetch(`https://www.skills.sh/api/search?q=${encodeURIComponent(q)}`, {
    signal: AbortSignal.timeout(15000),
  });
  if (!r.ok) throw new Error('skills.sh 搜索失败 HTTP ' + r.status);
  return r.json();
}

// 单个模糊查询会被热门大词淹没，拆成变体分别搜再合并
const variants = [...new Set([keyword, keyword.replace(/\s+/g, '-')])];
// 长度阈值原来写 >3，导致 pdf、ocr 这类三字关键词被过滤成空数组，
// every() 对空数组恒真，相关性过滤整体失效。改成 >=2
const words = keyword.toLowerCase().split(/[\s-]+/).filter((w) => w.length >= 2);
const pool = new Map();
for (const q of variants) {
  try {
    const d = await search(q);
    for (const s of d.skills || []) if (!pool.has(s.id) && parseId(s.id)) pool.set(s.id, s);
  } catch {
    /* 某个变体失败不影响整体 */
  }
}

const strict = [...pool.values()].filter((s) => words.every((w) => s.id.toLowerCase().includes(w)));
const picked = (strict.length ? strict : [...pool.values()])
  .sort((a, b) => (b.installs || 0) - (a.installs || 0))
  .slice(0, top);

console.log(`\n${C.bold(t('关键词', 'Keyword'))} ${keyword}   ${t('分析', 'analyzing')} ${picked.length} ${t('个同类', 'peers')}`);

const docs = [];
for (const s of picked) {
  const md = await fetchSkillMd(parseId(s.id));
  docs.push({
    id: s.id,
    installs: s.installs || 0,
    md,
    headings: extractHeadings(md).map(normHeading).filter(Boolean),
  });
}

console.log('\n' + C.bold('=== ' + t('同类（按安装量）', 'Peers (by installs)') + ' ==='));
for (const d of docs) {
  console.log(`  ${String(d.installs).padStart(7)}  ${d.id}${d.md ? '' : C.dim(t('  (正文取不到)', '  (body unavailable)'))}`);
}

// 按聚类键归并，记录每组的覆盖面
const groups = new Map();
for (const d of docs) {
  const seen = new Set();
  for (const h of d.headings) {
    const k = clusterKey(h);
    if (!k || seen.has(k)) continue;
    seen.add(k);
    if (!groups.has(k)) groups.set(k, { label: k, variants: new Set(), who: new Set() });
    groups.get(k).variants.add(h);
    groups.get(k).who.add(d.id);
  }
}

const total = docs.filter((d) => d.md).length || 1;
const rows = [...groups.values()]
  .map((v) => ({ label: v.label, variants: [...v.variants], count: v.who.size, who: [...v.who] }))
  .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label));

const structural = rows.filter((r) => STRUCTURAL.test(r.label));
const capability = rows.filter((r) => !STRUCTURAL.test(r.label));

console.log('\n' + C.bold('=== ' + t('能力分布（从章节标题提炼）', 'Capability distribution (from section headings)') + ' ==='));
for (const r of capability.slice(0, 20)) {
  const tag =
    r.count >= total * 0.6
      ? C.ok(String(r.count) + '/' + total)
      : r.count === 1
        ? C.warn(t('独有', 'unique'))
        : String(r.count) + '/' + total;
  const variants = r.variants.length > 1 ? C.dim(' (' + r.variants.slice(0, 3).join(' / ') + ')') : '';
  const who = r.count === 1 ? C.dim(' ← ' + r.who[0]) : '';
  console.log(`  ${tag.padEnd(14)} ${r.label.slice(0, 24).padEnd(26)}${variants}${who}`);
}

if (structural.length) {
  console.log('\n' + C.dim(t('  文档结构型（不计入能力）：', '  Structural headings (not capabilities): ') + structural.map((r) => r.label).slice(0, 8).join(t('、', ', '))));
}

// 差异化空间 = 只被少数同类覆盖的章节
const rare = capability.filter((r) => r.count <= Math.max(1, Math.floor(total * 0.34)));
console.log('\n' + C.bold('=== ' + t('差异化空间', 'Differentiation space') + ' ==='));
if (rare.length) {
  for (const r of rare) {
    console.log(`  ${r.label.slice(0, 38).padEnd(40)} ${C.dim('← ' + r.who.map((w) => w.split('/')[0]).join(', '))}`);
  }
  console.log(C.dim(t('\n  这些章节只有少数同类有。可能是差异化点，也可能是那个 skill 的特有场景，需要看正文确认。', '\n  Only a few peers cover these. Could be a gap, or just that peer\'s special case. Check the source.')));
} else {
  console.log(C.dim(t('  没有明显差异，所有章节都在多数同类里出现。这个赛道已经做满了。', '  No clear gap; most peers share every section. This space is saturated.')));
}

const withMd = docs.filter((d) => d.md).length;
console.log(C.dim(`\n判定依据：${withMd}/${docs.length} 个 SKILL.md 可读，标题归一化后按前两词/前两字聚类。`));
console.log(C.dim(t('局限：聚类是字符串级的，「发布流程」和「发布步骤」可能归到一起也可能没归上；', 'Limits: grouping is string-level; similar headings may or may not merge;')));
console.log(C.dim('作者不写小标题的 skill 提取不到内容。结论要回原文核对。\n'));

if (json) {
  console.log(
    JSON.stringify(
      {
        keyword,
        docs: docs.map((d) => ({ id: d.id, installs: d.installs, chars: d.md.length })),
        capability,
        structural,
      },
      null,
      2
    )
  );
}
