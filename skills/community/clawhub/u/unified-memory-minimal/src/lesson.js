/**
 * lesson.js — Lesson System MCP Adapter + Recall Tracking
 * 
 * Thin wrapper around lessons.js storage with added recall tracking.
 * - lessons.json: shared lesson storage (same format as lessons.js)
 * - lesson_access_log.json: tracks recall_count per lesson
 * 
 * MCP tool: memory_lessons (extract/recall/list/stats/delete/touch/candidates)
 */
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WORKSPACE = process.env.OPENCLAW_WORKSPACE_DIR ?? join(process.env.HOME ?? '/root', '.openclaw', 'workspace');
const SKILL_DIR = join(WORKSPACE, 'memory');
const LESSONS_FILE  = join(SKILL_DIR, 'lessons.json');
const ACCESS_FILE   = join(SKILL_DIR, 'lesson_access_log.json');

const LESSON_CANDIDATE_THRESHOLD = 5;
const MAX_LESSONS = 200;
const MAX_BODY_CHARS = 500;
const MAX_TITLE_CHARS = 120;

let lessonsCache = null, accessLogCache = null;

const load = (f, fallback) => {
  if (!existsSync(f)) return fallback;
  try { return JSON.parse(readFileSync(f, 'utf8')); } catch { return fallback; }
};
const save = (f, data) => {
  try { writeFileSync(f, JSON.stringify(data, null, 2), 'utf8'); } catch (e) { console.error('[lesson]', e.message); }
};

// Fixed: lessons.json is {lessons:[],version,lastUpdated}, not plain array
function getLessons() {
  if (lessonsCache !== null) return lessonsCache;
  const store = load(LESSONS_FILE, { lessons: [], version: '1.0', lastUpdated: Date.now() });
  lessonsCache = store.lessons || [];
  return lessonsCache;
}
function putLessons(lessons) {
  lessonsCache = lessons;
  save(LESSONS_FILE, { lessons, version: '1.0', lastUpdated: Date.now() });
}

function getLog() {
  if (accessLogCache !== null) return accessLogCache;
  accessLogCache = load(ACCESS_FILE, {});
  return accessLogCache;
}
function putLog(log) {
  accessLogCache = log;
  save(ACCESS_FILE, log);
}

/** Touch a lesson (increment its recall count) */
export function touchLesson(lessonId) {
  const log = getLog();
  if (!log[lessonId]) {
    log[lessonId] = { recall_count: 1, last_recall: Date.now(), created_at: Date.now() };
  } else {
    log[lessonId].recall_count++;
    log[lessonId].last_recall = Date.now();
  }
  putLog(log);
}

