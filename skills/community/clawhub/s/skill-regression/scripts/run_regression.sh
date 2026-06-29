#!/usr/bin/env bash
# run_regression.sh — Skill Regression main entry (open-source dual-backend)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR=""
THRESHOLD=7
TIMEOUT=120
CASES=3
ERROR_CASES=2
SKIP_AGENT=false
DETAIL_MODE=false
NO_AI_SUGGESTIONS=false
KEEP=5
RERUN_DIR=""
CASES_FILTER=""
BACKEND=""   # auto-detect (openclaw if CLI present, else api)

# Default workspace under HOME (no project-specific layout assumed)
DEFAULT_SPACE_ROOT="${HOME}/.skill-regression-space"
SPACE_ROOT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --threshold)   THRESHOLD="$2"; shift 2 ;;
    --timeout)     TIMEOUT="$2"; shift 2 ;;
    --cases)       CASES="$2"; shift 2 ;;
    --error-cases) ERROR_CASES="$2"; shift 2 ;;
    --skip-agent)         SKIP_AGENT=true; shift ;;
    --no-ai-suggestions)  NO_AI_SUGGESTIONS=true; shift ;;
    --detail)             DETAIL_MODE=true; shift ;;
    --space-dir)   SPACE_ROOT="$2"; shift 2 ;;
    --keep)        KEEP="$2"; shift 2 ;;
    --rerun)       RERUN_DIR="$2"; shift 2 ;;
    --backend)     BACKEND="$2"; shift 2 ;;
    --setup)       exec python3 "$SCRIPT_DIR/setup.py" ;;
    -h|--help)
      cat <<EOF
Usage: bash run_regression.sh <skill-dir> [options]

Options:
  --backend <openclaw|api>    Test backend (default: auto-detect)
  --space-dir <path>          Test workspace root (default: ~/.skill-regression-space)
  --threshold <N>             AI semantic score pass threshold (default: 7)
  --timeout <sec>             AI-layer single-case timeout (default: 120)
  --cases <N>                 Number of normal cases when no TEST.md (default: 3, range 2-20)
  --error-cases <N>           Number of error cases when no TEST.md (default: 2, range 1-5)
  --keep <N>                  Keep last N output runs (default: 5)
  --rerun <dir>               Re-run only failed cases from a previous output dir
  --skip-agent                Run script layer only (skip LLM/agent layer)
  --no-ai-suggestions         Skip LLM-generated improvement suggestions
  --detail                    Detailed report (each case full input/output)
  --setup                     Run interactive onboarding for SR_* config
  -h, --help                  Show this help

Configuration (see setup.py for interactive onboarding):
  Required for api backend       : SR_LLM_API_KEY, SR_LLM_BASE_URL, SR_LLM_MODEL
  Required for openclaw backend  : Above + SR_TARGET_AGENT (default: main)

Examples:
  bash run_regression.sh ~/skills/my-skill
  bash run_regression.sh ~/skills/my-skill --backend api --threshold 8 --detail
EOF
      exit 0 ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *)  SKILL_DIR="$1"; shift ;;
  esac
done

if [[ -z "$SKILL_DIR" ]]; then
  echo "Usage: bash run_regression.sh <skill-dir> [options]" >&2
  echo "       bash run_regression.sh --help" >&2
  exit 1
fi

SKILL_DIR="$(cd "$SKILL_DIR" 2>/dev/null && pwd)" || { echo "❌ Skill directory not found: $SKILL_DIR" >&2; exit 1; }

if [[ ! -d "$SKILL_DIR" ]]; then
  echo "❌ Error: Skill path does not exist: $SKILL_DIR" >&2
  exit 1
fi

SKILL_NAME="$(basename "$SKILL_DIR")"

[[ -z "$SPACE_ROOT" ]] && SPACE_ROOT="$DEFAULT_SPACE_ROOT"
SPACE_ROOT="${SPACE_ROOT/#\~/$HOME}"

TESTRES_DIR="${SPACE_ROOT}/testres/${SKILL_NAME}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
WORK_DIR="${SPACE_ROOT}/output/${SKILL_NAME}/${TIMESTAMP}"
mkdir -p "${WORK_DIR}/results"
mkdir -p "${TESTRES_DIR}"

