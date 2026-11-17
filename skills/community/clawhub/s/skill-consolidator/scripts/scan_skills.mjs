#!/usr/bin/env node
/**
 * scan_skills.mjs — 吸星大法 / Skill Consolidator 扫描器
 *
 * 确定性扫描脚本：扫描本地已知 AI Agent 的 skills/rules/commands 位置，
 * 解析 frontmatter，检测同名冲突 / 功能重叠 / 触发词冲突 / 版本差异，
 * 按类别归档，生成 Markdown 整理报告（同时输出到 stdout）或 JSON。
 *
 * 用法：
 *   node scan_skills.mjs [--output <report.md>] [--json] [--no-write] [--extra <path,...>]
 *
 * 注意：扫描目标表（TARGETS）是本 skill 扫描范围的单一事实来源。
 * 需要扩展扫描位置时直接改这里，不要改 SKILL.md。
 */
import { readFileSync, writeFileSync, existsSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { homedir } from 'node:os';
import { createHash } from 'node:crypto';

const VERSION = '2.0.0';
const HOME = homedir();
const EOL = '\n';

// ---------------- CLI ----------------
const args = process.argv.slice(2);
const getArg = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};
const hasFlag = (name) => args.includes(name);
const OUTPUT = resolve(getArg('--output') ?? 'skill-consolidation-report.md');
const WANT_JSON = hasFlag('--json');
const WANT_WRITE = !hasFlag('--no-write');
const EXTRA = (getArg('--extra') ?? '')
  .split(',')
  .map((s) => s.trim())
  .filter(Boolean)
  .map((p) => resolve(p.replace(/^~(?=\/|$)/, HOME)));

// ---------------- 扫描目标表（单一事实来源） ----------------
// type:
//   'dir'    → <base>/<name>/<filePattern>
//   'file'   → 单文件配置，<path> 本身即条目
//   'nested' → 在 <path> 下递归寻找名为 <nestedDir> 的目录，再扫描其中的 <name>/<filePattern>
const TARGETS = [
  // P0 目录型 SKILL.md
  { p: 'P0', tool: 'WorkBuddy',  type: 'dir',    project: '.workbuddy/skills', user: '~/.workbuddy/skills', filePattern: 'SKILL.md' },
  { p: 'P0', tool: 'Trae',       type: 'dir',    project: '.trae/skills',      user: '~/.trae-cn/skills',   filePattern: 'SKILL.md' },
  { p: 'P0', tool: 'Cursor',     type: 'dir',    project: '.cursor/skills',    user: '~/.cursor/skills',    filePattern: 'SKILL.md' },
  { p: 'P0', tool: 'Claude Code', type: 'dir',   project: '.claude/skills',    user: '~/.claude/skills',    filePattern: 'SKILL.md' },
  { p: 'P0', tool: 'Agents',     type: 'dir',    project: '.agents/skills',    user: '~/.agents/skills',    filePattern: 'SKILL.md' },
  // P1 目录型 plain rules（文件名即规则名）
  { p: 'P1', tool: 'Windsurf',   type: 'dir',    project: '.windsurf/rules',   user: '~/.windsurf/rules',   filePattern: '<name>.md' },
  { p: 'P1', tool: 'Cline',      type: 'dir',    project: '.cline/rules',      user: '~/.cline/rules',      filePattern: '<name>.md' },
  { p: 'P1', tool: 'Continue',   type: 'dir',    project: '.continue/rules',   user: '~/.continue/rules',   filePattern: '<name>.md' },
  { p: 'P1', tool: 'Roo Code',   type: 'dir',    project: '.roo/rules',        user: '~/.roo/rules',        filePattern: '<name>.md' },
  // P2 单文件配置
  { p: 'P2', tool: 'GitHub Copilot', type: 'file', path: '.github/copilot-instructions.md' },
  { p: 'P2', tool: 'OpenAI Codex',    type: 'file', path: '.codex/AGENTS.md' },
  { p: 'P2', tool: 'Aider',           type: 'file', path: '.aider.conf.yml' },
  { p: 'P2', tool: 'Augment',         type: 'file', path: 'augment-guidelines.md' },
  // P3 内置 / 插件缓存 skills（只读参考）
  { p: 'P3', tool: 'WorkBuddy plugins', type: 'nested', path: '~/.workbuddy/plugins/cache', nestedDir: 'skills', filePattern: 'SKILL.md', maxDirs: 400 },
  { p: 'P3', tool: 'Cursor plugins',    type: 'nested', path: '~/.cursor/plugins/cache',    nestedDir: 'skills', filePattern: 'SKILL.md', maxDirs: 400 },
];

