#!/bin/bash
# Guard test runner. Run from the guard directory before merging.
# Usage: bash test.sh
#
# Pipes test JSON into guard.mjs and checks if it allows or blocks.
# Exit 0 = all tests pass. Exit 1 = at least one failed.
#
# Note: compound command tests (Bug 2) and on-main tests need CWD
# to be in a repo on main. The script auto-detects and skips those
# tests if running from a branch/worktree.

GUARD="$(dirname "$0")/guard.mjs"
PASS=0
FAIL=0
SKIP=0

# Check if we're on main (for tests that need main-branch context)
ON_MAIN=false
BRANCH=$(git branch --show-current 2>/dev/null)
if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  ON_MAIN=true
fi

# Helper: build properly escaped JSON using node (avoids bash quote hell)
make_json() {
  local tool="$1" key="$2" value="$3"
  node -e "process.stdout.write(JSON.stringify({tool_name:'$tool',tool_input:{$key:process.argv[1]}}))" "$value"
}

# Helper: run a test case
# Args: description, expected (allow|deny), tool_name, command_or_filepath, [main_only]
test_case() {
  local desc="$1" expected="$2" tool="$3" input="$4" main_only="${5:-false}"

  if [[ "$main_only" == "true" && "$ON_MAIN" == "false" ]]; then
    echo "  SKIP: $desc (needs main branch)"
    ((SKIP++))
    return
  fi

  local json
  if [[ "$tool" == "Bash" ]]; then
    json=$(make_json Bash command "$input")
  elif [[ "$tool" == "Write" || "$tool" == "Edit" ]]; then
    json=$(make_json "$tool" file_path "$input")
  fi

  local output
  output=$(echo "$json" | node "$GUARD" 2>/dev/null)

  local actual="allow"
  if echo "$output" | grep -q '"deny"' 2>/dev/null; then
    actual="deny"
  fi

  if [[ "$actual" == "$expected" ]]; then
    echo "  PASS: $desc"
    ((PASS++))
  else
    echo "  FAIL: $desc (expected $expected, got $actual)"
    ((FAIL++))
  fi
}

echo "=== Branch Guard Tests ==="
echo ""
echo "--- Destructive commands (should DENY on any branch) ---"
test_case "git clean -fd" deny Bash "git clean -fd"
test_case "git checkout -- file.txt" deny Bash "git checkout -- file.txt"
test_case "git checkout ." deny Bash "git checkout ."
test_case "git stash drop" deny Bash "git stash drop"
test_case "git stash pop" deny Bash "git stash pop"
test_case "git stash clear" deny Bash "git stash clear"
test_case "git reset --hard" deny Bash "git reset --hard"
test_case "git restore file.txt" deny Bash "git restore file.txt"
test_case "python file write bypass" deny Bash "python3 -c \"open('f','w').write('x')\""
test_case "node file write bypass" deny Bash "node -e \"require('fs').writeFileSync('f','d')\""

echo ""
echo "--- Quoted strings: should NOT match inside quotes (Bug 1, 3) ---"
test_case "gh issue with git checkout in body" allow Bash "gh issue create --body 'use git checkout -- to fix'"
test_case "echo with git commit in quotes" allow Bash "echo 'dont run git commit on main'"
test_case "gh issue with git reset in body" allow Bash "gh issue create --body 'tried git reset --hard'"

echo ""
echo "--- Compound commands: each segment checked independently (Bug 2) ---"
echo "  (These only run when CWD is on main branch)"
test_case "rm with echo should still block" deny Bash "rm -f file ; echo done" true
test_case "safe compound (ls && echo)" allow Bash "ls -la && echo done" true
test_case "cd then rm should block" deny Bash "cd /tmp && rm -rf somedir" true

