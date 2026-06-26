/**
 * Lessons System v1.0
 * 
 * 从错误、纠正、最佳实践中自动学习。
 * 存储在 memories.json 的 `lessons` 数组中（与普通记忆分开）。
 * 
 * 核心功能：
 * 1. 记录错误模式（error patterns）
 * 2. 记录用户纠正（user corrections）
 * 3. 记录最佳实践（best practices）
 * 4. 语义搜索 lessons（基于 BM25 + 简单关键词）
 * 5. 按类型/主题过滤
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createHash } from 'crypto';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ============ Config ============

const LESSONS_FILE = join(__dirname, '..', '..', '..', 'memory', 'lessons.json');

const LESSON_CONFIG = {
  maxLessons: 500,          // 最多存储 lessons 数量
  dedupWindow: 20,         // 往前比较多少条记忆去重
  similarityThreshold: 0.72, // Jaccard 相似度阈值（超过则认为是重复）
  autoTag: true,
};

// Lesson types
const LESSON_TYPES = {
  ERROR: 'error',           // 命令/工具/代码错误
  CORRECTION: 'correction', // 用户纠正（"不对，应该是..."）
  BEST_PRACTICE: 'best_practice', // 发现的最佳实践
  PITFALL: 'pitfall',       // 踩坑记录
  PATTERN: 'pattern',       // 发现的模式
  TOOL_CHANGE: 'tool_change', // 工具/API 变化
};

// ============ Storage ============

function getLessonsStore() {
  if (!existsSync(LESSONS_FILE)) {
    return { lessons: [], version: '1.0', lastUpdated: Date.now() };
  }
  try {
    return JSON.parse(readFileSync(LESSONS_FILE, 'utf-8'));
  } catch {
    return { lessons: [], version: '1.0', lastUpdated: Date.now() };
  }
}

function saveLessonsStore(store) {
  try {
    const dir = join(__dirname, '..', '..', 'memory');
    mkdirSync(dir, { recursive: true });
    writeFileSync(LESSONS_FILE, JSON.stringify(store, null, 2), 'utf-8');
  } catch (e) {
    console.warn('[lessons] save failed:', e.message);
  }
}

// ============ Recall Tracking (lesson_access_log.json) ============

const ACCESS_FILE = join(__dirname, '..', '..', '..', 'memory', 'lesson_access_log.json');
let accessLogCache = null;

function getAccessLog() {
  if (accessLogCache !== null) return accessLogCache;
  if (!existsSync(ACCESS_FILE)) { accessLogCache = {}; return accessLogCache; }
  try { accessLogCache = JSON.parse(readFileSync(ACCESS_FILE, 'utf-8')); } catch { accessLogCache = {}; }
  return accessLogCache;
}
function saveAccessLog(log) {
  accessLogCache = log;
  try { writeFileSync(ACCESS_FILE, JSON.stringify(log, null, 2), 'utf-8'); } catch (e) { console.warn('[lessons] access log save failed:', e.message); }
}

/** Increment recall count for a lesson (call when lesson is retrieved) */
export function touchLesson(lessonId) {
  const log = getAccessLog();
  const now = Date.now();
  if (!log[lessonId]) log[lessonId] = { recall_count: 0, last_recall: 0, created_at: now };
  log[lessonId].recall_count++;
  log[lessonId].last_recall = now;
  saveAccessLog(log);
}

/** Memories recalled >= 5x but not yet turned into a lesson */
export function getLessonCandidates() {
  // Cross-ref access log with lessons — memories recalled often but no lesson yet
  // For now return recall stats per lesson ID
  const log = getAccessLog();
  const store = getLessonsStore();
  const lessonIds = new Set(store.lessons.map(l => l.id));
  return Object.entries(log)
    .filter(([id]) => !lessonIds.has(id) && log[id].recall_count >= 5)
    .map(([memory_id, e]) => ({ memory_id, recall_count: e.recall_count, last_recall: e.last_recall }))
    .sort((a, b) => b.recall_count - a.recall_count);
}

// ============ Core Utilities ============

function jaccardSimilarity(a, b) {
  if (!a || !b) return 0;
  const setA = new Set(a.toLowerCase().split(/\s+/).filter(Boolean));
  const setB = new Set(b.toLowerCase().split(/\s+/).filter(Boolean));
  const intersection = [...setA].filter(x => setB.has(x));
  const union = new Set([...setA, ...setB]);
  return union.size === 0 ? 0 : intersection.length / union.size;
}

function tokenize(text) {
  if (!text) return [];
  return text.toLowerCase()
    .replace(/[^\w\u4e00-\u9fff\s]/g, ' ')
    .split(/\s+/)
    .filter(t => t.length >= 2);
}

