/**
 * TieredContextEngine Standalone Scanner v2.0
 * 
 * Usage: node scripts/tiered_standalone_v2.js [--dry-run] [--min-size KB] [--agent NAME] [--task TASK]
 *   --dry-run   不实际执行压缩
 *   --min-size  最小文件大小（KB），默认 300
 *   --agent     只处理指定 agent
 *   --task      scan, stats, report, cleanup, migrate, dashboard, analyze
 */

const fs = require("fs");
const path = require("path");

const OPENCLAW_ROOT = "E:\\zhuazhua\\.openclaw";
const WORKSPACE = path.join(OPENCLAW_ROOT, ".openclaw", "workspace");
const PLUGIN_DIR = path.join(WORKSPACE, "plugins", "tiered-compactor");
const AGENTS_DIR = path.join(OPENCLAW_ROOT, "agents");
const BACKUP_DIR = path.join(WORKSPACE, "backups", "tiered-compactor");
const INBOX_DIR = "E:\\zhuazhua\\.openclaw-shared\\memory\\inbox";

// Load v2.0 modules
let TieredContextEngine, l3AI, memoryTier, crossAgent, realtimeMon, compStats;
try {
  const te = require(path.join(PLUGIN_DIR, "tiered-engine.js"));
  TieredContextEngine = te.TieredContextEngine;
  l3AI = require(path.join(PLUGIN_DIR, "l3_ai_compressor.js"));
  memoryTier = require(path.join(PLUGIN_DIR, "memory_tiering.js"));
  crossAgent = require(path.join(PLUGIN_DIR, "cross_agent_context.js"));
  realtimeMon = require(path.join(PLUGIN_DIR, "realtime_monitor.js"));
  compStats = require(path.join(PLUGIN_DIR, "compression_stats.js"));
  console.log("[v2.0] All modules loaded successfully");
} catch (e) {
  console.error(`Failed to load modules: ${e.message}`);
  process.exit(1);
}

// Parse args
const args = process.argv.slice(2);
const dryRun = args.includes("--dry-run");
const minSizeKb = args.includes("--min-size") ? parseInt(args[args.indexOf("--min-size") + 1]) || 300 : 300;
const agentFilter = args.includes("--agent") ? args[args.indexOf("--agent") + 1] : null;
const taskArg = args.includes("--task") ? args[args.indexOf("--task") + 1] : "scan";

console.log(`\n========================================`);
console.log(`TieredContextEngine Standalone Scanner v2.0`);
console.log(`========================================`);
console.log(`Mode: ${dryRun ? "DRY RUN" : "LIVE"}`);
console.log(`Task: ${taskArg}`);
console.log(`========================================\n`);

const logger = {
  info: (...a) => console.log(`[${new Date().toISOString().slice(11,19)}]`, ...a),
  warn: (...a) => console.warn(`[${new Date().toISOString().slice(11,19)}] WARN:`, ...a),
  error: (...a) => console.error(`[${new Date().toISOString().slice(11,19)}] ERROR:`, ...a)
};

const engine = new TieredContextEngine({ openclawVersion: "1.0.0", logger });

function estimateTokens(text) {
  if (!text || typeof text !== "string") return 0;
  const chinese = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const english = (text.match(/[a-zA-Z]/g) || []).length;
  const other = text.length - chinese - english;
  return Math.ceil(chinese * 1.5) + Math.ceil(english * 0.25) + other;
}

