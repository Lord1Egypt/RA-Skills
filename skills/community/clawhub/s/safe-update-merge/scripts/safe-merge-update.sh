#!/usr/bin/env bash
# safe-merge-update.sh
#
# Safe upstream merge pipeline with optional automated conflict resolution.
#
# ── Flags ─────────────────────────────────────────────────────────────────────
#   --dry-run          Show what would happen; make NO changes (fetch-only)
#   --no-auto-resolve  Stop on conflicts instead of invoking claude (manual review mode)
#   --resume <branch>  Skip merge; jump to build → stage → restart on an existing branch
#   --promote <branch> After user confirms gateway is healthy: push to TARGET_BRANCH,
#                      switch local branch, delete safe-merge branch. Run this ONLY
#                      after the user has verified the running gateway is acceptable.
#
# ── Two-phase promote model ────────────────────────────────────────────────────
#
#   Phase 1 (automated):
#     merge → build → restart gateway from safe-merge branch → report to user
#     TARGET_BRANCH (local-desktop-main) is NOT touched yet.
#     No force-push to remote until the user confirms.
#
#   Phase 2 (user-confirmed):
#     REPO_DIR=. ./scripts/safe-merge-update.sh --promote safe-merge-2026-03-02
#     → pushes safe-merge branch to TARGET_REMOTE/TARGET_BRANCH
#     → switches local branch to TARGET_BRANCH
#     → deletes safe-merge branch
#
#   This means a bad merge can be rolled back simply by restarting from the
#   previous TARGET_BRANCH — which was never overwritten.
#
# ── Required environment ──────────────────────────────────────────────────────
#   REPO_DIR          Path to your OpenClaw repo (required; git must be installed)
#
# ── Optional environment (all have sensible defaults) ─────────────────────────
#   UPSTREAM_REMOTE   Remote for upstream OpenClaw  (default: upstream)
#   UPSTREAM_BRANCH   Branch to merge from          (default: main)
#   TARGET_REMOTE     Remote to push to on --promote (default: myfork)
#   TARGET_BRANCH     Branch to promote to           (default: local-desktop-main)
#   LOCAL_BRANCH      Branch you are merging from   (default: current branch)
#   PACKAGE_MGR       Build tool: npm or pnpm       (default: auto-detect)
#
# ── Runtime requirements ──────────────────────────────────────────────────────
#   Required:  git (merge, branch, push)
#   Optional:  claude (--auto-resolve only; install: npm i -g @anthropic-ai/claude-code)
#              python3 (preflight JSON report)
#              systemctl (gateway restart; systemd hosts only)
#
# ── Usage examples ────────────────────────────────────────────────────────────
#   REPO_DIR=~/openclaw ./scripts/safe-merge-update.sh --dry-run
#   REPO_DIR=~/openclaw ./scripts/safe-merge-update.sh
#   REPO_DIR=~/openclaw ./scripts/safe-merge-update.sh --no-auto-resolve
#   REPO_DIR=~/openclaw ./scripts/safe-merge-update.sh --resume safe-merge-2026-03-02
#   REPO_DIR=~/openclaw ./scripts/safe-merge-update.sh --promote safe-merge-2026-03-02
#
# ⚠️  HIGH-IMPACT OPERATIONS:
#   Phase 1 (--dry-run safe): merge, build, gateway restart from safe-merge branch
#   Phase 2 (--promote only): force-push to TARGET_REMOTE/TARGET_BRANCH, branch delete
#   With --auto-resolve: sends redacted file content to the Anthropic API via claude CLI
#     (Edit+Read tools only; Bash explicitly excluded — no shell execution granted to model)
#
# Run scripts/preflight.sh first and review /tmp/safe-merge/preflight-report.json.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Flag parsing ──────────────────────────────────────────────────────────────
DRY_RUN=false
AUTO_RESOLVE=true
RESUME_BRANCH=""
PROMOTE_BRANCH=""
POSITIONAL=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)          DRY_RUN=true; shift ;;
    --no-auto-resolve)  AUTO_RESOLVE=false; shift ;;
    --auto-resolve)     AUTO_RESOLVE=true; shift ;;
    --resume)           RESUME_BRANCH="${2:-}"; shift 2 || shift ;;
    --promote)          PROMOTE_BRANCH="${2:-}"; shift 2 || shift ;;
    *)                  POSITIONAL+=("$1"); shift ;;
  esac
