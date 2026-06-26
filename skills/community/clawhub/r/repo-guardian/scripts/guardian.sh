#!/usr/bin/env bash
# Repo Guardian — dual-model PR review and issue triage
# Usage: guardian.sh <owner/repo> [--dry-run] [--no-merge] [--no-issues]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Defaults
REPO="${1:-${GUARDIAN_REPO:-}}"
DRY_RUN=false
AUTO_MERGE="${GUARDIAN_AUTO_MERGE:-true}"
AUTO_FIX="${GUARDIAN_AUTO_FIX:-false}"
MAX_PRS="${GUARDIAN_MAX_PRS:-5}"
MAX_ISSUES="${GUARDIAN_MAX_ISSUES:-3}"
PROCESS_ISSUES=true
AGENT_NAME="${GUARDIAN_AGENT:-${OPENCLAW_AGENT:-default}}"
REVIEWER_B_AGENT="${GUARDIAN_REVIEWER_B_AGENT:-$AGENT_NAME}"

# Parse flags
shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true ;;
    --no-merge) AUTO_MERGE=false ;;
    --no-issues) PROCESS_ISSUES=false ;;
    --auto-fix) AUTO_FIX=true ;;
    *) echo "[guardian] Unknown flag: $1" >&2; exit 1 ;;
  esac
  shift
done

if [[ -z "$REPO" ]]; then
  echo "[guardian] Usage: guardian.sh <owner/repo> [--dry-run] [--no-merge] [--no-issues]"
  exit 1
fi

echo "[guardian] Repo: $REPO | dry-run: $DRY_RUN | auto-merge: $AUTO_MERGE | auto-fix: $AUTO_FIX"

# Ensure GH_TOKEN (must be explicitly set — no fallback to gh auth to avoid scope leakage)
if [[ -z "${GH_TOKEN:-}" ]]; then
  echo "[guardian] ERROR: GH_TOKEN environment variable is required." >&2
  echo "[guardian] Set it in your .env or shell: export GH_TOKEN=ghp_..." >&2
  echo "[guardian] Recommended: use a fine-grained PAT scoped to the target repo only." >&2
  exit 1
fi

API="https://api.github.com"
AUTH="Authorization: Bearer $GH_TOKEN"
ACCEPT="Accept: application/vnd.github+json"

# ─── PR REVIEW ───────────────────────────────────────────────────────

