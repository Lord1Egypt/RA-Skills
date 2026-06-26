/**
 * TieredContextEngine Standalone Script
 * 
 * 主动扫描 agents 目录下的 session 文件，对超过阈值的 session 调用 TieredContextEngine 进行压缩。
 * 
 * 用法: node scripts/tiered_standalone.js [--dry-run] [--min-size KB] [--agent NAME]
 *   --dry-run   不实际执行压缩，只报告哪些 session 需要压缩
 *   --min-size  最小文件大小（KB），默认 300
 *   --agent     只处理指定 agent（如 main, stocks），默认全部
 */

const fs = require("fs");
const path = require("path");
const os = require("os");

// inbox 路径
const INBOX_DIR = "E:\\zhuazhua\\.openclaw-shared\\memory\\inbox";
const L3_QUEUE_FILE = path.join(INBOX_DIR, "l3_ai_compression_tasks.md");

// ============================================================
// 1. 解析命令行参数
// ============================================================
const args = process.argv.slice(2);
const dryRun = args.includes("--dry-run");
const minSizeKbIdx = args.indexOf("--min-size");
const minSizeKb = minSizeKbIdx >= 0 ? parseInt(args[minSizeKbIdx + 1]) || 300 : 300;
const agentFilter = args.includes("--agent") ? args[args.indexOf("--agent") + 1] : null;

console.log(`\n========================================`);
console.log(`TieredContextEngine Standalone Scanner`);
console.log(`========================================`);
console.log(`Mode: ${dryRun ? "DRY RUN (no changes)" : "LIVE (will compact)"}`);
console.log(`Min file size: ${minSizeKb} KB`);
console.log(`Agent filter: ${agentFilter || "all"}`);
console.log(`========================================\n`);

// ============================================================
// 2. 路径配置
// ============================================================
const OPENCLAW_ROOT = "E:\\zhuazhua\\.openclaw";
const AGENTS_DIR = path.join(OPENCLAW_ROOT, "agents");
const BACKUP_DIR = path.join(OPENCLAW_ROOT, ".openclaw", "workspace", "backups", "tiered-compactor");

// tiered-engine.js 路径（我们自己的代码）
const TIERED_ENGINE_PATH = path.join(OPENCLAW_ROOT, ".openclaw", "workspace", "plugins", "tiered-compactor", "tiered-engine.js");

// ============================================================
// 3. 日志记录器
// ============================================================
const stats = {
  scanned: 0,
  candidates: 0,
  compacted: 0,
  skipped: 0,
  errors: 0,
  l1Count: 0,
  l2Count: 0,
  l3Count: 0,
  totalTokensFreed: 0
};

function log(level, ...args) {
  const prefix = new Date().toISOString().slice(11, 19);
  console[level](`[${prefix}]`, ...args);
}

function logInfo(...args) { log("info", ...args); }
function logWarn(...args) { log("warn", ...args); }
function logError(...args) { log("error", ...args); }

// ============================================================
// 4. 加载 TieredContextEngine
// ============================================================
let TieredContextEngine;

try {
  // 加载 tiered-engine.js（我们自己的代码）
  const tieredMod = require(TIERED_ENGINE_PATH);
  TieredContextEngine = tieredMod.TieredContextEngine;
  console.log(`Loaded TieredContextEngine from plugin`);
} catch (e) {
  console.error(`Failed to load TieredContextEngine: ${e.message}`);
  process.exit(1);
}

// 创建引擎实例
const logger = {
  info: (...args) => logInfo("[Tiered]", ...args),
  warn: (...args) => logWarn("[Tiered]", ...args),
  error: (...args) => logError("[Tiered]", ...args)
};

const engine = new TieredContextEngine({
  openclawVersion: "1.0.0",
  compactEmbeddedPiSessionDirect,
  logger
});

// ============================================================
// 5. 工具函数
// ============================================================

/**
 * 估算 token 数量（与 tiered-engine.js 一致）
 */
function estimateTokens(text) {
  if (!text || typeof text !== "string") return 0;
  const chinese = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const english = (text.match(/[a-zA-Z]/g) || []).length;
  const other = text.length - chinese - english;
  return Math.ceil(chinese * 1.5) + Math.ceil(english * 0.25) + other;
}

/**
 * 将 L3 压缩任务写入 inbox
 */