echo ""
echo "--- Safe commands (should ALLOW) ---"
test_case "git status" allow Bash "git status"
test_case "git log" allow Bash "git log --oneline -5"
test_case "git diff" allow Bash "git diff"
test_case "git checkout branch" allow Bash "git checkout feature-branch"
test_case "git worktree add" allow Bash "git worktree add .worktrees/repo--branch -b feat"
test_case "git stash list" allow Bash "git stash list"
test_case "git stash show" allow Bash "git stash show"
test_case "git stash push -u" allow Bash "git stash push -u -- path/to/file"
test_case "git stash save" allow Bash "git stash save 'message'"
test_case "bare git stash" allow Bash "git stash"
test_case "git restore --staged" allow Bash "git restore --staged file.txt"
test_case "ls command" allow Bash "ls -la"
test_case "grep command" allow Bash "grep -r pattern ."
test_case "gh pr create" allow Bash "gh pr create --title test"
test_case "gh pr merge" allow Bash "gh pr merge 123 --merge"
test_case "echo" allow Bash "echo hello"
test_case "wip-release dry-run" allow Bash "wip-release patch --dry-run"
test_case "ldm install" allow Bash "ldm install"
test_case "mkdir .worktrees" allow Bash "mkdir -p .worktrees/repo--branch"

echo ""
echo "--- Temp directory operations (Phase 12 audit) ---"
test_case "cp to /tmp" allow Bash "cp source.txt /tmp/test.txt"
test_case "mv to /tmp" allow Bash "mv source.txt /tmp/test.txt"
test_case "rm in /tmp" allow Bash "rm /tmp/test.txt"
test_case "mkdir in /tmp" allow Bash "mkdir -p /tmp/test-dir"
test_case "touch in /tmp" allow Bash "touch /tmp/test-file"
test_case "redirect to /tmp" allow Bash "echo hello > /tmp/test.txt"
test_case "tee to /tmp" allow Bash "cat source | tee /tmp/test.txt"
test_case "cp to /var/tmp" allow Bash "cp source /var/tmp/test"

echo ""
echo "--- Worktree bootstrap operations (added 2026-04-20) ---"
# Enables the standard worktree bootstrap compound:
#   git worktree add .worktrees/<name> -b <branch>
#     && mkdir -p .worktrees/<name>/subdir
#     && cp /src/file .worktrees/<name>/subdir/file
# Before this allowlist, the cp step failed with ALLOWED_BASH_PATTERNS only
# covering mkdir. Now all the common bootstrap verbs work.
test_case "cp to .worktrees" allow Bash "cp src.txt .worktrees/repo--feat/ai/dest.md"
test_case "mv to .worktrees" allow Bash "mv src.txt .worktrees/repo--feat/ai/dest.md"
test_case "rm in .worktrees" allow Bash "rm .worktrees/repo--feat/ai/file.md"
test_case "touch in .worktrees" allow Bash "touch .worktrees/repo--feat/ai/file.md"
test_case "redirect to .worktrees" allow Bash "echo content > .worktrees/repo--feat/ai/file.md"
test_case "tee to .worktrees" allow Bash "cat src | tee .worktrees/repo--feat/ai/file.md"
# Regressions: on-main writes to non-.worktrees paths still deny
test_case "cp to main-tree path still denies" deny Bash "cp src.txt /some/repo/file.md" true
test_case "rm on main-tree path still denies" deny Bash "rm /some/repo/file.md" true

echo ""
echo "--- Plan files (should ALLOW Write/Edit) ---"
test_case "Edit plan file" allow Edit "$HOME/.claude/plans/my-plan.md"

echo ""
echo "--- Auto-memory files (should ALLOW Write/Edit; gitignored, harness-managed) ---"
test_case "Write auto-memory index" allow Write "$HOME/.claude/projects/-Users-lesa-example/memory/MEMORY.md"
test_case "Write auto-memory entry" allow Write "$HOME/.claude/projects/-Users-lesa-example/memory/feedback_example.md"
test_case "Edit auto-memory entry" allow Edit "$HOME/.claude/projects/-Users-lesa-example/memory/user_role.md"

