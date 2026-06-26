/**
 * Real-Time Compression Monitor v2.0
 * 
 * Monitors session growth in real-time and triggers compression:
 * 1. Session growth monitoring
 * 2. Threshold-triggered compression
 * 3. Historical data analysis
 * 4. Automatic threshold adjustment
 */

const fs = require("fs");
const path = require("path");
const os = require("os");

// Paths
const MONITOR_DIR = "E:\\zhuazhua\\.openclaw\\.openclaw\\workspace\\plugins\\tiered-compactor";
const HISTORY_DIR = path.join(MONITOR_DIR, "history");
const THRESHOLDS_FILE = path.join(MONITOR_DIR, "thresholds.json");
const STATS_FILE = path.join(MONITOR_DIR, "compression_stats.json");

// Default thresholds
const DEFAULT_THRESHOLDS = {
  // Token-based thresholds
  warningRatio: 0.60,     // 60% of budget - start monitoring
  compressionRatio: 0.75, // 75% - L1 micro compression
  aggressiveRatio: 0.90,  // 90% - L2 partial compression
  criticalRatio: 0.95,    // 95% - L3 AI compression
  
  // Size-based thresholds (KB)
  warningSizeKb: 200,
  compressSizeKb: 300,
  aggressiveSizeKb: 500,
  
  // Time-based (hours since last compression)
  forceCompactAfterHours: 24,
  
  // Adaptive settings
  enableAdaptive: true,
  adjustmentFactor: 0.05,  // 5% adjustment per analysis
  minThreshold: 0.50,
  maxThreshold: 0.95
};

// Monitoring state
let monitorState = {
  lastCheck: null,
  sessions: {},  // sessionId -> { lastSize, lastTokens, lastCheck, compactCount }
  thresholds: { ...DEFAULT_THRESHOLDS }
};

/**
 * Token estimation
 */
function estimateTokens(text) {
  if (!text || typeof text !== "string") return 0;
  const chinese = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const english = (text.match(/[a-zA-Z]/g) || []).length;
  const other = text.length - chinese - english;
  return Math.ceil(chinese * 1.5) + Math.ceil(english * 0.25) + other;
}

/**
 * Estimate session tokens from file
 */
function estimateSessionTokens(sessionFile) {
  try {
    if (!fs.existsSync(sessionFile)) return 0;
    
    const content = fs.readFileSync(sessionFile, "utf-8");
    const lines = content.split("\n");
    let totalTokens = 0;
    
    for (const line of lines) {
      if (!line.trim()) continue;
      try {
        const obj = JSON.parse(line);
        if (obj.type === "message" && obj.message?.content) {
          if (Array.isArray(obj.message.content)) {
            for (const block of obj.message.content) {
              if (block.text) totalTokens += estimateTokens(block.text);
            }
          } else if (typeof obj.message.content === "string") {
            totalTokens += estimateTokens(obj.message.content);
          }
        }
      } catch (e) {}
    }
    
    return totalTokens;
  } catch (e) {
    return 0;
  }
}

/**
 * Load thresholds from file
 */
function loadThresholds() {
  try {
    if (fs.existsSync(THRESHOLDS_FILE)) {
      const content = fs.readFileSync(THRESHOLDS_FILE, "utf-8");
      const saved = JSON.parse(content);
      monitorState.thresholds = { ...DEFAULT_THRESHOLDS, ...saved };
    }
  } catch (e) {}
  
  return monitorState.thresholds;
}

/**
 * Save thresholds to file
 */
function saveThresholds() {
  try {
    if (!fs.existsSync(MONITOR_DIR)) {
      fs.mkdirSync(MONITOR_DIR, { recursive: true });
    }
    fs.writeFileSync(THRESHOLDS_FILE, JSON.stringify(monitorState.thresholds, null, 2));
  } catch (e) {}
}

/**
 * Load compression statistics
 */
function loadStats() {
  try {
    if (fs.existsSync(STATS_FILE)) {
      return JSON.parse(fs.readFileSync(STATS_FILE, "utf-8"));
    }
  } catch (e) {}
  
  return {
    totalCompactions: 0,
    totalTokensSaved: 0,
    byLevel: { l1: 0, l2: 0, l3: 0 },
    bySession: {},
    history: []
  };
}

/**
 * Save compression statistics
 */
function saveStats(stats) {
  try {
    if (!fs.existsSync(MONITOR_DIR)) {
      fs.mkdirSync(MONITOR_DIR, { recursive: true });
    }
    fs.writeFileSync(STATS_FILE, JSON.stringify(stats, null, 2));
  } catch (e) {}
}

/**
 * Record a compression event
 */