function writeL3TaskToInbox(sessionFile, tokenBudget, currentTokenCount, reason) {
  const timestamp = new Date().toISOString();
  const taskEntry = `\n---\ntype: L3_COMPRESSION_TASK\nstatus: pending\nfrom: tiered_standalone\ntime: ${timestamp}\n---\n\nSession文件: ${sessionFile}\nToken预算: ${tokenBudget}\n当前Token数: ~${currentTokenCount.toFixed(0)}\n原因: ${reason}\n\n请用自己的AI能力压缩此session内容，生成摘要。\n处理方法：\n1. 读取session文件内容\n2. 用AI能力生成摘要压缩\n3. 写回压缩后的内容\n4. 完成后更新status为done\n`;
  
  try {
    if (!fs.existsSync(INBOX_DIR)) {
      fs.mkdirSync(INBOX_DIR, { recursive: true });
    }
    fs.appendFileSync(L3_QUEUE_FILE, taskEntry);
    logInfo(`L3压缩任务已写入inbox: ${path.basename(sessionFile)}`);
    return true;
  } catch (e) {
    logError(`写入inbox失败: ${e.message}`);
    return false;
  }
}

/**
 * 扫描 agents 目录，获取所有 sessions.json 文件
 */
function findSessionsJson() {
  if (!fs.existsSync(AGENTS_DIR)) {
    return [];
  }
  
  const results = [];
  const entries = fs.readdirSync(AGENTS_DIR, { withFileTypes: true });
  
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    if (agentFilter && entry.name !== agentFilter) continue;
    
    const sessionsJson = path.join(AGENTS_DIR, entry.name, "sessions", "sessions.json");
    if (fs.existsSync(sessionsJson)) {
      results.push({
        agent: entry.name,
        sessionsJson
      });
    }
  }
  
  return results;
}

/**
 * 获取 session 列表，按文件大小排序
 */
function loadSessions(sessionsJsonPath) {
  try {
    const content = fs.readFileSync(sessionsJsonPath, "utf-8");
    const sessions = JSON.parse(content);
    
    const result = [];
    for (const [sessionId, meta] of Object.entries(sessions)) {
      if (!meta.sessionFile) continue;
      
      const sessionFile = meta.sessionFile;
      if (!fs.existsSync(sessionFile)) continue;
      
      const stat = fs.statSync(sessionFile);
      const sizeKb = stat.size / 1024;
      
      result.push({
        sessionId,
        sessionFile,
        sizeKb,
        updatedAt: meta.updatedAt,
        compactionCount: meta.compactionCount || 0
      });
    }
    
    // 按文件大小降序排序
    result.sort((a, b) => b.sizeKb - a.sizeKb);
    return result;
  } catch (e) {
    logError(`Failed to load sessions.json: ${e.message}`);
    return [];
  }
}

/**
 * 读取 session 文件，估算 token 数
 */
function estimateSessionTokens(sessionFile) {
  try {
    const content = fs.readFileSync(sessionFile, "utf-8");
    // Session files use \n as delimiter, not os.EOL (\r\n on Windows)
    const lines = content.split("\n");
    let totalTokens = 0;
    
    for (const line of lines) {
      if (!line.trim()) continue;
      try {
        const obj = JSON.parse(line);
        if (obj.type === "message" && obj.message?.content) {
          if (Array.isArray(obj.message.content)) {
            for (const block of obj.message.content) {
              if (block.text) {
                totalTokens += estimateTokens(block.text);
              }
            }
          } else if (typeof obj.message.content === "string") {
            totalTokens += estimateTokens(obj.message.content);
          }
        }
      } catch (e) {
        // skip malformed lines
      }
    }
    
    return totalTokens;
  } catch (e) {
    return 0;
  }
}

/**
 * 执行压缩
 */
async function compactSession(session) {
  const tokenBudget = 100000;  // 默认 100k token budget
  const currentTokenCount = estimateSessionTokens(session.sessionFile);
  const ratio = currentTokenCount / tokenBudget;
  
  logInfo(`Compacting: ${path.basename(session.sessionFile)}`);
  logInfo(`  Size: ${session.sizeKb.toFixed(1)} KB`);
  logInfo(`  Tokens: ~${currentTokenCount.toFixed(0)} (ratio: ${ratio.toFixed(3)})`);
  
  if (dryRun) {
    logInfo(`  [DRY RUN] Would compact this session`);
    return { ok: true, compacted: true, reason: "dry_run", result: { summary: "Dry run - no actual compaction" } };
  }
  
  try {
    const result = await engine.compact({
      sessionFile: session.sessionFile,
      tokenBudget,
      currentTokenCount,
      sessionId: session.sessionId,
      runtimeContext: {
        workspaceDir: "E:\\zhuazhua\\.openclaw\\.openclaw\\workspace"
      }
    });
    
    if (result.compacted) {
      logInfo(`  Result: ${result.reason}`);
      if (result.result?.summary) {
        logInfo(`  Summary: ${result.result.summary}`);
      }
    } else {
      logInfo(`  No compaction performed: ${result.reason || "unknown"}`);
    }
    
    return result;
  } catch (e) {
    logError(`  Exception: ${e.message}`);
    return { ok: false, compacted: false, error: e.message };
  }
}

