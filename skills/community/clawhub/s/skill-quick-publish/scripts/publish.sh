#!/usr/bin/env bash
# publish.sh — One-click skill publishing orchestrator
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Defaults ──────────────────────────────────────────────
SKILL_PATH=""
GH_REPO="${SKILL_GH_REPO:-}"
BRANCH="main"
SKIP_BEAR=false
SKIP_GITHUB=false
DRY_RUN=false
FORCE=false
CONTINUE_ON_ERROR=false
CHANGELOG="Automated publish"
VERSION=""
BEAR_TAG="${SKILL_BEAR_TAG:-skill-dev}"

# ── Parse args ────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)       GH_REPO="$2"; shift 2 ;;
    --branch)     BRANCH="$2"; shift 2 ;;
    --skip-bear)  SKIP_BEAR=true; shift ;;
    --skip-github) SKIP_GITHUB=true; shift ;;
    --dry-run)    DRY_RUN=true; shift ;;
    --force)      FORCE=true; shift ;;
    --continue-on-error) CONTINUE_ON_ERROR=true; shift ;;
    --changelog)  CHANGELOG="$2"; shift 2 ;;
    --version)    VERSION="$2"; shift 2 ;;
    -*) echo "Unknown flag: $1"; exit 1 ;;
    *)  SKILL_PATH="$1"; shift ;;
  esac
done

# ── Validate ──────────────────────────────────────────────
if [[ -z "$SKILL_PATH" ]]; then
  echo "❌ Usage: publish.sh <skill-path> [--repo owner/repo] [options]"
  exit 1
fi

SKILL_PATH="$(cd "$SKILL_PATH" && pwd)"
SKILL_NAME="$(basename "$SKILL_PATH")"

if [[ ! -f "$SKILL_PATH/SKILL.md" ]]; then
  echo "❌ No SKILL.md found in $SKILL_PATH"
  exit 1
fi

# Extract version from SKILL.md frontmatter or use arg/default
if [[ -z "$VERSION" ]]; then
  VERSION="$(grep -m1 '^version:' "$SKILL_PATH/SKILL.md" 2>/dev/null | sed 's/version:[[:space:]]*//' | tr -d '"' | tr -d "'" || true)"
  VERSION="${VERSION:-0.1.0}"
fi

# Extract description for clawhub
SKILL_DESC="$(grep -m1 '^description:' "$SKILL_PATH/SKILL.md" | sed 's/description:[[:space:]]*//' | head -c 200)"

echo "🚀 Publishing skill: $SKILL_NAME v$VERSION"
echo "   Path: $SKILL_PATH"
[[ -n "$GH_REPO" ]] && echo "   Repo: $GH_REPO ($BRANCH)"
echo "   Changelog: $CHANGELOG"
echo ""

step_ok()   { echo "✅ $1"; }
step_fail() { echo "❌ $1"; if [[ "$CONTINUE_ON_ERROR" != "true" ]]; then exit 1; fi; }
dry_label() { echo "   (dry-run) $1"; }

# ── Step 1: Duplicate Check ──────────────────────────────
echo "── Step 1: Duplicate Check ──"

if [[ "$DRY_RUN" == "true" ]]; then
  dry_label "Would check local skills + ClawHub registry for '$SKILL_NAME'"