done
set -- "${POSITIONAL[@]+"${POSITIONAL[@]}"}"

# ── Config (all overridable via env) ─────────────────────────────────────────
REPO_DIR="${REPO_DIR:?REPO_DIR must be set to your OpenClaw repo path}"
UPSTREAM_REMOTE="${UPSTREAM_REMOTE:-upstream}"
UPSTREAM_BRANCH="${UPSTREAM_BRANCH:-main}"
TARGET_REMOTE="${TARGET_REMOTE:-myfork}"
TARGET_BRANCH="${TARGET_BRANCH:-local-desktop-main}"
LOCAL_BRANCH="${LOCAL_BRANCH:-}"

if [[ -z "${PACKAGE_MGR:-}" ]]; then
  if [[ -f "$REPO_DIR/package-lock.json" ]]; then
    PACKAGE_MGR="npm"
  elif [[ -f "$REPO_DIR/pnpm-lock.yaml" ]]; then
    PACKAGE_MGR="pnpm"
  else
    PACKAGE_MGR="npm"
  fi
fi

SOURCE_BRANCH="${UPSTREAM_REMOTE}/${UPSTREAM_BRANCH}"
DATE=$(date +%Y-%m-%d)
SAFE_BRANCH="safe-merge-${DATE}"

# ── Helpers ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info()    { echo -e "${CYAN}▶ $*${NC}"; }
success() { echo -e "${GREEN}✔ $*${NC}"; }
warn()    { echo -e "${YELLOW}⚠ $*${NC}"; }
fail()    { echo -e "${RED}✘ $*${NC}"; }

run_build() {
  "$PACKAGE_MGR" run build 2>&1
  "$PACKAGE_MGR" run ui:build 2>&1
}

build_failed() {
  fail "Build failed on ${1}."
  warn "Branch left intact for investigation: git checkout ${1}"
  warn "To discard: git checkout ${TARGET_BRANCH} && git branch -D ${1}"
  exit 1
}

restart_gateway() {
  if command -v systemctl &>/dev/null && systemctl --user list-units --type=service 2>/dev/null | grep -q "openclaw-gateway"; then
    info "Restarting gateway in 3s…"
    (sleep 3 && systemctl --user restart openclaw-gateway) &
  else
    warn "systemctl not found or openclaw-gateway unit not present — skipping gateway restart."
    warn "Restart manually if needed."
  fi
}

# ── Promote mode ──────────────────────────────────────────────────────────────
# Run ONLY after user confirms the gateway is healthy on the safe-merge branch.
# This is Phase 2 — it was intentionally not run automatically after the build.
if [[ -n "$PROMOTE_BRANCH" ]]; then
  cd "$REPO_DIR"

  if ! git rev-parse --verify "$PROMOTE_BRANCH" &>/dev/null; then
    fail "Branch '${PROMOTE_BRANCH}' does not exist."
    echo "  Available safe-merge branches:"
    git branch | grep "safe-merge" || echo "  (none)"
    exit 1
  fi

  echo ""
  info "Phase 2: Promoting ${PROMOTE_BRANCH} → ${TARGET_REMOTE}/${TARGET_BRANCH}"
  echo "  This will force-push ${PROMOTE_BRANCH} to ${TARGET_REMOTE}/${TARGET_BRANCH}"
  echo "  and delete the local ${PROMOTE_BRANCH} branch."
  echo ""

  git push "$TARGET_REMOTE" "${PROMOTE_BRANCH}:${TARGET_BRANCH}" --force
  success "Pushed to ${TARGET_REMOTE}/${TARGET_BRANCH}"

  git checkout "$TARGET_BRANCH"
  git reset --hard "$PROMOTE_BRANCH"
  git branch -D "$PROMOTE_BRANCH"

  # Clear the Phase 2 pending state file so the UI stops showing the prompt
  PENDING_STATE_FILE="${HOME}/.openclaw/safe-merge-pending.json"
  rm -f "$PENDING_STATE_FILE" 2>/dev/null || true

  success "Promoted. Now on ${TARGET_BRANCH}: $(git log --oneline -1)"
  echo ""
  echo "  ✅ Merge complete and confirmed."
  exit 0