// ---------------- 分类关键词 ----------------
const CATEGORIES = {
  research:  { zh: ['科研', '研究', '论文', '文献', '学术', '调研', '综述'], en: ['research', 'academic', 'paper', 'literature', 'survey', 'study'] },
  writing:   { zh: ['写作', '文案', '文章', '博客', '润色', '翻译', '作文'], en: ['writing', 'write', 'copywriting', 'essay', 'blog', 'polish', 'translate'] },
  coding:    { zh: ['编程', '代码', '开发', '前端', '后端', '重构', '脚本'], en: ['coding', 'code', 'develop', 'frontend', 'backend', 'refactor', 'program'] },
  debugging: { zh: ['调试', '报错', '修复错误', '排查问题', '错误定位'], en: ['debug', 'bug', 'troubleshoot', 'error'] },
  browser:   { zh: ['浏览器', '爬虫', '自动化', '网页抓取'], en: ['browser', 'automation', 'scrape', 'webdriver', 'selenium'] },
  design:    { zh: ['设计', 'ui', 'ux', '图标', '海报', '配色', 'figma'], en: ['design', 'ui', 'ux', 'icon', 'poster', 'figma'] },
  planning:  { zh: ['规划', '计划', '项目管理', '路线图', '任务管理'], en: ['planning', 'plan', 'roadmap', 'project management', 'todo'] },
  docs:      { zh: ['文档', 'docx', 'pdf', 'pptx', 'xlsx', '表格', 'word', 'excel', '幻灯片', '电子表格'], en: ['document', 'docx', 'pdf', 'pptx', 'xlsx', 'excel', 'word', 'slide', 'spreadsheet'] },
  finance:   { zh: ['金融', '股票', '基金', '投资', '财报', '估值', '行情', '量化', '外汇'], en: ['finance', 'stock', 'fund', 'invest', 'valuation', 'quant', 'trading', 'forex'] },
};

const EN_STOPWORDS = new Set([
  'the', 'and', 'for', 'with', 'from', 'that', 'this', 'these', 'those', 'you', 'your', 'use',
  'used', 'using', 'will', 'can', 'should', 'when', 'what', 'which', 'while', 'into', 'over',
  'under', 'then', 'than', 'they', 'them', 'their', 'have', 'has', 'had', 'not', 'are', 'was',
  'were', 'but', 'also', 'only', 'its', 'it', 'is', 'of', 'to', 'in', 'on', 'at', 'by', 'as',
  'or', 'if', 'be', 'been', 'being', 'skill', 'skills', 'agent', 'agents', 'ai', 'file', 'files',
  'tool', 'tools', 'task', 'tasks', 'work', 'works', 'make', 'makes', 'making', 'get', 'gets',
  'help', 'helps', 'support', 'supports', 'list', 'lists', 'build', 'built', 'create', 'creates',
  'generat', 'data', 'output', 'input', 'result', 'results', 'process', 'project', 'code',
  // 领域通用词：出现频率过高，不代表功能重叠
  'write', 'writes', 'writing', 'document', 'documents', 'documentation', 'text', 'content',
  'format', 'formats', 'example', 'examples', 'section', 'sections', 'version', 'versions',
  'description', 'descriptions', 'command', 'commands', 'need', 'needs', 'needed', 'ensure',
  'page', 'pages', 'language', 'languages', 'system', 'systems', 'based', 'standard', 'follow',
  'following', 'include', 'includes', 'including', 'must', 'may', 'might', 'way', 'ways', 'want',
  'wants', 'like', 'sure', 'well', 'one', 'two', 'new', 'about', 'after', 'before', 'such',
  'other', 'more', 'most', 'very', 'just', 'even', 'still', 'first', 'next', 'last', 'back',
  'case', 'cases', 'part', 'parts', 'point', 'points', 'step', 'steps', 'set', 'sets', 'line',
  'lines', 'time', 'times', 'name', 'names', 'path', 'paths', 'main', 'common', 'specific',
  'general', 'simple', 'easy', 'good', 'best', 'great', 'important', 'necessary', 'possible',
  'provide', 'provides', 'provided', 'produce', 'produces', 'produced', 'add', 'adds', 'added',
  'remove', 'removes', 'removed', 'change', 'changes', 'changed', 'show', 'shows', 'shown',
  'give', 'gives', 'given', 'take', 'takes', 'taken', 'call', 'calls', 'called', 'run', 'runs',
  'running', 'start', 'starts', 'started', 'stop', 'stops', 'stopped', 'save', 'saves', 'saved',
  'open', 'opens', 'opened', 'close', 'closes', 'closed', 'read', 'reads', 'writing', 'done',
]);

