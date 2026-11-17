const { db } = require('../db');
const { computeStreaks } = require('./streak');

// 直接从 checkins 实时计算 streak（不维护 user_stats 缓存集合，
// 避免「集合缺失」和「缓存不一致」两类坑）
async function fetchStreaks(openid) {
  const res = await db.collection('checkins').where({ openid }).orderBy('date', 'asc').get();
  const rows = res.data.map((c) => ({ date: c.date, done: !c.skipped }));
  return computeStreaks(rows); // { current, longest, total }
}

// 打卡后返回（camelCase，与前端提交接口一致）
async function recomputeStats(openid) {
  const { current, longest, total } = await fetchStreaks(openid);
  return { currentStreak: current, longestStreak: longest, totalDays: total };
}

// 查询读取（snake_case，与 me/排行字段一致）
async function getStats(openid) {
  const { current, longest, total } = await fetchStreaks(openid);
  return { current_streak: current, longest_streak: longest, total_days: total };
}

module.exports = { recomputeStats, getStats };
