// TieredContextEngine - 完全自主的 OpenClaw Session 压缩引擎
// L1微压缩 → L2部分压缩 → L3由我们自己的AI处理(通过inbox)
// v2.0: 集成所有改进模块

const fs = require("fs");
const path = require("path");
const os = require("os");

// Load v2.0 modules
const l3AI = require("./l3_ai_compressor.js");
const memoryTier = require("./memory_tiering.js");
const crossAgent = require("./cross_agent_context.js");
const realtimeMon = require("./realtime_monitor.js");
const compStats = require("./compression_stats.js");

const MIN_OPENCLAW_VERSION = "1.0.0";
const PLUGIN_INTERFACE_VERSION = "2.0.0";

// 安全配置
const BACKUP_DIR = "E:\\zhuazhua\\.openclaw\\.openclaw\\workspace\\backups\\tiered-compactor";
const MAX_BACKUPS = 20;
const MICRO_KEEP_LAST = 3;
const LEVEL1_THRESHOLD = 0.75;
const LEVEL2_THRESHOLD = 0.90;
const MIN_MESSAGES_FOR_COMPACT = 6;
const MAX_COMPACT_PER_SESSION = 3;

function parseVersion(ver) {
  if (typeof ver !== "string") return [0, 0, 0];
  const parts = ver.split(".").map(Number);
  if (parts.length < 2 || parts.some(isNaN)) return [0, 0, 0];
  return [parts[0] || 0, parts[1] || 0, parts[2] || 0];
}

function compareVersion(ver, minVer) {
  const a = parseVersion(ver);
  const b = parseVersion(minVer);
  for (let i = 0; i < 3; i++) {
    if (a[i] > b[i]) return 1;
    if (a[i] < b[i]) return -1;
  }
  return 0;
}

function ensureBackupDir() {
  try {
    if (!fs.existsSync(BACKUP_DIR)) {
      fs.mkdirSync(BACKUP_DIR, { recursive: true });
    }
    const files = fs.readdirSync(BACKUP_DIR).filter(f => f.endsWith('.bak'));
    if (files.length > MAX_BACKUPS) {
      files.sort((a, b) => {
        const statA = fs.statSync(path.join(BACKUP_DIR, a));
        const statB = fs.statSync(path.join(BACKUP_DIR, b));
        return statA.mtime - statB.mtime;
      });
      const toDelete = files.slice(0, files.length - MAX_BACKUPS);
      for (const f of toDelete) {
        try { fs.unlinkSync(path.join(BACKUP_DIR, f)); } catch (e) {}
      }
    }
  } catch (e) {}
}

function estimateTokens(text) {
  if (!text || typeof text !== "string") return 0;
  const chinese = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const english = (text.match(/[a-zA-Z]/g) || []).length;
  const other = text.length - chinese - english;
  return Math.ceil(chinese * 1.5) + Math.ceil(english * 0.25) + other;
}

function safeReadSession(sessionFile) {
  try {
    if (!sessionFile || !fs.existsSync(sessionFile)) {
      return { messages: [], rawLines: [], error: null };
    }
    const content = fs.readFileSync(sessionFile, "utf-8");
    const records = [];
    let start = 0;
    for (let i = 0; i < content.length - 1; i++) {
      if (content[i] === '}' && content[i+1] === '\n') {
        records.push(content.slice(start, i + 1));
        start = i + 2;
      }
    }
    const lastRecord = content.slice(start).trim();
    if (lastRecord) records.push(lastRecord);

    const messages = [];
    for (const line of records) {
      if (!line.trim()) continue;
      try {
        const obj = JSON.parse(line);
        if (obj.type === "message") {
          messages.push({
            raw: obj,
            role: obj.message?.role,
            content: obj.message?.content,
            id: obj.id,
            timestamp: obj.timestamp
          });
        }
      } catch (e) {}
    }
    return { messages, rawLines: records, error: null };
  } catch (e) {
    return { messages: [], rawLines: [], error: e.message };
  }
}