function hashText(text) {
  return createHash('sha256').update(text).digest('hex').slice(0, 16);
}

/**
 * Detect if text contains a user correction pattern
 */
function isCorrection(text) {
  const patterns = [
    /^不对/,
    /不对[:：]/,
    /错了/,
    /错误[:：]/,
    /应该[:：]/,
    /不是[:：]/,
    /改用/,
    /要用/,
    /要用的是/,
    /不对，我之前/,
    /我说的是/,
    /看清楚[:：]/,
    /错了，要/,
    /\bWRONG\b/i,
    /\bincorrect\b/i,
    /\bnot right\b/i,
    /这是错的/,
    /不对，应该是/,
  ];
  return patterns.some(p => p.test(text.trim()));
}

/**
 * Detect if text describes an error
 */
function isError(text) {
  const patterns = [
    /error|exception|failed|failure/i,
    /错误|异常|失败/i,
    /\bError\b|\bException\b/i,
    /command.*fail|工具.*失败/i,
    /SyntaxError|ReferenceError|TypeError|RuntimeError/i,
    /permission denied|no such file|not found/i,
    /找不到|权限|不存在|报错/i,
  ];
  return patterns.some(p => p.test(text));
}

/**
 * Detect if text describes a best practice
 */
function isBestPractice(text) {
  const patterns = [
    /better.*approach|better.*way|best practice|recommended/i,
    /更好的|最佳实践|推荐|建议使用|应该用/,
    /更优|更高效|更简洁|更好/i,
    /\bTIP\b|\bPRO TIP\b/i,
    /\bPro tip\b/i,
  ];
  return patterns.some(p => p.test(text));
}

/**
 * Detect if text describes a pitfall
 */
function isPitfall(text) {
  const patterns = [
    /\bwatch out\b|\bcaution\b|\bcareful\b|\btrap\b/i,
    /小心|注意|陷阱|坑|别/,
    /不要.*会|避免.*问题/i,
    /容易出错|经常踩坑|新手容易/,
    /\bDONT\b|\bAVOID\b/i,
  ];
  return patterns.some(p => p.test(text));
}

/**
 * Auto-detect lesson type from text content
 */
function detectLessonType(text) {
  if (isCorrection(text)) return LESSON_TYPES.CORRECTION;
  if (isPitfall(text)) return LESSON_TYPES.PITFALL;
  if (isBestPractice(text)) return LESSON_TYPES.BEST_PRACTICE;
  if (isError(text)) return LESSON_TYPES.ERROR;
  return LESSON_TYPES.PATTERN;
}

/**
 * Extract the "wrong" and "correct" parts from a correction
 */
function extractCorrectionPair(text) {
  const patterns = [
    /(不对|错了|应该)[:：]?\s*(.+)/i,
    /不是[:：]\s*(.+)\s*，?\s*(?:而?是|应该|要用)[:：]\s*(.+)/i,
    /(wrong|incorrect|not)[:：]\s*(.+)/i,
  ];
  
  for (const p of patterns) {
    const match = text.match(p);
    if (match) {
      return { wrong: match[2] || match[1], correct: match[3] || '' };
    }
  }
  return { wrong: text, correct: '' };
}

// ============ Lesson Storage ============

/**
 * Add a lesson to the store
 * @param {object} lesson - { text, type, wrong?, correct?, context?, tags?, importance? }
 * @returns {object|null} - the stored lesson or null if duplicate
 */
export function addLesson(lesson) {
  const store = getLessonsStore();
  const now = Date.now();
  const text = lesson.text?.trim();
  
  if (!text || text.length < 5) return null;
  
  // Deduplication: check against recent lessons
  const recent = store.lessons.slice(-LESSON_CONFIG.dedupWindow);
  for (const existing of recent) {
    const sim = jaccardSimilarity(text, existing.text);
    if (sim > LESSON_CONFIG.similarityThreshold) {
      // Update access stats on duplicate
      existing.last_access = now;
      existing.access_count = (existing.access_count || 0) + 1;
      saveLessonsStore(store);
      return null;
    }
  }
  
  const newLesson = {
    id: `les_${now}_${hashText(text).slice(0, 6)}`,
    text,
    type: lesson.type || detectLessonType(text),
    wrong: lesson.wrong || null,
    correct: lesson.correct || null,
    context: lesson.context || null,
    tags: lesson.tags || [],
    importance: lesson.importance ?? 0.75,
    created_at: now,
    updated_at: now,
    last_access: now,
    access_count: 1,
    version: '1.0',
  };
  
  store.lessons.push(newLesson);
  
  // Trim if over max
  if (store.lessons.length > LESSON_CONFIG.maxLessons) {
    store.lessons = store.lessons.slice(-LESSON_CONFIG.maxLessons);
  }
  
  store.lastUpdated = now;
  saveLessonsStore(store);
  
  console.log(`[lessons] Added: [${newLesson.type}] "${text.slice(0,40)}..."`);
  return newLesson;
}

