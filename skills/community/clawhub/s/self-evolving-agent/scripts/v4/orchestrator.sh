#!/usr/bin/env bash
# ============================================================
# orchestrator.sh — Self-Evolving Agent v4.0 메인 오케스트레이터
#
# 역할: 크론에 의해 호출되는 진입점.
#       각 독립 스테이지를 순서대로 실행하고,
#       한 스테이지가 실패해도 다음 스테이지는 계속 진행함.
#       최종 제안문을 stdout으로 출력 (크론 배달에 사용됨).
#
# 사용법:
#   bash orchestrator.sh
#   DRY_RUN=true bash orchestrator.sh   # LLM 호출 없이 테스트
#   VERBOSE=true bash orchestrator.sh   # 상세 로그
#
# 환경변수:
#   SEA_TMP_DIR  — 임시 파일 저장 위치 (기본: /tmp/sea-v4)
#   DRY_RUN      — true면 LLM 호출 없이 규칙 기반 분석
#   VERBOSE      — true면 스테이지 로그를 stderr에 표시
#   MAX_SESSIONS — 분석할 최대 세션 수 (기본: 30)
#   COLLECT_DAYS — 수집 기간 일수 (기본: 7)
#
# 설계 원칙:
#   - bash 3.2 호환 (macOS 기본 셸) — declare -A, 빈 배열 ${#arr[@]} 미사용
#   - 각 스테이지는 독립적으로 실행 가능
#   - SHELLOPTS= 전달로 부모 set -u 전파 차단
#   - 모든 외부 호출은 || true 로 감싸 exec 실패 방지
#   - 전체 실행 < 3분 목표
#
# 변경 이력:
#   v4.0 (2026-02-17) — 신규 구현 (멀티 스테이지 파이프라인)
# ============================================================

# SECURITY MANIFEST:
# Environment variables accessed: SEA_TMP_DIR, DRY_RUN, VERBOSE, MAX_SESSIONS,
#   COLLECT_DAYS, WORKSPACE, SEA_DAYS, SEA_MAX_SESSIONS, SEA_DISCORD_CHANNEL
# External endpoints called: None directly
#   (delegates to benchmark.sh which calls GitHub API and ClawHub API — both optional)
# Local files read:
#   <SKILL_DIR>/scripts/lib/config-loader.sh  (sourced)
#   ~/openclaw/skills/self-evolving-agent/config.yaml  (via config-loader)
#   /tmp/sea-v4/logs.json, /tmp/sea-v4/analysis.json,
#   /tmp/sea-v4/benchmarks.json, /tmp/sea-v4/effects.json  (stage outputs)
# Local files written:
#   /tmp/sea-v4/run-meta.json
#   /tmp/sea-v4/stage-<name>.log  (per-stage logs)
#   /tmp/sea-v4/proposal.md       (final output via synthesize-proposal.sh)
#   (all stage output files via sub-scripts)
# Network: None directly (see benchmark.sh for optional network calls)

set -euo pipefail

# ── 에러 카운터 (trap ERR) ──────────────────────────────────
_ORCH_ERRS=0
trap '_ORCH_ERRS=$(( _ORCH_ERRS + 1 ))' ERR

# ── 전역 설정 ──────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
TMP_DIR="${SEA_TMP_DIR:-/tmp/sea-v4}"
VERBOSE="${VERBOSE:-false}"
DRY_RUN="${DRY_RUN:-false}"
MAX_SESSIONS="${MAX_SESSIONS:-30}"
COLLECT_DAYS="${COLLECT_DAYS:-7}"
WORKSPACE="${WORKSPACE:-$HOME/openclaw}"

# ── config.yaml 검증 (있으면) ──────────────────────────────
# 실행 전 설정 유효성 검사. --quiet 모드: 오류만 표시.
if [[ -f "$SKILL_DIR/scripts/validate-config.sh" ]]; then
  bash "$SKILL_DIR/scripts/validate-config.sh" --quiet || {
    echo "❌ Config validation failed. Run: bash $SKILL_DIR/scripts/setup-wizard.sh" >&2
    exit 1
  }
fi

# ── config.yaml 로딩 (있으면) ──────────────────────────────
_CONFIG_LOADER="${SKILL_DIR}/scripts/lib/config-loader.sh"
if [[ -f "$_CONFIG_LOADER" ]]; then
  # shellcheck source=/dev/null
  source "$_CONFIG_LOADER" 2>/dev/null || true
  sea_load_config 2>/dev/null || true
  # config.yaml 값을 오케스트레이터 변수에 반영 (환경변수 우선)
  COLLECT_DAYS="${COLLECT_DAYS:-${SEA_DAYS:-7}}"
  MAX_SESSIONS="${MAX_SESSIONS:-${SEA_MAX_SESSIONS:-30}}"
  export COLLECT_DAYS MAX_SESSIONS SEA_DAYS SEA_MAX_SESSIONS SEA_DISCORD_CHANNEL
