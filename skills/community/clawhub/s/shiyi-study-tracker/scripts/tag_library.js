/**
 * tag_library.js
 * 每个考试独立的标签词库：识别前查、识别后写。
 * 保证同一考试内标签复用，不同考试互不干扰。
 *
 * data/tag_library.json 结构：
 * {
 *   "GRE": {
 *     "knowledge_points": ["逻辑关系词", "Text Completion 双空逻辑", ...],
 *     "subtypes": ["Text Completion", "Sentence Equivalence", ...],
 *     "last_used": { "逻辑关系词": "2026-03-19", ... }
 *   },
 *   "雅思": { ... }
 * }
 */

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const LIB_PATH = path.join(
  os.homedir(),
  '.openclaw/skills/shiyi/data/tag_library.json'
);

function loadLib() {
  try { return JSON.parse(fs.readFileSync(LIB_PATH, 'utf-8')); }
  catch (_) { return {}; }
}

function saveLib(lib) {
  const dir = path.dirname(LIB_PATH);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(LIB_PATH, JSON.stringify(lib, null, 2), 'utf-8');
}

// ─── 查：识别前拼进 prompt ────────────────────────────────────

/**
 * 取某考试最近 30 天用过的标签，注入到识别 prompt。
 * 超出 30 天的冷门标签不传，避免 prompt 过长。
 *
 * @param {string} examKey
 * @returns {string}  格式化后的标签提示段落，直接拼进 prompt
 */
function getTagsForPrompt(examKey) {
  const lib     = loadLib();
  const entry   = lib[examKey];
  if (!entry) return '';

  const cutoff  = new Date(Date.now() - 30 * 86400000).toISOString().slice(0, 10);
  const lastUsed = entry.last_used || {};

  const recentKP = (entry.knowledge_points || [])
    .filter(t => (lastUsed[t] ?? '2000-01-01') >= cutoff)
    .slice(-40);  // 最多40个，避免 prompt 爆长

  const recentST = (entry.subtypes || []).slice(-20);

  if (!recentKP.length && !recentST.length) return '';

  const lines = ['已有标签（优先复用，找不到合适的再新建）：'];
  if (recentST.length) lines.push(`  题型：${recentST.join(' / ')}`);
  if (recentKP.length) lines.push(`  知识点：${recentKP.join(' / ')}`);
  return lines.join('\n');
}

// ─── 写：识别后追加新标签 ─────────────────────────────────────

/**
 * 把本次识别出的标签追加进词库（去重）。
 * @param {string} examKey
 * @param {{ question_type?: string, knowledge_point?: string }} result
 */
function updateTagLibrary(examKey, result) {
  const lib   = loadLib();
  const today = new Date().toISOString().slice(0, 10);

  if (!lib[examKey]) {
    lib[examKey] = { knowledge_points: [], subtypes: [], last_used: {} };
  }
  const entry = lib[examKey];

  function addTag(arr, tag) {
    if (!tag || typeof tag !== 'string') return;
    const t = tag.trim();
    if (!t) return;
    if (!arr.includes(t)) arr.push(t);
    entry.last_used[t] = today;
  }

  addTag(entry.subtypes,          result.question_type);
  addTag(entry.knowledge_points,  result.knowledge_point);

  // 防止无限膨胀：每类最多保留 200 个，删最旧的
  if (entry.knowledge_points.length > 200) {
    const sorted = entry.knowledge_points
      .sort((a, b) => (entry.last_used[a] ?? '') < (entry.last_used[b] ?? '') ? -1 : 1);
    entry.knowledge_points = sorted.slice(-200);
  }
  if (entry.subtypes.length > 50) {
    entry.subtypes = entry.subtypes.slice(-50);
  }

  saveLib(lib);
}

// ─── 统计：高频错误标签 Top N ─────────────────────────────────

/**
 * 从 wrong_questions.json 里统计某考试的高频错误知识点。
 * @param {string} examKey
 * @param {object[]} questions  wrong_questions.json 的内容
 * @param {number} topN
 * @returns {{ tag: string, count: number }[]}
 */
function getTopTags(examKey, questions, topN = 5) {
  const freq = {};
  questions
    .filter(q => q.exam === examKey)
    .forEach(q => {
      if (q.knowledge_point) {
        freq[q.knowledge_point] = (freq[q.knowledge_point] || 0) + 1;
      }
    });

  return Object.entries(freq)
    .sort(([, a], [, b]) => b - a)
    .slice(0, topN)
    .map(([tag, count]) => ({ tag, count }));
}

module.exports = { getTagsForPrompt, updateTagLibrary, getTopTags };