// ============================================================
// 6. 主逻辑
// ============================================================

async function main() {
  const startTime = Date.now();
  logInfo("Starting tiered context engine scan...\n");
  
  // 确保备份目录存在
  if (!fs.existsSync(BACKUP_DIR)) {
    try {
      fs.mkdirSync(BACKUP_DIR, { recursive: true });
      logInfo(`Created backup directory: ${BACKUP_DIR}`);
    } catch (e) {
      logWarn(`Could not create backup dir: ${e.message}`);
    }
  }
  
  // 扫描 agents 目录
  const agentSessions = findSessionsJson();
  logInfo(`Found sessions.json in ${agentSessions.length} agent(s)\n`);
  
  for (const { agent, sessionsJson } of agentSessions) {
    logInfo(`========================================`);
    logInfo(`Agent: ${agent}`);
    logInfo(`========================================`);
    
    const sessions = loadSessions(sessionsJson);
    logInfo(`Loaded ${sessions.length} sessions from sessions.json`);
    
    // 过滤需要处理的 session（大小 >= minSizeKb）
    const candidates = sessions.filter(s => s.sizeKb >= minSizeKb);
    logInfo(`Sessions >= ${minSizeKb} KB: ${candidates.length}`);
    stats.candidates += candidates.length;
    
    if (candidates.length === 0) {
      logInfo("No sessions to process\n");
      continue;
    }
    
    // 显示候选 session 列表
    logInfo("\nCandidate sessions (sorted by size):");
    for (const s of candidates.slice(0, 10)) {
      logInfo(`  ${(s.sizeKb / 1024).toFixed(2)} MB - ${path.basename(s.sessionFile)} (compactionCount: ${s.compactionCount})`);
    }
    if (candidates.length > 10) {
      logInfo(`  ... and ${candidates.length - 10} more`);
    }
    
    // 逐个处理
    for (const session of candidates) {
      stats.scanned++;
      
      // 跳过已压缩次数过多的 session
      if (session.compactionCount >= 3) {
        logInfo(`SKIP: ${path.basename(session.sessionFile)} (already compacted ${session.compactionCount} times)`);
        stats.skipped++;
        continue;
      }
      
      const result = await compactSession(session);
      
      if (result.compacted) {
        stats.compacted++;
        
        // 统计 L1/L2/L3
        if (result.reason?.includes("l1")) {
          stats.l1Count++;
        } else if (result.reason?.includes("l2")) {
          stats.l2Count++;
        } else if (result.reason?.includes("l3")) {
          stats.l3Count++;
        }
        
        // 统计释放的 tokens
        if (result.result?.tokensBefore && result.result?.tokensAfter) {
          stats.totalTokensFreed += (result.result.tokensBefore - result.result.tokensAfter);
        }
      } else if (result.error) {
        stats.errors++;
      } else if (result.reason?.includes("needs_ai")) {
        // L3需要我们自己的AI来处理，写入inbox
        const sessionFile = result.result?.sessionFile || session.sessionFile;
        const tokenBudget = result.result?.tokenBudget || 100000;
        const currentTokenCount = result.result?.currentTokenCount || 0;
        writeL3TaskToInbox(sessionFile, tokenBudget, currentTokenCount, result.reason);
        stats.skipped++;
      } else {
        stats.skipped++;
      }
    }
    
    logInfo("");
  }
  
  // ============================================================
  // 7. 汇总报告
  // ============================================================
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  
  console.log(`\n========================================`);
  console.log(`TIERED CONTEXT ENGINE - SUMMARY REPORT`);
  console.log(`========================================`);
  console.log(`Scan duration: ${elapsed}s`);
  console.log(`Mode: ${dryRun ? "DRY RUN" : "LIVE"}`);
  console.log(`----------------------------------------`);
  console.log(`Scanned sessions:     ${stats.scanned}`);
  console.log(`Candidates (>=${minSizeKb}KB): ${stats.candidates}`);
  console.log(`Actually compacted:   ${stats.compacted}`);
  console.log(`Skipped:              ${stats.skipped}`);
  console.log(`Errors:               ${stats.errors}`);
  console.log(`----------------------------------------`);
  console.log(`L1 (micro) compactions:  ${stats.l1Count}`);
  console.log(`L2 (partial) compactions: ${stats.l2Count}`);
  console.log(`L3 (runtime) compactions: ${stats.l3Count}`);
  console.log(`----------------------------------------`);
  console.log(`Total tokens freed:   ~${stats.totalTokensFreed.toFixed(0)}`);
  console.log(`========================================\n`);
  
  // 如果有错误，退出码非零
  if (stats.errors > 0) {
    process.exit(1);
  }
}

main().catch(e => {
  logError(`Fatal error: ${e.message}`);
  process.exit(1);
});
