#!/usr/bin/env bash
# ============================================================
# measure-effects.sh — Self-Evolving Agent v4.0 효과 측정기
#
# 역할 (명세서 v4.0):
#   과거 제안이 실제로 효과가 있었는지 측정한다.
#   - data/proposals/*.json 읽기
#   - 각 제안의 타겟 패턴이 줄었는지 확인 (이번 주 vs 지난 주 로그)
#   - 품질 점수 변화 확인
#   - data/rejected-proposals.json 거절 이력 집계
#
# 출력 (명세서 필수 형식):
#   /tmp/sea-v4/effects.json
#   {
#     "applied_proposals": [{"id":"...", "pattern_before":15, "pattern_after":3, "effective":true}],
#     "overall_improvement": "+23%",
#     "ineffective_proposals": [...],
#     "rejected_count": 2
#   }
#
# 설계: bash 3.2 호환 / Python3 fallback / || true 패턴
#
# 사용법:
#   bash measure-effects.sh [--days N]
# ============================================================

# SECURITY MANIFEST:
# Environment variables accessed: SEA_DAYS, SEA_TMP_DIR
# External endpoints called: None
# Local files read:
#   <SKILL_DIR>/data/proposals/*.json       (past proposal files, up to 20)
#   <SKILL_DIR>/data/rejected-proposals.json
#   ~/.openclaw/agents/*/sessions/*.jsonl   (session transcripts for pattern counting)
#   ~/.openclaw/logs/cron-catchup.log       (scoped cron log for pattern counting)
#   ~/.openclaw/logs/heartbeat-cron.log     (scoped cron log for pattern counting)
#   ~/openclaw/memory/self-review/**        (quality score history, *.json / *.yaml)
# Local files written:
#   <SEA_TMP_DIR>/effects.json  (default: /tmp/sea-v4/effects.json)
# Network: None

# -e 제외: 외부 실패 시에도 계속 진행
set -o pipefail

# ── 경로 설정 ──────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROPOSALS_DIR="$SKILL_DIR/data/proposals"
REJECTED_FILE="$SKILL_DIR/data/rejected-proposals.json"
OUTPUT_DIR="${SEA_TMP_DIR:-/tmp/sea-v4}"
OUTPUT_FILE="$OUTPUT_DIR/effects.json"
DAYS="${SEA_DAYS:-7}"

mkdir -p "$OUTPUT_DIR" || true
echo "🔍 [measure-effects] 효과 측정 시작 (기준: 최근 ${DAYS}일)" >&2

# ── Python3 사용 가능 여부 ─────────────────────────────────
HAS_PY3=false
command -v python3 &>/dev/null && HAS_PY3=true || true

# ── Python3으로 핵심 로직 실행 ─────────────────────────────
if $HAS_PY3; then
  # >/dev/null: Python stdout 억제 (결과는 OUTPUT_FILE에 직접 저장)
  # stderr는 bash의 stderr로 전달 (디버그 출력)
  python3 - \
    "$PROPOSALS_DIR" \
    "${REJECTED_FILE}" \
    "$OUTPUT_FILE" \
    "$DAYS" \
    "${HOME}/.openclaw/logs" \
    "${HOME}/openclaw/memory/self-review" \
    >/dev/null <<'PYEOF' || true

import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta

# ── 인자 ───────────────────────────────────────────────────
proposals_dir   = Path(sys.argv[1])
rejected_file   = Path(sys.argv[2])
output_file     = Path(sys.argv[3])
days            = int(sys.argv[4])
log_dir         = Path(sys.argv[5])
review_dir      = Path(sys.argv[6])

now   = datetime.now(timezone.utc)
week_cutoff = now - timedelta(days=days)
prev_cutoff = now - timedelta(days=days * 2)

print(f"  → 분석 기간: {prev_cutoff.date()} ~ {now.date()} (주 기준: {week_cutoff.date()})", file=sys.stderr)

# ── 로그 파일에서 패턴 카운트 ────────────────────────────────
def count_pattern_in_logs(pattern: str, since: datetime, until: datetime) -> int:
    """세션 트랜스크립트와 크론 전용 로그에서만 패턴 발생 횟수 측정.
    gateway.log, gateway.err.log, rate-monitor.log 등 시스템 로그는 제외.
    이들 시스템 로그는 'error' 같은 일반 단어를 수천 건 포함해 측정값이 무의미해짐.
    """
    count = 0
    try:
        compiled = re.compile(pattern, re.IGNORECASE)
    except re.error:
        compiled = re.compile(re.escape(pattern), re.IGNORECASE)

    # ── 대상 1: 실제 세션 트랜스크립트 (*.jsonl) ──────────────
    agents_base = Path(os.environ.get("HOME", "~")).expanduser() / ".openclaw" / "agents"
    if agents_base.exists():
        try:
            for fpath in agents_base.glob("*/sessions/*.jsonl"):
                if not fpath.is_file():
                    continue
                try:
                    mtime = datetime.fromtimestamp(fpath.stat().st_mtime, tz=timezone.utc)
                except OSError:
                    continue
                if mtime < since or mtime > until:
                    continue
                try:
                    text = fpath.read_text(encoding="utf-8", errors="ignore")
                    count += len(compiled.findall(text))
                except (OSError, PermissionError):
                    continue
        except (PermissionError, OSError):
            pass

    # ── 대상 2: 크론 전용 로그만 (시스템 로그 제외) ────────────
    scoped_log_files = [
        "cron-catchup.log",
        "heartbeat-cron.log",
    ]
    for log_name in scoped_log_files:
        fpath = log_dir / log_name
        if not fpath.is_file():
            continue
        try:
            mtime = datetime.fromtimestamp(fpath.stat().st_mtime, tz=timezone.utc)
        except OSError:
            continue
        if mtime < since or mtime > until:
            continue
        try:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
            count += len(compiled.findall(text))
        except (OSError, PermissionError):
            continue

    return count

