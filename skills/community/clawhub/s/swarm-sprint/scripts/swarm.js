#!/usr/bin/env node
/**
 * Swarm — Parallel Coding Sprint with Git Worktree Isolation
 *
 * Inspired by Anthropic's leaked COORDINATOR_MODE architecture.
 * One coordinator, N isolated workers, each in their own git worktree.
 * Merged work lands on main. Worktrees always cleaned up after.
 *
 * Usage:
 *   node swarm.js --repo <path> --tasks <tasks.json> [--dry-run] [--verbose]
 *
 * Or via agent prompt:
 *   "Run a swarm sprint: task1, task2, task3"
 */

const fs   = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');

// ── Args ─────────────────────────────────────────────────────────────────────
const args       = process.argv.slice(2);
const dryRun     = args.includes('--dry-run');
const verbose    = args.includes('--verbose');
const repoIdx    = args.indexOf('--repo');
const tasksIdx   = args.indexOf('--tasks');
const planOnly   = args.includes('--plan-only');

const repoPath   = repoIdx !== -1 ? args[repoIdx + 1] : process.cwd();
const tasksFile  = tasksIdx !== -1 ? args[tasksIdx + 1] : null;

// ── Helpers ──────────────────────────────────────────────────────────────────
function log(msg)  { console.log(`[Swarm] ${msg}`); }
function warn(msg) { console.warn(`[Swarm:WARN] ${msg}`); }
function die(msg)  { console.error(`[Swarm:ERROR] ${msg}`); process.exit(1); }

function run(cmd, cwd, silent) {
  if (verbose && !silent) log(`$ ${cmd}`);
  const result = spawnSync('bash', ['-c', cmd], {
    cwd: cwd || repoPath,
    encoding: 'utf8',
    timeout: 30000
  });
  if (result.status !== 0) {
    throw new Error(`Command failed: ${cmd}\n${result.stderr}`);
  }
  return (result.stdout || '').trim();
}

function tryRun(cmd, cwd) {
  try { return run(cmd, cwd, true); } catch (e) { return null; }
}

// ── Phase 1: Analyze file overlap (the planning step) ────────────────────────
function analyzeTaskConflicts(tasks, repoPath) {
  log('Phase 1: Analyzing tasks for file conflicts...');

  // Ask each task what files it likely touches based on keywords
  const filePatterns = {
    'payroll':     ['payroll', 'timecard', 'wages', 'deduction'],
    'invoice':     ['invoice', 'billing', 'payment'],
    'talent':      ['talent', 'worker', 'employee'],
    'client':      ['client', 'customer', 'account'],
    'auth':        ['auth', 'login', 'session', 'token', 'jwt'],
    'schema':      ['schema', 'prisma', 'migration', 'database'],
    'frontend':    ['page', 'component', 'ui', 'react', 'tsx'],
    'backend':     ['route', 'endpoint', 'api', 'controller'],
    'test':        ['test', 'spec', 'e2e', 'playwright'],
    'mobile':      ['mobile', 'expo', 'native', 'ios', 'android'],
  };

  // Tag each task with file domain(s)
  const taggedTasks = tasks.map(task => {
    const desc = task.description.toLowerCase();
    const domains = [];
    for (const [domain, keywords] of Object.entries(filePatterns)) {
      if (keywords.some(k => desc.includes(k))) domains.push(domain);
    }
    return { ...task, domains: domains.length ? domains : ['general'] };
  });

  // Find conflicts — tasks sharing a high-risk domain
  const HIGH_CONFLICT_DOMAINS = ['schema', 'auth']; // prisma and auth touch shared files
  const conflicts = [];

  for (let i = 0; i < taggedTasks.length; i++) {
    for (let j = i + 1; j < taggedTasks.length; j++) {
      const a = taggedTasks[i];
      const b = taggedTasks[j];
      const shared = a.domains.filter(d => b.domains.includes(d));
      if (shared.length > 0) {
        const severity = shared.some(d => HIGH_CONFLICT_DOMAINS.includes(d)) ? 'HIGH' : 'LOW';
        conflicts.push({ taskA: a.id, taskB: b.id, shared, severity });
      }
    }
  }

  // Report
  if (conflicts.length === 0) {
    log('✓ No file conflicts detected — all tasks can run fully in parallel');
  } else {
    for (const c of conflicts) {
      if (c.severity === 'HIGH') {
        warn(`HIGH conflict: Task "${c.taskA}" and "${c.taskB}" both touch [${c.shared.join(', ')}] — recommend serializing these`);
      } else {
        log(`LOW conflict: Task "${c.taskA}" and "${c.taskB}" share [${c.shared.join(', ')}] — likely fine but watch merge`);
      }
    }
  }

  // Split into parallel-safe groups
  const highConflictPairs = conflicts.filter(c => c.severity === 'HIGH');
  const groups = [];
  const assigned = new Set();

  for (const task of taggedTasks) {
    if (assigned.has(task.id)) continue;
    const group = [task];
    assigned.add(task.id);

    // Add tasks that don't conflict with anything in this group
    for (const other of taggedTasks) {
      if (assigned.has(other.id)) continue;
      const conflictsWithGroup = group.some(g =>
        highConflictPairs.some(c =>
          (c.taskA === g.id && c.taskB === other.id) ||
          (c.taskB === g.id && c.taskA === other.id)
        )
      );
      if (!conflictsWithGroup) {
        group.push(other);
        assigned.add(other.id);
      }
    }
    groups.push(group);
  }

  if (groups.length > 1) {
    log(`Tasks split into ${groups.length} sequential groups to avoid conflicts:`);
    groups.forEach((g, i) => log(`  Group ${i+1}: ${g.map(t => t.id).join(', ')}`));
  } else {
    log(`All ${taggedTasks.length} tasks can run in parallel in one group`);
  }

  return { taggedTasks, conflicts, groups };
}