# Check config readiness early (will trigger onboarding if missing & TTY)
if [[ "$SKIP_AGENT" == "false" ]]; then
  if ! python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from _lib_config import resolve_config, require_config_ready
cfg = resolve_config(cli_args={'SR_BACKEND': '$BACKEND' or None})
require_config_ready(cfg, allow_onboarding=True)
print(cfg.get('SR_BACKEND', 'api'))
" > /tmp/.sr_backend.$$ 2>&1; then
    cat /tmp/.sr_backend.$$ >&2
    rm -f /tmp/.sr_backend.$$
    exit 2
  fi
  DETECTED_BACKEND=$(tail -1 /tmp/.sr_backend.$$)
  rm -f /tmp/.sr_backend.$$
  [[ -z "$BACKEND" ]] && BACKEND="$DETECTED_BACKEND"
fi

echo "=========================================="
echo "  Skill Regression Test: $SKILL_NAME"
echo "  Skill dir   : $SKILL_DIR"
echo "  Testres dir : $TESTRES_DIR"
echo "  Output dir  : $WORK_DIR"
echo "  Backend     : ${BACKEND:-skipped}"
echo "  AI threshold: $THRESHOLD | timeout: ${TIMEOUT}s"
echo "  Report mode : $([ "$DETAIL_MODE" = true ] && echo 'Detailed' || echo 'Simple')"
echo "=========================================="

# ── --rerun mode ──
if [[ -n "$RERUN_DIR" && "$SKIP_AGENT" == "true" ]]; then
  echo "❌ --rerun and --skip-agent are incompatible." >&2
  echo "   --rerun needs agent_results.json from the previous run to locate failures." >&2
  exit 1