# ── 품질 점수 평균 ───────────────────────────────────────────
def avg_quality(since: datetime, until: datetime) -> object:
    """self-review 디렉토리에서 기간 내 품질 점수 평균"""
    scores = []
    if not review_dir.exists():
        return None
    for fpath in review_dir.rglob("*"):
        if not fpath.is_file():
            continue
        try:
            mtime = datetime.fromtimestamp(fpath.stat().st_mtime, tz=timezone.utc)
        except OSError:
            continue
        if mtime < since or mtime > until:
            continue
        try:
            if fpath.suffix == ".json":
                data = json.loads(fpath.read_text(errors="ignore"))
                score = data.get("quality_score") or data.get("score")
            elif fpath.suffix in (".yaml", ".yml"):
                text = fpath.read_text(errors="ignore")
                m = re.search(r"quality_score:\s*([\d.]+)", text)
                score = float(m.group(1)) if m else None
            else:
                continue
            if score is not None:
                scores.append(float(score))
        except Exception:
            continue
    if not scores:
        return None
    return round(sum(scores) / len(scores), 1)

quality_prev = avg_quality(prev_cutoff, week_cutoff)
quality_this = avg_quality(week_cutoff, now)
print(f"  → 품질 점수: 지난 주={quality_prev}, 이번 주={quality_this}", file=sys.stderr)

# ── 제안 파일 수집 ───────────────────────────────────────────
proposal_files = []
if proposals_dir.exists():
    proposal_files = sorted(proposals_dir.glob("*.json"))
print(f"  → {len(proposal_files)}개 제안 파일 발견", file=sys.stderr)

# ── 제안별 패턴 키워드 추론 ─────────────────────────────────
def infer_pattern(prop_id: str, title: str, before_text: str) -> str:
    combined = f"{prop_id} {title} {before_text}".lower()
    if "exec" in combined:       return r"exec"
    if "heartbeat" in combined:  return r"heartbeat"
    if "error" in combined or "에러" in combined: return r"error|에러"
    if "retry" in combined or "재시도" in combined: return r"retry|재시도"
    if "session" in combined or "compaction" in combined: return r"compaction"
    if "gateway" in combined:    return r"gateway"
    if "git" in combined:        return r"\bgit\b"
    # 기본값: 제목에서 첫 단어
    words = re.split(r"\s+", title.strip())
    return re.escape(words[0]) if words else "unknown"

# ── 각 제안 효과 측정 ────────────────────────────────────────
applied_proposals = []
seen_proposal_ids = set()  # 중복 제안 방지
effective_count   = 0
ineffective_count = 0
total_before      = 0
total_after       = 0

for pfile in proposal_files:
    try:
        data = json.loads(pfile.read_text(errors="ignore"))
    except Exception:
        continue

    created_at = data.get("created_at", "unknown")
    status     = data.get("status", "unknown")
    proposals  = data.get("proposals", [])

    print(f"  → 처리: {pfile.name} ({len(proposals)}개 제안)", file=sys.stderr)

    for prop in proposals:
        pid       = prop.get("id", "unknown")
        # 중복 제안 스킵 (같은 ID는 최신 파일 우선 — 역순 정렬이므로 첫 번째만)
        dedup_key = f"{pid}_{prop.get('description','')[:30]}"
        if dedup_key in seen_proposal_ids:
            continue
        seen_proposal_ids.add(dedup_key)
        desc      = prop.get("title") or prop.get("description", "설명 없음")
        severity  = prop.get("severity", "medium")
        before_tx = prop.get("before", "")

        pattern = infer_pattern(pid, desc, before_tx)

        # 이번 주 vs 지난 주 카운트
        before_count = count_pattern_in_logs(pattern, prev_cutoff, week_cutoff)
        after_count  = count_pattern_in_logs(pattern, week_cutoff, now)

        # 효과 판정
        if before_count > 0 and after_count < before_count:
            effective = True
            effective_count += 1
            total_before += before_count
            total_after  += after_count
        elif before_count == 0 and after_count == 0:
            # 로그 없음 — status 기반 추론
            effective = None  # 측정 불가
            if status in ("applied", "completed"):
                effective = True
                effective_count += 1
        elif after_count >= before_count and before_count > 0:
            effective = False
            ineffective_count += 1
            total_before += before_count
            total_after  += after_count
        else:
            effective = None

        applied_proposals.append({
            "id":            pid,
            "date":          (created_at[:10] if len(created_at) >= 10 else created_at),
            "description":   desc[:80],
            "severity":      severity,
            "pattern_before": before_count,
            "pattern_after":  after_count,
            "effective":     effective,
            "status":        status,
        })

