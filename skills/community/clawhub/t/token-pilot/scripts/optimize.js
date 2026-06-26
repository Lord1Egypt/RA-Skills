#!/usr/bin/env node
/**
 * Token Pilot — Auto-Optimizer
 * 
 * Scans OpenClaw environment and generates actionable optimization recommendations.
 * Covers: workspace cleanup, AGENTS.md compression, cron model routing,
 * agent model tiering, and config tuning.
 * 
 * Usage:
 *   node optimize.js              Full scan + recommendations
 *   node optimize.js --apply      Apply safe optimizations (workspace cleanup only)
 *   node optimize.js --cron       Cron job optimization only
 *   node optimize.js --agents     Agent model tiering only
 *   node optimize.js --workspace  Workspace file optimization only
 * 
 * Pure Node.js, zero dependencies, cross-platform.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const HOME = path.join(os.homedir(), '.openclaw');

function readSafe(p) { try { return fs.readFileSync(p, 'utf-8'); } catch { return null; } }
function estimateTokens(text) {
  let t = 0;
  for (const ch of text) t += ch.charCodeAt(0) > 0x2000 ? 1.5 : 0.25;
  return Math.round(t);
}
function formatBytes(b) {
  if (b < 1024) return b + 'B';
  return (b / 1024).toFixed(1) + 'KB';
}

// ─── Workspace Optimization ───

function optimizeWorkspace(wsDir, apply = false) {
  console.log('\n📂 Workspace Optimization:', wsDir);
  console.log('─'.repeat(60));
  
  if (!fs.existsSync(wsDir)) { console.log('  Directory not found'); return; }

  let savings = 0;
  const issues = [];

  // 1. Detect junk files in root
  const junkExts = ['.txt', '.js', '.cmd', '.bat', '.ps1', '.log', '.tmp', '.bak'];
  const rootFiles = fs.readdirSync(wsDir);
  const junkFiles = rootFiles.filter(f => {
    const ext = path.extname(f).toLowerCase();
    return junkExts.includes(ext) && fs.statSync(path.join(wsDir, f)).isFile();
  });
  
  if (junkFiles.length) {
    const junkSize = junkFiles.reduce((sum, f) => sum + fs.statSync(path.join(wsDir, f)).size, 0);
    issues.push({
      type: 'junk',
      severity: 'high',
      msg: `${junkFiles.length} non-essential files in workspace root (${formatBytes(junkSize)})`,
      detail: junkFiles.map(f => `    ${f} (${formatBytes(fs.statSync(path.join(wsDir, f)).size)})`),
      fix: 'Move to scripts/ subdirectory or delete',
      savings: estimateTokens(junkFiles.map(f => readSafe(path.join(wsDir, f)) || '').join('')),
    });

    if (apply) {
      const scriptsDir = path.join(wsDir, 'scripts');
      if (!fs.existsSync(scriptsDir)) fs.mkdirSync(scriptsDir, { recursive: true });
      for (const f of junkFiles) {
        const src = path.join(wsDir, f);
        const dst = path.join(scriptsDir, f);
        fs.renameSync(src, dst);
      }
      console.log(`  ✅ Moved ${junkFiles.length} files to scripts/`);
    }
  }

  // 2. BOOTSTRAP.md still exists?
  const bootstrap = path.join(wsDir, 'BOOTSTRAP.md');
  if (fs.existsSync(bootstrap)) {
    const size = fs.statSync(bootstrap).size;
    issues.push({
      type: 'bootstrap',
      severity: 'high',
      msg: `BOOTSTRAP.md still exists (${formatBytes(size)}) — injected every session after setup is done`,
      fix: 'Delete it (bootstrap is complete)',
      savings: estimateTokens(readSafe(bootstrap) || ''),
    });
    if (apply) {
      fs.unlinkSync(bootstrap);
      console.log('  ✅ Deleted BOOTSTRAP.md');
    }
  }

  // 3. AGENTS.md too large?
  const agentsMd = path.join(wsDir, 'AGENTS.md');
  const agentsContent = readSafe(agentsMd);
  if (agentsContent) {
    const tok = estimateTokens(agentsContent);
    if (tok > 500) {
      issues.push({
        type: 'agents-large',
        severity: 'medium',
        msg: `AGENTS.md is ${tok} tok (target: <400 tok)`,
        detail: [
          '    Common bloat: group chat rules, reaction guides, voice storytelling,',
          '    detailed heartbeat tutorials, emoji guides, code examples',
        ],
        fix: 'Keep only: startup rules, memory rules, safety rules, platform formatting',
        savings: Math.max(0, tok - 350),
      });
    }
  }

  // 4. MEMORY.md too large?
  const memMd = path.join(wsDir, 'MEMORY.md');
  const memContent = readSafe(memMd);
  if (memContent) {
    const tok = estimateTokens(memContent);
    if (tok > 800) {
      issues.push({
        type: 'memory-large',
        severity: 'medium',
        msg: `MEMORY.md is ${tok} tok (target: <800 tok)`,
        fix: 'Distill to bullet points, archive old entries to memory/ daily files',
        savings: Math.max(0, tok - 400),
      });
    }
  }

  // 5. Check total injection size
  const mdFiles = rootFiles.filter(f => f.endsWith('.md') && fs.statSync(path.join(wsDir, f)).isFile());
  let totalTok = 0;
  for (const f of mdFiles) {
    const c = readSafe(path.join(wsDir, f));
    if (c) totalTok += estimateTokens(c);
  }
  if (totalTok > 2500) {
    issues.push({
      type: 'total-large',
      severity: 'low',
      msg: `Total workspace injection: ${totalTok} tok (target: <2000)`,
      fix: 'Compress individual files per recommendations above',
      savings: Math.max(0, totalTok - 2000),
    });
  }

  // Report
  if (!issues.length) {
    console.log('  ✅ Workspace is well optimized!');
    return;
  }

  for (const issue of issues) {
    const icon = issue.severity === 'high' ? '🔴' : issue.severity === 'medium' ? '🟡' : '🔵';
    console.log(`\n  ${icon} ${issue.msg}`);
    if (issue.detail) issue.detail.forEach(d => console.log(d));
    console.log(`     Fix: ${issue.fix}`);
    console.log(`     Est. savings: ~${issue.savings} tok/session`);
    savings += issue.savings;
  }

  console.log(`\n  💰 Total potential savings: ~${savings} tok/session`);
}

// ─── Cron Optimization ───

function optimizeCron() {
  console.log('\n⏰ Cron Job Optimization');
  console.log('─'.repeat(60));

  const cronPath = path.join(HOME, 'cron/jobs.json');
  const raw = readSafe(cronPath);
  if (!raw) { console.log('  No cron jobs found'); return; }

  let data;
  try { data = JSON.parse(raw); } catch { console.log('  Failed to parse jobs.json'); return; }
  
  const jobs = data.jobs || [];
  if (!jobs.length) { console.log('  No cron jobs'); return; }

  const lightKeywords = /inbox|dashboard|status|scan.*inbox|update.*status|patrol|check(?!.*brief)|daily.*pull/i;
  const heavyKeywords = /brief|morning|evening|architect|design|strateg|deep.*analysis|comprehensive|synthesis/i;
  const noLightKeywords = /brief|morning|evening|web.*search|competitor|content.*writ|deep.*dive|analysis/i;

  let recommendations = 0;

  console.log('\n  Job'.padEnd(30) + 'Model'.padEnd(24) + 'Light  Prompt  Issues');
  console.log('  ' + '─'.repeat(75));

  for (const job of jobs) {
    if (!job.enabled) continue;

    const msg = job.payload?.message || '';
    const model = job.payload?.model || '(agent default)';
    const hasLight = job.payload?.lightContext === true;
    const promptLen = msg.length;
    const issues = [];

    // Check: should be light? (not for jobs needing full context like briefs/search)
    if (!hasLight && lightKeywords.test(msg) && !noLightKeywords.test(msg)) {
      issues.push('→ add lightContext');
      recommendations++;
    }

    // Check: model routing
    if (!job.payload?.model) {
      if (lightKeywords.test(msg)) {
        issues.push('→ use cheap model');
        recommendations++;
      }
    } else if (model.includes('opus') && !heavyKeywords.test(msg)) {
      issues.push('→ downgrade from Opus');
      recommendations++;
    }

    // Check: prompt too long?
    if (promptLen > 300) {
      issues.push(`→ compress prompt (${promptLen} chars)`);
      recommendations++;
    }

    // Check: consecutive errors
    if (job.state?.consecutiveErrors > 2) {
      issues.push(`→ ${job.state.consecutiveErrors} consecutive errors!`);
      recommendations++;
    }

    const lightStr = hasLight ? 'YES' : 'no';
    const promptStr = promptLen > 200 ? `${promptLen}⚠️` : `${promptLen}`;
    const issueStr = issues.join('; ') || '✅';

    console.log(`  ${job.name.padEnd(28)}${model.substring(0, 22).padEnd(24)}${lightStr.padEnd(7)}${promptStr.padEnd(8)}${issueStr}`);
  }

  if (recommendations === 0) {
    console.log('\n  ✅ Cron jobs are well optimized!');
  } else {
    console.log(`\n  💡 ${recommendations} recommendation(s) found`);
    console.log('  Apply via: openclaw cron edit <job-id> --model <model> --light-context');
  }
}

// ─── Agent Model Tiering ───

function optimizeAgents() {
  console.log('\n🤖 Agent Model Tiering');
  console.log('─'.repeat(60));

  const configRaw = readSafe(path.join(HOME, 'openclaw.json'));
  if (!configRaw) { console.log('  openclaw.json not found'); return; }

  // Extract agent list with models (only from agents.list entries)
  const listStart = configRaw.indexOf('"list"');
  if (listStart === -1) { console.log('  No agents.list found'); return; }
  // Find the matching closing bracket for the list array
  let depth = 0, listEnd = listStart;
  for (let i = configRaw.indexOf('[', listStart); i < configRaw.length; i++) {
    if (configRaw[i] === '[') depth++;
    if (configRaw[i] === ']') { depth--; if (depth === 0) { listEnd = i; break; } }
  }
  const listSection = [null, configRaw.substring(listStart, listEnd + 1)];
  const agentPattern = /"id"\s*:\s*"([^"]+)"[\s\S]*?"primary"\s*:\s*"([^"]+)"/g;
  const agents = [];
  let m;
  while ((m = agentPattern.exec(listSection[1])) !== null) {
    agents.push({ id: m[1], model: m[2] });
  }

  if (agents.length <= 1) {
    console.log('  Single agent setup — no tiering needed');
    return;
  }

  // Find the most expensive model
  const modelTier = (model) => {
    if (/opus/i.test(model)) return 3;
    if (/gpt-5|sonnet/i.test(model)) return 2;
    if (/gemini|haiku|glm|kimi/i.test(model)) return 1;
    return 2;
  };

  const mainAgent = agents.find(a => a.id === 'main');
  const teamAgents = agents.filter(a => a.id !== 'main');
  
  let allSameTier = true;
  const mainTier = mainAgent ? modelTier(mainAgent.model) : 3;

  console.log(`\n  ${'Agent'.padEnd(22)}${'Model'.padEnd(30)}Tier  Recommendation`);
  console.log('  ' + '─'.repeat(70));

  for (const a of agents) {
    const tier = modelTier(a.model);
    const isMain = a.id === 'main';
    let rec = '✅';

    if (isMain) {
      rec = 'Keep best (your direct interaction)';
    } else if (tier === mainTier && mainTier >= 3) {
      rec = '→ Downgrade to mid-tier (saves 70-80%)';
      allSameTier = false;
    } else if (tier >= 3) {
      rec = '→ Downgrade to mid-tier';
      allSameTier = false;
    }

    const tierLabel = tier === 3 ? 'TOP' : tier === 2 ? 'MID' : 'LOW';
    console.log(`  ${a.id.padEnd(22)}${a.model.padEnd(30)}${tierLabel.padEnd(6)}${rec}`);
  }

  if (allSameTier && teamAgents.every(a => modelTier(a.model) < mainTier)) {
    console.log('\n  ✅ Agent models are well tiered!');
  } else if (!allSameTier) {
    console.log('\n  💡 Strategy: main agent = best model, team agents = mid-tier');
    console.log('  Team agents still have quality interaction; use /model to temporarily upgrade if needed.');
    console.log('  Cron jobs can override with even cheaper models per-job.');
  }
}

// ─── AGENTS.md Template ───

function showAgentsTemplate() {
  console.log('\n📝 Optimized AGENTS.md Template (~300 tok)');
  console.log('─'.repeat(60));
  console.log(`
# AGENTS.md

## Every Session
1. Read SOUL.md — who you are
2. Read USER.md — who you're helping
3. Read memory/YYYY-MM-DD.md (today + yesterday)
4. Main session only: Also read MEMORY.md

## Memory
- Daily logs: memory/YYYY-MM-DD.md — raw notes
- Long-term: MEMORY.md — curated (main session only, never leak in groups)
- "Remember this" → write to file. Mental notes don't survive restarts.
- Periodically distill daily logs into MEMORY.md.

## Safety
- Never exfiltrate private data. trash > rm. Ask before external actions.
- In groups: participate, don't dominate. Stay silent when no value to add.

## Heartbeats
- Read HEARTBEAT.md and follow strictly. Nothing to do → HEARTBEAT_OK.
- Quiet hours (23:00-08:00): skip unless urgent.

## Tools
Skills provide tools → check SKILL.md when needed.
`);
  console.log('  Copy this to replace a bloated default AGENTS.md (typically saves ~1500 tok)');
}

// ─── Main ───

const args = process.argv.slice(2);
const mode = args[0] || '';
const apply = args.includes('--apply');

if (mode === '--help' || mode === '-h') {
  console.log(`
Token Pilot — Auto-Optimizer

Usage:
  node optimize.js                Full scan + all recommendations
  node optimize.js --apply        Apply safe auto-fixes (workspace cleanup only)
  node optimize.js --workspace    Workspace optimization only
  node optimize.js --cron         Cron job optimization only
  node optimize.js --agents       Agent model tiering only
  node optimize.js --template     Show optimized AGENTS.md template
`);
  process.exit(0);
}

console.log('🚀 Token Pilot — Auto-Optimizer');
console.log('═'.repeat(60));

if (mode === '--workspace') {
  optimizeWorkspace(path.join(HOME, 'workspace'), apply);
} else if (mode === '--cron') {
  optimizeCron();
} else if (mode === '--agents') {
  optimizeAgents();
} else if (mode === '--template') {
  showAgentsTemplate();
} else {
  // Full scan
  optimizeWorkspace(path.join(HOME, 'workspace'), apply);
  
  // Scan additional workspaces
  const entries = fs.readdirSync(HOME).filter(d => d.startsWith('workspace-') && fs.statSync(path.join(HOME, d)).isDirectory());
  for (const ws of entries) {
    optimizeWorkspace(path.join(HOME, ws), apply);
  }

  optimizeCron();
  optimizeAgents();

  console.log('\n' + '═'.repeat(60));
  console.log('Run with --template to see optimized AGENTS.md');
  console.log('Run with --apply to auto-fix workspace issues');
}