/**
 * Add a lesson by type automatically detected
 * @param {string} text - lesson content
 * @param {object} options - { wrong?, correct?, context?, tags?, importance? }
 */
export function storeLesson(text, options = {}) {
  return addLesson({ text, ...options });
}

/**
 * Add an error lesson
 */
export function storeError(errorText, fix = null, context = null) {
  return addLesson({
    text: errorText,
    type: LESSON_TYPES.ERROR,
    correct: fix,
    context,
  });
}

/**
 * Add a user correction lesson
 */
export function storeCorrection(wrong, correct, context = null) {
  return addLesson({
    text: `纠正: ${wrong} → ${correct}`,
    type: LESSON_TYPES.CORRECTION,
    wrong,
    correct,
    context,
    importance: 0.9, // corrections are high importance
  });
}

/**
 * Add a best practice lesson
 */
export function storeBestPractice(practice, context = null) {
  return addLesson({
    text: practice,
    type: LESSON_TYPES.BEST_PRACTICE,
    context,
    importance: 0.8,
  });
}

/**
 * Add a pitfall lesson
 */
export function storePitfall(pitfall, solution = null, context = null) {
  return addLesson({
    text: pitfall,
    type: LESSON_TYPES.PITFALL,
    correct: solution,
    context,
    importance: 0.85,
  });
}

// ============ Lesson Search ============

/**
 * Simple keyword + pattern search for lessons
 * @param {string} query
 * @param {object} options - { type?, topK?, includeWrong? }
 * @returns {Array}
 */
export function searchLessons(query, options = {}) {
  const { type, topK = 5, includeWrong = false } = options;
  
  const store = getLessonsStore();
  let lessons = store.lessons;
  
  // Filter by type if specified
  if (type && LESSON_TYPES[type]) {
    lessons = lessons.filter(l => l.type === type);
  }
  
  if (!query || query.trim().length === 0) {
    // Return recent lessons
    return lessons
      .sort((a, b) => b.created_at - a.created_at)
      .slice(0, topK);
  }
  
  const queryTokens = tokenize(query);
  const scored = lessons.map(lesson => {
    const text = includeWrong && lesson.wrong
      ? `${lesson.text} ${lesson.wrong} ${lesson.correct || ''}`
      : lesson.text;
    const lessonTokens = tokenize(text);
    
    // Simple overlap scoring
    const overlap = queryTokens.filter(t => lessonTokens.includes(t)).length;
    const bonus = lessonTokens.some(t => queryTokens.includes(t)) ? 0.1 : 0;
    const importanceBonus = (lesson.importance || 0.5) * 0.2;
    
    return {
      ...lesson,
      score: overlap + bonus + importanceBonus,
    };
  });
  
  const results = scored
    .filter(l => l.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);

  // Track each lesson recall
  for (const lesson of results) touchLesson(lesson.id);

  return results;
}

/**
 * Get recent lessons by type
 */
export function getRecentLessons(type = null, limit = 5) {
  const store = getLessonsStore();
  let lessons = store.lessons;
  if (type && LESSON_TYPES[type]) {
    lessons = lessons.filter(l => l.type === type);
  }
  return lessons
    .sort((a, b) => b.created_at - a.created_at)
    .slice(0, limit);
}

/**
 * Get lesson statistics (now includes recall tracking from access log)
 */
export function getLessonStats() {
  const store = getLessonsStore();
  const log = getAccessLog();
  const totalRecalls = Object.values(log).reduce((s, e) => s + (e.recall_count ?? 0), 0);
  const byType = {};
  for (const type of Object.values(LESSON_TYPES)) {
    byType[type] = store.lessons.filter(l => l.type === type).length;
  }
  const rc = store.lessons.map(l => log[l.id]?.recall_count ?? 0);
  return {
    total: store.lessons.length,
    total_recalls: totalRecalls,
    byType,
    by_recall: {
      never_recalled: rc.filter(c => c === 0).length,
      one_to_five:    rc.filter(c => c >= 1 && c <= 5).length,
      six_to_ten:     rc.filter(c => c >= 6 && c <= 10).length,
      above_ten:      rc.filter(c => c > 10).length,
    },
    lesson_candidates: getLessonCandidates().length,
    lastUpdated: store.lastUpdated,
  };
}

/**
 * Clear all lessons (for testing)
 */
export function clearLessons() {
  const store = { lessons: [], version: '1.0', lastUpdated: Date.now() };
  saveLessonsStore(store);
  return true;
}