fi
if [[ -n "$RERUN_DIR" ]]; then
  RERUN_DIR="$(cd "$RERUN_DIR" && pwd)"
  if [[ ! -d "$RERUN_DIR" ]]; then
    echo "❌ --rerun directory not found: $RERUN_DIR" >&2
    exit 1
  fi
  if [[ ! -f "$RERUN_DIR/results/agent_results.json" ]]; then
    echo "❌ Missing agent_results.json in --rerun dir: $RERUN_DIR/results/" >&2
    exit 1
  fi

  echo ""
  echo "  🔁 Rerun mode: extracting failed cases from $RERUN_DIR"

  mapfile -t _RERUN_IDS < <(python3 -c "
import json, os
ar = json.load(open('$RERUN_DIR/results/agent_results.json'))
agent_results = ar.get('results', ar) if isinstance(ar, dict) else ar
agent_fail_ids = {
    r['id'] for r in agent_results
    if r.get('status') in ('fail', 'error', 'timeout', 'scoring_error')
}
script_fail_ids = set()
sp = '$RERUN_DIR/results/script_results.json'
if os.path.exists(sp):
    sr = json.load(open(sp))
    script_fail_ids = {r['id'] for r in sr if r.get('status') == 'fail'}
all_fail = agent_fail_ids | script_fail_ids
print(','.join(sorted(script_fail_ids)))
print(','.join(sorted(agent_fail_ids)))
print(','.join(sorted(all_fail)))
" 2>&1)
  SCRIPT_FAIL_IDS="${_RERUN_IDS[0]:-}"
  AGENT_FAIL_IDS="${_RERUN_IDS[1]:-}"
  CASES_FILTER="${_RERUN_IDS[2]:-}"

  if [[ -z "$CASES_FILTER" ]]; then
    echo "  ✅ No failures from previous run — nothing to rerun."
    exit 0
  fi

  [[ -n "$SCRIPT_FAIL_IDS" ]] && echo "  Script-layer fails: $SCRIPT_FAIL_IDS"
  [[ -n "$AGENT_FAIL_IDS"  ]] && echo "  AI-layer fails    : $AGENT_FAIL_IDS"

  cp "$RERUN_DIR/cases.json" "$WORK_DIR/cases.json"

  if [[ -z "$SCRIPT_FAIL_IDS" ]]; then
    cp "$RERUN_DIR/results/script_results.json" "$WORK_DIR/results/script_results.json"
    RERUN_SCRIPT_NEEDED=false
  else
    cp "$RERUN_DIR/results/script_results.json" "$WORK_DIR/results/script_results_base.json"
    RERUN_SCRIPT_NEEDED=true
  fi
  RERUN_BASE_RESULTS="$RERUN_DIR/results/agent_results.json"
  SKIP_ANALYZE=true
else
  SKIP_ANALYZE=false
  RERUN_BASE_RESULTS=""
  RERUN_SCRIPT_NEEDED=false
fi

if [[ "$SKIP_ANALYZE" == "false" ]]; then
  # Step 0: Normalize test file naming
  echo ""
  echo "【Step 0】Checking TEST.md..."
  python3 "$SCRIPT_DIR/normalize_testfile.py" --skill-dir "$SKILL_DIR" || true

  # Step 1: Analyze skill, load/generate cases
  echo ""
  echo "【Step 1】Analyzing skill, loading test cases..."
  ANALYZE_ARGS=(--skill-dir "$SKILL_DIR" --output "${WORK_DIR}/cases.json" --cases "$CASES" --error-cases "$ERROR_CASES")
  [[ "$SKIP_AGENT" == "true" ]] && ANALYZE_ARGS+=(--no-llm)
  python3 "$SCRIPT_DIR/analyze_skill.py" "${ANALYZE_ARGS[@]}"

  CASE_COUNT=$(python3 -c "import json; d=json.load(open('${WORK_DIR}/cases.json')); print(len(d['cases']))" 2>/dev/null || echo 0)
  echo "  → Loaded $CASE_COUNT test cases"

  # Step 2: Script-layer tests
  echo ""
  echo "【Step 2】Running script-layer tests..."
  python3 "$SCRIPT_DIR/run_script_tests.py" \
    --cases "${WORK_DIR}/cases.json" \
    --skill-dir "$SKILL_DIR" \
    --testres-dir "$TESTRES_DIR" \
    --work-dir "$WORK_DIR" \
    --output "${WORK_DIR}/results/script_results.json"

  SCRIPT_PASS=$(python3 -c "import json; d=json.load(open('${WORK_DIR}/results/script_results.json')); print(sum(1 for r in d if r['status']=='pass'))" 2>/dev/null || echo 0)
  echo "  → Script layer pass: $SCRIPT_PASS / $CASE_COUNT"
else
  CASE_COUNT=$(python3 -c "import json; d=json.load(open('${WORK_DIR}/cases.json')); print(len(d['cases']))" 2>/dev/null || echo 0)
  echo "  → Rerun mode: $CASE_COUNT cases"
  if [[ "$RERUN_SCRIPT_NEEDED" == "true" ]]; then
    echo ""
    echo "【Step 2】Rerunning script-layer failures ($SCRIPT_FAIL_IDS)..."
    python3 "$SCRIPT_DIR/run_script_tests.py" \
      --cases "${WORK_DIR}/cases.json" \
      --skill-dir "$SKILL_DIR" \
      --testres-dir "$TESTRES_DIR" \
      --work-dir "$WORK_DIR" \
      --cases-filter "$SCRIPT_FAIL_IDS" \
      --output "${WORK_DIR}/results/script_results_patch.json"

    python3 -c "
import json
base   = json.load(open('${WORK_DIR}/results/script_results_base.json'))
patch  = json.load(open('${WORK_DIR}/results/script_results_patch.json'))
patch_map = {r['id']: r for r in patch}
merged = [patch_map.get(r['id'], r) for r in base]
json.dump(merged, open('${WORK_DIR}/results/script_results.json', 'w'), ensure_ascii=False, indent=2)
print(f'  → Script-layer merged: rerun {len(patch)}, kept {len(base)-len(patch)}')
"
  fi
  SCRIPT_PASS=$(python3 -c "import json; d=json.load(open('${WORK_DIR}/results/script_results.json')); print(sum(1 for r in d if r['status']=='pass'))" 2>/dev/null || echo 0)
  echo "  → Script layer pass: $SCRIPT_PASS / $CASE_COUNT"
fi

# Step 3: AI/Agent layer
if [[ "$SKIP_AGENT" == "false" ]]; then
  echo ""
  echo "【Step 3】Running AI/agent-layer tests (per-case timeout ${TIMEOUT}s)..."
  AGENT_ARGS=(--cases "${WORK_DIR}/cases.json" --output "${WORK_DIR}/results/agent_results.json" --threshold "$THRESHOLD" --timeout "$TIMEOUT" --space-dir "$SPACE_ROOT")
  [[ -n "$BACKEND" ]] && AGENT_ARGS+=(--backend "$BACKEND")
  [[ -n "$CASES_FILTER" ]] && AGENT_ARGS+=(--cases-filter "$CASES_FILTER")
  python3 "$SCRIPT_DIR/run_agent_tests.py" "${AGENT_ARGS[@]}"

  AGENT_PASS=$(python3 -c "import json; d=json.load(open('${WORK_DIR}/results/agent_results.json')); r=d.get('results', d) if isinstance(d, dict) else d; print(sum(1 for x in r if x['status']=='pass'))" 2>/dev/null || echo 0)
  echo "  → AI layer pass: $AGENT_PASS / $CASE_COUNT"

  if [[ -n "$RERUN_BASE_RESULTS" ]]; then
    echo ""
    echo "  🔀 Merging rerun results..."
    python3 "$SCRIPT_DIR/merge_results.py" \
      --base   "$RERUN_BASE_RESULTS" \
      --patch  "${WORK_DIR}/results/agent_results.json" \
      --output "${WORK_DIR}/results/agent_results.json"
  fi
else
  echo ""
  echo "【Step 3】Skipping AI/agent layer (--skip-agent)"
  python3 "$SCRIPT_DIR/run_agent_tests.py" \
    --cases "${WORK_DIR}/cases.json" \
    --output "${WORK_DIR}/results/agent_results.json" \
    --threshold "$THRESHOLD" \
    --timeout "$TIMEOUT" \
    --space-dir "$SPACE_ROOT" \
    --skip
fi

# Step 4: Generate report
echo ""
echo "【Step 4】Generating Markdown report..."
python3 "$SCRIPT_DIR/generate_report.py" \
  --skill-dir "$SKILL_DIR" \
  --cases "${WORK_DIR}/cases.json" \
  --script-results "${WORK_DIR}/results/script_results.json" \
  --agent-results "${WORK_DIR}/results/agent_results.json" \
  --threshold "$THRESHOLD" \
  --skip-agent "$SKIP_AGENT" \
  --detail "$DETAIL_MODE" \
  --no-ai-suggestions "$NO_AI_SUGGESTIONS" \
  --space-dir "$SPACE_ROOT" \
  --output "${WORK_DIR}/report.md"

echo ""
echo "=========================================="
echo "  Regression test complete!"
echo "  Test resources: $TESTRES_DIR"
echo "  This run output: $WORK_DIR"
echo "=========================================="

# Cleanup hint (don't auto-delete)
OUTPUT_SKILL_DIR="${SPACE_ROOT}/output/${SKILL_NAME}"
if [[ -d "$OUTPUT_SKILL_DIR" ]]; then
  TOTAL_DIRS=$(ls -1d "${OUTPUT_SKILL_DIR}/"*/ 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$TOTAL_DIRS" -gt "$KEEP" ]]; then
    EXCESS=$(( TOTAL_DIRS - KEEP ))
    OLD_DIRS=$(ls -1d "${OUTPUT_SKILL_DIR}/"*/ 2>/dev/null | sort | head -n "${EXCESS}")
    echo ""
    echo "  ℹ️  History has ${TOTAL_DIRS} runs (over --keep=${KEEP}). Oldest ${EXCESS}:"
    while IFS= read -r dir; do
      echo "      $dir"
    done <<< "$OLD_DIRS"
    echo "  → Remove manually if not needed."
  fi
fi