echo ""
echo "--- SessionStart hook (new in 1.9.73) ---"

# SessionStart emits additionalContext when CWD is on main, otherwise exits
# silently. Test both shapes via direct stdin injection.

test_session_start() {
  local desc="$1" cwd="$2" expect="$3"  # expect: "warn" or "silent"
  local json output
  json=$(node -e "process.stdout.write(JSON.stringify({hook_event_name:'SessionStart',cwd:process.argv[1],source:'startup'}))" "$cwd")
  output=$(echo "$json" | node "$GUARD" 2>/dev/null)

  local actual="silent"
  if echo "$output" | grep -q 'GUARD WARNING' 2>/dev/null; then
    actual="warn"
  fi

  if [[ "$actual" == "$expect" ]]; then
    echo "  PASS: $desc"
    ((PASS++))
  else
    echo "  FAIL: $desc (expected $expect, got $actual)"
    ((FAIL++))
  fi
}

# Main tree of this repo on main (the test is running inside a worktree on a
# feature branch, so we pass the absolute path to the main tree).
MAIN_TREE=$(git worktree list --porcelain 2>/dev/null | awk '/^worktree /{print $2; exit}')
if [[ -n "$MAIN_TREE" ]]; then
  CURRENT_BRANCH_AT_MAIN=$(cd "$MAIN_TREE" && git branch --show-current 2>/dev/null)
  if [[ "$CURRENT_BRANCH_AT_MAIN" == "main" || "$CURRENT_BRANCH_AT_MAIN" == "master" ]]; then
    test_session_start "main tree on main branch warns" "$MAIN_TREE" "warn"
  else
    echo "  SKIP: main tree is not on main branch ($CURRENT_BRANCH_AT_MAIN)"
    ((SKIP++))
  fi
fi

# Current worktree is on a feature branch. SessionStart should exit silent.
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null)
if [[ "$CURRENT_BRANCH" != "main" && "$CURRENT_BRANCH" != "master" && -n "$CURRENT_BRANCH" ]]; then
  test_session_start "feature branch silent" "$PWD" "silent"
else
  echo "  SKIP: not on a feature branch for silent test"
  ((SKIP++))
fi

# Non-git directory: silent (nothing to warn about)
test_session_start "non-git /tmp silent" "/tmp" "silent"

echo ""
echo "--- Hook matcher includes Read|Glob (regression guard for 1.9.79) ---"
# The onboarding gate relies on Read calls populating state.read_files.
# That only works if Claude Code's hook matcher actually fires on Read.
# Prior to 1.9.79 the matcher was Write|Edit|NotebookEdit|Bash (no Read).
# Reads never fired the hook so state stayed empty forever; every fresh
# worktree became a permanent block. Static test so a future matcher
# change can't silently regress.
MATCHER=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$(dirname "$GUARD")/package.json','utf8')).claudeCode.hooks[0].matcher)")
if [[ "$MATCHER" == *"Read"* && "$MATCHER" == *"Glob"* ]]; then
  echo "  PASS: matcher contains Read and Glob ($MATCHER)"
  ((PASS++))
else
  echo "  FAIL: matcher missing Read or Glob: $MATCHER"
  ((FAIL++))
fi

echo ""
echo "--- Layer 3: onboarding + blocked-file tracking (new in 1.9.77) ---"

# Layer 3 tests build a fresh tmp git repo per test + redirect state to /tmp
# so they don't clobber the user's real ~/.ldm/state/guard-session.json.
# Canonicalize via `cd ... && pwd -P` because macOS /tmp -> /private/tmp
# and git rev-parse --show-toplevel returns the canonical path, so the
# session state keys must line up.
LAYER3_TMP_RAW="$(mktemp -d /tmp/guard-layer3-XXXX)"
LAYER3_TMP="$(cd "$LAYER3_TMP_RAW" && pwd -P)"
LAYER3_STATE="$LAYER3_TMP/state"
mkdir -p "$LAYER3_STATE"