else
  # Local check
  for existing in ~/.openclaw/skills/*/; do
    ename="$(basename "$existing")"
    if [[ "$ename" == "$SKILL_NAME" ]]; then
      echo "⚠️  Skill '$SKILL_NAME' already exists locally at $existing"
      if [[ "$FORCE" != "true" ]]; then
        echo "   Use --force to override"
        step_fail "Duplicate check failed"
      else
        echo "   --force set, continuing"
      fi
    fi
  done

  # ClawHub registry check
  if command -v clawhub &>/dev/null; then
    search_result="$(clawhub search "$SKILL_NAME" 2>/dev/null || true)"
    if echo "$search_result" | grep -qi "$SKILL_NAME"; then
      echo "⚠️  Skill '$SKILL_NAME' found on ClawHub registry"
      if [[ "$FORCE" != "true" ]]; then
        echo "   Use --force to override"
        step_fail "Duplicate check failed"
      else
        echo "   --force set, continuing"
      fi
    fi
  fi
  step_ok "Duplicate check passed"
fi

# ── Step 2: Bear Notes Sync ──────────────────────────────
echo "── Step 2: Bear Notes Sync ──"

if [[ "$SKIP_BEAR" == "true" ]]; then
  echo "⏭️  Skipped (flag)"
elif [[ "$DRY_RUN" == "true" ]]; then
  dry_label "Would create/append Bear note: [Skill Dev] $SKILL_NAME"
else
  NOTE_TITLE="[Skill Dev] $SKILL_NAME"
  NOTE_BODY="# $SKILL_NAME v$VERSION\n\n**Date:** $(date -u +"%Y-%m-%dT%H:%MZ")\n**Changelog:** $CHANGELOG\n"

  if command -v grizzly &>/dev/null; then
    echo -e "$NOTE_BODY" | grizzly create --title "$NOTE_TITLE" --tag "$BEAR_TAG" 2>/dev/null \
      && step_ok "Bear note synced" \
      || { echo "⚠️  Bear sync failed (non-fatal)"; step_ok "Bear sync skipped (grizzly error)"; }
  else
    # Structured log fallback
    echo "📝 Bear fallback log: title='$NOTE_TITLE' tag='$BEAR_TAG' version='$VERSION'"
    step_ok "Bear sync skipped (grizzly not available, log emitted)"
  fi
fi

# ── Step 3: GitHub Push ─────────────────────────────────
echo "── Step 3: GitHub Push ──"

if [[ "$SKIP_GITHUB" == "true" ]]; then
  echo "⏭️  Skipped (flag)"
elif [[ -z "$GH_REPO" ]]; then
  echo "⚠️  No --repo specified and SKILL_GH_REPO not set; skipping GitHub push"
elif [[ "$DRY_RUN" == "true" ]]; then
  dry_label "Would push $SKILL_NAME to $GH_REPO:$BRANCH"
else
  WORK_DIR="$(mktemp -d)"
  trap 'rm -rf "$WORK_DIR"' EXIT

  if git clone --depth 1 --branch "$BRANCH" "https://github.com/${GH_REPO}.git" "$WORK_DIR/repo" 2>/dev/null; then
    mkdir -p "$WORK_DIR/repo/skills/$SKILL_NAME"
    cp -r "$SKILL_PATH"/* "$WORK_DIR/repo/skills/$SKILL_NAME/"
    cd "$WORK_DIR/repo"
    git add -A
    git diff --cached --quiet && echo "ℹ️  No changes to commit" || {
      git commit -m "feat(skill): publish $SKILL_NAME v$VERSION"
      git push origin "$BRANCH"
    }
    step_ok "GitHub push complete → $GH_REPO:$BRANCH"
  else
    step_fail "GitHub push failed (clone/push error)"
  fi
fi

# ── Step 4: ClawHub Publish ─────────────────────────────
echo "── Step 4: ClawHub Publish ──"

if [[ "$DRY_RUN" == "true" ]]; then
  dry_label "Would run: clawhub publish $SKILL_PATH --slug $SKILL_NAME --version $VERSION --changelog '$CHANGELOG'"
else
  if command -v clawhub &>/dev/null; then
    clawhub publish "$SKILL_PATH" \
      --slug "$SKILL_NAME" \
      --name "$SKILL_NAME" \
      --version "$VERSION" \
      --changelog "$CHANGELOG" \
    && step_ok "ClawHub publish complete" \
    || step_fail "ClawHub publish failed"
  else
    step_fail "clawhub CLI not found"
  fi
fi

echo ""
echo "🎉 Publish pipeline complete for $SKILL_NAME v$VERSION"