function safeWriteSession(sessionFile, messages, rawLines, logger) {
  let backupFile = null;
  let tmpFile = null;

  try {
    const dir = path.dirname(sessionFile);
    const basename = path.basename(sessionFile);
    tmpFile = path.join(dir, `.${basename}.tmp`);

    const newLines = [];
    let msgIdx = 0;

    for (const line of rawLines) {
      if (!line.trim()) continue;
      try {
        const obj = JSON.parse(line);
        if (obj.type === "message" && msgIdx < messages.length) {
          const updated = { ...obj };
          updated.message = { ...updated.message, content: messages[msgIdx].content };
          newLines.push(JSON.stringify(updated));
          msgIdx++;
        } else {
          newLines.push(line.trim());
        }
      } catch (e) {
        newLines.push(line.trim());
      }
    }

    fs.writeFileSync(tmpFile, newLines.join("}\n") + "\n", "utf-8");

    ensureBackupDir();
    const timestamp = Date.now();
    backupFile = path.join(BACKUP_DIR, `${path.basename(sessionFile)}.${timestamp}.bak`);
    try {
      if (fs.existsSync(sessionFile)) {
        fs.copyFileSync(sessionFile, backupFile);
      }
    } catch (e) {
      logger.warn(`[TieredContextEngine] Backup failed: ${e.message}`);
    }

    fs.renameSync(tmpFile, sessionFile);
    tmpFile = null;

    return { ok: true, backupFile, error: null };
  } catch (e) {
    logger.error(`[TieredContextEngine] Write failed: ${e.message}`);

    if (backupFile && fs.existsSync(backupFile)) {
      try {
        fs.copyFileSync(backupFile, sessionFile);
        logger.info(`[TieredContextEngine] Auto-rollback triggered`);
      } catch (e2) {
        logger.error(`[TieredContextEngine] Auto-rollback failed: ${e2.message}`);
      }
    }

    return { ok: false, backupFile, error: e.message };
  } finally {
    if (tmpFile && fs.existsSync(tmpFile)) {
      try { fs.unlinkSync(tmpFile); } catch (e) {}
    }
  }
}

function getCompactCount(sessionFile) {
  if (!getCompactCount.cache) getCompactCount.cache = {};
  return getCompactCount.cache[sessionFile] || 0;
}

function incrementCompactCount(sessionFile) {
  if (!getCompactCount.cache) getCompactCount.cache = {};
  getCompactCount.cache[sessionFile] = (getCompactCount.cache[sessionFile] || 0) + 1;
}

function level1MicroCompact(messages, logger) {
  const lastN = Math.min(MICRO_KEEP_LAST, Math.max(2, Math.floor(messages.length / 2)));
  let compacted = 0;
  let tokensFreed = 0;

  for (let i = Math.max(0, messages.length - lastN); i < messages.length; i++) {
    const msg = messages[i];
    if (!msg.content || !Array.isArray(msg.content)) continue;

    for (const block of msg.content) {
      if (block.type === "toolResult" && block.text && estimateTokens(block.text) > 30) {
        tokensFreed += estimateTokens(block.text);
        block.text = `[truncated ${estimateTokens(block.text).toFixed(0)} tokens]`;
        compacted++;
      }
    }
  }

  if (compacted > 0) {
    logger.info(`[TieredContextEngine] L1: truncated ${compacted} toolResults, freed ~${tokensFreed.toFixed(0)} tokens`);
  }

  return { compacted, tokensFreed };
}

function level2PartialCompact(messages, logger) {
  const midpoint = Math.floor(messages.length / 2);
  let compacted = 0;
  let tokensFreed = 0;

  for (let i = 0; i < midpoint; i++) {
    const msg = messages[i];
    if (!msg.content || msg.role === "system" || !Array.isArray(msg.content)) continue;

    const newContent = [];
    for (const block of msg.content) {
      if (block.type === "toolResult") {
        const t = estimateTokens(block.text || "");
        if (t > 10) {
          tokensFreed += t;
          newContent.push({
            type: "text",
            text: `[tool: ${block.name || 'result'} ~${t.toFixed(0)} tokens]`
          });
          compacted++;
        }
      } else {
        newContent.push(block);
      }
    }
    msg.content = newContent;
  }

  if (compacted > 0) {
    logger.info(`[TieredContextEngine] L2: summarized ${compacted} toolResults, freed ~${tokensFreed.toFixed(0)} tokens`);
  }

  return { compacted, tokensFreed };
}

