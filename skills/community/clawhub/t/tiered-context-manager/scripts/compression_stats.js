/**
 * Compression Analysis & Statistics Module v2.0
 * 
 * Tracks compression effectiveness and generates reports:
 * 1. Record each compression's effect
 * 2. Calculate tokens saved
 * 3. Generate compression reports
 */

const fs = require("fs");
const path = require("path");
const os = require("os");

// Paths
const REPORTS_DIR = "E:\\zhuazhua\\.openclaw\\.openclaw\\workspace\\reports";
const STATS_DIR = "E:\\zhuazhua\\.openclaw\\.openclaw\\workspace\\plugins\\tiered-compactor";
const STATS_FILE = path.join(STATS_DIR, "compression_stats.json");
const DAILY_STATS_FILE = path.join(STATS_DIR, "daily_stats.json");

// Statistics structure
const EMPTY_STATS = {
  // Overall stats
  totalCompactions: 0,
  totalTokensBefore: 0,
  totalTokensAfter: 0,
  totalTokensSaved: 0,
  
  // By level
  byLevel: {
    l1: { count: 0, tokensSaved: 0, avgRatio: 0 },
    l2: { count: 0, tokensSaved: 0, avgRatio: 0 },
    l3: { count: 0, tokensSaved: 0, avgRatio: 0 }
  },
  
  // By session
  bySession: {},  // sessionName -> { compactions, tokensSaved, lastCompaction }
  
  // History (rolling window)
  history: [],  // Last 100 compression events
  
  // Daily aggregates
  daily: {}  // date -> { compactions, tokensSaved }
};

/**
 * Initialize or load stats
 */
function loadStats() {
  try {
    if (fs.existsSync(STATS_FILE)) {
      const content = fs.readFileSync(STATS_FILE, "utf-8");
      return JSON.parse(content);
    }
  } catch (e) {}
  return { ...EMPTY_STATS };
}

/**
 * Save stats to file
 */
function saveStats(stats) {
  try {
    if (!fs.existsSync(STATS_DIR)) {
      fs.mkdirSync(STATS_DIR, { recursive: true });
    }
    fs.writeFileSync(STATS_FILE, JSON.stringify(stats, null, 2));
  } catch (e) {
    console.error(`Failed to save stats: ${e.message}`);
  }
}

/**
 * Load daily stats
 */
function loadDailyStats() {
  try {
    if (fs.existsSync(DAILY_STATS_FILE)) {
      return JSON.parse(fs.readFileSync(DAILY_STATS_FILE, "utf-8"));
    }
  } catch (e) {}
  return {};
}

/**
 * Save daily stats
 */
function saveDailyStats(daily) {
  try {
    fs.writeFileSync(DAILY_STATS_FILE, JSON.stringify(daily, null, 2));
  } catch (e) {}
}

/**
 * Record a compression event
 */
function recordCompression(sessionFile, level, tokensBefore, tokensAfter, reason = "") {
  const stats = loadStats();
  const today = new Date().toISOString().slice(0, 10);
  const sessionName = path.basename(sessionFile);
  
  const tokensSaved = Math.max(0, tokensBefore - tokensAfter);
  const ratio = tokensBefore > 0 ? tokensSaved / tokensBefore : 0;
  
  // Update totals
  stats.totalCompactions++;
  stats.totalTokensBefore += tokensBefore;
  stats.totalTokensAfter += tokensAfter;
  stats.totalTokensSaved += tokensSaved;
  
  // Update by-level stats
  if (!stats.byLevel[level]) {
    stats.byLevel[level] = { count: 0, tokensSaved: 0, avgRatio: 0 };
  }
  const levelStats = stats.byLevel[level];
  const oldCount = levelStats.count;
  levelStats.count++;
  levelStats.tokensSaved += tokensSaved;
  levelStats.avgRatio = (levelStats.avgRatio * oldCount + ratio) / levelStats.count;
  
  // Update by-session stats
  if (!stats.bySession[sessionName]) {
    stats.bySession[sessionName] = {
      compactions: 0,
      tokensSaved: 0,
      tokensBefore: 0,
      tokensAfter: 0,
      lastCompaction: null,
      levels: {}
    };
  }
  const sessionStats = stats.bySession[sessionName];
  sessionStats.compactions++;
  sessionStats.tokensSaved += tokensSaved;
  sessionStats.tokensBefore += tokensBefore;
  sessionStats.tokensAfter += tokensAfter;
  sessionStats.lastCompaction = new Date().toISOString();
  sessionStats.levels[level] = (sessionStats.levels[level] || 0) + 1;
  
  // Add to history
  stats.history.push({
    timestamp: new Date().toISOString(),
    session: sessionName,
    level,
    tokensBefore,
    tokensAfter,
    tokensSaved,
    ratio: ratio.toFixed(3),
    reason
  });
  
  // Keep history bounded
  if (stats.history.length > 100) {
    stats.history = stats.history.slice(-100);
  }
  
  // Update daily stats
  if (!stats.daily[today]) {
    stats.daily[today] = { compactions: 0, tokensSaved: 0, byLevel: {} };
  }
  stats.daily[today].compactions++;
  stats.daily[today].tokensSaved += tokensSaved;
  stats.daily[today].byLevel[level] = (stats.daily[today].byLevel[level] || 0) + 1;
  
  saveStats(stats);
  
  return {
    tokensSaved,
    totalTokensSaved: stats.totalTokensSaved,
    totalCompactions: stats.totalCompactions,
    ratio: ratio.toFixed(3)
  };
}