fi

# 각 스테이지 출력 파일 경로
LOGS_JSON="${TMP_DIR}/logs.json"
ANALYSIS_JSON="${TMP_DIR}/analysis.json"
BENCHMARKS_JSON="${TMP_DIR}/benchmarks.json"
PROPOSAL_MD="${TMP_DIR}/proposal.md"
EFFECTS_JSON="${TMP_DIR}/effects.json"
RUN_META_JSON="${TMP_DIR}/run-meta.json"

# 스테이지 결과 추적 (bash 3.2: 개별 변수 사용, declare -A 미지원)
_ST_collect_logs="pending"
_ST_semantic_analyze="pending"
_ST_benchmark="pending"
_ST_measure_effects="pending"
_ST_synthesize="pending"

# ── 로그 유틸 ──────────────────────────────────────────────
log_info() { [[ "$VERBOSE" == "true" ]] && echo "[SEA-v4 $(date '+%H:%M:%S')] $*" >&2 || true; }
log_err()  { echo "[SEA-v4 ERR $(date '+%H:%M:%S')] $*" >&2; }

# ── run_stage: 스테이지 실행 래퍼 ──────────────────────────
# 사용법: run_stage <stage_key> <output_file> <script_path> [extra_env...] [-- pos_args...]
#
# extra_env: "KEY=VALUE" 형식 문자열 (위치 인자 앞에 와야 함)
# pos_args:  "--" 구분자 이후의 인자들 (스크립트에 전달됨)
#
# 핵심: SHELLOPTS= 전달 → 부모의 set -euo pipefail 중 -u(-nounset)가
#       자식 bash에 자동 전파되는 것을 차단 (bash 3.2 배열 버그 방지)
run_stage() {
  local _key="$1"
  local _outfile="$2"
  local _script="$3"
  shift 3

  log_info "스테이지 시작: ${_key}"
  local _t0
  _t0=$(date +%s)

  # 스크립트 존재 확인
  if [[ ! -f "$_script" ]]; then
    log_err "스크립트 없음: ${_script}"
    eval "_ST_${_key}=\"skipped:missing\""
    return 0
  fi

  # 타임아웃 (timeout 명령 있을 때만)
  local _tout=""
  command -v timeout &>/dev/null && _tout="timeout 150" || true

  # 스테이지 로그
  local _log="${TMP_DIR}/stage-${_key}.log"

  # ── 추가 env/args 파싱 (bash 3.2 호환 방식) ────────────────
  # bash 3.2: 빈 배열 set -u 충돌 회피를 위해 set +u 일시 해제
  set +u

  # "--" 구분자 기준으로 extra_env 와 pos_args 분리
  local _extra_env=""  # "KEY=VAL KEY2=VAL2" 공백 구분 문자열
  local _pos_args=""   # 위치 인자 (공백 구분)
  local _sep_found=false
  for _arg in "$@"; do
    if [[ "$_arg" == "--" ]]; then
      _sep_found=true
    elif [[ "$_sep_found" == "false" ]]; then
      _extra_env="${_extra_env} ${_arg}"
    else
      # 위치 인자는 따옴표 포함해서 저장 (공백 안전)
      _pos_args="${_pos_args} '${_arg}'"
    fi
  done

  # env 명령 구성 (문자열 기반, 배열 미사용)
  # SHELLOPTS= BASHOPTS= : 부모 shell options 전파 차단 (핵심!)
  local _env_str="SHELLOPTS= BASHOPTS="
  _env_str="${_env_str} SEA_TMP_DIR='${TMP_DIR}'"
  _env_str="${_env_str} DRY_RUN='${DRY_RUN}'"
  _env_str="${_env_str} VERBOSE='${VERBOSE}'"
  _env_str="${_env_str} MAX_SESSIONS='${MAX_SESSIONS}'"
  _env_str="${_env_str} COLLECT_DAYS='${COLLECT_DAYS}'"
  _env_str="${_env_str} WORKSPACE='${WORKSPACE}'"
  if [[ -n "${_extra_env# }" ]]; then
    _env_str="${_env_str} ${_extra_env}"
  fi

  # 스크립트 실행 (eval: 문자열 기반 env 명령 실행, || true: 실패 무시)
  # shellcheck disable=SC2086
  eval "env ${_env_str} ${_tout} bash '${_script}'${_pos_args}" \
    > "$_log" 2>&1 || true

  set -u
  # ── 파싱 끝 ────────────────────────────────────────────────

  local _elapsed=$(( $(date +%s) - _t0 ))

  # VERBOSE: 로그 출력
  if [[ "$VERBOSE" == "true" && -f "$_log" ]]; then
    cat "$_log" >&2 || true
  fi

  # 출력 파일 존재 여부로 성공/실패 판단
  if [[ -n "$_outfile" && -f "$_outfile" && -s "$_outfile" ]]; then
    eval "_ST_${_key}=\"ok:${_elapsed}s\""
    log_info "스테이지 완료: ${_key} (${_elapsed}s)"
  else
    eval "_ST_${_key}=\"failed:${_elapsed}s\""
    log_err "스테이지 실패: ${_key} (${_elapsed}s)"
    # 로그 힌트 (VERBOSE=false 시)
    if [[ "$VERBOSE" != "true" && -f "$_log" ]]; then
      tail -5 "$_log" >&2 2>/dev/null || true
    fi
  fi

  return 0  # 항상 0 반환 (오케스트레이터 set -e 트리거 방지)
}