// ── Phase 2: Create worktrees ─────────────────────────────────────────────────
function createWorktrees(tasks, repoPath) {
  log('Phase 2: Creating git worktrees...');
  const worktrees = [];
  const timestamp = Date.now();

  for (const task of tasks) {
    const branchName  = `swarm/${timestamp}-${task.id}`;
    const worktreePath = path.join(path.dirname(repoPath), `${path.basename(repoPath)}-swarm-${task.id}`);

    if (dryRun) {
      log(`[dry-run] Would create worktree: ${worktreePath} on branch ${branchName}`);
      worktrees.push({ task, branchName, worktreePath, created: false });
      continue;
    }

    try {
      run(`git worktree add "${worktreePath}" -b "${branchName}"`, repoPath);
      log(`✓ Created worktree for task "${task.id}" at ${path.basename(worktreePath)}`);
      worktrees.push({ task, branchName, worktreePath, created: true });
    } catch (e) {
      warn(`Failed to create worktree for task "${task.id}": ${e.message}`);
      worktrees.push({ task, branchName, worktreePath, created: false, error: e.message });
    }
  }
  return worktrees;
}

// ── Phase 3: Generate agent instructions ─────────────────────────────────────
function generateAgentInstructions(worktrees) {
  log('Phase 3: Generating agent task packages...');
  const packages = [];

  for (const wt of worktrees) {
    if (!wt.created && !dryRun) continue;

    const pkg = {
      agentId: `swarm-${wt.task.id}`,
      role: wt.task.role || 'coder',
      worktreePath: wt.worktreePath,
      branchName: wt.branchName,
      task: wt.task,
      instructions: buildAgentPrompt(wt),
    };

    if (verbose || dryRun) {
      log(`\nAgent package for "${wt.task.id}":`);
      log(`  Role: ${pkg.role}`);
      log(`  Path: ${wt.worktreePath}`);
      log(`  Branch: ${wt.branchName}`);
      log(`  Task: ${wt.task.description}`);
    }

    packages.push(pkg);
  }
  return packages;
}

function buildAgentPrompt(wt) {
  const roleInstructions = {
    coder: `You are a focused coder. Your only job is to implement the task below. 
Do not refactor unrelated code. Do not touch files outside your task scope.
Write clean, TypeScript-safe code. Run tsc --noEmit when done to verify.`,

    reviewer: `You are a skeptical code reviewer. Your job is to review the changes made in this worktree.
Look for: bugs, type errors, missing error handling, security issues, performance problems.
Be specific. Do not approve weak work. List issues found or confirm it looks good.`,

    tester: `You are a test writer. Your job is to write tests for the code in this worktree.
Focus on: happy path, edge cases, error conditions.
Use the existing test patterns in the codebase.`,
  };

  return `
## SWARM AGENT TASK

${roleInstructions[wt.task.role || 'coder']}

## YOUR WORKSPACE
- Working directory: ${wt.worktreePath}
- Branch: ${wt.branchName}  
- DO NOT modify files outside this directory
- DO NOT push to remote (coordinator handles that)

## YOUR TASK
${wt.task.description}

## SUCCESS CRITERIA
${(wt.task.successCriteria || ['Task implemented', 'TypeScript compiles clean', 'No unrelated files changed']).join('\n- ')}

## WHEN DONE
1. Stage and commit all your changes:
   Run: git add -A && git commit -m "<short description of what you built>"
2. Then report back with:
- STATUS: COMPLETE | BLOCKED | FAILED
- FILES_CHANGED: list of files you modified
- SUMMARY: one paragraph of what you did
- BLOCKERS: any issues encountered

Do NOT skip the git commit step. The coordinator cannot merge uncommitted work.
`.trim();
}

