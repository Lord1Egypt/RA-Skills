/**
 * update_daily.js
 * 写入每日记录和错题，适配自由标签模式。
 */

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const DATA_DIR = path.join(os.homedir(), '.openclaw/skills/shiyi/data');
const WQ_PATH  = path.join(DATA_DIR, 'wrong_questions.json');

function ensureDir(d) { if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true }); }

function loadJson(p, fb) {
  try { return JSON.parse(fs.readFileSync(p, 'utf-8')); } catch (_) { return fb; }
}

// ─── 备份 ─────────────────────────────────────────────────────

function backupWrongQuestions() {
  if (!fs.existsSync(WQ_PATH)) return;
  const backupDir = path.join(DATA_DIR, 'backups');
  ensureDir(backupDir);
  const ts   = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  fs.copyFileSync(WQ_PATH, path.join(backupDir, `wrong_questions.${ts}.json`));

  const all = fs.readdirSync(backupDir).filter(f => f.startsWith('wrong_questions.')).sort().reverse();
  all.slice(10).forEach(f => { try { fs.unlinkSync(path.join(backupDir, f)); } catch (_) {} });
}

// ─── 错题存储 ─────────────────────────────────────────────────

/**
 * 追加一条错题，写入前备份。
 * @param {object} question  来自 parse_input.js 的识别结果
 */
function saveWrongQuestion(question) {
  ensureDir(DATA_DIR);
  backupWrongQuestions();

  const questions = loadJson(WQ_PATH, []);
  const id = `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
  questions.push({ id, ...question });
  fs.writeFileSync(WQ_PATH, JSON.stringify(questions, null, 2), 'utf-8');
  return questions;
}

function updateWrongQuestionStatus(id, status) {
  if (!fs.existsSync(WQ_PATH)) return;
  backupWrongQuestions();
  const questions = loadJson(WQ_PATH, []);
  const q = questions.find(q => q.id === id);
  if (q) q.status = status;
  fs.writeFileSync(WQ_PATH, JSON.stringify(questions, null, 2), 'utf-8');
}

// ─── 每日记录 ─────────────────────────────────────────────────

function updateDailyRecord(parsed) {
  const dailyDir = path.join(DATA_DIR, 'daily');
  ensureDir(dailyDir);

  const date     = parsed.date || new Date().toISOString().slice(0, 10);
  const filePath = path.join(dailyDir, `${date}.json`);
  const existing = loadJson(filePath, {});

  const record = {
    date,
    exam:       parsed.exam      || '_generic',
    exam_name:  parsed.exam_name || '',
    ...existing,
    mood:       parsed.mood      || '中性',
    skip_today: parsed.skip_today || false,
    updated_at: new Date().toISOString(),
  };

  // 累计当日错题数（按考试分组）
  if (!record.wrong_count) record.wrong_count = {};
  const examKey = parsed.exam || '_generic';
  if (parsed.wrong_count) {
    record.wrong_count[examKey] = (record.wrong_count[examKey] || 0) + parsed.wrong_count;
  }

  fs.writeFileSync(filePath, JSON.stringify(record, null, 2), 'utf-8');

  // 更新连续打卡
  updateStreak(date);
  return record;
}

function updateStreak(today) {
  const cachePath = path.join(DATA_DIR, 'stats_cache.json');
  const cache     = loadJson(cachePath, { streak: 0, total_days: 0 });

  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  const yPath = path.join(DATA_DIR, 'daily', `${yesterday.toISOString().slice(0,10)}.json`);

  cache.streak     = fs.existsSync(yPath) ? (cache.streak || 0) + 1 : 1;
  cache.total_days = (cache.total_days || 0) + 1;
  cache.last_updated = today;
  fs.writeFileSync(cachePath, JSON.stringify(cache, null, 2), 'utf-8');
  return cache;
}

function readStatsCache() {
  return loadJson(path.join(DATA_DIR, 'stats_cache.json'), null);
}

module.exports = { saveWrongQuestion, updateWrongQuestionStatus, updateDailyRecord, readStatsCache };
