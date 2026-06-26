#!/usr/bin/env node
// wip-branch-guard/guard.mjs
// PreToolUse hook for Claude Code.
// Blocks ALL file writes and git commits when on main branch.
// Agents must work on branches or worktrees. Never on main.
// Also blocks dangerous flags (--no-verify, --force) on ANY branch.

import { execSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import {
  statSync,
  readFileSync,
  existsSync,
  readdirSync,
  writeFileSync,
  renameSync,
  mkdirSync,
  appendFileSync,
} from 'node:fs';
import { fileURLToPath } from 'node:url';

// ---- session-state + approval-backend (inlined from ./lib/*) ----
// PR 2.1 (v1.9.78): ldm install's file-copy mechanism doesn't recurse
// subdirectories of a tool's source, so lib/ contents silently didn't land
// in ~/.ldm/extensions/wip-branch-guard/. The installer is being fixed in a
// separate PR on wip-ldm-os-private. Inlining keeps the guard self-contained
// so nested imports aren't required to boot. Once the installer supports
// subdirs, this block can move back into lib/*.mjs and be re-imported.

const _STATE_HOME = process.env.HOME || '';
const _STATE_DIR = process.env.LDM_GUARD_STATE_DIR || join(_STATE_HOME, '.ldm', 'state');
const _AUDIT_PATH = join(_STATE_DIR, 'bypass-audit.jsonl');
const _AUDIT_MAX_BYTES = 50 * 1024 * 1024;
const _ONBOARD_TTL_MS = 2 * 60 * 60 * 1000;
const _RECENT_DENIALS_KEEP = 20;
const _RECENT_DENIAL_WINDOW_MS = 60 * 60 * 1000;
// Per-session state files live under _STATE_DIR and are pruned after
// _STATE_FILE_TTL_MS of inactivity. 24h keeps a day of browsable history
// while making sure long-lived state dirs don't accumulate forever.
const _STATE_FILE_TTL_MS = 24 * 60 * 60 * 1000;
// Lock budgets. _LOCK_WAIT_MS is how long we'll block waiting for a
// competing write; _LOCK_STALE_MS is when we assume a crashed process
// left the lockfile behind and take it over.
const _LOCK_WAIT_MS = 2000;
const _LOCK_STALE_MS = 10000;

function _ensureStateDir() {
  if (!existsSync(_STATE_DIR)) {
    try { mkdirSync(_STATE_DIR, { recursive: true }); } catch {}
  }
}

// Per-session state file path. Pre-v1.9.82 the guard wrote a single
// shared file at ~/.ldm/state/guard-session.json, which meant every CC
// session on the machine clobbered every other session's onboarding and
// read-tracking state on every tool call. Keying the filename by
// session_id makes each session's state independent. sessionId is
// sanitized to a safe filename segment so weird chars (slashes, dots,
// spaces) can't escape the state dir or collide across sessions.
function statePathFor(sessionId) {
  const safe = String(sessionId || 'no-session').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 64);
  return join(_STATE_DIR, `guard-session-${safe}.json`);
}

function readSessionState(sessionId) {
  try { return JSON.parse(readFileSync(statePathFor(sessionId), 'utf8')); }
  catch { return emptyState(); }
}

function writeSessionState(state) {
  _ensureStateDir();
  const p = statePathFor(state.session_id);
  withStateLock(p, () => {
    const tmp = p + '.tmp-' + process.pid;
    try {
      writeFileSync(tmp, JSON.stringify(state, null, 2));
      renameSync(tmp, p);
    } catch {}
  });
}

// Mutex around a per-session state-file write. Uses `openSync(..., 'wx')`
// to create a lockfile atomically (fails with EEXIST if it already
// exists). Prevents two guard.mjs processes spawned by parallel tool
// calls in the same session from racing on read-modify-write and losing
// each other's updates. On timeout or unexpected error we fall through
// without holding the lock: correctness is best-effort here, per-session
// files are the load-bearing fix, and a missed lock degrades to a lost
// read-file entry (recoverable) rather than a deadlock.
function withStateLock(statePath, action) {
  const lockPath = statePath + '.lock';
  const deadline = Date.now() + _LOCK_WAIT_MS;
  let acquired = false;
  while (Date.now() < deadline) {
    try {
      const fd = openSync(lockPath, 'wx');
      closeSync(fd);
      acquired = true;
      break;
    } catch (e) {
      if (e.code !== 'EEXIST') break;
      // Stale-lock recovery.
      try {
        const stat = statSync(lockPath);
        if (Date.now() - stat.mtimeMs > _LOCK_STALE_MS) {
          try { unlinkSync(lockPath); } catch {}
          continue;
        }
      } catch {}
      // Brief synchronous wait before retry. Atomics.wait blocks the
      // thread cleanly; busy-wait is the fallback for runtimes without
      // SharedArrayBuffer.
      try {
        Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 20);
      } catch {
        const end = Date.now() + 20;
        while (Date.now() < end) {} // eslint-disable-line no-empty
      }
    }
  }
  try {
    return action();
  } finally {
    if (acquired) {
      try { unlinkSync(lockPath); } catch {}
    }
  }
}

// Prune per-session state files older than the TTL. Called once per
// guard invocation; readdirSync on a small state dir is sub-millisecond,
// cheap enough that we don't need probabilistic gating. Matches both
// .json state files and .lock leftovers.
function cleanupStaleStateFiles() {
  try {
    const entries = readdirSync(_STATE_DIR);
    const now = Date.now();
    for (const name of entries) {
      if (!/^guard-session-.*\.(json|lock)$/.test(name)) continue;
      const p = join(_STATE_DIR, name);
      try {
        const stat = statSync(p);
        if (now - stat.mtimeMs > _STATE_FILE_TTL_MS) {
          unlinkSync(p);
        }
      } catch {}
    }
  } catch {}
}

function emptyState() {
  return {
    session_id: null,
    started_at: Date.now(),
    last_touch_ts: Date.now(),
    read_files: [],
    // Canonical-keyed mirror of read_files: entries are
    // { canonical, relpath } tuples. An onboarding check on repo X
    // matches if every required relpath is present under X's canonical
    // key, regardless of which worktree the Read happened in.
    read_files_canonical: [],
    onboarded_repos: {},
    // Mirror of onboarded_repos keyed by canonical repo id (origin URL or
    // main-worktree path). Same repo onboarded in worktree A covers
    // worktree B without re-asking. Added v1.9.81.
    onboarded_repos_canonical: {},
    recent_denials: [],
  };
}

// Canonical identity for a repo path. Collapses worktrees of the same repo
// so onboarding state is shared across them. First of:
//   1. git remote get-url origin  (stable across worktrees AND fresh clones)
//   2. Main working tree path via git worktree list --porcelain
//   3. repoPath itself (fallback, equivalent to pre-1.9.81 behavior)
// Returns a string. Never throws.
function canonicalRepoKey(repoPath) {
  if (!repoPath) return '';
  try {
    const url = execSync('git remote get-url origin 2>/dev/null', {
      cwd: repoPath, encoding: 'utf8', timeout: 3000,
    }).trim();
    if (url) return url;
  } catch {}
  try {
    const raw = execSync('git worktree list --porcelain 2>/dev/null', {
      cwd: repoPath, encoding: 'utf8', timeout: 3000,
    });
    const m = raw.match(/^worktree\s+(.+)$/m);
    if (m && m[1]) return m[1];
  } catch {}
  return repoPath;
}

// Compute canonical info for a file path: { canonical, relpath }. If the
// path isn't inside a known git repo, returns null and callers fall back
// to the legacy abs-path matching.
function canonicalFileInfo(absPath) {
  if (!absPath) return null;
  const repo = findRepoRoot(absPath);
  if (!repo) return null;
  const canonical = canonicalRepoKey(repo);
  let relpath = absPath;
  if (absPath === repo) relpath = '';
  else if (absPath.startsWith(repo + '/')) relpath = absPath.slice(repo.length + 1);
  return { canonical, relpath };
}

