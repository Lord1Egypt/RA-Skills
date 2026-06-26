/**
 * review_reminder.js
 * 隔天 20:00 cron 触发，随机抽3道待二刷题，让用户自评。
 * 连续答对2次自动标为"已掌握"。
 */

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const DATA_DIR    = path.join(os.homedir(), '.openclaw/skills/shiyi/data');
const WQ_PATH     = path.join(DATA_DIR, 'wrong_questions.json');
const STATE_PATH  = path.join(DATA_DIR, 'review_state.json');
const SESSION_PATH = path.join(DATA_DIR, 'review_session.json');

function loadJson(p, fb) {
  try { return JSON.parse(fs.readFileSync(p, 'utf-8')); } catch (_) { return fb; }
}
function saveJson(p, data) {
  const dir = path.dirname(p);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(p, JSON.stringify(data, null, 2), 'utf-8');
}

function pickQuestions(n = 3) {
  if (!fs.existsSync(WQ_PATH)) return [];
  const questions = loadJson(WQ_PATH, []);
  const state     = loadJson(STATE_PATH, {});
  const pending   = questions.filter(q => q.status !== '已掌握');
  if (!pending.length) return [];

  pending.sort((a, b) => {
    const ta = state[a.id]?.last_reviewed ?? '2000-01-01';
    const tb = state[b.id]?.last_reviewed ?? '2000-01-01';
    return ta.localeCompare(tb);
  });

  const pool = pending.slice(0, Math.min(n * 2, pending.length));
  const picked = [], used = new Set();
  while (picked.length < n && picked.length < pool.length) {
    const idx = Math.floor(Math.random() * pool.length);
    if (!used.has(idx)) { used.add(idx); picked.push(pool[idx]); }
  }
  return picked;
}

function formatQuestion(q) {
  const lines = [];
  const label = [q.section, q.question_type].filter(Boolean).join(' · ');
  if (label) lines.push(`[${label}]`);
  if (q.knowledge_point) lines.push(`考点：${q.knowledge_point}`);
  if (q.question_text) lines.push(q.question_text.slice(0, 200));
  if (q.visual_description) lines.push(`图形：${q.visual_description.slice(0, 120)}`);
  if (q.answer) lines.push(`答案：${q.answer}`);
  return lines.join('\n');
}

function buildReminderMessage() {
  const questions = pickQuestions(3);
  if (!questions.length) return '待二刷的题都清空了，今天不用复习，去刷新题吧。';

  const session = {
    date:      new Date().toISOString().slice(0, 10),
    questions: questions.map(q => q.id),
    current:   0,
    answers:   {},
  };
  saveJson(SESSION_PATH, session);

  const first = questions[0];
  return [
    `二刷时间，抽到 ${questions.length} 道待复习的题。`,
    '',
    `第 1 / ${questions.length} 道：`,
    formatQuestion(first),
    '',
    '还记得这题的解法吗？回复 记得 或 不记得',
  ].join('\n');
}

function handleReviewReply(userText) {
  if (!fs.existsSync(SESSION_PATH)) return null;
  const session = loadJson(SESSION_PATH, null);
  if (!session || session.current >= session.questions.length) return null;

  const text       = (userText || '').trim();
  const isRemember = /记得|会了|掌握|对|知道/.test(text);
  const isForget   = /不记得|忘了|不会|错了|不对|不知道/.test(text);
  if (!isRemember && !isForget) return null;

  const currentId = session.questions[session.current];
  if (!session.answers[currentId]) session.answers[currentId] = [];
  session.answers[currentId].push(isRemember ? '记得' : '不记得');

  const state = loadJson(STATE_PATH, {});
  if (!state[currentId]) state[currentId] = { correct_streak: 0, total: 0 };
  state[currentId].last_reviewed = new Date().toISOString().slice(0, 10);
  state[currentId].total += 1;
  state[currentId].correct_streak = isRemember
    ? (state[currentId].correct_streak || 0) + 1
    : 0;
  saveJson(STATE_PATH, state);

  const mastered = state[currentId].correct_streak >= 2;
  if (mastered) {
    const questions = loadJson(WQ_PATH, []);
    const q = questions.find(q => q.id === currentId);
    if (q) q.status = '已掌握';
    fs.writeFileSync(WQ_PATH, JSON.stringify(questions, null, 2), 'utf-8');
  }

  session.current += 1;
  saveJson(SESSION_PATH, session);

  const feedback = mastered
    ? '已标记为「已掌握」。'
    : isRemember ? '记录了，再答对一次就标为已掌握。'
    : '记下了，下次还会抽到这道。';

  if (session.current >= session.questions.length) {
    const remaining = loadJson(WQ_PATH, []).filter(q => q.status !== '已掌握').length;
    return `${feedback}\n\n本次复习完成，还剩 ${remaining} 道待二刷。`;
  }

  const allQ  = loadJson(WQ_PATH, []);
  const nextQ = allQ.find(q => q.id === session.questions[session.current]);
  if (!nextQ) return `${feedback}\n\n（找不到下一题，本次结束）`;

  return [
    feedback, '',
    `第 ${session.current + 1} / ${session.questions.length} 道：`,
    formatQuestion(nextQ), '',
    '还记得这题的解法吗？回复 记得 或 不记得',
  ].join('\n');
}

if (require.main === module) console.log(buildReminderMessage());

module.exports = { buildReminderMessage, handleReviewReply };