function recordCompression(sessionFile, level, tokensBefore, tokensAfter, reason) {
  const stats = loadStats();
  
  const sessionName = path.basename(sessionFile);
  const tokensSaved = Math.max(0, tokensBefore - tokensAfter);
  
  // Update totals
  stats.totalCompactions++;
  stats.totalTokensSaved += tokensSaved;
  stats.byLevel[level] = (stats.byLevel[level] || 0) + 1;
  
  // Update per-session stats
  if (!stats.bySession[sessionName]) {
    stats.bySession[sessionName] = {
      compactions: 0,
      tokensSaved: 0,
      lastCompaction: null
    };
  }
  stats.bySession[sessionName].compactions++;
  stats.bySession[sessionName].tokensSaved += tokensSaved;
  stats.bySession[sessionName].lastCompaction = new Date().toISOString();
  
  // Add to history (keep last 100)
  stats.history.push({
    timestamp: new Date().toISOString(),
    session: sessionName,
    level,
    tokensBefore,
    tokensAfter,
    tokensSaved,
    reason
  });
  
  if (stats.history.length > 100) {
    stats.history = stats.history.slice(-100);
  }
  
  saveStats(stats);
  
  return { tokensSaved, totalCompactions: stats.totalCompactions };
}

/**
 * Analyze historical compression data
 */
function analyzeHistory() {
  const stats = loadStats();
  
  if (stats.history.length < 5) {
    return {
      analysis: "Insufficient history for analysis",
      recommendations: []
    };
  }
  
  const recentHistory = stats.history.slice(-20);
  
  // Calculate metrics
  const avgTokensSaved = stats.history.reduce((sum, h) => sum + h.tokensSaved, 0) / stats.history.length;
  const avgByLevel = {
    l1: stats.byLevel.l1 / Math.max(1, stats.totalCompactions),
    l2: stats.byLevel.l2 / Math.max(1, stats.totalCompactions),
    l3: stats.byLevel.l3 / Math.max(1, stats.totalCompactions)
  };
  
  // Find sessions that get compressed frequently
  const frequentSessions = Object.entries(stats.bySession)
    .filter(([_, data]) => data.compactions >= 3)
    .map(([name, data]) => ({ name, compactions: data.compactions }));
  
  // Calculate time since last compression for each session
  const now = Date.now();
  const sessionsNeedingAttention = [];
  for (const [sessionName, data] of Object.entries(stats.bySession)) {
    if (data.lastCompaction) {
      const hoursSince = (now - new Date(data.lastCompaction).getTime()) / (1000 * 60 * 60);
      if (hoursSince > DEFAULT_THRESHOLDS.forceCompactAfterHours) {
        sessionsNeedingAttention.push({
          name: sessionName,
          hoursSinceLastCompaction: hoursSince.toFixed(1)
        });
      }
    }
  }
  
  return {
    analysis: {
      totalCompactions: stats.totalCompactions,
      avgTokensSaved: avgTokensSaved.toFixed(0),
      compressionLevelDistribution: stats.byLevel,
      frequentCompressionSessions: frequentSessions,
      sessionsNeedingAttention
    },
    recommendations: generateRecommendations(stats)
  };
}

/**
 * Generate threshold adjustment recommendations
 */
function generateRecommendations(stats) {
  const recommendations = [];
  const thresholds = monitorState.thresholds;
  
  if (!thresholds.enableAdaptive) {
    return [{ type: "info", message: "Adaptive thresholds disabled" }];
  }
  
  // Check if thresholds are too aggressive (lots of L3 compactions)
  if (stats.byLevel.l3 > stats.byLevel.l1 + stats.byLevel.l2) {
    recommendations.push({
      type: "reduce_threshold",
      message: "High L3 ratio detected. Consider lowering criticalRatio threshold.",
      current: thresholds.criticalRatio,
      suggested: Math.max(DEFAULT_THRESHOLDS.minThreshold, thresholds.criticalRatio - thresholds.adjustmentFactor)
    });
  }
  
  // Check if thresholds are too conservative (many skipped compactions)
  if (stats.history.length >= 10) {
    const recentHistory = stats.history.slice(-10);
    const skippedCount = recentHistory.filter(h => h.tokensSaved === 0).length;
    if (skippedCount > 5) {
      recommendations.push({
        type: "raise_threshold",
        message: "Many compression attempts with no savings. Thresholds may be too low.",
        current: thresholds.compressionRatio,
        suggested: Math.min(DEFAULT_THRESHOLDS.maxThreshold, thresholds.compressionRatio + thresholds.adjustmentFactor)
      });
    }
  }
  
  return recommendations;
}