# Build a tmp repo with README + CLAUDE.md, then add a git worktree. The
# worktree is where writes happen so the branch-guard's worktree check
# passes, leaving Layer 3 as the only gate in play.
LAYER3_SRC="$LAYER3_TMP/src"
LAYER3_REPO="$LAYER3_TMP/wt"
mkdir -p "$LAYER3_SRC"
(
  cd "$LAYER3_SRC"
  git init -q -b main
  echo "# Repo" > README.md
  echo "# Repo" > CLAUDE.md
  git add README.md CLAUDE.md
  git -c user.email=test@test -c user.name=test commit -q -m "init"
  git worktree add -q -b feature-branch "$LAYER3_REPO"
  # Copy onboarding docs into the worktree so readdirSync picks them up there.
  cp README.md CLAUDE.md "$LAYER3_REPO/"
) >/dev/null 2>&1

# Helper: run a Layer 3 check. Args: session_id, tool, file_path_or_cmd, expect.
layer3_call() {
  local sid="$1" tool="$2" arg="$3" expect="$4" desc="$5" extra_env="$6"
  local json
  if [[ "$tool" == "Bash" ]]; then
    json=$(node -e "process.stdout.write(JSON.stringify({hook_event_name:'PreToolUse',session_id:process.argv[1],tool_name:'Bash',tool_input:{command:process.argv[2]}}))" "$sid" "$arg")
  else
    json=$(node -e "process.stdout.write(JSON.stringify({hook_event_name:'PreToolUse',session_id:process.argv[1],tool_name:process.argv[2],tool_input:{file_path:process.argv[3]}}))" "$sid" "$tool" "$arg")
  fi
  local output actual="allow"
  output=$(echo "$json" | env LDM_GUARD_STATE_DIR="$LAYER3_STATE" $extra_env node "$GUARD" 2>/dev/null)
  if echo "$output" | grep -q '"deny"'; then actual="deny"; fi
  if [[ "$actual" == "$expect" ]]; then
    echo "  PASS: $desc"
    ((PASS++))
  else
    echo "  FAIL: $desc (expected $expect, got $actual)"
    ((FAIL++))
  fi
}

# 1. First write without reading onboarding docs -> deny
layer3_call "s1" "Write" "$LAYER3_REPO/src.md" "deny" "onboarding: first write without reads denies"

# 2. Read README + CLAUDE, then write -> allow
layer3_call "s1" "Read" "$LAYER3_REPO/README.md" "allow" "onboarding: Read README tracked"
layer3_call "s1" "Read" "$LAYER3_REPO/CLAUDE.md" "allow" "onboarding: Read CLAUDE.md tracked"
layer3_call "s1" "Write" "$LAYER3_REPO/src.md" "allow" "onboarding: after required reads, write allows"

# 3-4. LDM_GUARD_SKIP_ONBOARDING is ignored (removed v1.9.82)
# The env var used to bypass onboarding as a workaround for the
# cross-session state-file bug. With that bug fixed at the root (per-
# session state files), the bypass is gone. Setting the env var has no
# effect: the block stands until the docs are read.
layer3_call "s2" "Write" "$LAYER3_REPO/src.md" "deny" "onboarding: LDM_GUARD_SKIP_ONBOARDING=repo IGNORED (still denies)" "LDM_GUARD_SKIP_ONBOARDING=$LAYER3_REPO"
layer3_call "s3" "Write" "$LAYER3_REPO/src.md" "deny" "onboarding: LDM_GUARD_SKIP_ONBOARDING=1 IGNORED (still denies)" "LDM_GUARD_SKIP_ONBOARDING=1"