/**
 * Format a lesson for injection into prompt
 */
export function formatLessonForPrompt(lesson) {
  const lines = [`[${lesson.type}] ${lesson.text}`];
  if (lesson.correct) {
    lines.push(`  ✓ ${lesson.correct}`);
  }
  if (lesson.wrong) {
    lines.push(`  ✗ ${lesson.wrong}`);
  }
  if (lesson.context) {
    lines.push(`  → ${lesson.context}`);
  }
  return lines.join('\n');
}

/**
 * Format multiple lessons for prompt injection
 */
export function formatLessonsForPrompt(lessons) {
  if (lessons.length === 0) return '';
  const formatted = lessons.map(l => `  - ${formatLessonForPrompt(l)}`).join('\n');
  return `\n[Relevant Lessons - avoid repeating past mistakes]\n${formatted}\n[/Lessons]\n`;
}

// ============ Lesson Detection (for hook integration) ============

/**
 * Detect and auto-capture lessons from a message
 * Returns detected lessons (doesn't auto-store to avoid noise)
 */
export function detectLessons(text) {
  const detections = [];
  
  // Check for correction patterns
  if (isCorrection(text)) {
    const pair = extractCorrectionPair(text);
    detections.push({
      type: LESSON_TYPES.CORRECTION,
      text,
      wrong: pair.wrong,
      correct: pair.correct,
      auto: true,
    });
  }
  
  // Check for error patterns
  if (isError(text)) {
    detections.push({
      type: LESSON_TYPES.ERROR,
      text,
      auto: true,
    });
  }
  
  // Check for best practice
  if (isBestPractice(text)) {
    detections.push({
      type: LESSON_TYPES.BEST_PRACTICE,
      text,
      auto: true,
    });
  }
  
  // Check for pitfall
  if (isPitfall(text)) {
    detections.push({
      type: LESSON_TYPES.PITFALL,
      text,
      auto: true,
    });
  }
  
  return detections;
}

// ============ QMD Integration ============

/**
 * Search local documents via QMD CLI
 * @param {string} query
 * @param {number} topK
 * @returns {Array} - { path, snippet, score }
 */
export async function searchDocuments(query, topK = 3) {
  try {
    const { execSync } = await import('child_process');
    
    // Use qmd search (BM25 only, no embedding needed)
    const result = execSync(
      `qmd search "${query.replace(/"/g, '\\"')}" --limit ${topK} 2>/dev/null`,
      { encoding: 'utf-8', timeout: 10000 }
    );
    
    const lines = result.split('\n').filter(l => l.trim() && !l.startsWith('Warning'));
    
    return lines.slice(0, topK).map(line => {
      // Try to extract path and snippet from qmd output
      const pathMatch = line.match(/^\[(.+?)\]|(https?:\/\/\S+)|(\/.+?):/);
      const path = pathMatch ? (pathMatch[1] || pathMatch[2] || pathMatch[3] || line.split(':')[0]) : line.split(':')[0];
      const snippet = line.includes(':') ? line.split(':').slice(1).join(':').trim() : line;
      
      return {
        path: path.slice(0, 100),
        snippet: snippet.slice(0, 150),
        score: 1.0,
      };
    }).filter(r => r.path);
  } catch (e) {
    // QMD not available or failed
    return [];
  }
}

/**
 * Search QMD with embeddings (hybrid search)
 * Falls back to BM25-only if embeddings not ready
 */
export async function searchDocumentsHybrid(query, topK = 3) {
  try {
    const { execSync } = await import('child_process');
    
    const result = execSync(
      `qmd query "${query.replace(/"/g, '\\"')}" --limit ${topK} 2>/dev/null`,
      { encoding: 'utf-8', timeout: 15000 }
    );
    
    const lines = result.split('\n').filter(l => l.trim() && !l.startsWith('Warning'));
    
    return lines.slice(0, topK).map(line => {
      const pathMatch = line.match(/^\[(.+?)\]|(https?:\/\/\S+)|(\/.+?):/);
      const path = pathMatch ? (pathMatch[1] || pathMatch[2] || pathMatch[3] || line.split(':')[0]) : line.split(':')[0];
      const snippet = line.includes(':') ? line.split(':').slice(1).join(':').trim() : line;
      
      return {
        path: path.slice(0, 100),
        snippet: snippet.slice(0, 150),
        score: 1.0,
      };
    }).filter(r => r.path);
  } catch {
    // Fallback to BM25 search
    return searchDocuments(query, topK);
  }
}

export {
  LESSON_TYPES,
  LESSON_CONFIG,
  isCorrection,
  isError,
  isBestPractice,
  isPitfall,
  detectLessonType,
};