class TieredContextEngine {
  constructor({ openclawVersion = "0.0.0", logger } = {}) {
    this._logger = logger || console;
    this._openclawVersion = openclawVersion;
    this._isCompatible = compareVersion(openclawVersion, MIN_OPENCLAW_VERSION) >= 0;

    this.info = {
      id: "tiered-compactor",
      name: "Tiered Compactor Engine",
      version: "2.0.0"
    };

    ensureBackupDir();

    this._logger.info(
      `[TieredContextEngine] Initialized (v2.0.0). ` +
      `OpenClaw ${openclawVersion}, compatible: ${this._isCompatible}. ` +
      `L1<<${LEVEL1_THRESHOLD}, L2<<${LEVEL2_THRESHOLD}. ` +
      `Backup dir: ${BACKUP_DIR} (max ${MAX_BACKUPS})`
    );

    // Initialize v2.0 modules
    this._logger.info(`[TieredContextEngine] v2.0 modules loaded: L3_AI, Memory_Tier, CrossAgent, RealtimeMon, CompStats`);
  }

  async ingest(_params) {
    return { ingested: false };
  }

  async assemble(params) {
    return { messages: params.messages, estimatedTokens: 0 };
  }

  async afterTurn(_params) {}

  async compact(params) {
    const { sessionFile, tokenBudget, currentTokenCount } = params;
    const ratio = tokenBudget > 0 && currentTokenCount > 0
      ? currentTokenCount / tokenBudget
      : 1.0;

    this._logger.info(`[TieredContextEngine] compact() ratio=${ratio.toFixed(3)}, session=${sessionFile ? path.basename(sessionFile) : 'unknown'}`);

    // 读取session
    const { messages, rawLines, error } = safeReadSession(sessionFile);
    if (error || messages.length < MIN_MESSAGES_FOR_COMPACT) {
      this._logger.info(`[TieredContextEngine] Skipping: ${error || 'too few messages (' + messages.length + ')'}`);
      return { ok: true, compacted: false, reason: 'tiered_read_error' };
    }

    // 防重复压缩检查
    const compactCount = getCompactCount(sessionFile);
    if (compactCount >= MAX_COMPACT_PER_SESSION) {
      this._logger.info(`[TieredContextEngine] Skipping: session already compacted ${compactCount} times`);
      return { ok: true, compacted: false, reason: 'tiered_max_compact_reached' };
    }

    let l1Result = null;
    let l2Result = null;

    // L1: 微压缩 (ratio < 0.75)
    if (ratio < LEVEL1_THRESHOLD) {
      l1Result = level1MicroCompact(messages, this._logger);
      if (l1Result.compacted > 0) {
        const writeResult = safeWriteSession(sessionFile, messages, rawLines, this._logger);
        if (writeResult.ok) {
          incrementCompactCount(sessionFile);
          return {
            ok: true,
            compacted: true,
            reason: `tiered_l1_micro`,
            result: {
              summary: `L1微压缩: ${l1Result.compacted}项, 释放~${l1Result.tokensFreed.toFixed(0)}tokens`,
              tokensBefore: currentTokenCount,
              tokensAfter: Math.max(0, currentTokenCount - l1Result.tokensFreed),
              details: { level: 1, compacted: l1Result.compacted, backup: writeResult.backupFile }
            }
          };
        } else {
          this._logger.error(`[TieredContextEngine] L1 write failed: ${writeResult.error}`);
          return { ok: false, compacted: false, reason: 'tiered_l1_write_error' };
        }
      }
      // L1 没找到可压缩内容,停止
      this._logger.info(`[TieredContextEngine] L1 found nothing to compress, stopping`);
      return { ok: true, compacted: false, reason: "tiered_l1_nothing_to_compress" };
    }

    // L2: 部分压缩 (0.75 <= ratio < 0.90)
    if (ratio < LEVEL2_THRESHOLD) {
      l2Result = level2PartialCompact(messages, this._logger);
      if (l2Result.compacted > 0) {
        const writeResult = safeWriteSession(sessionFile, messages, rawLines, this._logger);
        if (writeResult.ok) {
          incrementCompactCount(sessionFile);
          return {
            ok: true,
            compacted: true,
            reason: `tiered_l2_partial`,
            result: {
              summary: `L2部分压缩: ${l2Result.compacted}项, 释放~${l2Result.tokensFreed.toFixed(0)}tokens`,
              tokensBefore: currentTokenCount,
              tokensAfter: Math.max(0, currentTokenCount - l2Result.tokensFreed),
              details: { level: 2, compacted: l2Result.compacted, backup: writeResult.backupFile }
            }
          };
        } else {
          this._logger.error(`[TieredContextEngine] L2 write failed: ${writeResult.error}`);
          return { ok: false, compacted: false, reason: 'tiered_l2_write_error' };
        }
      }
      // L2 没找到可压缩内容,停止
      this._logger.info(`[TieredContextEngine] L2 found nothing to compress, stopping`);
      return { ok: true, compacted: false, reason: "tiered_l2_nothing_to_compress" };
    }

    // L3: 需要我们自己的AI来处理(写入inbox)
    this._logger.info(`[TieredContextEngine] L3 needs AI compression, writing to inbox`);

    // Use L3 AI Compressor module to create task
    const l3Result = l3AI.createL3Task(sessionFile, tokenBudget, currentTokenCount, `ratio=${ratio.toFixed(3)}`);

    if (l3Result.ok) {
      // Record compression attempt
      compStats.recordCompression(sessionFile, 'l3', currentTokenCount, currentTokenCount, 'l3_ai_queued');

      return {
        ok: true,
        compacted: false,
        reason: "tiered_l3_needs_ai",
        result: {
          summary: `L3 AI压缩任务已创建: ${l3Result.taskId}`,
          sessionFile: params.sessionFile,
          tokenBudget: params.tokenBudget,
          currentTokenCount: currentTokenCount,
          taskId: l3Result.taskId,
          taskFile: l3Result.taskFile,
          details: { level: 3, needs_ai: true, task_queued: true }
        }
      };
    } else {
      this._logger.error(`[TieredContextEngine] L3 task creation failed: ${l3Result.error}`);
      return { ok: false, compacted: false, reason: 'tiered_l3_task_error' };
    }
  }
  