/**
 * Get overall statistics
 */
function getStats() {
  const stats = loadStats();
  
  return {
    summary: {
      totalCompactions: stats.totalCompactions,
      totalTokensBefore: stats.totalTokensBefore,
      totalTokensAfter: stats.totalTokensAfter,
      totalTokensSaved: stats.totalTokensSaved,
      overallRatio: stats.totalTokensBefore > 0 
        ? (stats.totalTokensSaved / stats.totalTokensBefore * 100).toFixed(1) + "%"
        : "0%"
    },
    byLevel: stats.byLevel,
    topSessions: getTopSessions(stats, 5),
    recentHistory: stats.history.slice(-10)
  };
}

/**
 * Get top sessions by tokens saved
 */
function getTopSessions(stats, limit = 5) {
  return Object.entries(stats.bySession)
    .map(([name, data]) => ({
      session: name,
      compactions: data.compactions,
      tokensSaved: data.tokensSaved,
      ratio: data.tokensBefore > 0 
        ? (data.tokensSaved / data.tokensBefore * 100).toFixed(1) + "%"
        : "0%",
      lastCompaction: data.lastCompaction
    }))
    .sort((a, b) => b.tokensSaved - a.tokensSaved)
    .slice(0, limit);
}

/**
 * Get daily statistics
 */
function getDailyStats(days = 7) {
  const daily = loadDailyStats();
  const result = [];
  
  for (let i = 0; i < days; i++) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().slice(0, 10);
    
    result.push({
      date: dateStr,
      compactions: daily[dateStr]?.compactions || 0,
      tokensSaved: daily[dateStr]?.tokensSaved || 0,
      byLevel: daily[dateStr]?.byLevel || {}
    });
  }
  
  return result;
}

/**
 * Generate text report
 */
function generateTextReport() {
  const stats = loadStats();
  const statsData = getStats();
  const daily = getDailyStats(7);
  
  const lines = [];
  lines.push("=".repeat(60));
  lines.push("TIERED CONTEXT MANAGER - COMPRESSION REPORT");
  lines.push(`Generated: ${new Date().toISOString()}`);
  lines.push("=".repeat(60));
  
  // Summary
  lines.push("\n## OVERALL SUMMARY");
  lines.push("-".repeat(40));
  lines.push(`Total Compactions:  ${stats.totalCompactions}`);
  lines.push(`Tokens Before:      ~${stats.totalTokensBefore.toLocaleString()}`);
  lines.push(`Tokens After:       ~${stats.totalTokensAfter.toLocaleString()}`);
  lines.push(`Tokens Saved:       ~${stats.totalTokensSaved.toLocaleString()}`);
  lines.push(`Overall Savings:    ${statsData.summary.overallRatio}`);
  
  // By level
  lines.push("\n## BY COMPRESSION LEVEL");
  lines.push("-".repeat(40));
  for (const [level, data] of Object.entries(stats.byLevel)) {
    if (data.count > 0) {
      lines.push(`Level ${level.toUpperCase()}:`);
      lines.push(`  Compactions:  ${data.count}`);
      lines.push(`  Tokens Saved: ~${data.tokensSaved.toLocaleString()}`);
      lines.push(`  Avg Ratio:    ${(data.avgRatio * 100).toFixed(1)}%`);
    }
  }
  
  // Top sessions
  lines.push("\n## TOP SESSIONS BY TOKENS SAVED");
  lines.push("-".repeat(40));
  for (const session of statsData.topSessions) {
    lines.push(`${session.session}:`);
    lines.push(`  Compactions: ${session.compactions}, Saved: ~${session.tokensSaved.toLocaleString()} (${session.ratio})`);
  }
  
  // Daily breakdown
  lines.push("\n## DAILY BREAKDOWN (Last 7 Days)");
  lines.push("-".repeat(40));
  for (const day of daily) {
    lines.push(`${day.date}: ${day.compactions} compactions, ~${day.tokensSaved.toLocaleString()} tokens saved`);
  }
  
  lines.push("\n" + "=".repeat(60));
  
  return lines.join("\n");
}

/**
 * Generate markdown report
 */