# ── 초기화 ──────────────────────────────────────────────────
mkdir -p "$TMP_DIR" 2>/dev/null || true

RUN_ID="sea-v4-$(date +%Y%m%d-%H%M%S)"
RUN_START=$(date +%s)

# 실행 메타 파일 생성
python3 - > "$RUN_META_JSON" 2>/dev/null <<PYEOF || true
import json
print(json.dumps({
    "run_id": "${RUN_ID}",
    "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "dry_run": "${DRY_RUN}" == "true",
    "script_dir": "${SCRIPT_DIR}",
    "tmp_dir": "${TMP_DIR}",
    "max_sessions": int("${MAX_SESSIONS}"),
    "collect_days": int("${COLLECT_DAYS}"),
}, indent=2, ensure_ascii=False))
PYEOF

log_info "=== SEA v4.0 오케스트레이터 시작 (${RUN_ID}) ==="
log_info "TMP_DIR=${TMP_DIR} | DRY_RUN=${DRY_RUN} | SESSIONS=${MAX_SESSIONS} | DAYS=${COLLECT_DAYS}"

# ════════════════════════════════════════════════════════════
# 스테이지 실행
# ════════════════════════════════════════════════════════════

# ── Stage 1: 로그 수집 ──────────────────────────────────────
# collect-logs.sh: 위치 인자로 출력 경로 전달
run_stage "collect_logs" "$LOGS_JSON" \
  "${SCRIPT_DIR}/collect-logs.sh" \
  -- "$LOGS_JSON"

# ── Stage 2: 시맨틱 분석 ─────────────────────────────────────
# semantic-analyze.sh: 환경변수로 경로 지정 (LOGS_JSON, OUTPUT_JSON)
# "--" 이전이 extra_env, 이후가 pos_args
run_stage "semantic_analyze" "$ANALYSIS_JSON" \
  "${SCRIPT_DIR}/semantic-analyze.sh" \
  "LOGS_JSON=${LOGS_JSON}" "OUTPUT_JSON=${ANALYSIS_JSON}"

# ── Stage 3: 벤치마크 수집 ──────────────────────────────────
# benchmark.sh: SEA_TMP_DIR 환경변수로 출력 디렉토리 지정 (공통 env에 이미 포함)
run_stage "benchmark" "$BENCHMARKS_JSON" \
  "${SCRIPT_DIR}/benchmark.sh"

# ── Stage 4: 효과 측정 ──────────────────────────────────────
# measure-effects.sh: 위치 인자로 출력 경로 전달
# (synthesize보다 먼저 실행 — 제안서에 효과 정보 포함)
run_stage "measure_effects" "$EFFECTS_JSON" \
  "${SCRIPT_DIR}/measure-effects.sh" \
  -- "$EFFECTS_JSON"

# ── Stage 5: 제안 합성 ──────────────────────────────────────
# synthesize-proposal.sh: 입력/출력 모두 위치 인자로 전달
# ANALYSIS, BENCHMARKS, EFFECTS env var도 함께 (폴백 지원)
run_stage "synthesize" "$PROPOSAL_MD" \
  "${SCRIPT_DIR}/synthesize-proposal.sh" \
  -- "$ANALYSIS_JSON" "$BENCHMARKS_JSON" "$EFFECTS_JSON" "$PROPOSAL_MD"

# ════════════════════════════════════════════════════════════
# 실행 결과 집계
# ════════════════════════════════════════════════════════════
ELAPSED=$(( $(date +%s) - RUN_START ))

# 스테이지 상태 JSON 직렬화 (bash 3.2 호환: eval로 동적 변수 참조)
STAGE_JSON="{"
_is_first=true
for _k in collect_logs semantic_analyze benchmark measure_effects synthesize; do
  [[ "$_is_first" == "true" ]] && _is_first=false || STAGE_JSON+=","
  _v=$(eval "echo \"\${_ST_${_k}:-unknown}\"")
  STAGE_JSON+="\"${_k}\":\"${_v}\""
