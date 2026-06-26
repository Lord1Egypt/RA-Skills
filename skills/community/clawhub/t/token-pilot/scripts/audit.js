#!/usr/bin/env node
/**
 * Token Pilot — Workspace & Config Auditor
 * 
 * Usage:
 *   node audit.js [workspace-path]         Audit workspace files
 *   node audit.js --skills [skills-dir]    Audit installed skills
 *   node audit.js --config                 Check openclaw.json optimizations
 *   node audit.js --synergy                Plugin synergy check
 *   node audit.js --all                    Run all audits
 * 
 * Pure Node.js, zero dependencies, cross-platform.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const CHARS_PER_TOKEN = 4; // rough estimate for mixed en/zh
const OPENCLAW_HOME = path.join(os.homedir(), '.openclaw');

// ─── Helpers ───

function estimateTokens(text) {
  // CJK chars ≈ 1.5 tok each, ASCII ≈ 0.25 tok each
  let tokens = 0;
  for (const ch of text) {
    tokens += ch.charCodeAt(0) > 0x2000 ? 1.5 : 0.25;
  }
  return Math.round(tokens);
}

function readSafe(p) {
  try { return fs.readFileSync(p, 'utf-8'); } catch { return null; }
}

function formatBytes(b) {
  if (b < 1024) return b + 'B';
  if (b < 1024 * 1024) return (b / 1024).toFixed(1) + 'KB';
  return (b / (1024 * 1024)).toFixed(1) + 'MB';
}

function getConfigValue(raw, key) {
  // Search entire file for any occurrence of "key": value
  // Handles nested JSON, escaped quotes, various spacing
  const patterns = [
    new RegExp(`["']${key}["']\\s*:\\s*"([^"]+)"`),
    new RegExp(`["']${key}["']\\s*:\\s*(\\d+)`),
    new RegExp(`["']${key}["']\\s*:\\s*(true|false)`),
  ];
  for (const re of patterns) {
    const m = raw.match(re);
    if (m) return m[1];
  }
  return null;
}

// ─── Workspace Audit ───

// Bootstrap files: OpenClaw ONLY loads these specific named files (whitelist, NOT all files)
// Source: workspace-DGJIk8rw.js loadWorkspaceBootstrapFiles()
const BOOTSTRAP_FILES = [
  'AGENTS.md', 'SOUL.md', 'TOOLS.md', 'IDENTITY.md',
  'USER.md', 'HEARTBEAT.md', 'BOOTSTRAP.md', 'MEMORY.md', 'memory.md'
];

function auditWorkspace(dir) {
  console.log('\n📂 Workspace Audit:', dir);
  console.log('─'.repeat(60));

  if (!fs.existsSync(dir)) {
    console.log('  ❌ Directory not found');
    return;
  }

  // Only scan actual bootstrap files (OpenClaw whitelist, not all files in directory)
  // Note: MEMORY.md and memory.md are the same on case-insensitive filesystems (Windows)
  const seen = new Set();
  const files = [];
  for (const f of BOOTSTRAP_FILES) {
    const fp = path.join(dir, f);
    if (fs.existsSync(fp)) {
      // On case-insensitive FS, deduplicate by resolving to real path
      try {
        const real = fs.realpathSync.native(fp);
        if (!seen.has(real)) {
          seen.add(real);
          files.push(f);
        }
      } catch {
        if (!seen.has(f.toLowerCase())) {
          seen.add(f.toLowerCase());
          files.push(f);
        }
      }
    }
  }

  // Also detect non-bootstrap files in root (these are NOT injected but may indicate workspace bloat)
  const allFiles = fs.readdirSync(dir).filter(f => {
    const ext = path.extname(f).toLowerCase();
    return ['.md', '.txt', '.js', '.json', '.yaml', '.yml'].includes(ext);
  });
  const nonBootstrapFiles = allFiles.filter(f => !BOOTSTRAP_FILES.includes(f));

  let totalSize = 0, totalTokens = 0;
  const rows = [];
  const issues = [];

  for (const f of files) {
    const fp = path.join(dir, f);
    const stat = fs.statSync(fp);
    if (!stat.isFile()) continue;

    const content = readSafe(fp);
    if (!content) continue;

    const tokens = estimateTokens(content);
    totalSize += stat.size;
    totalTokens += tokens;

    const flag = tokens > 3000 ? '⚠️' : tokens > 1000 ? '⚡' : '✅';
    rows.push({ name: f, size: stat.size, tokens, flag });

    if (tokens > 3000) {
      issues.push(`  ⚠️  ${f} (${tokens} tok) — consider splitting or compressing`);
    }
  }

  // Sort by tokens desc
  rows.sort((a, b) => b.tokens - a.tokens);

  console.log('\n  File'.padEnd(35) + 'Size'.padEnd(10) + 'Est.Tokens'.padEnd(12) + 'Status');
  console.log('  ' + '─'.repeat(55));
  for (const r of rows) {
    console.log(
      `  ${r.name.padEnd(33)}${formatBytes(r.size).padEnd(10)}${String(r.tokens).padEnd(12)}${r.flag}`
    );
  }

  console.log(`\n  Total: ${formatBytes(totalSize)}, ~${totalTokens} tokens injected per session`);

  // Check bootstrapMaxChars
  const configRaw = readSafe(path.join(OPENCLAW_HOME, 'openclaw.json'));
  if (configRaw) {
    const maxChars = parseInt(getConfigValue(configRaw, 'bootstrapMaxChars') || '0');
    const totalMaxChars = parseInt(getConfigValue(configRaw, 'bootstrapTotalMaxChars') || '0');
    if (maxChars > 0) {
      console.log(`\n  bootstrapMaxChars: ${maxChars} (files > this get truncated)`);
      const truncated = rows.filter(r => r.size > maxChars);
      if (truncated.length) {
        console.log(`  ⚠️  ${truncated.length} file(s) will be truncated:`);
        truncated.forEach(r => console.log(`      ${r.name} (${formatBytes(r.size)} > ${formatBytes(maxChars)})`));
      }
    }
    if (totalMaxChars > 0) {
      console.log(`  bootstrapTotalMaxChars: ${totalMaxChars}`);
      if (totalSize > totalMaxChars) {
        console.log(`  ⚠️  Total ${formatBytes(totalSize)} exceeds limit — some files will be dropped!`);
      }
    }
  }

  if (issues.length) {
    console.log('\n  Issues:');
    issues.forEach(i => console.log(i));
  }

  // Check for non-bootstrap files in workspace root (these are NOT injected but suggest workspace needs cleanup)
  if (nonBootstrapFiles.length) {
    console.log(`\n  📁 Non-bootstrap files in root (NOT injected, but consider moving to subdirs):`);
    nonBootstrapFiles.forEach(f => console.log(`      ${f}`));
  }
}

// ─── Skills Audit ───

function auditSkills(dir) {
  console.log('\n🔧 Skills Audit:', dir);
  console.log('─'.repeat(60));

  if (!fs.existsSync(dir)) {
    console.log('  ❌ Directory not found');
    return;
  }

  const skills = fs.readdirSync(dir).filter(d =>
    fs.existsSync(path.join(dir, d, 'SKILL.md'))
  );

  let totalTokens = 0;
  const rows = [];

  for (const s of skills) {
    const fp = path.join(dir, s, 'SKILL.md');
    const content = readSafe(fp);
    if (!content) continue;

    const tokens = estimateTokens(content);
    totalTokens += tokens;

    // Extract description from frontmatter
    const descMatch = content.match(/description:\s*(.+?)(?:\n|$)/);
    const desc = descMatch ? descMatch[1].substring(0, 50) : '';

    rows.push({ name: s, tokens, desc });
  }

  rows.sort((a, b) => b.tokens - a.tokens);

  console.log('\n  Skill'.padEnd(35) + 'SKILL.md Tokens'.padEnd(18) + 'Description');
  console.log('  ' + '─'.repeat(70));
  for (const r of rows) {
    const flag = r.tokens > 3000 ? '⚠️' : '';
    console.log(`  ${r.name.padEnd(33)}${String(r.tokens).padEnd(18)}${r.desc}${flag}`);
  }

  console.log(`\n  Total: ${skills.length} skills`);
  console.log(`  Note: Only descriptions (~50-100 tok each) are always loaded.`);
  console.log(`  SKILL.md files are loaded on-demand when the skill is activated.`);

  const heavy = rows.filter(r => r.tokens > 3000);
  if (heavy.length) {
    console.log(`\n  ⚠️  Heavy skills (>3000 tok when loaded):`);
    heavy.forEach(r => console.log(`      ${r.name}: ${r.tokens} tok — consider splitting into SKILL.md + references/`));
  }
}

// ─── Config Audit ───

function auditConfig() {
  console.log('\n⚙️  Config Audit: openclaw.json');
  console.log('─'.repeat(60));

  const configPath = path.join(OPENCLAW_HOME, 'openclaw.json');
  const raw = readSafe(configPath);
  if (!raw) {
    console.log('  ❌ openclaw.json not found');
    return;
  }

  const checks = [
    { key: 'bootstrapMaxChars',     recommended: '12000',     desc: 'Single file injection limit' },
    { key: 'bootstrapTotalMaxChars', recommended: '20000',    desc: 'Total injection limit' },
  ];

  let score = 0;
  for (const c of checks) {
    const val = getConfigValue(raw, c.key);
    const ok = val !== null;
    if (ok) score++;
    const status = ok ? `✅ ${c.key} = ${val}` : `❌ ${c.key} — missing (recommend: ${c.recommended})`;
    console.log(`  ${status}`);
    if (!ok) console.log(`     → ${c.desc}`);
  }

  // Check heartbeat
  const hbEvery = raw.match(/"every"\s*:\s*"([^"]+)"/);
  if (hbEvery) {
    console.log(`  ✅ heartbeat.every = ${hbEvery[1]}`);
    score++;
  } else {
    console.log(`  ❌ heartbeat.every — missing (recommend: "55m" for cache warm-keeping)`);
  }

  // Check activeHours
  const activeHours = raw.includes('activeHours');
  if (activeHours) {
    console.log(`  ✅ heartbeat.activeHours configured`);
    score++;
  } else {
    console.log(`  ❌ heartbeat.activeHours — missing (saves nighttime heartbeat calls)`);
  }

  // Check compaction
  const compaction = getConfigValue(raw, 'mode');
  if (raw.includes('"compaction"')) {
    console.log(`  ✅ compaction configured`);
    score++;
  } else {
    console.log(`  ❌ compaction — missing (recommend: { "mode": "safeguard" })`);
  }

  // Check lightContext in cron
  const cronPath = path.join(OPENCLAW_HOME, 'cron/jobs.json');
  const cronRaw = readSafe(cronPath);
  if (cronRaw) {
    const lightCount = (cronRaw.match(/"lightContext"\s*:\s*true/g) || []).length;
    const totalJobs = (cronRaw.match(/"id"\s*:/g) || []).length;
    console.log(`\n  Cron: ${lightCount}/${totalJobs} jobs use lightContext`);
    
    // Check model routing
    const modelOverrides = (cronRaw.match(/"model"\s*:\s*"([^"]+)"/g) || []);
    const opusJobs = modelOverrides.filter(m => m.includes('opus')).length;
    const cheapJobs = modelOverrides.filter(m => !m.includes('opus')).length;
    console.log(`  Cron models: ${opusJobs} Opus, ${cheapJobs} cheaper, ${totalJobs - modelOverrides.length} using agent default`);
  }

  const total = checks.length + 3; // checks + heartbeat.every + activeHours + compaction
  console.log(`\n  Optimization Score: ${score}/${total}`);
  if (score >= total - 1) console.log('  🏆 Well optimized!');
  else if (score >= total - 2) console.log('  ⚡ Good, but room for improvement');
  else console.log('  ⚠️  Significant savings possible — apply recommendations above');
}

// ─── Plugin Synergy Audit ───

function auditSynergy() {
  console.log('\n🔗 Plugin Synergy Check');
  console.log('─'.repeat(60));

  const skillsDir = path.join(OPENCLAW_HOME, 'skills');
  const plugins = [
    {
      name: 'qmd',
      check: () => {
        // Check qmd skill or builtin
        const builtinQmd = path.join(process.env.APPDATA || '', 'npm/node_modules/openclaw/skills/qmd/SKILL.md');
        const localQmd = path.join(skillsDir, 'qmd', 'SKILL.md');
        return fs.existsSync(localQmd) || fs.existsSync(builtinQmd);
      },
      benefit: 'Search-before-read: find exact file+line via index instead of reading multiple full files',
      fallback: 'grep / Select-String / find with targeted patterns',
      savings: '~500-2000 tok per search (avoid reading 3-5 irrelevant files)',
    },
    {
      name: 'smart-agent-memory',
      check: () => fs.existsSync(path.join(skillsDir, 'smart-agent-memory', 'scripts', 'memory-cli.js')),
      benefit: 'Recall past solutions: skip re-investigation of known issues, learn from mistakes',
      fallback: 'memory_search tool + manual MEMORY.md / memory/*.md reads',
      savings: '~1000-5000 tok per avoided re-investigation',
    },
    {
      name: 'coding-lead',
      check: () => fs.existsSync(path.join(skillsDir, 'coding-lead', 'SKILL.md')),
      benefit: 'Context-file pattern: write context to disk, lean ACP prompt saves ~90% vs embedding',
      fallback: 'Embed context in spawn prompt (works but costs more tokens)',
      savings: '~3000-8000 tok per ACP spawn',
    },
    {
      name: 'multi-search-engine',
      check: () => fs.existsSync(path.join(skillsDir, 'multi-search-engine', 'SKILL.md')),
      benefit: 'Search economy: targeted engine selection, avoid redundant multi-engine searches',
      fallback: 'web_search (native Brave) or tavily exec',
      savings: '~200-500 tok per optimized search',
    },
  ];

  let synergies = 0;
  for (const p of plugins) {
    const installed = p.check();
    if (installed) {
      synergies++;
      console.log(`  ✅ ${p.name}`);
      console.log(`     Synergy: ${p.benefit}`);
      console.log(`     Est. savings: ${p.savings}`);
    } else {
      console.log(`  ⬜ ${p.name} (not installed)`);
      console.log(`     Fallback: ${p.fallback}`);
    }
    console.log();
  }

  // Check team workspace
  const teamWs = path.join(OPENCLAW_HOME, 'workspace-team');
  if (fs.existsSync(teamWs)) {
    console.log('  📋 Team Workspace Detected');
    
    // Count agent SOULs and their sizes
    const agentsDir = path.join(teamWs, 'agents');
    if (fs.existsSync(agentsDir)) {
      const agents = fs.readdirSync(agentsDir).filter(d =>
        fs.existsSync(path.join(agentsDir, d, 'SOUL.md'))
      );
      let totalSoulTokens = 0;
      let hasRefs = 0;
      for (const a of agents) {
        const soul = readSafe(path.join(agentsDir, a, 'SOUL.md'));
        if (soul) totalSoulTokens += estimateTokens(soul);
        if (fs.existsSync(path.join(agentsDir, a, 'references'))) hasRefs++;
      }
      console.log(`     ${agents.length} agents, total SOUL.md: ~${totalSoulTokens} tok`);
      console.log(`     ${hasRefs}/${agents.length} use references/ pattern (on-demand methodology)`);
      
      if (totalSoulTokens > agents.length * 600) {
        console.log(`     ⚠️  Average ${Math.round(totalSoulTokens/agents.length)} tok/agent — target <600 tok each`);
      } else {
        console.log(`     ✅ Average ${Math.round(totalSoulTokens/agents.length)} tok/agent — well optimized`);
      }
    }

    // Check shared dir size
    const sharedDir = path.join(teamWs, 'shared');
    if (fs.existsSync(sharedDir)) {
      let sharedFiles = 0, sharedSize = 0;
      const walk = (dir) => {
        for (const f of fs.readdirSync(dir, { withFileTypes: true })) {
          if (f.isDirectory()) walk(path.join(dir, f.name));
          else if (f.name.endsWith('.md')) {
            sharedFiles++;
            sharedSize += fs.statSync(path.join(dir, f.name)).size;
          }
        }
      };
      walk(sharedDir);
      console.log(`     shared/: ${sharedFiles} files, ${formatBytes(sharedSize)}`);
      console.log(`     (Not injected at startup — loaded on-demand via qmd or direct read)`);
    }
  }

  console.log(`  Synergy Score: ${synergies}/${plugins.length} plugins active`);
}

// ─── Main ───

const args = process.argv.slice(2);
const mode = args[0] || '';

if (mode === '--help' || mode === '-h') {
  console.log(`
Token Pilot — Workspace & Config Auditor

Usage:
  node audit.js [workspace-path]         Audit workspace files
  node audit.js --skills [skills-dir]    Audit installed skills
  node audit.js --config                 Check openclaw.json optimizations
  node audit.js --synergy                Plugin synergy check
  node audit.js --all                    Run all audits
`);
  process.exit(0);
}

if (mode === '--config') {
  auditConfig();
} else if (mode === '--skills') {
  const dir = args[1] || path.join(OPENCLAW_HOME, 'skills');
  auditSkills(dir);
} else if (mode === '--synergy') {
  auditSynergy();
} else if (mode === '--all') {
  // Auto-discover all workspaces
  auditWorkspace(path.join(OPENCLAW_HOME, 'workspace'));
  try {
    fs.readdirSync(OPENCLAW_HOME)
      .filter(d => d.startsWith('workspace-') && fs.statSync(path.join(OPENCLAW_HOME, d)).isDirectory())
      .forEach(d => auditWorkspace(path.join(OPENCLAW_HOME, d)));
  } catch {}
  auditSkills(path.join(OPENCLAW_HOME, 'skills'));
  auditConfig();
  auditSynergy();
} else {
  // Explicit path or auto-discover all
  if (args[0] && !args[0].startsWith('-')) {
    auditWorkspace(args[0]);
  } else {
    auditWorkspace(path.join(OPENCLAW_HOME, 'workspace'));
    try {
      fs.readdirSync(OPENCLAW_HOME)
        .filter(d => d.startsWith('workspace-') && fs.statSync(path.join(OPENCLAW_HOME, d)).isDirectory())
        .forEach(d => auditWorkspace(path.join(OPENCLAW_HOME, d)));
    } catch {}
  }
}