# 6. Session reset: new session_id gets its own per-session state file
# First, onboard s5 by reading + writing
layer3_call "s5" "Read" "$LAYER3_REPO/README.md" "allow" "session-reset: s5 reads README"
layer3_call "s5" "Read" "$LAYER3_REPO/CLAUDE.md" "allow" "session-reset: s5 reads CLAUDE.md"
layer3_call "s5" "Write" "$LAYER3_REPO/src.md" "allow" "session-reset: s5 first write after reads"
# Fresh session has its own empty state file, must re-read.
layer3_call "s6" "Write" "$LAYER3_REPO/src.md" "deny" "session-reset: new session requires fresh reads"

# 6b. Cross-session state isolation (v1.9.82+ regression guard)
#     Pre-1.9.82: single shared ~/.ldm/state/guard-session.json; every
#     session's tool calls wiped every other session's onboarding + reads.
#     Post-1.9.82: one file per session at guard-session-<sid>.json. This
#     test does the exact pattern that broke in prior versions: session A
#     onboards, session B makes a tool call, session A writes again.
layer3_call "iso-a" "Read" "$LAYER3_REPO/README.md" "allow" "iso: session A reads README"
layer3_call "iso-a" "Read" "$LAYER3_REPO/CLAUDE.md" "allow" "iso: session A reads CLAUDE.md"
layer3_call "iso-a" "Write" "$LAYER3_REPO/iso-a1.md" "allow" "iso: session A writes after onboarding"
# Session B's activity must not clobber A's state.
layer3_call "iso-b" "Read" "$LAYER3_REPO/README.md" "allow" "iso: session B reads README (does not wipe A)"
# Session A's second write should still pass. THIS IS THE BUG: pre-1.9.82
# this denied because session B's tool call wiped the shared state file.
layer3_call "iso-a" "Write" "$LAYER3_REPO/iso-a2.md" "allow" "iso: session A still onboarded after B's activity"
# Session B is NOT onboarded for this repo (only read README, not CLAUDE).
# Per-session state keeps its partial-onboarding isolated to itself.
layer3_call "iso-b" "Write" "$LAYER3_REPO/iso-b1.md" "deny" "iso: session B still needs its own CLAUDE.md read"
# Per-session files actually exist on disk with the expected names.
if [[ -f "$LAYER3_STATE/guard-session-iso-a.json" ]]; then
  echo "  PASS: iso: per-session file for A exists on disk"
  ((PASS++))
else
  echo "  FAIL: iso: per-session file for A missing"
  ((FAIL++))
fi
if [[ -f "$LAYER3_STATE/guard-session-iso-b.json" ]]; then
  echo "  PASS: iso: per-session file for B exists on disk"
  ((PASS++))
else
  echo "  FAIL: iso: per-session file for B missing"
  ((FAIL++))
fi

# 7. Blocked-file tracking: to exercise the recent-denials tail, we need a
#    prior denial on a specific path. Onboarding denials are path=repo, not
#    path=file, so they don't trigger blocked-file-retry on a subsequent
#    file-specific write. Instead, simulate by running Write on main (which
#    denies with path=file) and then try to Bash-write the same file.
#    (main-branch tests only work when test runner is on main.)
if [[ "$ON_MAIN" == "true" ]]; then
  rm -f "$LAYER3_STATE/guard-session.json"
  # Pretend we're editing a main-tree file (uses the test runner's own repo)
  MAIN_TREE=$(git rev-parse --show-toplevel)
  TEST_FILE="$MAIN_TREE/tools/wip-branch-guard/this-file-does-not-exist.md"
  layer3_call "s7" "Edit" "$TEST_FILE" "deny" "blocked-file: Edit on main denies"
  layer3_call "s7" "Bash" "cat > $TEST_FILE" "deny" "blocked-file: Bash cat > same path denies (equivalent-action)"
  # LDM_GUARD_ACK_BLOCKED_FILE is ignored (removed v1.9.82). The block
  # stands; surface the original denial rather than ack-and-continue.
  layer3_call "s7" "Bash" "cat > $TEST_FILE" "deny" "blocked-file: LDM_GUARD_ACK_BLOCKED_FILE=path IGNORED (still denies)" "LDM_GUARD_ACK_BLOCKED_FILE=$TEST_FILE"
