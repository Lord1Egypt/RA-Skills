#!/usr/bin/env node
/**
 * Session Tracker - Cross-Session Usage Analytics
 *
 * Sessions 日志是唯一真相源；daily/weekly 报告均由 sessions 派生聚合。
 * 费用按币种分组，绝不跨币种相加。
 *
 * Security Notice:
 * - All data stored locally in .data/
 * - No session content stored, only usage metrics
 * - No external data transmission
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = process.env.TOKEN_MANAGER_DATA_DIR || path.join(__dirname, '..', '.data');
const SESSION_FILE = path.join(DATA_DIR, 'sessions.json');

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Load session data
function loadSessions() {
  try {
    if (fs.existsSync(SESSION_FILE)) {
      return JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    }
  } catch (e) {}
  return { sessions: [], providers: {} };
}

function saveSessions(data) {
  fs.writeFileSync(SESSION_FILE, JSON.stringify(data, null, 2));
}

function addCost(costs, currency, amount) {
  const c = currency || 'CNY';
  costs[c] = (costs[c] || 0) + (amount || 0);
}

// Record a new session（只追加原始日志；报告由聚合函数派生）
function recordSession(sessionData) {
  const data = loadSessions();
  const now = new Date();
  const dateKey = now.toISOString().split('T')[0];

  const session = {
    id: `session_${now.getTime()}`,
    timestamp: now.toISOString(),
    date: dateKey,
    provider: sessionData.provider || 'unknown',
    model: sessionData.model || 'unknown',
    tokensIn: sessionData.tokensIn || 0,
    tokensOut: sessionData.tokensOut || 0,
    cost: sessionData.cost || 0,
    currency: sessionData.currency || 'CNY',
    duration: sessionData.duration || 0 // minutes
  };

  data.sessions.push(session);

  // Cleanup old sessions (keep 90 days)
  const ninetyDaysAgo = now.getTime() - 90 * 86400000;
  data.sessions = data.sessions.filter(s => new Date(s.timestamp).getTime() > ninetyDaysAgo);

  // 旧版本遗留的 daily 增量聚合已废弃（报告改为实时派生），顺带清理
  delete data.daily;

  saveSessions(data);
  return session;
}

function aggregate(sessions) {
  const result = { totalTokens: 0, totalCost: {}, sessionCount: sessions.length, providers: {} };
  for (const s of sessions) {
    result.totalTokens += s.tokensIn + s.tokensOut;
    addCost(result.totalCost, s.currency, s.cost);
    const p = result.providers[s.provider] = result.providers[s.provider] || { tokens: 0, totalCost: {} };
    p.tokens += s.tokensIn + s.tokensOut;
    addCost(p.totalCost, s.currency, s.cost);
  }
  return result;
}

// Generate daily report
function generateDailyReport(date = null) {
  const data = loadSessions();
  const targetDate = date || new Date().toISOString().split('T')[0];

  const daySessions = data.sessions.filter(s => s.date === targetDate);
  if (daySessions.length === 0) {
    return { success: false, error: `No data for ${targetDate}` };
  }

  return {
    success: true,
    date: targetDate,
    summary: aggregate(daySessions)
  };
}

// Generate weekly report
function generateWeeklyReport() {
  const data = loadSessions();
  const weekAgo = Date.now() - 7 * 86400000;

  const weekSessions = data.sessions.filter(s => new Date(s.timestamp).getTime() > weekAgo);
  if (weekSessions.length === 0) {
    return { success: false, error: 'No sessions in the last 7 days' };
  }

  return {
    success: true,
    period: 'Last 7 days',
    summary: aggregate(weekSessions),
    trend: calculateTrend(data.sessions)
  };
}

// Calculate cost trend：按币种分别计算，避免跨币种混算；全零成本时稳定返回 stable（无 NaN）
function calculateTrend(sessions) {
  const byDate = {};
  for (const s of sessions) {
    byDate[s.date] = byDate[s.date] || {};
    const c = s.currency || 'CNY';
    byDate[s.date][c] = (byDate[s.date][c] || 0) + (s.cost || 0);
  }
  const dates = Object.keys(byDate).sort().slice(-7);
  if (dates.length < 2) return null;

  const currencies = [...new Set(dates.flatMap(d => Object.keys(byDate[d])))];
  const trend = {};
  for (const c of currencies) {
    const series = dates.map(d => byDate[d][c] || 0);
    const n = Math.min(3, dates.length);
    const firstAvg = series.slice(0, 3).reduce((a, b) => a + b, 0) / n;
    const lastAvg = series.slice(-3).reduce((a, b) => a + b, 0) / n;
    const change = firstAvg === 0 ? 0 : ((lastAvg - firstAvg) / firstAvg) * 100;
    trend[c] = {
      direction: change > 1 ? 'up' : change < -1 ? 'down' : 'stable',
      changePercent: Math.abs(change).toFixed(1),
      avgDailyCost: (series.reduce((a, b) => a + b, 0) / dates.length).toFixed(4)
    };
  }
  return trend;
}

// Get top recommendations based on history
function getRecommendations() {
  const data = loadSessions();
  const weekAgo = Date.now() - 7 * 86400000;
  const weekSessions = data.sessions.filter(s => new Date(s.timestamp).getTime() > weekAgo);

  const recommendations = [];

  if (weekSessions.length === 0) {
    return { success: true, recommendations: [] };
  }

  // Check for high-cost patterns（按各币种各自的阈值判断）
  const highCostSessions = weekSessions.filter(s => s.cost > (s.currency === 'USD' ? 0.15 : 1));
  if (highCostSessions.length > 3) {
    recommendations.push({
      priority: 'high',
      en: 'Multiple high-cost sessions detected. Consider using sub-agents or disabling reasoning for simpler tasks.',
      cn: '检测到多个高成本会话。建议对简单任务使用子代理或关闭推理。',
      action: 'optimize_large_sessions'
    });
  }

  // Check for expensive models（现行旗舰/高价模型）
  const expensiveModels = weekSessions.filter(s =>
    /opus|fable|terra-pro|sol-pro|argon/.test(s.model) ||
    (s.model.includes('k3.1-pro') && !s.model.includes('highspeed'))
  );
  if (expensiveModels.length > 5) {
    recommendations.push({
      priority: 'medium',
      en: 'Frequent use of premium models. Consider cheaper alternatives (Claude Sonnet/Haiku, GPT-6.1 Terra, kimi-k3.1-pro-highspeed, DeepSeek Flash) for non-critical tasks.',
      cn: '频繁使用高级模型。对非关键任务考虑更便宜的替代（Claude Sonnet/Haiku、GPT-6.1 Terra、kimi-k3.1-pro-highspeed、DeepSeek Flash）。',
      action: 'consider_cheaper_models'
    });
  }

  // Check daily spend（分币种检查：CNY > ¥10 / USD > $2 视为超标）
  const today = new Date().toISOString().split('T')[0];
  const todayAgg = aggregate(data.sessions.filter(s => s.date === today));
  for (const [currency, amount] of Object.entries(todayAgg.totalCost)) {
    const limit = currency === 'USD' ? 2 : 10;
    if (amount > limit) {
      const symbol = currency === 'USD' ? '$' : '¥';
      recommendations.push({
        priority: 'high',
        en: `Daily spending ${symbol}${amount.toFixed(2)} exceeds the ${currency} limit. Consider enabling strict save mode.`,
        cn: `今日 ${currency} 花费 ${symbol}${amount.toFixed(2)} 超过阈值。建议开启严格省钱模式。`,
        action: 'enable_save_mode'
      });
    }
  }

  return {
    success: true,
    basedOn: `${weekSessions.length} sessions in last 7 days`,
    recommendations: recommendations
  };
}

// CLI mode
function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'record':
      // record <provider> <model> <tokensIn> <tokensOut> <cost> [currency]
      const session = recordSession({
        provider: args[1],
        model: args[2],
        tokensIn: parseInt(args[3]) || 0,
        tokensOut: parseInt(args[4]) || 0,
        cost: parseFloat(args[5]) || 0,
        currency: args[6] || 'CNY'
      });
      console.log(JSON.stringify({ success: true, session }, null, 2));
      break;

    case 'daily':
      console.log(JSON.stringify(generateDailyReport(args[1]), null, 2));
      break;

    case 'weekly':
      console.log(JSON.stringify(generateWeeklyReport(), null, 2));
      break;

    case 'recommend':
      console.log(JSON.stringify(getRecommendations(), null, 2));
      break;

    default:
      console.log(JSON.stringify({
        usage: 'node session-tracker.js <command> [args]',
        commands: {
          record: 'Record a session (provider model tokensIn tokensOut cost currency)',
          daily: 'Generate daily report [date]',
          weekly: 'Generate weekly report',
          recommend: 'Get usage recommendations'
        }
      }, null, 2));
  }
}

module.exports = {
  recordSession,
  generateDailyReport,
  generateWeeklyReport,
  calculateTrend,
  getRecommendations,
  loadSessions
};

if (require.main === module) {
  main();
}