function markReadFile(state, absPath) {
  if (!absPath) return;
  if (!state.read_files.includes(absPath)) state.read_files.push(absPath);
  const info = canonicalFileInfo(absPath);
  if (info) {
    if (!state.read_files_canonical) state.read_files_canonical = [];
    const alreadyHave = state.read_files_canonical.some(
      e => e.canonical === info.canonical && e.relpath === info.relpath
    );
    if (!alreadyHave) state.read_files_canonical.push(info);
  }
}

function checkOnboarding(state, repoPath, requiredReads) {
  const now = Date.now();
  const canonical = canonicalRepoKey(repoPath);
  // Canonical-keyed entry first (covers any worktree of the same repo).
  const canonicalEntry = state.onboarded_repos_canonical
    && state.onboarded_repos_canonical[canonical];
  if (canonicalEntry && (now - canonicalEntry.last_touch_ts) < _ONBOARD_TTL_MS) {
    return { ok: true, missing: [] };
  }
  // Legacy path-keyed entry (pre-1.9.81 state compat).
  const entry = state.onboarded_repos[repoPath];
  if (entry && (now - entry.last_touch_ts) < _ONBOARD_TTL_MS) {
    return { ok: true, missing: [] };
  }
  // Otherwise resolve required reads against both absolute-path and
  // canonical-relpath stores. Either match satisfies a given required read.
  const canonicalReads = (state.read_files_canonical || [])
    .filter(e => e.canonical === canonical)
    .map(e => e.relpath);
  const missing = requiredReads.filter(f => {
    if (state.read_files.includes(f)) return false;
    // Convert absolute required-read to relpath and check canonical store.
    if (f.startsWith(repoPath + '/')) {
      const rel = f.slice(repoPath.length + 1);
      if (canonicalReads.includes(rel)) return false;
    }
    return true;
  });
  return { ok: missing.length === 0, missing };
}

function markOnboarded(state, repoPath) {
  const now = Date.now();
  state.onboarded_repos[repoPath] = { onboarded_at_ts: now, last_touch_ts: now };
  const canonical = canonicalRepoKey(repoPath);
  if (!state.onboarded_repos_canonical) state.onboarded_repos_canonical = {};
  state.onboarded_repos_canonical[canonical] = { onboarded_at_ts: now, last_touch_ts: now };
  state.last_touch_ts = now;
}

function appendDenial(state, { path, tool, command_stripped }) {
  const now = Date.now();
  state.recent_denials.unshift({ ts: now, path, tool, command_stripped });
  if (state.recent_denials.length > _RECENT_DENIALS_KEEP) {
    state.recent_denials.length = _RECENT_DENIALS_KEEP;
  }
}

function wasRecentlyDenied(state, absPath) {
  if (!absPath) return null;
  const cutoff = Date.now() - _RECENT_DENIAL_WINDOW_MS;
  for (const d of state.recent_denials) {
    if (d.ts < cutoff) break;
    if (d.path === absPath) return d;
  }
  return null;
}

function appendAudit(event) {
  _ensureStateDir();
  try {
    if (existsSync(_AUDIT_PATH) && statSync(_AUDIT_PATH).size > _AUDIT_MAX_BYTES) {
      const dated = _AUDIT_PATH + '.' + new Date().toISOString().slice(0, 10);
      try { renameSync(_AUDIT_PATH, dated); } catch {}
    }
    appendFileSync(_AUDIT_PATH, JSON.stringify(event) + '\n');
  } catch {}
}

// Approval backend for operator-authorized overrides. v1.9.82 removed
// LDM_GUARD_SKIP_ONBOARDING and LDM_GUARD_ACK_BLOCKED_FILE: those env
// vars were workarounds for the cross-session state-file bug that
// v1.9.82 fixes at the root. External-PR approval stays because it is a
// legitimate scope-specific authorization (Parker green-lighting a PR
// to an upstream repo), not a workaround for a guard bug.
const _APPROVAL_ENV_MAP = {
  'external-pr-create': 'LDM_GUARD_UPSTREAM_PR_APPROVED',
};

function approvalCheck(action, _context = {}) {
  const backend = process.env.LDM_GUARD_APPROVAL_BACKEND || 'env';
  if (backend !== 'env') {
    return { approved: false, reason: `unknown backend: ${backend}`, via: null };
  }
  const envVar = _APPROVAL_ENV_MAP[action.kind];
  if (!envVar) return { approved: false, reason: `no env mapping for ${action.kind}`, via: 'env' };
  const value = process.env[envVar];
  if (!value) return { approved: false, reason: `${envVar} not set`, via: 'env' };
  if (action.target && value !== action.target && value !== '1' && value !== 'true') {
    return { approved: false, reason: `${envVar} does not match target`, via: 'env' };
  }
  return { approved: true, reason: `${envVar} set`, via: 'env' };
}
// ---- end inlined lib ----

if (process.argv.includes('--version') || process.argv.includes('-v')) {
  const __dirname = dirname(fileURLToPath(import.meta.url));
  const pkg = JSON.parse(readFileSync(join(__dirname, 'package.json'), 'utf8'));
  console.log(pkg.version);
  process.exit(0);
}

// Tools that modify files or git state
const WRITE_TOOLS = new Set(['Write', 'Edit', 'NotebookEdit']);
const BASH_TOOL = 'Bash';

// Git commands that should be blocked on main
const BLOCKED_GIT_PATTERNS = [
  /\bgit\s+commit\b/,
  /\bgit\s+add\b/,
  /\bgit\s+stash\b/,
  /\bgit\s+reset\b/,
  /\bgit\s+revert\b/,
  /\bgit\s+clean\b/,
  /\bgit\s+restore\b/,
];

// Destructive git commands blocked on ANY branch, not just main.
// These destroy work that may belong to other agents or the user.
// Checked against STRIPPED command (quoted content removed) to avoid false positives (#232).
const DESTRUCTIVE_PATTERNS = [
  /\bgit\s+clean\s+-[a-zA-Z]*f/,        // git clean -f, -fd, -fdx (deletes untracked files)
  /\bgit\s+checkout\s+--\s/,             // git checkout -- <path> (reverts files)
  /\bgit\s+checkout\s+\.\s*$/,           // git checkout . (reverts everything)
  /\bgit\s+stash\s+drop\b/,             // git stash drop (permanently deletes stashed work)
  /\bgit\s+stash\s+pop\b/,              // git stash pop (overwrites working tree, drops on success)
  /\bgit\s+stash\s+clear\b/,            // git stash clear (drops all stashes)
  /\bgit\s+reset\s+--hard\b/,           // git reset --hard (nukes all uncommitted changes)
  /\bgit\s+restore\s+(?!--staged)/,     // git restore <path> (reverts files, but --staged is safe)

  // Gap B (v1.9.83): shell redirection to protected deployed paths.
  // Edit/Write tools are blocked on main for repo files, and wip-file-guard
  // protects identity files. Bash redirects (`>`, `>>`, `tee`) into
  // deployed extensions, config, secrets, credentials, and agent auth-profiles
  // were not pattern-matched. These are never legitimate via Bash redirect;
  // the canonical path to modify them is the source repo + ldm install.
  // Closes the "jq > openclaw.json" and "echo > ~/.openclaw/..." bypass
  // class Parker surfaced on 2026-04-19.
  /(>>?|\btee\b).*\.openclaw\/openclaw\.json\b/,                                    // OpenClaw main config
  /(>>?|\btee\b).*\.openclaw\/agents\/[^\/\s|;&]+\/agent\/(auth-profiles|settings)\.json\b/, // agent auth/settings
  /(>>?|\btee\b).*\.openclaw\/(extensions|credentials|secrets)\/[^\s|;&]+/,          // deployed exts, imessage pairing, SA token
  /(>>?|\btee\b).*\.ldm\/extensions\/[^\s|;&]+/,                                     // LDM OS deployed extensions
  /(>>?|\btee\b).*\.ldm\/config\.json\b/,                                            // LDM OS root config
  /(>>?|\btee\b).*\.ldm\/agents\/[^\/\s|;&]+\/config\.json\b/,                       // LDM OS agent configs
];

