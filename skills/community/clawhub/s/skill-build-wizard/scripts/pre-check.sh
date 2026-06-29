#!/usr/bin/env bash
# pre-check.sh — skill-build-wizard pre-flight checks
# Checks: workspace git initialized
# Prints recommendations: long-task tolerance, cross-session continuity
# Platform: Linux / macOS (POSIX subset)
#
# Usage:
#   bash pre-check.sh                # run all checks
#   bash pre-check.sh --skip git     # skip the git check
#   bash pre-check.sh --skip all     # skip everything (just print summary)
#   bash pre-check.sh --help         # show this help

set -euo pipefail

# ── Parse --skip flag ────────────────────────────
SKIP_GIT=0
SKIP_ALL=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip)
      shift
      if [[ $# -eq 0 ]]; then
        echo "ERROR: --skip requires an argument (git / all)" >&2
        exit 2
      fi
      IFS=',' read -ra ITEMS <<< "$1"
      for item in "${ITEMS[@]}"; do
        case "$item" in
          git)     SKIP_GIT=1 ;;
          all)     SKIP_ALL=1; SKIP_GIT=1 ;;
          *)
            echo "ERROR: unknown skip item '$item' (allowed: git, all)" >&2
            exit 2 ;;
        esac
      done
      shift
      ;;
    --help|-h)
      sed -n '2,12p' "$0"
      exit 0
      ;;
    *)
      echo "ERROR: unknown argument '$1' (try --help)" >&2
      exit 2
      ;;
  esac
done

PASS=0
WARN=0
FAIL=0

ok()   { echo "  ✅ $*";  PASS=$((PASS+1)); }
warn() { echo "  ⚠️  $*"; WARN=$((WARN+1)); }
fail() { echo "  ❌ $*";  FAIL=$((FAIL+1)); }

echo "════════════════════════════════════════════"
echo "  skill-build-wizard pre-flight checks"
echo "════════════════════════════════════════════"
echo ""

# ── Check 1: workspace git ────────────────────────
if [[ "$SKIP_GIT" -eq 1 ]]; then
  echo "【1】Workspace Git — SKIPPED"
else
  echo "【1】Workspace Git (version control for your skill workdir)"
  # Detect a useful workdir: prefer current dir if it's a git repo,
  # otherwise check common skill locations.
  CWD_GIT=0
  if git -C "$PWD" rev-parse --git-dir >/dev/null 2>&1; then
    CWD_GIT=1
    ok "current directory is a git repo: $PWD"
  fi

  if [[ "$CWD_GIT" -eq 0 ]]; then
    # Try common workspace locations
    for guess in \
      "${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}" \
      "$HOME/.claude/workspace" \
      "$HOME/skills" \
      "$HOME/workspace"; do
      if [[ -d "$guess" ]] && git -C "$guess" rev-parse --git-dir >/dev/null 2>&1; then
        ok "found git repo at: $guess"
        CWD_GIT=1
        break
      fi
    done
  fi

  if [[ "$CWD_GIT" -eq 0 ]]; then
    warn "no git repo detected in CWD or common workspace paths"
    echo "       Tip: initialize git in your skill workdir before starting:"
    echo "         cd <your-workdir> && git init && git add . && git commit -m 'initial'"
    echo "       This protects against accidental file overwrites during AI-assisted editing."
  fi
fi
echo ""

# ── Recommendation 1: long-task tolerance ─────────
echo "【2】Long-running task tolerance (recommendation only)"
echo "  ℹ️  Building a non-trivial skill often takes several minutes per turn."
echo "      Make sure your agent/IDE supports long-running tasks:"
echo "        - Subagent / tool timeout ≥ 5 minutes"
echo "        - Sufficient max-output-tokens"
echo "        - Background execution (so slow steps don't block)"
echo "      Knobs are platform-specific — consult your agent's docs."
echo ""

# ── Recommendation 2: cross-session continuity ────
echo "【3】Cross-session continuity (recommendation only)"
echo "  ℹ️  Skill builds often span multiple conversations. To avoid losing context:"
echo "        - Save the Stage 2 design to a persistent file (DESIGN.md, wiki, Notion, ...)"
echo "        - Make sure your agent supports conversation history export/resume"
echo "        - Commit work-in-progress to git frequently"
echo ""

# ── Summary ──────────────────────────────────────
echo "════════════════════════════════════════════"
echo "  Summary: ${PASS} pass / ${WARN} warn / ${FAIL} fail"
echo "════════════════════════════════════════════"

if [[ "$FAIL" -gt 0 ]]; then
  echo ""
  echo "❌ Pre-flight failed — fix the failing item(s) or skip explicitly with --skip"
  exit 1
elif [[ "$WARN" -gt 0 ]]; then
  echo ""
  echo "⚠️  Pre-flight passed with warnings — ask the user whether to continue or fix first"
  exit 0
else
  echo ""
  echo "✅ Pre-flight clean — proceed to Stage 2 (spec clarification)"
  exit 0
fi