fi

# ── Resume mode ───────────────────────────────────────────────────────────────
# Skip merge; run build → stage → restart on an existing safe-merge branch.
# Use after manually resolving conflicts.
if [[ -n "$RESUME_BRANCH" ]]; then
  cd "$REPO_DIR"
  git checkout "$RESUME_BRANCH"
  info "Resuming from build on ${RESUME_BRANCH}…"
  run_build || { fail "Build failed."; exit 1; }
  success "Build passed."

  restart_gateway

  echo ""
  success "Resume + restart complete. Gateway running from ${RESUME_BRANCH}."
  echo ""
  warn "⚠️  TARGET_BRANCH (${TARGET_BRANCH}) has NOT been updated yet."
  echo "  Verify the gateway is working, then run:"
  echo "    REPO_DIR=${REPO_DIR} $0 --promote ${RESUME_BRANCH}"
  exit 0
fi

# ── Preflight ─────────────────────────────────────────────────────────────────
cd "$REPO_DIR"

# Ensure unique branch name
COUNTER=2; ORIG="$SAFE_BRANCH"
while git rev-parse --verify "$SAFE_BRANCH" &>/dev/null; do
  SAFE_BRANCH="${ORIG}-${COUNTER}"; COUNTER=$((COUNTER + 1))
done

LOCAL_BRANCH="${LOCAL_BRANCH:-$(git branch --show-current)}"

$DRY_RUN && warn "DRY RUN — no changes will be made"
info "Safe-merge update"
echo "  Repo:     ${REPO_DIR}"
echo "  Source:   ${SOURCE_BRANCH}"
echo "  Target:   ${TARGET_REMOTE}/${TARGET_BRANCH}  ← pushed only after --promote"
echo "  Branch:   ${SAFE_BRANCH}"
echo "  Builder:  ${PACKAGE_MGR}"
echo "  Dry-run:  ${DRY_RUN}"
echo "  Auto-resolve conflicts: ${AUTO_RESOLVE}"
echo ""

CURRENT=$(git branch --show-current)
if [[ "$CURRENT" != "$TARGET_BRANCH" ]]; then
  fail "Must be on '${TARGET_BRANCH}' (currently on '${CURRENT}')."
  echo "  Run: git checkout ${TARGET_BRANCH}"
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  fail "Working tree is not clean. Commit or stash changes first."
  exit 1
fi

info "Fetching remotes…"
git fetch --all --quiet

# ── Dry-run: show divergence and exit ────────────────────────────────────────
if $DRY_RUN; then
  BEHIND=$(git rev-list --count "HEAD..${SOURCE_BRANCH}" 2>/dev/null || echo "?")
  AHEAD=$(git rev-list --count "${SOURCE_BRANCH}..HEAD" 2>/dev/null || echo "?")
  echo ""
  info "Divergence vs ${SOURCE_BRANCH}:"
  echo "  Behind (upstream commits to pull): ${BEHIND}"
  echo "  Ahead  (local commits not in upstream): ${AHEAD}"
  echo ""
  CONFLICTS=$(git merge-tree "$(git merge-base HEAD "${SOURCE_BRANCH}")" HEAD "${SOURCE_BRANCH}" \
    2>/dev/null | grep -c "^+<<<<<<" || true)
  echo "  Estimated conflicting hunks: ${CONFLICTS}"
  echo ""
  success "Dry run complete — no changes made."
  exit 0
fi