echo "[guardian] Fetching open PRs..."
PRS=$(curl -s -H "$AUTH" -H "$ACCEPT" "$API/repos/$REPO/pulls?state=open&per_page=$MAX_PRS" 2>/dev/null)
PR_COUNT=$(echo "$PRS" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")

echo "[guardian] Found $PR_COUNT open PR(s)"

if [[ "$PR_COUNT" -gt 0 ]]; then
  echo "$PRS" | python3 -c "
import sys, json
prs = json.load(sys.stdin)
for pr in prs:
    labels = [l['name'] for l in pr.get('labels', [])]
    if 'skip-guardian' in labels:
        continue
    print(f\"{pr['number']}|{pr['title']}|{pr['head']['ref']}|{pr['html_url']}\")
" | while IFS='|' read -r PR_NUM PR_TITLE PR_BRANCH PR_URL; do
    echo ""
    echo "[guardian] ═══════════════════════════════════════════"
    echo "[guardian] PR #$PR_NUM: $PR_TITLE"
    echo "[guardian] Branch: $PR_BRANCH"
    echo "[guardian] URL: $PR_URL"
    echo "[guardian] ═══════════════════════════════════════════"
    
    # Fetch PR diff
    DIFF=$(curl -s -H "$AUTH" -H "Accept: application/vnd.github.v3.diff" "$API/repos/$REPO/pulls/$PR_NUM" 2>/dev/null)
    DIFF_LINES=$(echo "$DIFF" | wc -l)
    echo "[guardian] Diff: $DIFF_LINES lines"
    
    # Truncate large diffs for context window
    if [[ $DIFF_LINES -gt 500 ]]; then
      DIFF=$(echo "$DIFF" | head -500)
      DIFF="$DIFF\n\n[... truncated, $DIFF_LINES total lines ...]"
    fi
    
    # Fetch PR files list
    FILES=$(curl -s -H "$AUTH" -H "$ACCEPT" "$API/repos/$REPO/pulls/$PR_NUM/files" 2>/dev/null | \
      python3 -c "import sys,json; [print(f['filename']) for f in json.load(sys.stdin)]" 2>/dev/null || echo "unknown")
    
    REVIEW_PROMPT="You are reviewing PR #$PR_NUM on $REPO.

Title: $PR_TITLE
Branch: $PR_BRANCH
Files changed:
$FILES

Diff:
\`\`\`diff
$DIFF
\`\`\`

Review this PR against these criteria:
1. CORRECTNESS — Does the code do what the PR title/description claims?
2. SECURITY — Any vulnerabilities, secret exposure, injection risks?
3. TESTS — Are changes tested? Could they break existing tests?
4. SCOPE — Does the PR stay within its stated purpose?
5. QUALITY — Code style, error handling, edge cases, naming

Return your verdict as JSON:
{
  \"verdict\": \"APPROVE\" or \"REQUEST_CHANGES\",
  \"summary\": \"One-line summary of your assessment\",
  \"findings\": [
    {\"severity\": \"critical|major|minor\", \"file\": \"path\", \"line\": 0, \"issue\": \"description\", \"fix\": \"suggestion\"}
  ],
  \"confidence\": \"high\" or \"medium\" or \"low\"
}

If the PR is clean and correct, use verdict APPROVE with an empty findings array.
If you find issues, use REQUEST_CHANGES with specific findings.
Only use severity critical for security vulnerabilities or data loss risks.
Return ONLY the JSON object, no other text."

    echo "[guardian] Dispatching Opus review..."
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "[guardian] DRY RUN — would dispatch Opus review"
      OPUS_RESULT='{"verdict":"APPROVE","summary":"dry run","findings":[],"confidence":"high"}'
    else
      OPUS_RESULT=$(openclaw agent --agent "$AGENT_NAME" --local --message "$REVIEW_PROMPT" --json 2>/dev/null | \
        python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('text','{}'))" 2>/dev/null || echo '{"verdict":"ERROR","summary":"dispatch failed"}')
    fi
    
    echo "[guardian] Dispatching GPT review..."
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "[guardian] DRY RUN — would dispatch GPT review"
      GPT_RESULT='{"verdict":"APPROVE","summary":"dry run","findings":[],"confidence":"high"}'
    else
      GPT_RESULT=$(openclaw agent --agent "$REVIEWER_B_AGENT" --local --message "$REVIEW_PROMPT" --json 2>/dev/null | \
        python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('text','{}'))" 2>/dev/null || echo '{"verdict":"ERROR","summary":"dispatch failed"}')
      
      # Fallback to Sonnet if GPT failed
      GPT_VERDICT=$(echo "$GPT_RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('verdict','ERROR'))" 2>/dev/null || echo "ERROR")
      if [[ "$GPT_VERDICT" == "ERROR" ]]; then
        echo "[guardian] GPT failed, falling back to Sonnet..."
        GPT_RESULT=$(openclaw agent --agent "$REVIEWER_B_AGENT" --local --message "$REVIEW_PROMPT" --json 2>/dev/null | \
          python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('text','{}'))" 2>/dev/null || echo '{"verdict":"ERROR","summary":"fallback failed"}')
      fi
    fi
    
    # Parse verdicts
    OPUS_VERDICT=$(echo "$OPUS_RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('verdict','ERROR'))" 2>/dev/null || echo "ERROR")
    GPT_VERDICT=$(echo "$GPT_RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('verdict','ERROR'))" 2>/dev/null || echo "ERROR")
    OPUS_SUMMARY=$(echo "$OPUS_RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('summary','No summary'))" 2>/dev/null || echo "No summary")
    GPT_SUMMARY=$(echo "$GPT_RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('summary','No summary'))" 2>/dev/null || echo "No summary")
    
    echo "[guardian] Opus verdict: $OPUS_VERDICT — $OPUS_SUMMARY"
    echo "[guardian] GPT verdict:  $GPT_VERDICT — $GPT_SUMMARY"
    
    # Consensus logic
    if [[ "$OPUS_VERDICT" == "APPROVE" && "$GPT_VERDICT" == "APPROVE" ]]; then
      echo "[guardian] ✅ CONSENSUS: Both models approve"
      
      if [[ "$AUTO_MERGE" == "true" && "$DRY_RUN" == "false" ]]; then
        # Post approval comment (JSON-safe via Python to prevent injection)
        COMMENT_BODY=$(python3 -c "
import json, sys
opus_summary = sys.argv[1]
gpt_summary = sys.argv[2]
body = '## 🤖 Repo Guardian — Dual-Model Review\n\n'
body += f'**Opus:** ✅ APPROVE — {opus_summary}\n'
body += f'**GPT-5.4:** ✅ APPROVE — {gpt_summary}\n\n'
body += '*Auto-merging on dual consensus.*'
print(json.dumps({'body': body}))
" "$OPUS_SUMMARY" "$GPT_SUMMARY")
        curl -s -X POST -H "$AUTH" -H "$ACCEPT" \
          "$API/repos/$REPO/issues/$PR_NUM/comments" \
          -d "$COMMENT_BODY" > /dev/null
        
        # Squash merge (JSON-safe title)
        MERGE_BODY=$(python3 -c "
import json, sys
title = sys.argv[1]
pr_num = sys.argv[2]
print(json.dumps({'merge_method': 'squash', 'commit_title': f'{title} (#{pr_num})'}))
" "$PR_TITLE" "$PR_NUM")
        curl -s -X PUT -H "$AUTH" -H "$ACCEPT" \
          "$API/repos/$REPO/pulls/$PR_NUM/merge" \
          -d "$MERGE_BODY" > /dev/null
        echo "[guardian] ✅ PR #$PR_NUM merged (squash)"
      else
        echo "[guardian] Would merge PR #$PR_NUM (dry-run or auto-merge disabled)"
      fi
      
    else
      echo "[guardian] ❌ NO CONSENSUS — requesting changes"
      
      if [[ "$DRY_RUN" == "false" ]]; then
        # Collect findings from both models
        OPUS_FINDINGS=$(echo "$OPUS_RESULT" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
    for f in data.get('findings', []):
        print(f'- **[{f.get(\"severity\",\"?\")}]** {f.get(\"file\",\"?\")}:{f.get(\"line\",\"?\")} — {f.get(\"issue\",\"?\")}')
        if f.get('fix'):
            print(f'  Fix: {f[\"fix\"]}')
except: pass
" 2>/dev/null || echo "- Could not parse findings")

        GPT_FINDINGS=$(echo "$GPT_RESULT" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
    for f in data.get('findings', []):
        print(f'- **[{f.get(\"severity\",\"?\")}]** {f.get(\"file\",\"?\")}:{f.get(\"line\",\"?\")} — {f.get(\"issue\",\"?\")}')
        if f.get('fix'):
            print(f'  Fix: {f[\"fix\"]}')
except: pass
" 2>/dev/null || echo "- Could not parse findings")

        # Build comment body safely via Python (no shell interpolation in JSON)
        COMMENT_BODY=$(_OPUS_FINDINGS="$OPUS_FINDINGS" _GPT_FINDINGS="$GPT_FINDINGS" \
          python3 -c "
import json, sys, os
opus_verdict = sys.argv[1]
opus_summary = sys.argv[2]
opus_findings = os.environ.get('_OPUS_FINDINGS', '- No findings parsed')
gpt_verdict = sys.argv[3]
gpt_summary = sys.argv[4]
gpt_findings = os.environ.get('_GPT_FINDINGS', '- No findings parsed')
body = '## 🤖 Repo Guardian — Dual-Model Review\n\n'
body += f'**Opus:** {opus_verdict} — {opus_summary}\n{opus_findings}\n\n'
body += f'**GPT-5.4:** {gpt_verdict} — {gpt_summary}\n{gpt_findings}\n\n'
body += '*Changes requested. Please address findings and push updates.*'
print(json.dumps({'body': body}))
" "$OPUS_VERDICT" "$OPUS_SUMMARY" "$GPT_VERDICT" "$GPT_SUMMARY" 2>/dev/null) || \
        COMMENT_BODY='{"body": "Repo Guardian reviewed this PR. Changes requested by one or both models. See logs for details."}'
        
        curl -s -X POST -H "$AUTH" -H "$ACCEPT" \
          "$API/repos/$REPO/issues/$PR_NUM/comments" \
          -d "$COMMENT_BODY" > /dev/null
        
        echo "[guardian] Posted review comments on PR #$PR_NUM"
      fi
    fi
  done
fi

# ─── ISSUE TRIAGE ────────────────────────────────────────────────────

if [[ "$PROCESS_ISSUES" == "true" ]]; then
  echo ""
  echo "[guardian] Fetching open issues..."
  ISSUES=$(curl -s -H "$AUTH" -H "$ACCEPT" "$API/repos/$REPO/issues?state=open&per_page=$MAX_ISSUES&sort=created&direction=asc" 2>/dev/null)
  
  # Filter out PRs (GitHub API returns PRs in issues endpoint)
  ISSUE_COUNT=$(echo "$ISSUES" | python3 -c "
import sys, json
issues = json.load(sys.stdin)
count = sum(1 for i in issues if 'pull_request' not in i)
print(count)
" 2>/dev/null || echo "0")
  
  echo "[guardian] Found $ISSUE_COUNT open issue(s) (excluding PRs)"
  
  if [[ "$ISSUE_COUNT" -gt 0 && "$AUTO_FIX" == "true" && "$DRY_RUN" == "false" ]]; then
    echo "[guardian] Auto-fix enabled — would process issues (not yet implemented in v1)"
    echo "[guardian] Issue auto-fix will use gh-issues skill or OpenForge PRD in future version"
  elif [[ "$ISSUE_COUNT" -gt 0 ]]; then
    echo "[guardian] Issues found but auto-fix disabled (use --auto-fix to enable)"
  fi
fi

echo ""
echo "[guardian] ✅ Guardian run complete"