/**
 * Apply threshold adjustments based on history
 */
function adjustThresholds() {
  const analysis = analyzeHistory();
  
  if (!monitorState.thresholds.enableAdaptive) {
    return { adjusted: false, reason: "Adaptive disabled" };
  }
  
  let adjusted = false;
  
  for (const rec of analysis.recommendations) {
    if (rec.type === "reduce_threshold") {
      monitorState.thresholds.criticalRatio = rec.suggested;
      adjusted = true;
    } else if (rec.type === "raise_threshold") {
      monitorState.thresholds.compressionRatio = rec.suggested;
      adjusted = true;
    }
  }
  
  if (adjusted) {
    saveThresholds();
  }
  
  return { adjusted, analysis };
}

/**
 * Check if session needs compression
 */
function checkCompressionNeeded(sessionFile, tokenBudget = 100000) {
  const thresholds = loadThresholds();
  const tokens = estimateSessionTokens(sessionFile);
  const ratio = tokens / tokenBudget;
  
  // Get session state
  const sessionName = path.basename(sessionFile);
  if (!monitorState.sessions[sessionName]) {
    monitorState.sessions[sessionName] = {
      lastSize: 0,
      lastTokens: 0,
      lastCheck: Date.now(),
      compactCount: 0
    };
  }
  
  const state = monitorState.sessions[sessionName];
  const growthRate = state.lastTokens > 0 
    ? (tokens - state.lastTokens) / state.lastTokens 
    : 0;
  
  // Update state
  state.lastTokens = tokens;
  state.lastCheck = Date.now();
  
  // Determine compression level needed
  let level = null;
  let reason = null;
  
  if (ratio >= thresholds.criticalRatio) {
    level = 3;
    reason = "critical_ratio";
  } else if (ratio >= thresholds.aggressiveRatio) {
    level = 2;
    reason = "aggressive_ratio";
  } else if (ratio >= thresholds.compressionRatio) {
    level = 1;
    reason = "compression_ratio";
  } else if (ratio >= thresholds.warningRatio) {
    level = 0;  // Warning only, no compression
    reason = "warning_ratio";
  }
  
  return {
    needed: level !== null,
    level,
    reason,
    tokens,
    ratio: ratio.toFixed(3),
    thresholds: {
      warning: thresholds.warningRatio,
      compression: thresholds.compressionRatio,
      aggressive: thresholds.aggressiveRatio,
      critical: thresholds.criticalRatio
    },
    growthRate: growthRate.toFixed(3),
    sessionState: state
  };
}

/**
 * Monitor a session and return compression decision
 */
function monitorSession(sessionFile, tokenBudget = 100000) {
  const result = checkCompressionNeeded(sessionFile, tokenBudget);
  
  // Check force compact time
  const sessionName = path.basename(sessionFile);
  const state = monitorState.sessions[sessionName];
  
  if (state) {
    const hoursSinceCheck = (Date.now() - state.lastCheck) / (1000 * 60 * 60);
    if (hoursSinceCheck >= monitorState.thresholds.forceCompactAfterHours) {
      // Force compact even if not at threshold
      if (!result.needed || result.level < 1) {
        result.level = 1;
        result.reason = "force_timeout";
        result.needed = true;
      }
    }
  }
  
  return result;
}

/**
 * Get monitoring dashboard data
 */
function getDashboard() {
  const thresholds = loadThresholds();
  const stats = loadStats();
  const analysis = analyzeHistory();
  
  return {
    thresholds,
    stats: {
      totalCompactions: stats.totalCompactions,
      totalTokensSaved: stats.totalTokensSaved,
      byLevel: stats.byLevel
    },
    analysis,
    recommendations: analysis.recommendations,
    monitorState: {
      sessionsTracked: Object.keys(monitorState.sessions).length,
      lastCheck: monitorState.lastCheck
    }
  };
}

/**
 * Export historical data
 */
function exportHistory() {
  const stats = loadStats();
  
  if (!fs.existsSync(HISTORY_DIR)) {
    fs.mkdirSync(HISTORY_DIR, { recursive: true });
  }
  
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  const exportFile = path.join(HISTORY_DIR, `compression_history_${timestamp}.json`);
  
  fs.writeFileSync(exportFile, JSON.stringify(stats, null, 2));
  
  return exportFile;
}

module.exports = {
  DEFAULT_THRESHOLDS,
  estimateTokens,
  estimateSessionTokens,
  loadThresholds,
  saveThresholds,
  loadStats,
  saveStats,
  recordCompression,
  analyzeHistory,
  adjustThresholds,
  checkCompressionNeeded,
  monitorSession,
  getDashboard,
  exportHistory
};