done
STAGE_JSON+="}"

# 메타 파일 업데이트
python3 - > "${RUN_META_JSON}.tmp" 2>/dev/null <<PYEOF && mv "${RUN_META_JSON}.tmp" "$RUN_META_JSON" 2>/dev/null || true
import json
try:
    with open("${RUN_META_JSON}") as f:
        m = json.load(f)
except Exception:
    m = {"run_id": "${RUN_ID}"}
m.update({
    "completed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "elapsed_seconds": ${ELAPSED},
    "stages": ${STAGE_JSON},
    "error_count": ${_ORCH_ERRS},
})
print(json.dumps(m, indent=2, ensure_ascii=False))
PYEOF

log_info "완료: ${ELAPSED}초 | 에러: ${_ORCH_ERRS}건"
log_info "스테이지: ${STAGE_JSON}"

# ════════════════════════════════════════════════════════════
# 최종 출력 (stdout → 크론 배달)
# ════════════════════════════════════════════════════════════

if [[ -f "$PROPOSAL_MD" && -s "$PROPOSAL_MD" ]]; then
  # proposal.md 있으면 그대로 출력
  cat "$PROPOSAL_MD"

elif [[ -f "$ANALYSIS_JSON" && -s "$ANALYSIS_JSON" ]]; then
  # 폴백 1: analysis.json 요약 출력
  log_err "proposal.md 없음 — 폴백 요약 생성"
  python3 - "$ANALYSIS_JSON" "$STAGE_JSON" 2>/dev/null <<'PYEOF' || true
import json, sys

with open(sys.argv[1]) as f:
    data = json.load(f)
stages = sys.argv[2]

print("## 🤖 SEA v4.0 요약 (폴백)")
print()

summary = data.get("summary", {})
print(f"- 세션: {summary.get('sessions_analyzed', 'N/A')}개")
print(f"- 불만: {summary.get('complaint_hits', 0)}건")
print(f"- exec재시도: {summary.get('exec_retries', 0)}건")
print()

proposals = data.get("proposals", [])
if proposals:
    print("### 주요 제안")
    for p in proposals[:3]:
        print(f"- **{p.get('title', '?')}** ({p.get('priority', '?')}): {p.get('description', '')[:100]}")
else:
    print("_이번 주기 특별한 개선 사항 없음_")

print()
print(f"---")
print(f"*스테이지: {stages}*")
PYEOF

else
  # 폴백 2: 메타 정보만 출력
  echo "## SEA v4.0 실행 결과"
  echo ""
  echo "_분석 데이터 없음 — 로그를 확인하세요_"
  echo ""
  echo "- Run ID: ${RUN_ID}"
  echo "- 소요: ${ELAPSED}초"
  echo "- 스테이지: ${STAGE_JSON}"
fi

# ════════════════════════════════════════════════════════════
# 멀티플랫폼 배달 (discord 제외)
# Discord는 OpenClaw 크론 delivery 설정이 자동 처리 → deliver.sh 불필요
# ════════════════════════════════════════════════════════════
_DELIVER_PLATFORM="${SEA_DELIVERY_PLATFORM:-discord}"

if [[ "$_DELIVER_PLATFORM" != "discord" && -f "$PROPOSAL_MD" && -s "$PROPOSAL_MD" ]]; then
  log_info "배달 시작: ${_DELIVER_PLATFORM}"
  _DELIVER_SCRIPT="${SCRIPT_DIR}/deliver.sh"

  if [[ -f "$_DELIVER_SCRIPT" ]]; then
    PLATFORM="$_DELIVER_PLATFORM" \
    SLACK_URL="${SEA_SLACK_WEBHOOK_URL:-}" \
    TG_TOKEN="${SEA_TG_BOT_TOKEN:-}" \
    TG_CHAT_ID="${SEA_TG_CHAT_ID:-}" \
    WEBHOOK_URL="${SEA_WEBHOOK_URL:-}" \
    WEBHOOK_METHOD="${SEA_WEBHOOK_METHOD:-POST}" \
      bash "$_DELIVER_SCRIPT" "$PROPOSAL_MD" 2>&1 \
      | while IFS= read -r _line; do
          log_info "[deliver] ${_line}"
        done || true
  else
    log_err "deliver.sh 없음: ${_DELIVER_SCRIPT}"
  fi
else
  if [[ "$_DELIVER_PLATFORM" == "discord" ]]; then
    log_info "Discord 배달: OpenClaw 크론 native 배달 사용 (stdout 출력으로 처리)"
  fi
fi

# ── 임시 파일 정리 (30일 이상) ─────────────────────────────
find "$TMP_DIR" -maxdepth 1 -name "stage-*.log" -mtime +30 -delete 2>/dev/null || true

log_info "=== 오케스트레이터 종료 ==="
exit 0