else
  echo "  SKIP: blocked-file main-tree tests (needs main branch)"
  ((SKIP+=3))
fi

# 8. Audit log: every deny writes a line; verify after the test run
if [[ -f "$LAYER3_STATE/bypass-audit.jsonl" ]]; then
  audit_lines=$(wc -l < "$LAYER3_STATE/bypass-audit.jsonl" | tr -d ' ')
  if [[ "$audit_lines" -gt 0 ]]; then
    echo "  PASS: audit log written ($audit_lines entries)"
    ((PASS++))
  else
    echo "  FAIL: audit log exists but empty"
    ((FAIL++))
  fi
else
  echo "  FAIL: audit log not created"
  ((FAIL++))
fi

# 9. Approval-backend behavior is covered end-to-end by the onboarding
#    override tests above (target-match, boolean "1", wrong-target). The
#    standalone unit check lived against lib/approval-backend.mjs which was
#    inlined in v1.9.78 after the installer's subdir-flatten bug; no separate
#    module exists to import-test. Skip.

# 10. Shared-state file writes still allowed even without onboarding (regression)
rm -f "$LAYER3_STATE/guard-session.json"
layer3_call "s-shared" "Write" "$HOME/.claude/plans/test-layer3-plan.md" "allow" "layer3 skips shared-state (plans) without onboarding"
layer3_call "s-shared2" "Write" "$HOME/.claude/projects/x/memory/test.md" "allow" "layer3 skips shared-state (auto-memory) without onboarding"

# Cleanup
rm -rf "$LAYER3_TMP"

echo ""
echo "--- External-PR guard (new in 1.9.80) ---"
# Builds two tmp git repos with different origins (wipcomputer vs lesaai),
# so the cwd-based origin resolution path can be exercised. All JSON
# payloads include cwd so the guard resolves origin from the test repo,
# not the harness's own cwd.

EPR_TMP_RAW="$(mktemp -d /tmp/guard-ext-pr-XXXX)"
EPR_TMP="$(cd "$EPR_TMP_RAW" && pwd -P)"
EPR_WIP="$EPR_TMP/wipcomputer-repo"
EPR_EXT="$EPR_TMP/lesaai-repo"
EPR_STATE="$EPR_TMP/state"
mkdir -p "$EPR_WIP" "$EPR_EXT" "$EPR_STATE"
(
  cd "$EPR_WIP" && git init -q -b main && git remote add origin git@github.com:wipcomputer/imsg.git
  cd "$EPR_EXT" && git init -q -b main && git remote add origin git@github.com:lesaai/imsg.git
) >/dev/null 2>&1

# Helper: send a Bash tool_use with a given command and cwd.
epr_call() {
  local desc="$1" expect="$2" cmd="$3" cwd="$4" extra_env="$5"
  local json output actual="allow"
  json=$(node -e "process.stdout.write(JSON.stringify({hook_event_name:'PreToolUse',session_id:'epr',tool_name:'Bash',tool_input:{command:process.argv[1]},cwd:process.argv[2]}))" "$cmd" "$cwd")
  output=$(echo "$json" | env LDM_GUARD_STATE_DIR="$EPR_STATE" $extra_env node "$GUARD" 2>/dev/null)
  if echo "$output" | grep -q '"deny"'; then actual="deny"; fi
  if [[ "$actual" == "$expect" ]]; then
    echo "  PASS: $desc"
    ((PASS++))
  else
    echo "  FAIL: $desc (expected $expect, got $actual)"
    ((FAIL++))
  fi
}