// ---------------- 工具函数 ----------------
function expand(p) {
  return p ? p.replace(/^~(?=\/|$)/, HOME) : null;
}

function readSafe(p) {
  try {
    return readFileSync(p, 'utf8');
  } catch {
    return null;
  }
}

function contentHash(text) {
  return createHash('sha1').update(text).digest('hex').slice(0, 12);
}

/** 解析简单 YAML frontmatter（仅支持单行 key: value，嵌套块自动跳过） */
function parseFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return { fm: {}, raw: '' };
  const raw = m[1];
  const fm = {};
  for (const line of raw.split(/\r?\n/)) {
    const kv = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!kv) continue;
    let v = kv[2].trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
      v = v.slice(1, -1);
    }
    fm[kv[1]] = v;
  }
  return { fm, raw };
}

/** 提取正文：frontmatter 之后的内容，截取头部 N 字符（headings 优先） */
function extractBody(text) {
  const m = text.match(/^---\r?\n[\s\S]*?\r?\n---\r?\n?([\s\S]*)$/);
  if (!m) return text.slice(0, 1200);
  const body = m[1];
  const headings = (body.match(/^#{1,3}\s+.*$/gm) ?? []).join('\n');
  return (headings + '\n' + body).slice(0, 1600);
}

/** 提取英文有效词（长度 ≥ 4，去停用词） */
function enWords(text) {
  const words = (text.match(/[A-Za-z]{4,}/g) ?? [])
    .map((w) => w.toLowerCase())
    .filter((w) => !EN_STOPWORDS.has(w));
  return [...new Set(words)];
}

/** 提取触发词：description 中的 /command 形式 */
function slashCommands(text) {
  return [...new Set((text.match(/\/[a-z0-9_-]+/gi) ?? []).map((s) => s.toLowerCase()))];
}

/** 分类打分：返回 { category, score } */
function categorize(desc, body) {
  const haystack = (desc + '\n' + body).toLowerCase();
  const scores = {};
  for (const [cat, kw] of Object.entries(CATEGORIES)) {
    let s = 0;
    for (const k of kw.zh) if (haystack.includes(k)) s += 2;
    for (const k of kw.en) if (haystack.includes(k)) s += 2;
    if (s > 0) scores[cat] = s;
  }
  const entries = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  return entries.length ? entries[0][0] : 'other';
}

/** 递归收集 <root> 下所有名为 <dirName> 的目录 */
function findDirsNamed(root, dirName, maxDirs) {
  const out = [];
  if (!existsSync(root)) return out;
  const stack = [root];
  let visited = 0;
  while (stack.length && out.length < maxDirs && visited < maxDirs * 10) {
    const dir = stack.pop();
    visited++;
    let entries;
    try {
      entries = readdirSync(dir, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const e of entries) {
      if (!e.isDirectory()) continue;
      const p = join(dir, e.name);
      if (e.name === dirName) {
        out.push(p);
        if (out.length >= maxDirs) break;
      } else {
        stack.push(p);
      }
    }
  }
  return out;
}

// ---------------- 扫描 ----------------
function scanBase(base, target, skillEntries, sourceScope, counts) {
  if (!existsSync(base)) return;
  const dirs = readdirSync(base, { withFileTypes: true }).filter((e) => e.isDirectory());
  for (const d of dirs) {
    const dirPath = join(base, d.name);
    const file =
      target.filePattern === '<name>.md' ? join(dirPath, `${d.name}.md`) : join(dirPath, target.filePattern);
    if (!existsSync(file)) continue;
    const text = readSafe(file);
    if (text == null) continue;
    const { fm } = parseFrontmatter(text);
    const name = fm.name || d.name;
    const desc = fm.description || extractBody(text).split('\n').find((l) => l.trim().length > 10) || '';
    skillEntries.push({
      name,
      tool: target.tool,
      priority: target.p,
      scope: sourceScope,
      path: file,
      desc: desc.slice(0, 300),
      body: extractBody(text),
      hash: contentHash(text),
      category: categorize(fm.description || '', extractBody(text)),
    });
    counts[target.tool] = (counts[target.tool] ?? 0) + 1;
  }
}

const skillEntries = [];
const counts = {};

for (const t of TARGETS) {
  if (t.type === 'dir') {
    for (const [scope, p] of [['project', t.project], ['user', t.user]]) {
      if (p) scanBase(expand(p), t, skillEntries, scope, counts);
    }
  } else if (t.type === 'file') {
    const p = expand(t.path);
    if (!p || !existsSync(p)) continue;
    const text = readSafe(p);
    if (text == null) continue;
    const { fm } = parseFrontmatter(text);
    skillEntries.push({
      name: fm.name || t.tool,
      tool: t.tool,
      priority: t.p,
      scope: existsSync(join(process.cwd(), t.path)) ? 'project' : 'user',
      path: p,
      desc: fm.description || text.slice(0, 200),
      body: extractBody(text),
      hash: contentHash(text),
      category: categorize(fm.description || '', extractBody(text)),
    });
    counts[t.tool] = (counts[t.tool] ?? 0) + 1;
  } else if (t.type === 'nested') {
    const root = expand(t.path);
    const skillsDirs = root ? findDirsNamed(root, t.nestedDir, t.maxDirs ?? 400) : [];
    for (const skillsDir of skillsDirs) {
      scanBase(skillsDir, { ...t, tool: t.tool }, skillEntries, 'user', counts);
    }
  }
}

// 额外目录
for (const extra of EXTRA) {
  const t = { p: 'EXTRA', tool: 'Extra', type: 'dir', filePattern: 'SKILL.md' };
  scanBase(extra, t, skillEntries, 'user', counts);
}

// ---------------- 冲突检测 ----------------
const groups = new Map();
for (const s of skillEntries) {
  const key = s.name.toLowerCase().replace(/[\s/]+/g, '-');
  if (!groups.has(key)) groups.set(key, []);
  groups.get(key).push(s);
}

const nameCollisions = [];
const versionDivergences = [];
for (const [key, list] of groups) {
  if (list.length < 2) continue;
  const byHash = new Map();
  for (const s of list) {
    if (!byHash.has(s.hash)) byHash.set(s.hash, []);
    byHash.get(s.hash).push(s);
  }
  if (byHash.size === 1) {
    nameCollisions.push({ name: list[0].name, entries: list, identical: true });
  } else {
    versionDivergences.push({ name: list[0].name, entries: list, groups: [...byHash.values()] });
  }
}

// 功能重叠 + 触发词冲突：两两比较
const functionalOverlaps = [];
const triggerConflicts = [];
const OVERLAP_DISPLAY_CAP = 40; // 报告展示上限，避免刷屏
for (let i = 0; i < skillEntries.length; i++) {
  for (let j = i + 1; j < skillEntries.length; j++) {
    const a = skillEntries[i];
    const b = skillEntries[j];
    if (a.path === b.path) continue;
    // 同名条目已在"同名冲突/版本差异"中上报，这里不再重复
    if (a.name.toLowerCase() === b.name.toLowerCase()) continue;
    // 类别关键词重合度（只统计共享的、属于分类关键词的命中）
    const categoryKeywords = new Set([
      ...Object.values(CATEGORIES).flatMap((k) => k.zh),
      ...Object.values(CATEGORIES).flatMap((k) => k.en),
    ]);
    const wordsA = new Set((a.desc + a.body).toLowerCase().match(/[a-z]{4,}|[\u4e00-\u9fa5]{2,4}/g) ?? []);
    const wordsB = new Set((b.desc + b.body).toLowerCase().match(/[a-z]{4,}|[\u4e00-\u9fa5]{2,4}/g) ?? []);
    const shared = [...wordsA].filter((w) => wordsB.has(w) && categoryKeywords.has(w));
    const sharedScore = shared.length;

    // 英文有效词重叠
    const enA = enWords(a.desc + ' ' + a.body);
    const enB = enWords(b.desc + ' ' + b.body);
    const sharedEn = enA.filter((w) => enB.includes(w)).length;

    // 判定为功能重叠：至少共享 1 个分类关键词，且重叠足够显著
    // P3（插件缓存）之间的重叠从严：需要共享 ≥2 个分类关键词
    const significant = sharedScore >= 2 || (sharedScore >= 1 && sharedEn >= 4) || sharedEn >= 6;
    const bothP3 = a.priority === 'P3' && b.priority === 'P3';
    if ((bothP3 ? sharedScore >= 2 : significant)) {
      functionalOverlaps.push({ a, b, shared: shared.slice(0, 8), sharedEn, score: sharedScore * 2 + sharedEn });
    }
    // 触发词冲突：共享 /command
    const cmdsA = slashCommands(a.desc);
    const cmdsB = slashCommands(b.desc);
    const sharedCmds = cmdsA.filter((c) => cmdsB.includes(c));
    if (sharedCmds.length) {
      triggerConflicts.push({ a, b, commands: sharedCmds });
    }
  }
}

// ---------------- 报告生成 ----------------
function fmtPath(p) {
  return p.replace(HOME, '~');
}

function markdownReport() {
  const lines = [];
  const now = new Date().toISOString().slice(0, 16).replace('T', ' ');
  lines.push('# Skill Consolidation Report');
  lines.push('');
  lines.push(`> 由 吸星大法 v${VERSION} 生成于 ${now} · 共发现 ${skillEntries.length} 个 skill / rule / command`);
  lines.push('');

  // 摘要
  const projectCount = skillEntries.filter((s) => s.scope === 'project').length;
  const userCount = skillEntries.filter((s) => s.scope === 'user').length;
  lines.push('## 摘要 Summary');
  lines.push('');
  lines.push(`- 扫描到 **${skillEntries.length}** 个条目（项目级 ${projectCount}，用户级 ${userCount}）`);
  lines.push(`- 同名冲突 **${nameCollisions.length}** 处，版本差异 **${versionDivergences.length}** 处`);
  lines.push(`- 功能重叠 **${functionalOverlaps.length}** 处，触发词冲突 **${triggerConflicts.length}** 处`);
  lines.push('');

  // 总览表
  lines.push('## 总览 Overview');
  lines.push('');
  lines.push('| name | tool | scope | category | path |');
  lines.push('|---|---|---|---|---|');
  for (const s of skillEntries) {
    lines.push(`| ${s.name} | ${s.tool} | ${s.scope} | ${s.category} | \`${fmtPath(s.path)}\` |`);
  }
  lines.push('');

  // 同名冲突
  if (nameCollisions.length) {
    lines.push('## 同名冲突 Name Collisions');
    lines.push('');
    for (const c of nameCollisions) {
      lines.push(`### \`${c.name}\`${c.identical ? '（内容相同，为重复副本）' : ''}`);
      lines.push('');
      for (const s of c.entries) lines.push(`- [${s.tool}/${s.scope}] \`${fmtPath(s.path)}\``);
      lines.push(`- **建议**：${c.identical ? '保留高优先级（P0 优先、项目级优先）的一份，其余禁用/删除。' : '同一名称内容不同，核实后保留最新、删除陈旧版本，或重命名其中一个。'}`);
      lines.push('');
    }
  }

  // 版本差异
  if (versionDivergences.length) {
    lines.push('## 版本差异 Version Divergence');
    lines.push('');
    for (const v of versionDivergences) {
      lines.push(`### \`${v.name}\``);
      lines.push('');
      for (const s of v.entries) {
        lines.push(`- [${s.tool}/${s.scope}] \`${fmtPath(s.path)}\` (hash ${s.hash})`);
      }
      lines.push(`- **建议**：对比差异后保留目标版本，其余禁用或改名。`);
      lines.push('');
    }
  }

  // 功能重叠（按分数降序，超出上限只展示前 N 条）
  if (functionalOverlaps.length) {
    lines.push('## 功能重叠 Functional Overlap');
    lines.push('');
    const sorted = [...functionalOverlaps].sort((x, y) => y.score - x.score);
    const shown = sorted.slice(0, OVERLAP_DISPLAY_CAP);
    if (sorted.length > OVERLAP_DISPLAY_CAP) {
      lines.push(`> 共 ${sorted.length} 处，仅展示重叠度最高的 ${OVERLAP_DISPLAY_CAP} 处。`);
      lines.push('');
    }
    for (const o of shown) {
      lines.push(`### \`${o.a.name}\` ↔ \`${o.b.name}\``);
      lines.push('');
      lines.push(`- ${o.a.name}（${o.a.tool}/${o.a.scope}，类别 ${o.a.category}）↔ ${o.b.name}（${o.b.tool}/${o.b.scope}，类别 ${o.b.category}）`);
      if (o.shared.length) lines.push(`- 共享关键词：${o.shared.join('、')}`);
      if (o.sharedEn) lines.push(`- 英文词重叠：${o.sharedEn} 个`);
      lines.push(`- **建议**：合并为 \`MASTER-${o.a.category !== 'other' ? o.a.category : 'misc'}\`，或重写 description 提升区分度。`);
      lines.push('');
    }
  }

  // 触发词冲突
  if (triggerConflicts.length) {
    lines.push('## 触发词冲突 Trigger Conflict');
    lines.push('');
    for (const t of triggerConflicts) {
      lines.push(`### \`${t.a.name}\` ↔ \`${t.b.name}\``);
      lines.push('');
      lines.push(`- 共享触发词：${t.commands.join('、')}`);
      lines.push(`- **建议**：两个 skill 会命中相同指令，保留主 skill，另一个移除该触发词或重命名命令。`);
      lines.push('');
    }
  }

  // 分类索引
  const byCat = new Map();
  for (const s of skillEntries) {
    if (!byCat.has(s.category)) byCat.set(s.category, []);
    byCat.get(s.category).push(s);
  }
  lines.push('## 分类索引 Categorized Index');
  lines.push('');
  for (const [cat, list] of [...byCat.entries()].sort()) {
    lines.push(`### ${cat}（${list.length}）`);
    lines.push('');
    for (const s of list) lines.push(`- ${s.name} — ${s.tool}/${s.scope}`);
    lines.push('');
  }

  // 建议
  const totalIssues = nameCollisions.length + versionDivergences.length + functionalOverlaps.length + triggerConflicts.length;
  lines.push('## 整理建议 Recommendations');
  lines.push('');
  if (totalIssues === 0) {
    lines.push('未发现冲突。当前 skills 目录状态健康，无需整理。');
  } else {
    lines.push('1. 优先处理同名冲突与版本差异（可能影响 skill 加载）。');
    lines.push('2. 对功能重叠的同类 skill，合并为 `MASTER-<category>` 主 skill。');
    lines.push('3. 对触发词冲突，调整 description 中的命令/关键词，避免抢命中。');
    lines.push('4. 以上操作均需用户确认后执行；本脚本只读，不修改任何文件。');
  }
  lines.push('');
  return lines.join(EOL);
}

function jsonReport() {
  return JSON.stringify(
    {
      version: VERSION,
      generatedAt: new Date().toISOString(),
      summary: {
        total: skillEntries.length,
        project: skillEntries.filter((s) => s.scope === 'project').length,
        user: skillEntries.filter((s) => s.scope === 'user').length,
        nameCollisions: nameCollisions.length,
        versionDivergences: versionDivergences.length,
        functionalOverlaps: functionalOverlaps.length,
        triggerConflicts: triggerConflicts.length,
      },
      skills: skillEntries,
      conflicts: {
        nameCollisions: nameCollisions.map((c) => ({ name: c.name, identical: c.identical, paths: c.entries.map((s) => s.path) })),
        versionDivergences: versionDivergences.map((v) => ({ name: v.name, paths: v.entries.map((s) => s.path) })),
        functionalOverlaps: functionalOverlaps.map((o) => ({ a: o.a.path, b: o.b.path, shared: o.shared, score: o.score })),
        triggerConflicts: triggerConflicts.map((t) => ({ a: t.a.path, b: t.b.path, commands: t.commands })),
      },
    },
    null,
    2,
  );
}

// ---------------- 输出 ----------------
if (WANT_JSON) {
  const out = jsonReport();
  process.stdout.write(out + EOL);
  if (WANT_WRITE) writeFileSync(OUTPUT, out, 'utf8');
} else {
  const report = markdownReport();
  process.stdout.write(report);
  if (WANT_WRITE) {
    writeFileSync(OUTPUT, report, 'utf8');
    console.error(`\n[吸星大法] 报告已写入 ${OUTPUT}`);
  }
}
