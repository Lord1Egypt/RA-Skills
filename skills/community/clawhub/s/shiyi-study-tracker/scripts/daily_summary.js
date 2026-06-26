/**
 * daily_summary.js
 * 每天 21:00 cron 触发，发当日总结。
 */

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const DATA_DIR = path.join(os.homedir(), '.openclaw/skills/shiyi/data');

function loadJson(p, fb) {
  try { return JSON.parse(fs.readFileSync(p, 'utf-8')); } catch (_) { return fb; }
}

function buildSummaryMessage() {
  const today     = new Date().toISOString().slice(0, 10);
  const dailyPath = path.join(DATA_DIR, 'daily', `${today}.json`);
  const cache     = loadJson(path.join(DATA_DIR, 'stats_cache.json'), {});

  if (!fs.existsSync(dailyPath)) {
    return '今天还没打卡，要发一下今天的题目情况吗？（发「跳过」可以记录休息）';
  }

  const daily = loadJson(dailyPath, {});
  if (daily.skip_today) return '今天休息了，记下来了。';

  const wq      = loadJson(path.join(DATA_DIR, 'wrong_questions.json'), []);
  const todayWQ = wq.filter(q => q.date === today);

  if (!todayWQ.length) {
    return '今天的记录有点简略，有空补充一下错题吗？';
  }

  // 按 section 汇总
  const bySection = {};
  todayWQ.forEach(q => {
    const s = q.section || q.exam_name || '未分类';
    bySection[s] = (bySection[s] || 0) + 1;
  });

  const sectionLine = Object.entries(bySection)
    .map(([s, n]) => `${s} ${n}错`)
    .join(' / ');

  // 最高频知识点
  const kpFreq = {};
  todayWQ.forEach(q => {
    if (q.knowledge_point) kpFreq[q.knowledge_point] = (kpFreq[q.knowledge_point] || 0) + 1;
  });
  const topKP = Object.entries(kpFreq).sort(([,a],[,b]) => b-a)[0];

  const streak     = cache.streak || 1;
  const streakLine = streak >= 3 ? `连续打卡第 ${streak} 天` : '今天打卡完成';
  const pending    = wq.filter(q => q.status !== '已掌握').length;

  const lines = [`今日：${sectionLine}`];
  if (topKP) lines.push(`高频考点：${topKP[0]}（${topKP[1]}次）`);
  lines.push(`待二刷 ${pending} 道 · ${streakLine}`);

  return lines.join('\n');
}

if (require.main === module) console.log(buildSummaryMessage());

module.exports = { buildSummaryMessage };