# 1. --repo flag: external -> deny
epr_call "--repo steipete/imsg denies" deny "gh pr create --repo steipete/imsg --title x --body y" "$EPR_WIP"
# 2. --repo flag: wipcomputer -> allow (internal)
epr_call "--repo wipcomputer/imsg allows" allow "gh pr create --repo wipcomputer/imsg --title x --body y" "$EPR_WIP"
# 3. Override: target-specific env
epr_call "LDM_GUARD_UPSTREAM_PR_APPROVED=target allows" allow "gh pr create --repo steipete/imsg --title x --body y" "$EPR_WIP" "LDM_GUARD_UPSTREAM_PR_APPROVED=steipete/imsg"
# 4. Override: boolean
epr_call "LDM_GUARD_UPSTREAM_PR_APPROVED=1 allows" allow "gh pr create --repo steipete/imsg --title x --body y" "$EPR_WIP" "LDM_GUARD_UPSTREAM_PR_APPROVED=1"
# 5. Override: wrong target denies
epr_call "LDM_GUARD_UPSTREAM_PR_APPROVED=mismatch denies" deny "gh pr create --repo steipete/imsg --title x --body y" "$EPR_WIP" "LDM_GUARD_UPSTREAM_PR_APPROVED=other/repo"
# 6. Implicit: cwd origin = lesaai/imsg -> deny
epr_call "implicit origin lesaai/ denies" deny "gh pr create --title x --body y" "$EPR_EXT"
# 7. Implicit: cwd origin = wipcomputer/imsg -> allow
epr_call "implicit origin wipcomputer/ allows" allow "gh pr create --title x --body y" "$EPR_WIP"
# 8. Raw API POST to pulls on external -> deny
epr_call "gh api pulls POST external denies" deny "gh api repos/steipete/imsg/pulls -X POST -f title=x -f head=main -f base=main" "$EPR_WIP"
# 9. Raw API POST to pulls on wipcomputer -> allow
epr_call "gh api pulls POST internal allows" allow "gh api repos/wipcomputer/imsg/pulls -X POST -f title=x" "$EPR_WIP"
# 10. Non-create gh: pr view external -> allow (read-only)
epr_call "gh pr view external allows" allow "gh pr view 5 --repo steipete/imsg" "$EPR_WIP"
# 11. Non-create gh: pr merge external -> allow (merge is on own PR, not create)
epr_call "gh pr merge external allows" allow "gh pr merge 5 --repo steipete/imsg --merge" "$EPR_WIP"
# 12. Non-create gh api: issues on external -> allow
epr_call "gh api issues external allows" allow "gh api repos/steipete/imsg/issues -X POST -f title=bug" "$EPR_WIP"

# Cleanup
rm -rf "$EPR_TMP"

echo ""
echo "--- Canonical repo key: onboarding shared across worktrees (new in 1.9.81) ---"
# Build a tmp src repo with a stable remote origin + two worktrees off
# feature branches. Onboarding in worktree A should satisfy worktree B
# of the same repo without re-reading.

CAN_TMP_RAW="$(mktemp -d /tmp/guard-canonical-XXXX)"
CAN_TMP="$(cd "$CAN_TMP_RAW" && pwd -P)"
CAN_SRC="$CAN_TMP/src"
CAN_WT_A="$CAN_TMP/wt-a"
CAN_WT_B="$CAN_TMP/wt-b"
CAN_STATE="$CAN_TMP/state"
mkdir -p "$CAN_SRC" "$CAN_STATE"
(
  cd "$CAN_SRC"
  git init -q -b main
  git remote add origin git@github.com:testowner/testrepo.git
  echo "# test" > README.md
  echo "# test" > CLAUDE.md
  git add README.md CLAUDE.md
  git -c user.email=t@t -c user.name=t commit -q -m init
  git worktree add -q -b feat-a "$CAN_WT_A"
  git worktree add -q -b feat-b "$CAN_WT_B"
) >/dev/null 2>&1