// Code execution bypass patterns. Checked against ORIGINAL command because
// the attack IS inside quotes (e.g. python -c "open('f').write('x')").
const DESTRUCTIVE_CODE_PATTERNS = [
  /\bpython3?\s+-c\s+.*\bopen\s*\(/,    // python -c "open().write()" bypass (#241)
  /\bnode\s+-e\s+.*\bwriteFile/,         // node -e "require('fs').writeFile()" or "fs.writeFile()" bypass
];

// Strip quoted string contents to prevent regex matching inside data.
// "gh issue create --body 'use git checkout -- to fix'" becomes
// "gh issue create --body ''" so git checkout -- doesn't false-positive.
function stripQuotedContent(cmd) {
  return cmd.replace(/"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'/g, '""');
}

// Check each segment of a compound command independently.
// "rm -f file ; echo done" splits into ["rm -f file", "echo done"].
// Each segment checked against blocked, then allowed. An allowed match
// on one segment can't excuse a blocked match on a different segment (#232).
function isBlockedCompoundCommand(cmd, blockedPatterns, allowedPatterns) {
  const stripped = stripQuotedContent(cmd);
  const segments = stripped.split(/\s*(?:&&|\|\||[;|])\s*/).filter(Boolean);
  for (const segment of segments) {
    if (blockedPatterns.some(p => p.test(segment))) {
      if (!allowedPatterns.some(p => p.test(segment))) return true;
    }
  }
  return false;
}

// Git commands that are ALLOWED on main (read-only or safe operations)
const ALLOWED_GIT_PATTERNS = [
  /\bgit\s+merge\b/,
  /\bgit\s+pull\b/,
  /\bgit\s+fetch\b/,
  /\bgit\s+push\b/,
  /\bgit\s+status\b/,
  /\bgit\s+log\b/,
  /\bgit\s+diff\b/,
  /\bgit\s+branch\b/,
  /\bgit\s+checkout\s+(?!--)[\w\-\/]+/,  // git checkout <branch> only, NOT git checkout -- <path>
  /\bgit\s+worktree\b/,
  /\bgit\s+stash\s+list\b/,              // read-only, just lists stashes
  /\bgit\s+stash\s+show\b/,              // read-only, just shows stash contents
  /\bgit\s+stash\s+(push|save)\b/,       // saving to stash is non-destructive; drop/pop/clear blocked in DESTRUCTIVE_PATTERNS
  /\bgit\s+stash\s*$/,                   // bare "git stash" = "git stash push"; same safety
  /\bgit\s+remote\b/,
  /\bgit\s+describe\b/,
  /\bgit\s+tag\b/,
  /\bgit\s+rev-parse\b/,
  /\bgit\s+show\b/,
  /\bgit\s+restore\s+--staged\b/,        // unstaging is safe (doesn't change working tree)
];

// Non-git bash commands that write files (common patterns)
const BLOCKED_BASH_PATTERNS = [
  /\bcp\s+/,
  /\bmv\s+/,
  /\brm\s+/,
  /\bmkdir\s+/,
  /\btouch\s+/,
  />\s/,          // redirects
  /\btee\s+/,
  /\bsed\s+-i/,
];

// Allowed bash patterns (read-only operations, even though they match blocked patterns)
const ALLOWED_BASH_PATTERNS = [
  /\bls\b/,
  /\bcat\b/,
  /\bhead\b/,
  /\btail\b/,
  /\bgrep\b/,
  /\brg\b/,
  /\bfind\b/,
  /\bwc\b/,
  /\becho\b/,
  /\bcurl\b/,
  /\bgh\s+(issue|pr|release|api)\b/,
  /\bgh\s+pr\s+merge\b/,
  /\blsof\b/,
  /\bopen\s+-a\b/,
  /\bpwd\b/,
  /--dry-run/,
  /--help/,
  /\bwip-release\b.*--dry-run/,
  /\bnpm\s+install\s+-g\b/,   // global installs modify /opt/homebrew/, not the repo
  /\bnpm\s+link\b/,            // global operation, not repo-local
  /\bldm\s+(install|init|doctor|stack|updates)\b/,  // LDM OS commands modify ~/.ldm/, not the repo
  /\brm\s+.*\.ldm\/state\//,    // cleaning LDM state files only, not repo files
  /\brm\s+.*\.(openclaw|ldm)\/extensions\//,  // cleaning deployed extensions (managed by ldm install, not source code)
  /\bcp\s+.*\.(openclaw|ldm)\/extensions\//,  // hotfix deploy: cp plugin builds to extensions (ldm install is canonical)
  /\bmv\s+.*\.(openclaw|ldm)\/extensions\//,  // hotfix deploy: mv within extensions
  /\bmkdir\s+.*\.(openclaw|ldm)\/extensions\//, // hotfix deploy: create extension dirs
  /\bclaude\s+mcp\b/,          // MCP registration, not repo files
  /\bmkdir\s+.*\.worktrees\b/,  // creating .worktrees/ directory is part of the process

  // Worktree bootstrap operations (added 2026-04-20).
  // Symmetric with the mkdir-into-.worktrees allow above. The standard worktree
  // bootstrap compound (create worktree -> mkdir subdir -> cp files in) would
  // otherwise fail at the first cp because .worktrees/ wasn't in cp's allow list.
  // The 2026-04-19 session demonstrated this block. Fix symmetric with the
  // temp-dir pattern below. Agents are the primary caller of these patterns;
  // false-positive risk (.worktrees appearing as source path of a cp TO main)
  // is tiny and matches the existing mkdir precedent's imprecision.
  /\b(cp|mv|rm|touch)\s+.*\.worktrees\b/,
  />\s+[^|;&]*\.worktrees\b/,
  /\btee\s+.*\.worktrees\b/,

  /\brm\s+.*\.trash-approved-to-rm/,  // Parker's approved-for-deletion folder (only Parker moves files here, agents only rm)
  /\brm\s+.*\/_trash\//,              // agent trash directories (agents can mv here and rm here)

  // Temp-directory operations (added 2026-04-05, Phase 12 escape-hatch audit).
  // /tmp, /var/tmp, and macOS /var/folders/<hash>/T/ are explicitly ephemeral
  // scratch areas outside any git repo. Scripts often need to write test
  // fixtures, staging tarballs, or captured command output there. Blocking
  // these forces agents into awkward workarounds or tool-swaps for trivial
  // operations. Since temp paths are never tracked by git and the guard is
  // about protecting repo state, temp writes are safe to allow everywhere.
  /\b(cp|mv|rm|mkdir|touch)\s+[^|;&]*\/(tmp|var\/tmp|var\/folders\/[^\s|;&]+\/T)\//,
  />\s+[^|;&]*\/(tmp|var\/tmp|var\/folders\/[^\s|;&]+\/T)\//,
  /\btee\s+[^|;&]*\/(tmp|var\/tmp|var\/folders\/[^\s|;&]+\/T)\//,
];

// Shared-state file patterns. Writes to these are ALWAYS allowed (agents
// share context here; they're not source code). Hoisted to module scope so
// Layer 3 gates can skip onboarding / blocked-file checks for them.
const SHARED_STATE_PATTERNS = [
  /CLAUDE\.md$/,
  /\.openclaw\/workspace\//,
  /workspace\/SHARED-CONTEXT\.md$/,
  /workspace\/TOOLS\.md$/,
  /workspace\/MEMORY\.md$/,
  /workspace\/IDENTITY\.md$/,
  /workspace\/SOUL\.md$/,
  /workspace\/WHERE-TO-WRITE\.md$/,
  /workspace\/HEARTBEAT\.md$/,
  /workspace\/memory\/.*\.md$/,
  /\.ldm\/agents\/.*\/memory\/daily\/.*\.md$/,
  /\.ldm\/memory\/shared-log\.jsonl$/,
  /\.ldm\/memory\/daily\/.*\.md$/,
  /\.ldm\/logs\//,
  /\.claude\/plans\//,
  /\.claude\/projects\/.*\/memory\//,
  /\.ldm\/shared\//,
  /\.ldm\/messages\//,
  /\.ldm\/templates\//,
  /\.claude\/rules\//,
  /\.openclaw\/extensions\//,
  /\.ldm\/extensions\//,
];

// Workflow steps for error messages (#213)
const WORKFLOW_ON_MAIN = `
The process: worktree -> branch -> commit -> push -> PR -> merge -> wip-release -> deploy-public.

Step 1: git worktree add .worktrees/<repo>--<branch> -b cc-mini/your-feature
Step 2: Edit files in the worktree
Step 3: git add + git commit (with co-authors)
Step 4: git push -u origin cc-mini/your-feature
Step 5: gh pr create, then gh pr merge --merge --delete-branch
Step 6: Back in main repo: git pull
Step 7: wip-release patch (with RELEASE-NOTES on the branch, not after)
Step 8: deploy-public.sh to sync public repo

Release notes go ON the feature branch, committed with the code. Not as a separate PR.

STUCK clearing an untracked file before git pull? Use stash (non-destructive):
  git stash push -u -- <path>    # move untracked file aside
  git pull                       # pulls cleanly
  git stash list                 # file is preserved in stash, not lost`.trim();

const WORKFLOW_NOT_WORKTREE = `
You're on a branch but not in a worktree. Use a worktree so the main working tree stays clean.

Step 1: git checkout main (go back to main first)
Step 2: git worktree add ../my-worktree -b your-branch-name
Step 3: Edit files in the worktree directory`.trim();

function deny(reason, ctx = {}) {
  // Every deny lands in the audit log. ctx lets Layer 3 call sites enrich
  // the entry with session_id / tool / path / command. Existing call sites
  // that don't pass ctx still get a minimal timestamped deny record.
  try {
    appendAudit({
      kind: ctx.kind || 'deny',
      ts: Date.now(),
      session_id: ctx.session_id || null,
      tool: ctx.tool || null,
      path: ctx.path || null,
      command_stripped: ctx.command_stripped || null,
      reason: String(reason).slice(0, 200),
    });
  } catch {}
  const output = {
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'deny',
      permissionDecisionReason: reason,
    },
  };
  process.stdout.write(JSON.stringify(output));
}

function findRepoRoot(filePath) {
  // Walk up from a file path to find the git repo root
  try {
    let dir = filePath;
    // If it's a file, start from its directory
    try {
      if (statSync(dir).isFile()) dir = dirname(dir);
    } catch {
      dir = dirname(dir); // File might not exist yet
    }

    // Walk up until we find an existing directory (handles mkdir for new paths)
    while (dir && dir !== '/') {
      try {
        const s = statSync(dir);
        if (s.isDirectory()) break;
        dir = dirname(dir);
      } catch {
        dir = dirname(dir);
      }
    }

    // Use git rev-parse from the directory
    const result = execSync('git rev-parse --show-toplevel 2>/dev/null', {
      cwd: dir,
      encoding: 'utf8',
      timeout: 3000,
    }).trim();
    return result;
  } catch {}
  return null;
}

function extractPathsFromCommand(command) {
  // Extract absolute paths from a bash command
  // Matches paths like /Users/foo/bar, /tmp/something, etc.
  const paths = [];
  const regex = /(\/(?:Users|home|tmp|var|opt|etc|private)[^\s"'|;&>)]+)/g;
  let match;
  while ((match = regex.exec(command)) !== null) {
    paths.push(match[1]);
  }
  return paths;
}

// Parse a bash command for external-PR-create intent. Returns the target
// <owner>/<repo> string if this command would create a PR (implicit via
// worktree origin, explicit via --repo flag, or raw API POST), or null if
// the command isn't a PR-create operation. Caller decides if the owner is
// internal (wipcomputer) or needs approval.
//
// Recognized shapes:
//   - gh pr create --repo <owner>/<repo> ...
//   - gh pr create --repo <owner>/<repo> --head <fork>:<branch>   (cross-fork)
//   - gh pr create [--web] [--title ...] ...   (origin inferred from cwd)
//   - gh api repos/<owner>/<repo>/pulls ... -X POST
//
// Non-create shapes pass through (gh pr view/list/merge/edit, gh api /issues).
function parseExternalPRCreate(command, cwd) {
  if (!command) return null;
  const stripped = stripQuotedContent(command);
  // Split on chain operators so only the actual gh segment is matched.
  const segments = stripped.split(/\s*(?:&&|\|\||[;|])\s*/).filter(Boolean);
  for (const seg of segments) {
    // Raw API: gh api repos/<owner>/<repo>/pulls ... -X POST
    if (/\bgh\s+api\s+repos\/[^\s]+\/pulls\b/.test(seg) && /-X\s+POST\b/.test(seg)) {
      const m = seg.match(/\bgh\s+api\s+repos\/([^/\s]+)\/([^/\s]+)\/pulls/);
      if (m) return `${m[1]}/${m[2]}`;
    }
    if (!/\bgh\s+pr\s+create\b/.test(seg)) continue;
    // Explicit --repo flag
    const repoFlag = seg.match(/--repo\s+([^\s]+\/[^\s]+)/);
    if (repoFlag) return repoFlag[1];
    // Implicit: resolve origin of the cwd git repo
    try {
      const url = execSync('git remote get-url origin 2>/dev/null', {
        cwd: cwd || process.cwd(),
        encoding: 'utf8',
        timeout: 3000,
      }).trim();
      const m = url.match(/github\.com[:/]([^/]+)\/([^/.\s]+?)(?:\.git)?(?:\s|$)/);
      if (m) return `${m[1]}/${m[2]}`;
    } catch {}
  }
  return null;
}

// Required reads for first write in a repo. Root-level README.md, CLAUDE.md,
// and anything matching RUNBOOK / LANDMINES / WORKFLOW (the docs that tell
// an agent what the repo expects). Returns absolute paths of files that
// exist; the agent must have Read each of them in this session before the
// onboarding gate lets a write through.
function getRequiredReads(repoPath) {
  if (!repoPath) return [];
  const required = [];
  try {
    const entries = readdirSync(repoPath, { withFileTypes: true });
    for (const e of entries) {
      if (!e.isFile()) continue;
      if (e.name === 'README.md' || e.name === 'CLAUDE.md') {
        required.push(join(repoPath, e.name));
      } else if (/^(.*RUNBOOK.*|.*LANDMINES.*|WORKFLOW.*)\.md$/i.test(e.name)) {
        required.push(join(repoPath, e.name));
      }
    }
  } catch {}
  return required;
}

// Detect whether the current tool call is a file-write. For Write/Edit this
// is trivially true. For Bash it depends on the command shape. Returns the
// target path(s) of the write so blocked-file tracking can check for prior
// denials against the same filesystem target.
function extractWriteTargets(toolName, toolInput, command) {
  if (WRITE_TOOLS.has(toolName)) {
    const p = toolInput.file_path || toolInput.filePath || '';
    return p ? [p] : [];
  }
  if (toolName !== BASH_TOOL || !command) return [];
  if (!BLOCKED_BASH_PATTERNS.some(p => p.test(command))) return [];
  return extractPathsFromCommand(command);
}

function getCurrentBranch(cwd) {
  try {
    return execSync('git branch --show-current 2>/dev/null', {
      cwd: cwd || process.cwd(),
      encoding: 'utf8',
      timeout: 3000,
    }).trim();
  } catch {
    return null; // Not in a git repo
  }
}

function isInWorktree(cwd) {
  try {
    const gitDir = execSync('git rev-parse --git-dir 2>/dev/null', {
      cwd: cwd || process.cwd(),
      encoding: 'utf8',
      timeout: 3000,
    }).trim();
    return gitDir.includes('/worktrees/');
  } catch {
    return false;
  }
}

// CLI mode
if (process.argv.includes('--check')) {
  const branch = getCurrentBranch();
  const worktree = isInWorktree();
  console.log(`Branch: ${branch || '(not in git repo)'}`);
  console.log(`Worktree: ${worktree ? 'yes' : 'no'}`);
  console.log(`Status: ${branch === 'main' || branch === 'master' ? 'BLOCKED (on main)' : 'OK'}`);
  process.exit(branch === 'main' || branch === 'master' ? 1 : 0);
}

/**
 * SessionStart handler. Fires once per session boot (startup, resume,
 * and post-compaction resume). If the session's CWD is a main-branch
 * working tree of a protected git repo, inject a warning into the boot
 * context with available worktrees and the stash workaround so the
 * agent does not enter the compaction loop that wasted approximately
 * $900 of tokens on 2026-04-05.
 *
 * Uses `additionalContext` in the hookSpecificOutput response to
 * inject text into the session's context without blocking boot.
 *
 * Related:
 *   ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md Phase 7
 *   ai/product/bugs/master-plans/bugs-plan-04-05-2026-002.md Wave 2 phase 13
 */
function handleSessionStart(input) {
  const cwd = input.cwd || process.cwd();
  const sessionId = input.session_id || null;

  // State sanity check (v1.9.83). Surface a corrupt or stale per-session
  // state file at boot rather than silently resetting on the first tool
  // call. Runs regardless of branch so any session sees the warning.
  const stateWarning = checkSessionStateSanity(sessionId);

  // Bypass audit escalation (v1.9.84 / Gap C). Warn if repeat denials
  // or env-var overrides appear in the audit log tail. Global check,
  // doesn't depend on cwd.
  const bypassEscalation = checkBypassAuditEscalation();

  // Proactive onboarding advisory (v1.9.84 / Gap A). If cwd is a git
  // repo with onboarding docs, inject a boot-context advisory listing
  // the required reads so the agent does them up-front instead of
  // hitting the onboarding gate on first write.
  const onboardingAdvisory = checkProactiveOnboardingAdvisory(cwd);

  let branch = null;
  let repoRoot = null;
  try {
    repoRoot = execSync('git rev-parse --show-toplevel 2>/dev/null', {
      cwd, encoding: 'utf8', timeout: 3000,
    }).trim();
    branch = execSync('git branch --show-current 2>/dev/null', {
      cwd, encoding: 'utf8', timeout: 3000,
    }).trim();
  } catch {
    // Not a git repo, or git plumbing unavailable. Emit collected
    // warnings (state + bypass). Onboarding advisory is null here since
    // checkProactiveOnboardingAdvisory also requires a git repo.
    const pre = [stateWarning, bypassEscalation].filter(Boolean).join('\n\n---\n\n');
    emitSessionStartContext(pre || null);
    process.exit(0);
  }

  if (!branch || (branch !== 'main' && branch !== 'master')) {
    // On a feature branch. No on-main warning, but emit other warnings
    // if any (state, bypass, onboarding).
    const pre = [stateWarning, bypassEscalation, onboardingAdvisory].filter(Boolean).join('\n\n---\n\n');
    emitSessionStartContext(pre || null);
    process.exit(0);
  }

  // We are on main. Enumerate available worktrees so the warning is actionable.
  const worktrees = [];
  try {
    const raw = execSync('git worktree list --porcelain 2>/dev/null', {
      cwd, encoding: 'utf8', timeout: 3000,
    });
    let current = {};
    for (const line of raw.split('\n')) {
      if (line.startsWith('worktree ')) {
        if (current.path) worktrees.push(current);
        current = { path: line.slice('worktree '.length) };
      } else if (line.startsWith('branch ')) {
        current.branch = line.slice('branch '.length).replace(/^refs\/heads\//, '');
      } else if (line.startsWith('HEAD ')) {
        current.head = line.slice('HEAD '.length);
      } else if (line === 'detached') {
        current.detached = true;
      }
    }
    if (current.path) worktrees.push(current);
  } catch {}

  // The first entry is always the main working tree. Drop it to get
  // the list of linked worktrees only.
  const linkedWorktrees = worktrees.filter(w => w.path !== repoRoot);

  let worktreeList;
  if (linkedWorktrees.length === 0) {
    worktreeList = '  (no existing worktrees; create one with: git worktree add .worktrees/<repo>--cc-mini--<feature> -b cc-mini/<feature>)';
  } else {
    worktreeList = linkedWorktrees
      .slice(0, 10)
      .map(w => `  cd ${w.path}  # branch: ${w.branch || '(detached)'}`)
      .join('\n');
    if (linkedWorktrees.length > 10) {
      worktreeList += `\n  ... and ${linkedWorktrees.length - 10} more (see: git worktree list)`;
    }
  }

  const mainWarning = `⚠️  GUARD WARNING: You are in ${repoRoot} on the main branch.

The branch-guard will block file-modifying operations here. Before editing any file, switch to a worktree:

${worktreeList}

Or create a fresh worktree:
  git worktree add .worktrees/<repo>--cc-mini--<feature> -b cc-mini/<feature>

If you hit "git pull" failing on an untracked file that is already on origin/main, use the native stash escape hatch (shipped 2026-04-05):
  git stash push -u -- <path>
  git pull
  git stash list

Related context:
  ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md
  ai/product/bugs/master-plans/bugs-plan-04-05-2026-002.md`;

  const messages = [stateWarning, bypassEscalation, onboardingAdvisory, mainWarning].filter(Boolean);
  emitSessionStartContext(messages.join('\n\n---\n\n'));
  process.exit(0);
}

function emitSessionStartContext(text) {
  if (!text) return;
  const output = {
    hookSpecificOutput: {
      hookEventName: 'SessionStart',
      additionalContext: text,
    },
  };
  process.stdout.write(JSON.stringify(output));
}

// State sanity check (v1.9.83). Returns a warning string if the
// per-session state file is corrupt, missing started_at, or older than
// the TTL cleanup window. Returns null if state is healthy or absent.
// Failures here never block boot ... worst case we silently skip the
// warning.
function checkSessionStateSanity(sessionId) {
  if (!sessionId) return null;
  let statePath;
  try {
    statePath = statePathFor(sessionId);
  } catch {
    return null;
  }
  if (!existsSync(statePath)) return null; // fresh session, no state yet
  let content;
  try {
    content = readFileSync(statePath, 'utf8');
  } catch (err) {
    return `⚠️  GUARD STATE WARNING: per-session state file unreadable at ${statePath}: ${err.message}. Fresh state will be created on next tool call.`;
  }
  let parsed = null;
  try {
    parsed = JSON.parse(content);
  } catch {
    return `⚠️  GUARD STATE WARNING: per-session state file at ${statePath} is unparseable. Fresh state will be created on next tool call. Delete manually if corruption persists: rm -f ${statePath}`;
  }
  if (!parsed.started_at || typeof parsed.started_at !== 'number') {
    return `⚠️  GUARD STATE WARNING: per-session state file at ${statePath} is missing or has invalid started_at. File will be regenerated.`;
  }
  const ageMs = Date.now() - parsed.started_at;
  if (ageMs > 24 * 60 * 60 * 1000) {
    return `⚠️  GUARD STATE WARNING: per-session state file at ${statePath} is >24h old (started_at=${new Date(parsed.started_at).toISOString()}). TTL cleanup should remove stale per-session files on next invocation. If this warning persists on the next session, TTL cleanup is not running. Safe to delete manually: rm -f ${statePath}`;
  }
  return null;
}

// Proactive onboarding advisory (v1.9.84 / Gap A). Injects a boot-context
// advisory when cwd is a git repo with onboarding docs, listing the
// required reads so the agent does them up-front instead of hitting the
// onboarding gate on first Write/Edit/Bash-write. Non-blocking.
// Rationale: the onboarding gate is reactive (fires on first write). If
// the agent hasn't done the reads by the time it writes, it hits the
// deny, triggers retry-after-block, which the auto-mode decider false-
// positives on. Surfacing the required reads up-front eliminates the
// retry cycle entirely.
function checkProactiveOnboardingAdvisory(cwd) {
  if (!cwd) return null;
  let repoRoot;
  try {
    repoRoot = execSync('git rev-parse --show-toplevel 2>/dev/null', {
      cwd, encoding: 'utf8', timeout: 3000,
    }).trim();
  } catch {
    return null;
  }
  if (!repoRoot) return null;

  const required = [];
  for (const name of ['README.md', 'CLAUDE.md']) {
    try {
      if (existsSync(join(repoRoot, name))) required.push(name);
    } catch {}
  }
  try {
    for (const name of readdirSync(repoRoot)) {
      if (!name.endsWith('.md')) continue;
      if (/RUNBOOK/i.test(name) || /LANDMINES/i.test(name) || /^WORKFLOW/i.test(name)) {
        if (!required.includes(name)) required.push(name);
      }
    }
  } catch {}

  if (required.length === 0) return null;

  const readList = required.map(f => `  Read ${repoRoot}/${f}`).join('\n');
  return `📖 ONBOARDING ADVISORY: ${repoRoot} has onboarding docs. Before your first Write/Edit/Bash-write in this session, Read these in parallel (one turn):

${readList}

The guard enforces onboarding on first write; reading up-front avoids retry-after-block cycles that Claude Code's auto-mode decider false-positives on.`;
}

// Bypass audit escalation (v1.9.84 / Gap C). Reads the bypass-audit.jsonl
// tail, warns if any path was denied 3+ times in the last 24h or any
// env-var override fired at all. The former catches recurring false
// positives or repeated bypass attempts; the latter catches stale
// deployed guards (pre-v1.9.82 allowed LDM_GUARD_SKIP_ONBOARDING /
// LDM_GUARD_ACK_BLOCKED_FILE, which were removed in v1.9.82).
function checkBypassAuditEscalation() {
  const auditPath = join(_STATE_HOME, '.ldm', 'state', 'bypass-audit.jsonl');
  if (!existsSync(auditPath)) return null;
  let content;
  try {
    content = readFileSync(auditPath, 'utf8');
  } catch {
    return null;
  }
  const lines = content.trim().split('\n').slice(-500);
  const entries = [];
  for (const line of lines) {
    try {
      const e = JSON.parse(line);
      if (e && typeof e.ts === 'number') entries.push(e);
    } catch {}
  }
  const cutoff = Date.now() - 24 * 60 * 60 * 1000;
  const recent = entries.filter(e => e.ts >= cutoff);
  if (recent.length === 0) return null;

  const pathCounts = new Map();
  for (const e of recent) {
    if (e.kind === 'deny' && e.path) {
      pathCounts.set(e.path, (pathCounts.get(e.path) || 0) + 1);
    }
  }
  const repeat = [...pathCounts.entries()]
    .filter(([, count]) => count >= 3)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  const envOverrides = recent.filter(e =>
    e.kind && typeof e.kind === 'string' && e.kind.endsWith('-approved')
  );

  if (repeat.length === 0 && envOverrides.length === 0) return null;

  const sections = [];
  if (repeat.length > 0) {
    sections.push(`🚨 BYPASS AUDIT: paths denied 3+ times in the last 24h:`);
    for (const [p, count] of repeat) {
      sections.push(`  ${p} (${count}x)`);
    }
    sections.push(`\nReview deny reasons in ${auditPath} and either fix the underlying operation or file a guard bug. This pattern usually means the guard is false-positiving on a legitimate need OR an agent is repeatedly trying a bypass.`);
  }
  if (envOverrides.length > 0) {
    sections.push(`\n⚠️  ENV-VAR OVERRIDES recorded in the last 24h (${envOverrides.length}x). v1.9.82 removed LDM_GUARD_SKIP_ONBOARDING and LDM_GUARD_ACK_BLOCKED_FILE; only LDM_GUARD_UPSTREAM_PR_APPROVED remains legitimate. If other overrides appear here, the deployed guard is pre-v1.9.82 ... run "ldm install" to update.`);
  }

  return sections.join('\n');
}

async function main() {
  let raw = '';
  for await (const chunk of process.stdin) {
    raw += chunk;
  }

  let input;
  try {
    input = JSON.parse(raw);
  } catch {
    process.exit(0);
  }

  // Branch on hook event. Claude Code sends `hook_event_name` in the input
  // for every hook, so we can dispatch without a separate script per event.
  // PreToolUse payloads carry tool_name + tool_input; SessionStart payloads
  // carry cwd + source. Fall back on shape detection for harnesses that omit
  // hook_event_name (older Claude Code versions, OpenClaw, etc.).
  const eventName =
    input.hook_event_name ||
    input.hookEventName ||
    (input.tool_name ? 'PreToolUse' : (input.cwd || input.source ? 'SessionStart' : 'unknown'));

  if (eventName === 'SessionStart') {
    handleSessionStart(input);
    return; // handleSessionStart exits
  }

  const toolName = input.tool_name || '';
  const toolInput = input.tool_input || {};

  // --- Layer 3: session-state setup ------------------------------------
  // State is keyed by session_id via statePathFor() (v1.9.82+). Each CC
  // session has its own file, so there's no cross-session wipe to guard
  // against: readSessionState() on a fresh sid just returns emptyState()
  // naturally. cleanupStaleStateFiles() prunes old per-session files so
  // the state dir doesn't grow unbounded.
  const sessionId = input.session_id || input.sessionId || null;
  cleanupStaleStateFiles();
  let sessionState = readSessionState(sessionId);
  let stateDirty = false;
  if (!sessionState.session_id && sessionId) {
    sessionState.session_id = sessionId;
    stateDirty = true;
  }

  // Track Read/Glob calls so the onboarding gate can verify "has the agent
  // read this repo's README?" without a separate tool.
  if (toolName === 'Read' || toolName === 'Glob') {
    const rp = toolInput.file_path || toolInput.filePath || toolInput.path || '';
    if (rp) {
      markReadFile(sessionState, rp);
      stateDirty = true;
    }
    if (stateDirty) writeSessionState(sessionState);
    process.exit(0);
  }

  // Block destructive commands on ANY branch.
  // These destroy work that may belong to other agents or the user.
  if (toolName === BASH_TOOL) {
    const cmd = (toolInput.command || '');
    const strippedCmd = stripQuotedContent(cmd);

    // Git destructive patterns: check against stripped command (no quoted content)
    for (const pattern of DESTRUCTIVE_PATTERNS) {
      if (pattern.test(strippedCmd)) {
        deny(`BLOCKED: Destructive command detected.

"${cmd.substring(0, 80)}" can permanently destroy uncommitted work (yours, the user's, or another agent's).

DO NOT retry. DO NOT work around this. Instead:
1. STOP. Think about what you actually need to accomplish.
2. If you need a clean working tree, use a WORKTREE instead of destroying files on main.
3. If something is stuck (merge conflict, dirty state), create a safety checkpoint first:
   git stash create  (saves all uncommitted work without modifying the tree)
   git stash store <sha> -m "checkpoint before cleanup"
4. THEN proceed carefully with the minimum necessary operation.

These commands have destroyed work belonging to the user and other agents multiple times.`);
        process.exit(0);
      }
    }
    // Code execution bypasses: check against original command (the attack IS inside quotes)
    for (const pattern of DESTRUCTIVE_CODE_PATTERNS) {
      if (pattern.test(cmd)) {
        deny(`BLOCKED: Code execution bypass detected.

"${cmd.substring(0, 80)}" writes files through a scripting language, bypassing git protections.

Use the proper workflow: edit files in a worktree, commit, push, PR.`);
        process.exit(0);
      }
    }
  }

  // Block dangerous flags on ANY branch (these bypass safety checks)
  if (toolName === BASH_TOOL) {
    const cmd = (toolInput.command || '');
    if (/--no-verify\b/.test(cmd)) {
      deny('BLOCKED: --no-verify bypasses git hooks. Remove it and let the hooks run.');
      process.exit(0);
    }
    if (/\bgit\s+push\b.*--force\b/.test(cmd) && !/--force-with-lease\b/.test(cmd)) {
      deny('BLOCKED: git push --force can destroy remote history. Use --force-with-lease or ask Parker.');
      process.exit(0);
    }

    // External-PR guard: `gh pr create` (or raw `gh api repos/.../pulls -X POST`)
    // against a non-wipcomputer/ owner needs Parker's explicit approval.
    // Catches the 2026-04-18 PR #89 class of mistake where an agent opened
    // a PR directly against an upstream (steipete/imsg) without asking.
    // wipcomputer/ owners are internal; everything else routes through the
    // approval backend (env var LDM_GUARD_UPSTREAM_PR_APPROVED today, bridge
    // + biometric backends drop in later without touching this block).
    {
      const cwdForOrigin = input.cwd || process.env.CWD || process.cwd();
      const prTarget = parseExternalPRCreate(cmd, cwdForOrigin);
      if (prTarget) {
        const owner = prTarget.split('/')[0];
        if (owner !== 'wipcomputer') {
          const approval = approvalCheck({ kind: 'external-pr-create', target: prTarget });
          if (approval.approved) {
            appendAudit({
              kind: 'external-pr-create-approved',
              ts: Date.now(),
              session_id: sessionId,
              target: prTarget,
              tool: toolName,
              via: approval.via,
              reason: approval.reason,
              command_stripped: stripQuotedContent(cmd),
            });
          } else {
            deny(`BLOCKED: PR create against external repo "${prTarget}".

Creating a PR on a repo you don't own (${owner}/ is not wipcomputer/) needs Parker's explicit approval. The 2026-04-18 PR #89 incident (agent opened a PR directly to steipete/imsg without asking) is the reason this guard exists.

Options:
1. Push to our fork instead: gh pr create --repo wipcomputer/<repo>
2. If Parker authorized this specific PR:
     export LDM_GUARD_UPSTREAM_PR_APPROVED=${prTarget}
3. Blanket approval for this run:
     export LDM_GUARD_UPSTREAM_PR_APPROVED=1

Every approval is recorded in ~/.ldm/state/bypass-audit.jsonl.`, {
              kind: 'external-pr-create',
              tool: toolName,
              command_stripped: stripQuotedContent(cmd),
              session_id: sessionId,
              path: prTarget,
            });
            process.exit(0);
          }
        }
      }
    }

    // Block npm install -g right after a release (#73)
    // wip-release writes ~/.ldm/state/.last-release on completion.
    // If a release happened < 5 minutes ago, block install unless user explicitly said "install".
    // Exception: prerelease installs (@alpha, @beta) skip the cooldown. The cooldown exists
    // to enforce dogfooding stable releases. Prerelease installs ARE the dogfooding.
    if (/\bnpm\s+install\s+-g\b/.test(cmd) && !/@(alpha|beta)\b/.test(cmd)) {
      try {
        const releasePath = join(process.env.HOME || '', '.ldm', 'state', '.last-release');
        if (existsSync(releasePath)) {
          const data = JSON.parse(readFileSync(releasePath, 'utf8'));
          const age = Date.now() - new Date(data.timestamp).getTime();
          if (age < 5 * 60 * 1000) { // 5 minutes
            deny(`BLOCKED: Release completed ${Math.round(age / 1000)}s ago. Dogfood first. Remove ~/.ldm/state/.last-release when ready to install.`);
            process.exit(0);
          }
        }
      } catch {}
    }

    // Warn when creating worktrees outside .worktrees/ (#212)
    const wtMatch = cmd.match(/\bgit\s+worktree\s+add\s+["']?([^\s"']+)/);
    if (wtMatch) {
      const wtPath = wtMatch[1];
      if (!wtPath.includes('.worktrees')) {
        deny(`WARNING: Creating worktree outside .worktrees/. Use: ldm worktree add <branch>

The convention is .worktrees/<repo>--<branch>/ so worktrees are hidden and don't mix with real repos.
Manual equivalent: git worktree add .worktrees/<repo>--<branch> -b <branch>

This is a warning, not a block. If you need to create it here, retry.`);
        process.exit(0);
      }
    }
  }

  // Determine which repo to check.
  // Claude Code always opens in .openclaw, but edits files in other repos.
  // We need to check the branch of THE REPO THE FILE LIVES IN, not the CWD.
  const filePath = toolInput.file_path || toolInput.filePath || '';
  const command = toolInput.command || '';

  // For Write/Edit: derive repo from the file path
  // For Bash: try to extract repo path from the command (cd, or file paths in args)
  let repoDir = null;

  if (filePath) {
    // Walk up from file path to find .git directory
    repoDir = findRepoRoot(filePath);
    if (!repoDir) {
      // File is outside any git repo (e.g. ~/.claude/plans/, /tmp/).
      // The guard only protects git repos. Allow it.
      process.exit(0);
    }
  }

  if (!repoDir && command) {
    // Try to extract a path from the bash command
    // Common patterns: cd "/path/to/repo" && ..., or paths in arguments
    const cdMatch = command.match(/cd\s+["']?([^"'&|;]+?)["']?\s*(?:&&|;|$)/);
    if (cdMatch) {
      repoDir = findRepoRoot(cdMatch[1].trim());
    }
    // Also check for git -C /path/to/repo
    const gitCMatch = command.match(/git\s+-C\s+["']?([^"'&|;]+?)["']?\s/);
    if (!repoDir && gitCMatch) {
      repoDir = findRepoRoot(gitCMatch[1].trim());
    }
    // Extract absolute paths from the command itself (handles mkdir, cp, mv, etc.)
    if (!repoDir) {
      const paths = extractPathsFromCommand(command);
      for (const p of paths) {
        const resolved = findRepoRoot(p);
        if (resolved) {
          repoDir = resolved;
          break;
        }
      }
    }
  }

  // Fall back to CWD
  if (!repoDir) {
    repoDir = process.env.CWD || process.cwd();
  }

  // Check if the target repo is on main AND if we're in a worktree
  const branch = getCurrentBranch(repoDir);
  const worktree = isInWorktree(repoDir);

  if (!branch) {
    // Not in a git repo, allow
    process.exit(0);
  }

  // Allow everything in repos with zero commits (bootstrap)
  try {
    const hasCommits = execSync('git rev-parse HEAD', { cwd: repoDir, stdio: 'pipe' });
  } catch {
    // No commits yet. Allow the first commit so the repo can be bootstrapped.
    process.exit(0);
  }

  // --- Layer 3 gates --------------------------------------------------
  // Only apply to writes (Write/Edit/NotebookEdit or a Bash command whose
  // shape matches a file-writing pattern). Reads/searches fall through.
  const writeTargets = extractWriteTargets(toolName, toolInput, command);
  const stripped = stripQuotedContent(command || '');

  // Skip Layer 3 for shared-state files: they're the one place agents are
  // meant to collaboratively edit on main, and adding an onboarding gate
  // there would make routine workspace updates hit the guard every session.
  const isSharedState = filePath && SHARED_STATE_PATTERNS.some(p => p.test(filePath));

  // Filter writeTargets to paths Layer 3 actually cares about. Excludes:
  //  - Temp dirs (/tmp, /var/tmp, /var/folders/.../T): ephemeral scratch,
  //    not repo state, never tracked in git. Bash writes here shouldn't
  //    trigger onboarding or blocked-file tracking. The temp-dir
  //    allowance in ALLOWED_BASH_PATTERNS only gates Layer 1; without
  //    this filter, Layer 3 fires first on any Bash write-shape command
  //    in a session-new repo, denying "cp source /tmp/x" with an
  //    onboarding message even though /tmp is outside the repo.
  //  - Shared-state paths: symmetric with isSharedState (which only
  //    checks filePath for Edit/Write tools). Bash writes to shared-state
  //    paths should also bypass Layer 3.
  // Surfaced by the Phase 12 audit tests on 2026-04-21 when wip-release
  // first ran the test suite from main; 8 temp-dir tests failed because
  // Layer 3 was denying before Layer 1's allow-pattern check could fire.
  const isTempPath = (p) => /^\/(tmp|var\/tmp|var\/folders\/[^\/]+\/T)\//.test(p);
  const isSharedStatePath = (p) => SHARED_STATE_PATTERNS.some(pat => pat.test(p));
  const repoWriteTargets = writeTargets.filter(p => !isTempPath(p) && !isSharedStatePath(p));

  if (repoWriteTargets.length > 0 && !isSharedState) {
    // Blocked-file tracking: if the same target was denied earlier in this
    // session, a new tool attempting to hit the same path is an
    // equivalent-action bypass. v1.9.82 removed LDM_GUARD_ACK_BLOCKED_FILE;
    // the only path here is to stop and surface the original block to
    // Parker rather than ack-and-continue.
    for (const target of repoWriteTargets) {
      const prior = wasRecentlyDenied(sessionState, target);
      if (!prior) continue;
      deny(`BLOCKED: "${target}" was just denied via ${prior.tool} at ${new Date(prior.ts).toISOString()}.

Retrying through ${toolName} is an equivalent-action bypass (same filesystem effect, different tool). Stop and surface the original block to Parker.`, {
        kind: 'blocked-file-retry',
        path: target,
        session_id: sessionId,
        tool: toolName,
        command_stripped: stripped,
      });
      // Also record so further retries keep the tail fresh.
      appendDenial(sessionState, { path: target, tool: toolName, command_stripped: stripped });
      writeSessionState(sessionState);
      process.exit(0);
    }

    // Onboarding: first write to a repo requires the agent to have read
    // the repo's onboarding docs in this session. Required reads =
    // README.md, CLAUDE.md, and any RUNBOOK / LANDMINES / WORKFLOW at
    // root that exist. v1.9.82 removed LDM_GUARD_SKIP_ONBOARDING; the
    // only path to onboarded is actually reading the docs.
    const required = getRequiredReads(repoDir);
    const onb = checkOnboarding(sessionState, repoDir, required);
    if (!onb.ok) {
      const readList = onb.missing.map(f => '  Read ' + f).join('\n');
      deny(`BLOCKED: Onboarding required before first write to ${repoDir}.

Read these repo docs first (they explain the expected workflow and known landmines):

${readList}

Then retry the write.`, {
        kind: 'onboarding',
        path: repoDir,
        session_id: sessionId,
        tool: toolName,
        command_stripped: stripped,
      });
      process.exit(0);
    } else {
      markOnboarded(sessionState, repoDir);
      stateDirty = true;
    }
  }

  if (stateDirty) writeSessionState(sessionState);

  if (branch !== 'main' && branch !== 'master' && worktree) {
    // On a branch AND in a worktree. Correct workflow. Allow.
    process.exit(0);
  }

  if (branch !== 'main' && branch !== 'master' && !worktree) {
    // On a branch but NOT in a worktree. Block writes.
    const isWriteOp = WRITE_TOOLS.has(toolName) ||
      (toolName === BASH_TOOL && command &&
        isBlockedCompoundCommand(command, BLOCKED_BASH_PATTERNS, ALLOWED_BASH_PATTERNS));
    if (isWriteOp) {
      for (const t of writeTargets) appendDenial(sessionState, { path: t, tool: toolName, command_stripped: stripped });
      if (writeTargets.length) writeSessionState(sessionState);
      deny(`BLOCKED: On branch "${branch}" but not in a worktree.\n\n${WORKFLOW_NOT_WORKTREE}`, {
        kind: 'not-worktree',
        path: writeTargets[0] || null,
        session_id: sessionId,
        tool: toolName,
        command_stripped: stripped,
      });
      process.exit(0);
    }
    process.exit(0);
  }

  // On main. Shared-state files (hoisted module-level list) always allow.
  if (isSharedState) {
    process.exit(0);
  }

  // Block Write/Edit tools entirely on main
  if (WRITE_TOOLS.has(toolName)) {
    if (filePath) appendDenial(sessionState, { path: filePath, tool: toolName, command_stripped: stripped });
    if (filePath) writeSessionState(sessionState);
    deny(`BLOCKED: Cannot ${toolName} while on main branch.\n\n${WORKFLOW_ON_MAIN}`, {
      kind: 'main-write',
      path: filePath || null,
      session_id: sessionId,
      tool: toolName,
      command_stripped: stripped,
    });
    process.exit(0);
  }

  // For Bash, check each command segment independently (#232).
  // No fast-path: an allowed pattern on one segment can't excuse a blocked pattern on another.
  if (toolName === BASH_TOOL && command) {
    // Check for blocked git commands (per-segment, quote-stripped)
    if (isBlockedCompoundCommand(command, BLOCKED_GIT_PATTERNS, ALLOWED_GIT_PATTERNS)) {
      deny(`BLOCKED: Cannot run "${command.substring(0, 60)}..." on main branch.\n\n${WORKFLOW_ON_MAIN}`, {
        kind: 'main-git',
        session_id: sessionId,
        tool: toolName,
        command_stripped: stripped,
      });
      process.exit(0);
    }

    // Check for file-writing bash commands (per-segment, quote-stripped)
    if (isBlockedCompoundCommand(command, BLOCKED_BASH_PATTERNS, ALLOWED_BASH_PATTERNS)) {
      for (const t of writeTargets) appendDenial(sessionState, { path: t, tool: toolName, command_stripped: stripped });
      if (writeTargets.length) writeSessionState(sessionState);
      deny(`BLOCKED: Cannot run file-modifying command on main branch.\n\n${WORKFLOW_ON_MAIN}`, {
        kind: 'main-bash-write',
        path: writeTargets[0] || null,
        session_id: sessionId,
        tool: toolName,
        command_stripped: stripped,
      });
      process.exit(0);
    }
  }

  // Allow everything else (Read, Glob, Grep, Agent, etc.)
  process.exit(0);
}

main().catch(() => process.exit(0));
