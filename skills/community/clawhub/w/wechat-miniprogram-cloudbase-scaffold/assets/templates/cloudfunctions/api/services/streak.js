// streak 计算：连续「完成」的天数，向后截断到今天/昨天（昨天截断 = 今天还没做但没断）
// 纯函数，不依赖数据库，可单独单元测试
const MILESTONES = [7, 21, 100];

function todayStr() {
  // 东八区日期，避免 UTC 边界把晚上打卡算到第二天
  const now = new Date(Date.now() + 8 * 3600 * 1000);
  return now.toISOString().slice(0, 10);
}

function shiftDate(dateStr, days) {
  const d = new Date(`${dateStr}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + days);
  return d.toISOString().slice(0, 10);
}

// rows: [{date, done}] 按日期升序；done=true 表示当天完成
function computeStreaks(rows) {
  const okDays = new Set(rows.filter((r) => r.done).map((r) => r.date));
  const today = todayStr();
  const yesterday = shiftDate(today, -1);

  // current：从今天（或昨天）往前数连续 ok 天
  let current = 0;
  let cursor = okDays.has(today) ? today : okDays.has(yesterday) ? yesterday : null;
  while (cursor && okDays.has(cursor)) {
    current += 1;
    cursor = shiftDate(cursor, -1);
  }

  // longest & total：全量扫描
  let longest = 0;
  let run = 0;
  let prev = null;
  for (const d of [...okDays].sort()) {
    run = prev && shiftDate(prev, 1) === d ? run + 1 : 1;
    longest = Math.max(longest, run);
    prev = d;
  }

  return { current, longest: Math.max(longest, current), total: okDays.size };
}

module.exports = { MILESTONES, todayStr, computeStreaks };
