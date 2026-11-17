#!/usr/bin/env node

/**
 * cybernetic-thinking — skill installer
 *
 * UX mirrors `npx impeccable skills install` using @clack/prompts:
 *   1. Scan for known AI coding agents.
 *   2. Show detected agents with paths.
 *   3. Prompt: detected-only or customize selection.
 *   4. Prompt: project or global install location.
 *   5. Link the skill into each selected agent's skills directory.
 *
 * Non-interactive fallback (CI, piped stdin): installs for all detected
 * agents at global scope.
 *
 * Flags (for scripting / CI):
 *   --agents, -a <slugs>   Comma-separated agent slugs (skip prompts)
 *   --path <dir>           Install into a custom directory
 *   --global, -g           Global scope only
 *   --local, -l            Project scope only
 *   --yes, -y              Skip prompts (use detected agents)
 *   --copy, -c             Copy files instead of symlinking (also the automatic
 *                         fallback when junction creation fails)
 *   --count               Print the number of known agents and exit
 *   --force, -f            Overwrite existing links
 *   --help, -h             Show help
 *
 * Agent registry (0.6.0): each agent may declare multiple candidate roots so
 * detection survives version/variant drift (e.g. Kilo reads both ~/.kilo and
 * ~/.kilocode; Trae + Trae Work share ~/.trae-cn). Two cross-agent targets are
 * included: `.agents` (the Agent Skills standard, read by Trae/Kilo/Claude and
 * others) — this IS the user-level shared folder requested.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const pkg = require(path.join(__dirname, '..', 'package.json'));
const skillName = pkg.name;
const skillDir = path.join(__dirname, '..');

// ─────────────────────────────────────────────────────────────────────────────
// Agent registry
// Detection: <base>/<root> exists (global = ~/ ; project = ./ )
// Install:   <base>/<root>/skills/<skillName>
// `roots` is an ordered list — the first existing root wins for detection; if
// none exist, the first root is used as the install target.
// ─────────────────────────────────────────────────────────────────────────────

const agents = [
  { name: 'Claude Code',    slug: 'claude',    roots: ['.claude'] },
  { name: 'Codex CLI',      slug: 'codex',     roots: ['.codex'] },
  { name: 'Cursor',         slug: 'cursor',    roots: ['.cursor'] },
  { name: 'Gemini CLI',     slug: 'gemini',    roots: ['.gemini'] },
  { name: 'GitHub Copilot', slug: 'copilot',   roots: ['.copilot'] },
  { name: 'Kilo',           slug: 'kilo',      roots: ['.kilo', '.kilocode'] },
  { name: 'Aider',          slug: 'aider',     roots: ['.aider'] },
  { name: 'Windsurf',       slug: 'windsurf',  roots: ['.windsurf'] },
  { name: 'Zed',            slug: 'zed',        roots: ['.zed'] },
  // Added in 0.6.0
  { name: 'WorkBuddy',      slug: 'workbuddy', roots: ['.workbuddy'] },
  { name: 'Trae',           slug: 'trae',      roots: ['.trae', '.trae-cn'] }, // Trae Work shares ~/.trae-cn
  { name: 'Agent Skills standard', slug: 'agents', roots: ['.agents'] }, // cross-agent ~/.agents/skills — the user-level shared folder
];

const SKILL_SUBDIR = 'skills';

// ─────────────────────────────────────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────────────────────────────────────

function dirExists(p) {
  try { return fs.statSync(p).isDirectory(); } catch { return false; }
}

function isTTY() {
  return process.stdin.isTTY === true && process.stdout.isTTY === true;
}

function relHome(p) {
  const home = os.homedir();
  if (p === home) return '~';
  if (p.startsWith(home)) return '~' + p.slice(home.length).replace(/\\/g, '/');
  return p.replace(/\\/g, '/');
}

// All candidate roots for an agent at a given scope.
function agentRoots(a, scope) {
  const base = scope === 'global' ? os.homedir() : process.cwd();
  return a.roots.map(r => path.join(base, r));
}

// First existing root at this scope, or null if none detected.
function detectRoot(a, scope) {
  for (const d of agentRoots(a, scope)) {
    if (dirExists(d)) return d;
  }
  return null;
}

// Roots to install into: prefer an existing root, else the primary (first) root.
function installRoots(a, scope) {
  const roots = agentRoots(a, scope);
  const existing = roots.find(d => dirExists(d));
  return existing ? [existing] : [roots[0]];
}

function globalDetect(a)  { return detectRoot(a, 'global'); }
function projectDetect(a) { return detectRoot(a, 'project'); }

function detectAll() {
  const found = [];
  for (const a of agents) {
    const gd = globalDetect(a);
    const pd = projectDetect(a);
    if (gd) found.push({ agent: a, scope: 'global',  dir: gd });
    if (pd) found.push({ agent: a, scope: 'project', dir: pd });
  }
  return found;
}

function linkSkill(targetParentDir, { force = false, copy = false } = {}) {
  const dest = path.join(targetParentDir, skillName);
  const label = relHome(targetParentDir);
  if (fs.existsSync(dest)) {
    if (!force) { console.log(`  [skip] ${label} (already installed)`); return 'skipped'; }
    try { fs.rmSync(dest, { recursive: true, force: true }); } catch (e) {
      console.log(`  [fail] ${label} (${e.message})`); return 'failed';
    }
  }
  try {
    fs.mkdirSync(targetParentDir, { recursive: true });
    if (copy) {
      fs.cpSync(skillDir, dest, { recursive: true });
      console.log(`  [ok]   ${label} (copied)`);
    } else {
      try {
        fs.symlinkSync(skillDir, dest, 'junction');
        console.log(`  [ok]   ${label} (linked)`);
      } catch (e) {
        // Junction creation can fail on locked-down or non-admin Windows, and some
        // agents don't resolve junctions at runtime. Fall back to a real copy so the
        // install still succeeds.
        console.log(`  [warn] ${label} symlink failed (${e.code || e.message}); copying instead`);
        fs.cpSync(skillDir, dest, { recursive: true });
        console.log(`  [ok]   ${label} (copied as fallback)`);
      }
    }
    return 'installed';
  } catch (e) {
    console.log(`  [fail] ${label} (${e.message})`);
    console.log(`         try manually: cp -r "${skillDir}" "${dest}"`);
    return 'failed';
  }
}

function doInstall(targetAgents, scope, force, copy) {
  let installed = 0, skipped = 0, failed = 0;
  for (const a of targetAgents) {
    const dirs = [];
    if (scope === 'global' || scope === 'all')  dirs.push(...installRoots(a, 'global'));
    if (scope === 'project' || scope === 'all') dirs.push(...installRoots(a, 'project'));
    for (const d of dirs) {
      const r = linkSkill(path.join(d, SKILL_SUBDIR), { force, copy });
      if (r === 'installed') installed++; else if (r === 'skipped') skipped++; else failed++;
    }
  }
  return { installed, skipped, failed };
}

// ─────────────────────────────────────────────────────────────────────────────
// Help
// ─────────────────────────────────────────────────────────────────────────────

function printHelp() {
  console.log(`Usage: npx ${skillName} install [options]

Scans for installed AI coding agents and links this skill into their skills
directories. Runs interactively when stdin is a TTY; otherwise installs for all
detected agents at global scope (CI-friendly).

Options:
  --agents, -a <list>   Comma-separated agent slugs (e.g. -a claude,codex,workbuddy)
  --path <dir>          Install into a custom directory
  --global, -g          Global scope only
  --local, -l           Project scope only
  --yes, -y             Skip prompts (use detected agents)
  --copy, -c            Copy files instead of symlinking (auto-fallback on link failure)
  --count               Print the number of known agents and exit
  --force, -f           Overwrite existing links
  --help, -h            Show this help message

Known agent slugs:
${agents.map(a => `  ${a.slug.padEnd(12)} ${a.name}`).join('\n')}

Examples:
  npx ${skillName} install
  npx ${skillName} install -a claude,codex,workbuddy
  npx ${skillName} install --path ~/my-agent/skills
  npx ${skillName} install -g --force
`);
}

// ─────────────────────────────────────────────────────────────────────────────
// Non-interactive install
// ─────────────────────────────────────────────────────────────────────────────

function nonInteractive({ selectedAgents, scope, customPath, force, copy }) {
  if (customPath) {
    console.log(`Installing to custom path: ${customPath}`);
    const r = linkSkill(customPath, { force, copy });
    return {
      installed: r === 'installed' ? 1 : 0,
      skipped:   r === 'skipped'   ? 1 : 0,
      failed:    r === 'failed'    ? 1 : 0,
    };
  }

  let target;
  if (selectedAgents && selectedAgents.length > 0) {
    target = selectedAgents;
  } else {
    const detected = detectAll();
    const effectiveScope = scope === 'all' ? 'global' : scope;
    target = [...new Set(detected.filter(d => d.scope === effectiveScope).map(d => d.agent))];
  }

  if (target.length === 0) {
    console.log('No agents detected.');
    console.log(`Specify agents with: npx ${skillName} install -a claude,codex`);
    console.log(`Or a custom path:    npx ${skillName} install --path <dir>`);
    return { installed: 0, skipped: 0, failed: 0 };
  }

  const effectiveScope = scope === 'all' ? 'global' : scope;
  console.log(`Installing for: ${target.map(a => a.name).join(', ')}`);
  console.log(`Scope: ${effectiveScope}`);
  console.log('');
  return doInstall(target, effectiveScope, force, copy);
}

// ─────────────────────────────────────────────────────────────────────────────
// Interactive install (clack TUI — mirrors impeccable UX)
// ─────────────────────────────────────────────────────────────────────────────

async function interactive({ force, copy }) {
  const clack = require('@clack/prompts');

  clack.intro(`${skillName} install`);

  // 1. Detect
  const detected = detectAll();
  const detectedAgents = [...new Set(detected.map(d => d.agent))];

  if (detected.length > 0) {
    const lines = detected.map(d => `  ${d.agent.name.padEnd(20)} ${relHome(d.dir)}`).join('\n');
    console.log(`\n◇ Detected agents\n${lines}\n`);
  } else {
    console.log('\n◇ No agents detected on this machine.\n');
  }

  // No agents detected — offer all or abort
  if (detectedAgents.length === 0) {
    const proceed = await clack.select({
      message: 'No agents detected. Install for all known agents?',
      options: [
        { value: 'all',    label: 'Yes, install for all (creates their dirs)' },
        { value: 'abort',  label: 'Abort' },
      ],
    });
    if (clack.isCancel(proceed) || proceed === 'abort') {
      clack.cancel('Aborted');
      process.exit(0);
    }
    const location = await clack.select({
      message: 'Install location',
      options: [
        { value: 'project', label: `Project (${process.cwd()})` },
        { value: 'global',  label: 'Global (~)' },
      ],
    });
    if (clack.isCancel(location)) { clack.cancel('Aborted'); process.exit(0); }
    console.log('');
    const r = doInstall(agents, location, force, copy);
    clack.outro(`Done! installed: ${r.installed}, skipped: ${r.skipped}, failed: ${r.failed}`);
    if (r.failed > 0) process.exit(1);
    return;
  }

  // 2. Detected only or customize?
  const mode = await clack.select({
    message: 'Install for detected agents only, or add more?',
    options: [
      { value: 'detected', label: `Detected only (${detectedAgents.map(a => a.slug).join(', ')})` },
      { value: 'custom',   label: 'Customize...' },
    ],
  });
  if (clack.isCancel(mode)) { clack.cancel('Aborted'); process.exit(0); }

  // 3. Select agents (if customize)
  let targetAgents;
  if (mode === 'custom') {
    const opts = agents.map(a => ({
      value: a.slug,
      label: a.name,
      hint: a.slug,
    }));
    const picked = await clack.multiselect({
      message: 'Select agents',
      options: opts,
      required: true,
    });
    if (clack.isCancel(picked)) { clack.cancel('Aborted'); process.exit(0); }
    targetAgents = agents.filter(a => picked.includes(a.slug));
  } else {
    targetAgents = detectedAgents;
  }

  // 4. Install location
  const location = await clack.select({
    message: 'Install location',
    options: [
      { value: 'project', label: `Project (${process.cwd()})` },
      { value: 'global',  label: 'Global (~)' },
    ],
  });
  if (clack.isCancel(location)) { clack.cancel('Aborted'); process.exit(0); }

  // 5. Install
  console.log('');
  const r = doInstall(targetAgents, location, force, copy);
  clack.outro(`Done! installed: ${r.installed}, skipped: ${r.skipped}, failed: ${r.failed}`);
  if (r.failed > 0) process.exit(1);
}

// ─────────────────────────────────────────────────────────────────────────────
// Arg parsing
// ─────────────────────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const positional = [];
  const opts = { agents: null, path: null, scope: 'all', force: false, yes: false, help: false, copy: false, count: false };
  let i = 0;
  while (i < argv.length) {
    const a = argv[i];
    if (a === '--agents' || a === '-a') {
      opts.agents = (argv[++i] || '').split(',').map(s => s.trim().toLowerCase()).filter(Boolean);
      i++;
    } else if (a === '--path') {
      opts.path = path.resolve(argv[++i]);
      i++;
    } else if (a === '--global' || a === '-g') {
      opts.scope = 'global'; i++;
    } else if (a === '--local' || a === '-l' || a === '--project') {
      opts.scope = 'project'; i++;
    } else if (a === '--all') {
      opts.scope = 'all'; i++;
    } else if (a === '--force' || a === '-f') {
      opts.force = true; i++;
    } else if (a === '--copy' || a === '-c') {
      opts.copy = true; i++;
    } else if (a === '--count') {
      opts.count = true; i++;
    } else if (a === '--yes' || a === '-y') {
      opts.yes = true; i++;
    } else if (a === '--help' || a === '-h') {
      opts.help = true; i++;
    } else if (!a.startsWith('-')) {
      positional.push(a); i++;
    } else {
      console.log(`Unknown option: ${a}  (use --help)`);
      process.exit(1);
    }
  }
  return { positional, opts };
}

// ─────────────────────────────────────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────────────────────────────────────

async function main() {
  const { positional, opts } = parseArgs(process.argv.slice(2));

  if (opts.help) { printHelp(); return; }
  if (opts.count) { console.log(agents.length); return; }

  // Subcommand: accept 'install' or none
  const subcommand = positional[0];
  if (subcommand && subcommand !== 'install') {
    console.log(`Unknown subcommand: ${subcommand}  (use --help)`);
    process.exit(1);
  }

  // Custom path: bypass everything
  if (opts.path) {
    const r = nonInteractive({ customPath: opts.path, force: opts.force, copy: opts.copy });
    console.log(`\nDone! installed: ${r.installed}, skipped: ${r.skipped}, failed: ${r.failed}`);
    if (r.failed > 0) process.exit(1);
    return;
  }

  // Explicit --agents: non-interactive
  if (opts.agents) {
    const selected = agents.filter(a => opts.agents.includes(a.slug));
    if (selected.length === 0) {
      console.log('No matching agents. Available slugs:');
      agents.forEach(a => console.log(`  ${a.slug.padEnd(12)} ${a.name}`));
      process.exit(1);
    }
    const scope = opts.scope === 'all' ? 'global' : opts.scope;
    const r = nonInteractive({ selectedAgents: selected, scope, force: opts.force, copy: opts.copy });
    console.log(`\nDone! installed: ${r.installed}, skipped: ${r.skipped}, failed: ${r.failed}`);
    if (r.failed > 0) process.exit(1);
    return;
  }

  // Interactive vs non-interactive
  if (isTTY() && !opts.yes) {
    await interactive({ force: opts.force, copy: opts.copy });
  } else {
    const r = nonInteractive({ scope: opts.scope, force: opts.force, copy: opts.copy });
    console.log(`\nDone! installed: ${r.installed}, skipped: ${r.skipped}, failed: ${r.failed}`);
    if (r.failed > 0) process.exit(1);
  }
}

main().catch(err => { console.error('Installer error:', err); process.exit(1); });