# ── 전체 개선율 ──────────────────────────────────────────────
if total_before > 0:
    delta = total_before - total_after
    if delta > 0:
        pct = round(delta * 100 / total_before)
        overall_improvement = f"+{pct}%"
    elif delta < 0:
        pct = round(abs(delta) * 100 / total_before)
        overall_improvement = f"-{pct}% (악화)"
    else:
        overall_improvement = "0% (변화 없음)"
else:
    overall_improvement = "측정 불가 (로그 데이터 부족)"

# ── 비효과적 제안 목록 ───────────────────────────────────────
ineffective_proposals = [p for p in applied_proposals if p["effective"] is False]

# ── 거절된 제안 ──────────────────────────────────────────────
rejected_count = 0
rejected_proposals = []
if rejected_file.exists():
    try:
        rdata = json.loads(rejected_file.read_text(errors="ignore"))
        if isinstance(rdata, list):
            rejected_proposals = rdata
            rejected_count = len(rdata)
    except Exception:
        pass
print(f"  → 거절된 제안: {rejected_count}개", file=sys.stderr)

# ── 품질 트렌드 요약 ─────────────────────────────────────────
if quality_prev is not None and quality_this is not None:
    quality_summary = f"지난 주 {quality_prev} → 이번 주 {quality_this}"
else:
    quality_summary = "측정 불가 (self-review 데이터 없음)"

# ── 최종 JSON 출력 (명세서 형식) ────────────────────────────
result = {
    "generated_at":           now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "measurement_period_days": days,
    "total_proposal_files":   len(proposal_files),
    "applied_proposals":      applied_proposals,
    "effective_count":        effective_count,
    "ineffective_count":      ineffective_count,
    "overall_improvement":    overall_improvement,
    "pattern_before_total":   total_before,
    "pattern_after_total":    total_after,
    "quality_trend": {
        "prev_week": quality_prev,
        "this_week": quality_this,
        "summary":   quality_summary,
    },
    "ineffective_proposals":  ineffective_proposals,
    "rejected_count":         rejected_count,
    "rejected_proposals":     rejected_proposals,
}

output_file.parent.mkdir(parents=True, exist_ok=True)
output_file.write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(f"✅ [measure-effects] Python 완료 → {output_file}", file=sys.stderr)
print(f"   효과 있음: {effective_count} / 효과 없음: {ineffective_count} / 거절: {rejected_count}", file=sys.stderr)
# stdout 없음 — bash에서 cat으로 출력
PYEOF

# Python3 성공 여부 확인
if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
  echo "✅ [measure-effects] Python3 경로 성공" >&2
  cat "$OUTPUT_FILE"
  exit 0
fi

fi  # end if HAS_PY3

# ── Python3 없을 때: 최소 JSON fallback ─────────────────────
echo "  ⚠️  Python3 없음 또는 실패 — 기본 JSON 생성" >&2

PROPOSAL_COUNT=0
if [ -d "$PROPOSALS_DIR" ]; then
  PROPOSAL_COUNT=$(find "$PROPOSALS_DIR" -name "*.json" 2>/dev/null | wc -l | tr -d ' ' || echo 0)
fi

REJECTED_COUNT=0
if [ -f "$REJECTED_FILE" ] && command -v jq &>/dev/null; then
  REJECTED_COUNT=$(jq 'length' "$REJECTED_FILE" 2>/dev/null || echo 0)
fi

cat > "$OUTPUT_FILE" <<FALLBACK_JSON
{
  "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "measurement_period_days": $DAYS,
  "total_proposal_files": $PROPOSAL_COUNT,
  "applied_proposals": [],
  "effective_count": 0,
  "ineffective_count": 0,
  "overall_improvement": "측정 불가 (Python3 없음)",
  "pattern_before_total": 0,
  "pattern_after_total": 0,
  "quality_trend": {
    "prev_week": null,
    "this_week": null,
    "summary": "측정 불가 (Python3 없음)"
  },
  "ineffective_proposals": [],
  "rejected_count": $REJECTED_COUNT,
  "rejected_proposals": []
}
FALLBACK_JSON

echo "✅ [measure-effects] fallback JSON 생성 완료 → $OUTPUT_FILE" >&2
cat "$OUTPUT_FILE"