canonical_call() {
  local desc="$1" tool="$2" arg="$3" expect="$4" extra_env="$5"
  local json output actual="allow"
  if [[ "$tool" == "Bash" ]]; then
    json=$(node -e "process.stdout.write(JSON.stringify({hook_event_name:'PreToolUse',session_id:'canon',tool_name:'Bash',tool_input:{command:process.argv[1]}}))" "$arg")
  else
    json=$(node -e "process.stdout.write(JSON.stringify({hook_event_name:'PreToolUse',session_id:'canon',tool_name:process.argv[1],tool_input:{file_path:process.argv[2]}}))" "$tool" "$arg")
  fi
  output=$(echo "$json" | env LDM_GUARD_STATE_DIR="$CAN_STATE" $extra_env node "$GUARD" 2>/dev/null)
  if echo "$output" | grep -q '"deny"'; then actual="deny"; fi
  if [[ "$actual" == "$expect" ]]; then
    echo "  PASS: $desc"
    ((PASS++))
  else
    echo "  FAIL: $desc (expected $expect, got $actual)"
    ((FAIL++))
  fi
}

# 1. Read both onboarding docs in worktree A.
canonical_call "worktree A: Read README" "Read" "$CAN_WT_A/README.md" "allow"
canonical_call "worktree A: Read CLAUDE.md" "Read" "$CAN_WT_A/CLAUDE.md" "allow"
# 2. Write in worktree A: allowed (onboarded).
canonical_call "worktree A: Write allows after reads" "Write" "$CAN_WT_A/src.md" "allow"
# 3. Write in worktree B of the SAME repo, no Reads in B, same session.
#    Must allow because canonical key (origin URL) matches.
canonical_call "worktree B: Write allows without re-reading (canonical key shared)" "Write" "$CAN_WT_B/src.md" "allow"

# 4. Regression: different repo, different canonical key, still requires onboarding.
CAN_OTHER_SRC="$CAN_TMP/other-src"
CAN_OTHER_WT="$CAN_TMP/other-wt"
mkdir -p "$CAN_OTHER_SRC"
(
  cd "$CAN_OTHER_SRC"
  git init -q -b main
  git remote add origin git@github.com:other/otherrepo.git
  echo "# other" > README.md
  echo "# other" > CLAUDE.md
  git add README.md CLAUDE.md
  git -c user.email=t@t -c user.name=t commit -q -m init
  git worktree add -q -b feat "$CAN_OTHER_WT"
) >/dev/null 2>&1
canonical_call "different repo: Write still denies even with same session" "Write" "$CAN_OTHER_WT/src.md" "deny"

# 5. Repo with no origin URL: fallback to main-worktree path still shares
#    onboarding across worktrees of that repo.
CAN_NOREMOTE_SRC="$CAN_TMP/noremote-src"
CAN_NOREMOTE_WT="$CAN_TMP/noremote-wt"
mkdir -p "$CAN_NOREMOTE_SRC"
(
  cd "$CAN_NOREMOTE_SRC"
  git init -q -b main
  echo "# nr" > README.md
  echo "# nr" > CLAUDE.md
  git add README.md CLAUDE.md
  git -c user.email=t@t -c user.name=t commit -q -m init
  git worktree add -q -b feat "$CAN_NOREMOTE_WT"
) >/dev/null 2>&1
canonical_call "no-origin repo: Read README in src" "Read" "$CAN_NOREMOTE_SRC/README.md" "allow"
canonical_call "no-origin repo: Read CLAUDE in src" "Read" "$CAN_NOREMOTE_SRC/CLAUDE.md" "allow"
canonical_call "no-origin repo: Write in worktree uses main-tree fallback" "Write" "$CAN_NOREMOTE_WT/src.md" "allow"

# Cleanup
rm -rf "$CAN_TMP"

echo ""
echo "=== Results: $PASS passed, $FAIL failed, $SKIP skipped ==="
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