  // ==================== v2.0 API Methods ====================

  /**
   * Get compression statistics
   */
  getStats() {
    return compStats.getStats();
  }

  /**
   * Get memory tier statistics
   */
  getMemoryStats() {
    return memoryTier.getMemoryStats();
  }

  /**
   * Get monitoring dashboard data
   */
  getDashboard() {
    return realtimeMon.getDashboard();
  }

  /**
   * Generate compression report
   */
  generateReport(format = 'text') {
    if (format === 'markdown') {
      return compStats.generateMarkdownReport();
    }
    return compStats.generateTextReport();
  }

  /**
   * Extract and share knowledge from session
   */
  extractAndShare(sessionFile, agentName = 'unknown') {
    return crossAgent.extractAndPublish(sessionFile, agentName);
  }

  /**
   * Create context package for agent handoff
   */
  createHandoff(sessionFile, targetAgent, purpose = 'continuation') {
    return crossAgent.createContextPackage(sessionFile, targetAgent, purpose);
  }

  /**
   * Get recent shared knowledge
   */
  getRecentKnowledge(count = 5) {
    return crossAgent.getRecentKnowledge(count);
  }

  /**
   * Migrate memories to tiered system
   */
  migrateMemories(dryRun = true) {
    return memoryTier.migrateMemoriesToTiered(dryRun);
  }

  /**
   * List cleanup candidates
   */
  listCleanupCandidates() {
    return memoryTier.listCleanupCandidates();
  }

  /**
   * Cleanup expired memories
   */
  cleanupMemories(dryRun = true) {
    return memoryTier.cleanupExpiredMemories(dryRun);
  }

  /**
   * Monitor session and get compression decision
   */
  monitorSession(sessionFile, tokenBudget = 100000) {
    return realtimeMon.monitorSession(sessionFile, tokenBudget);
  }

  /**
   * Get L3 AI compression statistics
   */
  getL3Stats() {
    return l3AI.getL3Stats();
  }

  async dispose() {}
}

module.exports = {
  TieredContextEngine,
  MIN_OPENCLAW_VERSION,
  PLUGIN_INTERFACE_VERSION,
  safeReadSession,
  safeWriteSession,
  level1MicroCompact,
  level2PartialCompact,
  estimateTokens,
  BACKUP_DIR,
  MAX_BACKUPS,
  MICRO_KEEP_LAST,
  LEVEL1_THRESHOLD,
  LEVEL2_THRESHOLD,
  MIN_MESSAGES_FOR_COMPACT,
  MAX_COMPACT_PER_SESSION
};