function generateId() {
  return `les_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
}

/** Create or update a lesson */
function upsertLesson(id, fields) {
  const lessons = getLessons();
  const idx = lessons.findIndex(l => l.id === id);
  const updated = { ...fields, id, updated_at: Date.now(), recall_count: idx >= 0 ? (lessons[idx].recall_count ?? 0) : 0 };
  if (idx >= 0) lessons[idx] = updated;
  else lessons.unshift(updated);
  if (lessons.length > MAX_LESSONS) lessons.splice(MAX_LESSONS);
  putLessons(lessons);
  return updated;
}

/** Search lessons by text similarity + recency boost */
export function recallLessons(query, { limit = 5 } = {}) {
  const lessons = getLessons();
  const qWords = new Set(query.toLowerCase().split(/\s+/).filter(w => w.length > 2));
  if (!qWords.size) return lessons.slice(0, limit).map(l => ({ ...l, match_score: 1.0 }));

  const scored = lessons.map(l => {
    const all = new Set([...(l.title || ''), ...(l.text || ''), ...(l.tags || [])].join(' ').toLowerCase().split(/\s+/).filter(w => w.length > 2));
    const inter = [...qWords].filter(w => all.has(w)).length;
    const union = new Set([...qWords, ...all]).size;
    const score = union === 0 ? 0 : inter / union;
    return { ...l, match_score: Math.min(score + Math.log1p(l.recall_count ?? 0) * 0.05, 1.0) };
  });
  return scored.filter(l => l.match_score > 0).sort((a, b) => b.match_score - a.match_score).slice(0, limit);
}

/** Memories recalled >= threshold but no lesson yet */
export function getLessonCandidates() {
  const log = getLog();
  return Object.entries(log)
    .filter(([, e]) => e.recall_count >= LESSON_CANDIDATE_THRESHOLD)
    .map(([memory_id, e]) => ({ memory_id, recall_count: e.recall_count, last_recall: e.last_recall }))
    .sort((a, b) => b.recall_count - a.recall_count);
}

export function lessonStats() {
  const lessons = getLessons(), log = getLog();
  const totalRecalls = Object.values(log).reduce((s, e) => s + (e.recall_count ?? 0), 0);
  const tagCounts = {};
  for (const l of lessons) for (const t of l.tags ?? []) tagCounts[t] = (tagCounts[t] ?? 0) + 1;
  const topTags = Object.entries(tagCounts).sort((a, b) => b[1] - a[1]).slice(0, 10).map(([tag, count]) => ({ tag, count }));
  const rc = lessons.map(l => l.recall_count ?? 0);
  return {
    total_lessons: lessons.length,
    total_recalls: totalRecalls,
    top_tags: topTags,
    lesson_candidates: getLessonCandidates().length,
    by_recall: {
      total: lessons.length,
      never_recalled: rc.filter(c => c === 0).length,
      one_to_five:   rc.filter(c => c >= 1 && c <= 5).length,
      six_to_ten:    rc.filter(c => c >= 6 && c <= 10).length,
      above_ten:     rc.filter(c => c > 10).length,
      total_recalls: totalRecalls,
    },
  };
}

// ===== MCP Tool: memory_lessons =====
export function memoryLessonsTool({ action, memory_id, title, body, tags, query, lesson_id, limit, tag } = {}) {
  try {
    switch (action) {
      case 'extract': {
        if (!title || !body) throw new Error('title and body required');
        const lesson = upsertLesson(generateId(), {
          text: String(body).slice(0, MAX_BODY_CHARS),
          title: String(title).slice(0, MAX_TITLE_CHARS),
          type: 'general',
          tags: Array.isArray(tags) ? tags.slice(0, 20) : [],
          source_memory: memory_id ?? null,
          created_at: Date.now(),
        });
        return { content: [{ type: 'text', text: JSON.stringify(lesson, null, 2) }] };
      }

      case 'recall': {
        if (!query) throw new Error('query required');
        const results = recallLessons(query, { limit: limit ?? 5 });
        for (const r of results) touchLesson(r.id);
        return { content: [{ type: 'text', text: JSON.stringify({ count: results.length, lessons: results }, null, 2) }] };
      }

      case 'list': {
        const all = getLessons();
        const filtered = tag ? all.filter(l => l.tags?.includes(tag)) : all;
        return { content: [{ type: 'text', text: JSON.stringify({ count: filtered.length, lessons: filtered.slice(0, limit ?? 50) }, null, 2) }] };
      }

      case 'stats':
        return { content: [{ type: 'text', text: JSON.stringify({ ...lessonStats(), top_candidates: getLessonCandidates().slice(0, 5) }, null, 2) }] };

      case 'delete': {
        if (!lesson_id) throw new Error('lesson_id required');
        const lessons2 = getLessons().filter(l => l.id !== lesson_id);
        putLessons(lessons2);
        return { content: [{ type: 'text', text: JSON.stringify({ success: true }, null, 2) }] };
      }

      case 'touch': {
        if (!lesson_id) throw new Error('lesson_id required');
        touchLesson(lesson_id);
        return { content: [{ type: 'text', text: JSON.stringify({ success: true }, null, 2) }] };
      }

      case 'candidates':
        return { content: [{ type: 'text', text: JSON.stringify({ count: getLessonCandidates().length, candidates: getLessonCandidates() }, null, 2) }] };

      default:
        return { content: [{ type: 'text', text: JSON.stringify({ error: `Unknown action: ${action}`, hint: 'extract/recall/list/stats/delete/touch/candidates' }, null, 2) }], isError: true };
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
}