# ── Prune stale safe-merge branches ──────────────────────────────────────────
STALE=$(git branch | grep -E "^\s*safe-merge-" | tr -d ' ' || true)
if [[ -n "$STALE" ]]; then
  info "Pruning stale safe-merge branches…"
  for b in $STALE; do git branch -D "$b" && echo "  deleted: $b"; done
fi

# ── Create + merge ────────────────────────────────────────────────────────────
info "Creating branch: ${SAFE_BRANCH}"
git checkout -b "$SAFE_BRANCH"

info "Merging ${SOURCE_BRANCH}…"
if git merge "$SOURCE_BRANCH" --no-edit; then
  success "Merge clean — no conflicts."
else
  CONFLICT_LIST=$(git diff --name-only --diff-filter=U)
  CONFLICT_COUNT=$(echo "$CONFLICT_LIST" | wc -l | tr -d ' ')
  warn "${CONFLICT_COUNT} conflict(s) detected."

  if ! $AUTO_RESOLVE; then
    fail "Conflicts detected. Resolve manually and re-run with --resume."
    echo "$CONFLICT_LIST" | while read -r f; do warn "  $f"; done
    warn "  To resume:  REPO_DIR=${REPO_DIR} $0 --resume ${SAFE_BRANCH}"
    exit 1
  fi

  if ! command -v claude &>/dev/null; then
    fail "'claude' CLI not found — cannot auto-resolve."
    warn "Install: npm i -g @anthropic-ai/claude-code"
    warn "Then resume: REPO_DIR=${REPO_DIR} $0 --resume ${SAFE_BRANCH}"
    exit 1
  fi

  # ── Redact secrets before sending to claude ─────────────────────────────
  # redact-secrets.sh writes the map to fd 3 (not stdout/stderr).
  # We wire fd 3 to a per-file temp file in a mode-700 dir.
  # Maps are deleted immediately after secret restoration.
  REDACT_SCRIPT="${SCRIPT_DIR}/redact-secrets.sh"
  REDACT_MAP_DIR=$(mktemp -d)
  chmod 700 "$REDACT_MAP_DIR"
  declare -A REDACT_MAPS

  if [[ -x "$REDACT_SCRIPT" ]]; then
    info "Redacting secrets in conflicted files before model transmission…"
    info "(Maps written to mode-700 temp dir: ${REDACT_MAP_DIR} — deleted after restoration)"
    while IFS= read -r file; do
      [[ -z "$file" || ! -f "$file" ]] && continue
      MAP_FILE="${REDACT_MAP_DIR}/$(echo "$file" | tr '/' '_').map"
      exec 3>"$MAP_FILE"
      REDACTED=$("$REDACT_SCRIPT" "$file")
      exec 3>&-
      echo "$REDACTED" > "$file"
      REDACT_MAPS["$file"]="$MAP_FILE"
    done <<< "$CONFLICT_LIST"
    success "Secrets redacted. Maps held in ${REDACT_MAP_DIR} (mode 700, deleted after restore)."
  else
    warn "redact-secrets.sh not found — proceeding WITHOUT secret redaction."
    warn "Inspect conflicted files for secrets before continuing."
  fi

  # ── Invoke claude to resolve conflicts ───────────────────────────────────
  info "Invoking claude to resolve ${CONFLICT_COUNT} conflict(s)…"
  # Bash tool intentionally excluded — the script commits after claude exits.
  # Claude can only read and edit files; no shell execution granted.
  claude --allowedTools "Edit,Read" --print "$(cat <<PROMPT
You are resolving git merge conflicts in the OpenClaw repository at ${REPO_DIR}.
Branch: ${SAFE_BRANCH}

Conflicted files:
${CONFLICT_LIST}

NOTE: File content has been pre-processed for security. Do not attempt to un-redact
or infer any [REDACTED_N] placeholders — leave them exactly as-is.

Resolution strategy (priority order):
1. local-desktop-main UI/vault/navigation customizations → keep HEAD (ours)
2. Upstream security and bug fixes → keep incoming when clearly a fix
3. Both sides add new code (additive) → include both
4. TypeScript type unions → union both sides
5. Genuinely ambiguous → prefer HEAD