// ── Phase 4: Cleanup ──────────────────────────────────────────────────────────
function cleanup(worktrees, repoPath, results) {
  log('Phase 4: Cleaning up worktrees...');

  for (const wt of worktrees) {
    if (!wt.created) continue;

    if (dryRun) {
      log(`[dry-run] Would remove worktree: ${wt.worktreePath}`);
      continue;
    }

    try {
      run(`git worktree remove "${wt.worktreePath}" --force`, repoPath);
      log(`✓ Removed worktree: ${path.basename(wt.worktreePath)}`);
    } catch (e) {
      warn(`Could not remove worktree ${wt.worktreePath}: ${e.message}`);
      // Try manual removal
      tryRun(`rm -rf "${wt.worktreePath}"`);
    }

    // Delete branch if task was merged or rejected
    const result = results && results.find(r => r.taskId === wt.task.id);
    if (!result || result.status === 'MERGED' || result.status === 'REJECTED') {
      tryRun(`git branch -D "${wt.branchName}"`, repoPath);
      log(`✓ Deleted branch: ${wt.branchName}`);
    }
  }

  // Prune stale worktree references
  tryRun('git worktree prune', repoPath);
}

// ── Phase 5: Write sprint log ─────────────────────────────────────────────────
function writeSprintLog(tasks, results, repoPath) {
  // Write log relative to the repo's parent, or fall back to cwd
  const logDir  = path.join(path.dirname(repoPath), 'memory');
  const logFile = path.join(logDir, 'swarm-log.md');
  const ts      = new Date().toISOString();

  const entry = `
## Swarm Sprint — ${ts}
- Repo: ${repoPath}
- Tasks: ${tasks.length}
- Results:
${(results || tasks.map(t => ({ taskId: t.id, status: dryRun ? 'DRY_RUN' : 'PENDING' }))).map(r =>
  `  - ${r.taskId}: ${r.status}${r.summary ? ' — ' + r.summary : ''}`
).join('\n')}
`;

  if (!dryRun) {
    fs.mkdirSync(logDir, { recursive: true });
    fs.appendFileSync(logFile, entry);
  }
  log(`Sprint log written to memory/swarm-log.md`);
}

// ── Main ──────────────────────────────────────────────────────────────────────
function main() {
  log(`Starting swarm sprint${dryRun ? ' (DRY RUN)' : ''}`);
  log(`Repo: ${repoPath}`);

  // Load tasks
  let tasks;
  if (tasksFile) {
    tasks = JSON.parse(fs.readFileSync(tasksFile, 'utf8'));
  } else {
    // Example tasks for testing
    tasks = [
      {
        id: 'task-1',
        description: 'Example task 1 — replace with real task',
        role: 'coder',
        successCriteria: ['Feature implemented', 'TypeScript clean']
      }
    ];
    log('No --tasks file provided. Using example task. Pass --tasks tasks.json for real use.');
  }

  log(`Tasks loaded: ${tasks.length}`);
  tasks.forEach(t => log(`  - [${t.id}] ${t.description}`));

  // Phase 1: Plan — check for conflicts
  const { groups } = analyzeTaskConflicts(tasks, repoPath);

  if (planOnly) {
    log('--plan-only mode: stopping after conflict analysis');
    return;
  }

  // Phase 2: Create worktrees for first group
  // (If multiple groups needed, coordinator runs them sequentially)
  const firstGroup = groups[0];
  const worktrees  = createWorktrees(firstGroup, repoPath);

  // Phase 3: Generate agent instructions
  const packages = generateAgentInstructions(worktrees);

  // Output the packages for the coordinator (Lando) to use when spawning subagents
  const outputFile = path.join(path.dirname(repoPath), 'swarm-packages.json');
  if (!dryRun) {
    fs.writeFileSync(outputFile, JSON.stringify(packages, null, 2));
    log(`\nAgent packages written to: swarm-packages.json`);
    log('Coordinator should now spawn subagents using these packages.');
    log('When all agents complete, call cleanup:');
    log(`  node swarm.js --repo ${repoPath} --cleanup swarm-packages.json`);
  } else {
    log('\n[dry-run] Would write agent packages to swarm-packages.json');
    log('Sample package:');
    if (packages[0]) console.log(JSON.stringify(packages[0], null, 2));
  }

  // If --cleanup flag, run cleanup from saved packages and exit early
  if (args.includes('--cleanup')) {
    const packagesFile = args[args.indexOf('--cleanup') + 1];
    if (!packagesFile || !fs.existsSync(packagesFile)) die('--cleanup requires a valid swarm-packages.json path');
    const loadedPackages = JSON.parse(fs.readFileSync(packagesFile, 'utf8'));
    const wts = loadedPackages.map(p => ({ task: p.task, branchName: p.branchName, worktreePath: p.worktreePath, created: fs.existsSync(p.worktreePath) }));
    cleanup(wts, repoPath, []);
    writeSprintLog(loadedPackages.map(p => p.task), [], repoPath);
    if (!dryRun) fs.unlinkSync(packagesFile);
    log('Cleanup complete');
    return;
  }

  log('\nSwarm setup complete ✓');
  log(`${worktrees.filter(w => w.created || dryRun).length} worktrees ready`);
  if (groups.length > 1) {
    log(`Note: ${groups.length - 1} additional task group(s) to run after first group merges`);
  }
}

main();