function generateMarkdownReport(title = "Compression Report") {
  const statsData = getStats();
  const daily = getDailyStats(7);
  const timestamp = new Date().toISOString();
  
  let md = `# ${title}

> Generated: ${timestamp}

## Summary

| Metric | Value |
|--------|-------|
| Total Compactions | ${statsData.summary.totalCompactions} |
| Tokens Before | ~${statsData.summary.totalTokensBefore.toLocaleString()} |
| Tokens After | ~${statsData.summary.totalTokensAfter.toLocaleString()} |
| Tokens Saved | ~${statsData.summary.totalTokensSaved.toLocaleString()} |
| Overall Savings | ${statsData.summary.overallRatio} |

## By Compression Level

| Level | Compactions | Tokens Saved | Avg Ratio |
|-------|-------------|--------------|-----------|
`;
  
  for (const [level, data] of Object.entries(statsData.byLevel)) {
    if (data.count > 0) {
      md += `| ${level.toUpperCase()} | ${data.count} | ~${data.tokensSaved.toLocaleString()} | ${(data.avgRatio * 100).toFixed(1)}% |\n`;
    }
  }
  
  md += `\n## Top Sessions\n\n`;
  md += `| Session | Compactions | Tokens Saved | Ratio | Last Compaction |\n`;
  md += `|---------|-------------|--------------|-------|----------------|\n`;
  
  for (const session of statsData.topSessions) {
    const lastCompaction = session.lastCompaction 
      ? new Date(session.lastCompaction).toLocaleString()
      : "Never";
    md += `| ${session.session} | ${session.compactions} | ~${session.tokensSaved.toLocaleString()} | ${session.ratio} | ${lastCompaction} |\n`;
  }
  
  md += `\n## Daily Breakdown\n\n`;
  md += `| Date | Compactions | Tokens Saved | By Level |\n`;
  md += `|------|-------------|--------------|----------|\n`;
  
  for (const day of daily) {
    const byLevel = Object.entries(day.byLevel)
      .map(([l, c]) => `${l}:${c}`)
      .join(", ") || "-";
    md += `| ${day.date} | ${day.compactions} | ~${day.tokensSaved.toLocaleString()} | ${byLevel} |\n`;
  }
  
  return md;
}

/**
 * Save report to file
 */
function saveReport(report, filename) {
  try {
    if (!fs.existsSync(REPORTS_DIR)) {
      fs.mkdirSync(REPORTS_DIR, { recursive: true });
    }
    
    const filepath = path.join(REPORTS_DIR, filename);
    fs.writeFileSync(filepath, report);
    return filepath;
  } catch (e) {
    return null;
  }
}

/**
 * Generate and save daily report
 */
function generateDailyReport() {
  const today = new Date().toISOString().slice(0, 10);
  const md = generateMarkdownReport(`Daily Compression Report - ${today}`);
  const filename = `compression_report_${today}.md`;
  const filepath = saveReport(md, filename);
  
  return filepath ? { ok: true, filepath } : { ok: false };
}

/**
 * Get compression efficiency score
 */
function getEfficiencyScore() {
  const stats = loadStats();
  
  if (stats.totalCompactions === 0) {
    return { score: 0, grade: "N/A", message: "No compression data yet" };
  }
  
  // Calculate efficiency score (0-100)
  let score = 0;
  
  // Factor 1: Overall savings ratio (0-40 points)
  const savingsRatio = stats.totalTokensBefore > 0 
    ? stats.totalTokensSaved / stats.totalTokensBefore 
    : 0;
  score += savingsRatio * 40;
  
  // Factor 2: L1/L2 usage vs L3 (0-30 points) - prefer L1/L2
  const l1l2Count = (stats.byLevel.l1?.count || 0) + (stats.byLevel.l2?.count || 0);
  const l3Count = stats.byLevel.l3?.count || 0;
  const l1l2Ratio = stats.totalCompactions > 0 ? l1l2Count / stats.totalCompactions : 0;
  score += l1l2Ratio * 30;
  
  // Factor 3: Frequency of compactions (0-20 points)
  const avgCompactionsPerSession = Object.keys(stats.bySession).length > 0
    ? stats.totalCompactions / Object.keys(stats.bySession).length
    : 0;
  score += Math.min(20, avgCompactionsPerSession * 5);
  
  // Factor 4: Consistency (0-10 points)
  const recentHistory = stats.history.slice(-20);
  const consistentCount = recentHistory.filter(h => h.tokensSaved > 0).length;
  const consistencyRatio = recentHistory.length > 0 
    ? consistentCount / recentHistory.length 
    : 0;
  score += consistencyRatio * 10;
  
  // Determine grade
  let grade;
  if (score >= 90) grade = "A+";
  else if (score >= 80) grade = "A";
  else if (score >= 70) grade = "B+";
  else if (score >= 60) grade = "B";
  else if (score >= 50) grade = "C";
  else grade = "D";
  
  return {
    score: Math.round(score),
    grade,
    details: {
      savingsContribution: (savingsRatio * 40).toFixed(1),
      levelDistributionContribution: (l1l2Ratio * 30).toFixed(1),
      frequencyContribution: Math.min(20, avgCompactionsPerSession * 5).toFixed(1),
      consistencyContribution: (consistencyRatio * 10).toFixed(1)
    }
  };
}

module.exports = {
  EMPTY_STATS,
  loadStats,
  saveStats,
  recordCompression,
  getStats,
  getDailyStats,
  generateTextReport,
  generateMarkdownReport,
  saveReport,
  generateDailyReport,
  getEfficiencyScore
};