Steps:
1. Read each conflicted file (look for <<<<<<< HEAD / ======= / >>>>>>> markers)
2. Resolve each conflict per strategy using the Edit tool — write clean content with no conflict markers
3. When ALL files are resolved, reply with: CONFLICTS_RESOLVED

Do NOT run any shell commands (git, npm, etc.) — the calling script handles those.
Do NOT modify files that have no conflict markers.
PROMPT
)"

  # Script handles the commit — not claude (Bash tool not granted)
  if git diff --name-only | grep -q . || git diff --cached --name-only | grep -q .; then
    git add -A && git commit --no-edit
  fi

  # ── Restore redacted secrets ─────────────────────────────────────────────
  if [[ -x "$REDACT_SCRIPT" && ${#REDACT_MAPS[@]} -gt 0 ]]; then
    info "Restoring redacted secrets…"
    for file in "${!REDACT_MAPS[@]}"; do
      MAP_FILE="${REDACT_MAPS[$file]}"
      if [[ -f "$file" && -f "$MAP_FILE" && -s "$MAP_FILE" ]]; then
        RESTORED=$(cat "$file" | "$REDACT_SCRIPT" --restore --map-file "$MAP_FILE")
        echo "$RESTORED" > "$file"
      fi
    done
    rm -rf "$REDACT_MAP_DIR"
    success "Secrets restored. Map directory deleted."
  fi

  # ── Verify all conflicts resolved ────────────────────────────────────────
  if git diff --name-only --diff-filter=U | grep -q .; then
    fail "Claude did not resolve all conflicts."
    git diff --name-only --diff-filter=U | while read -r f; do warn "  unresolved: $f"; done
    warn "Resolve manually, then: REPO_DIR=${REPO_DIR} $0 --resume ${SAFE_BRANCH}"
    exit 1
  fi

  success "All conflicts resolved."
fi

# ── Build ─────────────────────────────────────────────────────────────────────
info "Building (${PACKAGE_MGR})…"
run_build || build_failed "$SAFE_BRANCH"
success "Build passed."

# ── Phase 1 complete: restart gateway, await confirmation ─────────────────────
# ⚠️  TARGET_BRANCH is intentionally NOT updated here.
# The gateway restarts from the current working tree (safe-merge branch).
# The user must verify and then run --promote to push to TARGET_BRANCH.
restart_gateway

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
success "Phase 1 complete — merge built and gateway restarting."
echo ""
echo "  Safe-merge branch : ${SAFE_BRANCH}"
echo "  Gateway running from: ${SAFE_BRANCH} build (dist/)"
echo ""
warn "  ⚠️  ${TARGET_BRANCH} has NOT been updated yet."
warn "  ⚠️  Remote ${TARGET_REMOTE}/${TARGET_BRANCH} has NOT been pushed yet."
echo ""
echo "  ➡️  Please verify the gateway is working, then confirm with:"
echo "      REPO_DIR=${REPO_DIR} $0 --promote ${SAFE_BRANCH}"
echo ""
echo "  To roll back (before confirming): restart gateway — ${TARGET_BRANCH} is unchanged."
echo "  To discard this merge entirely:   git checkout ${TARGET_BRANCH} && git branch -D ${SAFE_BRANCH}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Write Phase 2 pending state file so the UI can show an approval notification
PENDING_STATE_FILE="${HOME}/.openclaw/safe-merge-pending.json"
mkdir -p "$(dirname "$PENDING_STATE_FILE")" 2>/dev/null || true
cat > "$PENDING_STATE_FILE" <<PENDING_EOF
{
  "branch": "${SAFE_BRANCH}",
  "repoDir": "${REPO_DIR}",
  "targetRemote": "${TARGET_REMOTE}",
  "targetBranch": "${TARGET_BRANCH}",
  "completedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
PENDING_EOF
echo "  📋 Phase 2 state written: ${PENDING_STATE_FILE}"