function findSessionsJson() {
  if (!fs.existsSync(AGENTS_DIR)) return [];
  const results = [];
  for (const entry of fs.readdirSync(AGENTS_DIR, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    if (agentFilter && entry.name !== agentFilter) continue;
    const sj = path.join(AGENTS_DIR, entry.name, "sessions", "sessions.json");
    if (fs.existsSync(sj)) results.push({ agent: entry.name, sessionsJson: sj });
  }
  return results;
}

function loadSessions(sj) {
  try {
    const sessions = JSON.parse(fs.readFileSync(sj, "utf-8"));
    return Object.entries(sessions)
      .filter(([, m]) => m.sessionFile && fs.existsSync(m.sessionFile))
      .map(([id, m]) => {
        const stat = fs.statSync(m.sessionFile);
        return { sessionId: id, sessionFile: m.sessionFile, sizeKb: stat.size / 1024, compactionCount: m.compactionCount || 0 };
      })
      .sort((a, b) => b.sizeKb - a.sizeKb);
  } catch { return []; }
}

function estimateSessionTokens(sf) {
  try {
    let total = 0;
    for (const line of fs.readFileSync(sf, "utf-8").split("\n")) {
      if (!line.trim()) continue;
      try {
        const obj = JSON.parse(line);
        if (obj.type === "message" && obj.message?.content) {
          const c = obj.message.content;
          if (Array.isArray(c)) c.forEach(b => { if (b.text) total += estimateTokens(b.text); });
          else if (typeof c === "string") total += estimateTokens(c);
        }
      } catch {}
    }
    return total;
  } catch { return 0; }
}

async function taskScan() {
  const start = Date.now();
  if (!fs.existsSync(BACKUP_DIR)) fs.mkdirSync(BACKUP_DIR, { recursive: true });
  
  const stats = { scanned: 0, candidates: 0, compacted: 0, skipped: 0, errors: 0, l1: 0, l2: 0, l3: 0, freed: 0 };
  
  for (const { agent, sessionsJson } of findSessionsJson()) {
    console.log(`\n== Agent: ${agent} ==`);
    const sessions = loadSessions(sessionsJson);
    const candidates = sessions.filter(s => s.sizeKb >= minSizeKb);
    stats.candidates += candidates.length;
    
    for (const s of candidates) {
      stats.scanned++;
      if (s.compactionCount >= 3) { stats.skipped++; continue; }
      
      const tokens = estimateSessionTokens(s.sessionFile);
      const ratio = tokens / 100000;
      console.log(`  ${path.basename(s.sessionFile)}: ${(s.sizeKb/1024).toFixed(2)}MB, ~${tokens.toFixed(0)} tokens (${ratio.toFixed(2)})`);
      
      if (dryRun) continue;
      
      try {
        const r = await engine.compact({ sessionFile: s.sessionFile, tokenBudget: 100000, currentTokenCount: tokens });
        if (r.compacted) {
          stats.compacted++;
          if (r.reason?.includes("l1")) stats.l1++;
          else if (r.reason?.includes("l2")) stats.l2++;
          else if (r.reason?.includes("l3")) stats.l3++;
          if (r.result?.tokensBefore && r.result?.tokensAfter) stats.freed += r.result.tokensBefore - r.result.tokensAfter;
        } else if (r.reason?.includes("needs_ai")) { stats.skipped++; }
        else stats.skipped++;
      } catch (e) { stats.errors++; }
    }
  }
  
  console.log(`\n========================================`);
  console.log(`SCAN COMPLETE (${((Date.now()-start)/1000).toFixed(1)}s)`);
  console.log(`Scanned: ${stats.scanned}, Candidates: ${stats.candidates}, Compacted: ${stats.compacted}, Skipped: ${stats.skipped}`);
  console.log(`L1: ${stats.l1}, L2: ${stats.l2}, L3: ${stats.l3}, Tokens freed: ~${stats.freed.toFixed(0)}`);
  console.log(`========================================\n`);
}

function taskStats() {
  console.log("=== COMPRESSION STATISTICS ===");
  console.log(JSON.stringify(engine.getStats(), null, 2));
  console.log("\n=== EFFICIENCY ===");
  console.log(JSON.stringify(compStats.getEfficiencyScore(), null, 2));
}

function taskReport() {
  const md = engine.generateReport('markdown');
  const reportsDir = path.join(WORKSPACE, "reports");
  if (!fs.existsSync(reportsDir)) fs.mkdirSync(reportsDir, { recursive: true });
  const f = path.join(reportsDir, `tiered_report_${new Date().toISOString().slice(0,10)}.md`);
  fs.writeFileSync(f, md);
  console.log(`Report saved to: ${f}`);
  console.log(md);
}

function taskDashboard() {
  console.log("=== DASHBOARD ===");
  console.log(JSON.stringify(engine.getDashboard(), null, 2));
  console.log("\n=== MEMORY STATS ===");
  console.log(JSON.stringify(engine.getMemoryStats(), null, 2));
  console.log("\n=== CLEANUP CANDIDATES ===");
  console.log(JSON.stringify(engine.listCleanupCandidates(), null, 2));
}

function taskCleanup() {
  const r = engine.cleanupMemories(dryRun);
  console.log(`Cleanup (dryRun=${dryRun}): Ephemeral=${r.ephemeral?.length||0}, Normal=${r.normal?.length||0}, Protected=${r.protected?.length||0}, Errors=${r.errors?.length||0}`);
  if (!dryRun && r.errors?.length) r.errors.forEach(e => console.log(`  Error: ${e.file}: ${e.error}`));
}

function taskMigrate() {
  const r = engine.migrateMemories(dryRun);
  console.log(`Migration (dryRun=${dryRun}): ${r.length} unknown memories`);
  r.forEach(m => console.log(`  ${m.basename} -> ${m.suggestedTier}`));
}

function taskAnalyze() {
  console.log("=== HISTORICAL ANALYSIS ===");
  const a = realtimeMon.analyzeHistory();
  console.log(JSON.stringify(a, null, 2));
  const adj = realtimeMon.adjustThresholds();
  if (adj.adjusted) console.log("Thresholds adjusted based on history");
}

async function main() {
  switch (taskArg) {
    case "scan": await taskScan(); break;
    case "stats": taskStats(); break;
    case "report": taskReport(); break;
    case "dashboard": taskDashboard(); break;
    case "cleanup": taskCleanup(); break;
    case "migrate": taskMigrate(); break;
    case "analyze": taskAnalyze(); break;
    default: console.error(`Unknown task: ${taskArg}`); process.exit(1);
  }
}

main().catch(e => { console.error(e); process.exit(1); });
