#!/usr/bin/env bash
# ============================================================
# pattern-library.sh — Self-Evolving Agent v5.0 패턴 라이브러리
#
# 역할: 과거 제안과 적용 효과에서 "검증된 규칙"을 자동 추출하여
#       패턴 카탈로그를 구축하고 새 패턴 감지 시 규칙을 제안.
#
# 기능:
#   - 모든 과거 제안 스캔 + 효과 측정값 수집
#   - "known_good_rules" 카탈로그 빌드 (측정된 impact 포함)
#   - 새 패턴에 대해 라이브러리에서 유사 규칙 제안
#   - `sea patterns` CLI 명령으로 브라우즈
#
# 출력:
#   - data/patterns/library.json  — 패턴 카탈로그
#   - stdout                      — 인간 가독 브라우저 뷰
#
# 사용법:
#   bash pattern-library.sh                      # 라이브러리 빌드 + 표시
#   bash pattern-library.sh --build              # 빌드만 (출력 없음)
#   bash pattern-library.sh --list               # 모든 패턴 목록
#   bash pattern-library.sh --search <keyword>   # 키워드 검색
#   bash pattern-library.sh --suggest <text>     # 텍스트에서 규칙 제안
#   bash pattern-library.sh --json               # JSON 출력
#   bash pattern-library.sh --top N              # 상위 N개 고영향 패턴
#
# 변경 이력:
#   v5.0 (2026-02-18) — 신규 구현
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
PROPOSALS_DIR="$DATA_DIR/proposals"
PATTERNS_DIR="$DATA_DIR/patterns"
LIBRARY_FILE="$PATTERNS_DIR/library.json"
ALERTS_DIR="$DATA_DIR/alerts"

R=$'\033[0;31m'; G=$'\033[0;32m'; Y=$'\033[1;33m'
C=$'\033[0;36m'; B=$'\033[1m';    N=$'\033[0m'

mkdir -p "$PATTERNS_DIR" 2>/dev/null || true

# ── 라이브러리 빌드 ────────────────────────────────────────
build_library() {
  local quiet="${1:-false}"
  [[ "$quiet" == "false" ]] && echo -e "${C}📚 패턴 라이브러리 빌드 중...${N}"

  python3 - "$PROPOSALS_DIR" "$ALERTS_DIR" "$LIBRARY_FILE" <<'PYEOF'
import json, os, sys, glob, re, datetime
from collections import defaultdict

proposals_dir = sys.argv[1]
alerts_dir    = sys.argv[2]
library_file  = sys.argv[3]

# ── 제안에서 패턴 추출 ──────────────────────────────────────
patterns = {}  # pattern_id → pattern_data

def make_pattern_id(title, section):
    """패턴 ID 생성 (제목 + 섹션 기반)"""
    text = f"{title}_{section}".lower()
    text = re.sub(r'[^\w]', '_', text)
    text = re.sub(r'_+', '_', text).strip('_')
    return text[:60]

for pf in sorted(glob.glob(os.path.join(proposals_dir, "**/*.json"), recursive=True)):
    try:
        with open(pf) as f:
            d = json.load(f)
    except:
        continue

    # 최상위 수준 제안
    proposal_list = d.get("proposals", [d])
    if not isinstance(proposal_list, list):
        proposal_list = [d]

    base_score    = d.get("quality_score", None)
    base_date     = d.get("generated_at", d.get("week_end", ""))[:10]
    base_status   = d.get("status", "unknown")
    base_sessions = d.get("sessions_analyzed", 0)

    for prop in proposal_list:
        if not isinstance(prop, dict):
            continue

        title   = prop.get("title", "")
        section = prop.get("target_section", prop.get("section", ""))
        before  = prop.get("before", "")
        after   = prop.get("after", "")
        pattern = prop.get("target_pattern", "")
        sev     = prop.get("severity", "medium")
        effect  = prop.get("effect", None)
        delta   = prop.get("effect_delta", None)
        hits_b  = prop.get("pattern_hits_before", 0)
        hits_a  = prop.get("pattern_hits_after", 0)
        evid    = prop.get("evidence", "")
        change  = prop.get("change_type", "")
        status  = prop.get("status", base_status)
        prop_id = prop.get("id", "")

        if not title:
            continue

        pid = make_pattern_id(title, section)

        if pid not in patterns:
            patterns[pid] = {
                "id":           pid,
                "title":        title,
                "section":      section,
                "before":       before,
                "after":        after,
                "target_pattern": pattern,
                "change_type":  change,
                "severity":     sev,
                "evidence_samples": [],
                "occurrences":  0,
                "applied_count": 0,
                "impact_scores": [],
                "hit_reductions": [],
                "dates":        [],
                "is_known_good": False,
                "impact_rating": "unknown",
                "confidence":   0.0,
                "tags":         [],
            }

        p = patterns[pid]
        p["occurrences"] += 1
        if base_date:
            p["dates"].append(base_date)

        if evid and evid not in p["evidence_samples"]:
            p["evidence_samples"].append(evid)

        if status in ("applied", "approved"):
            p["applied_count"] += 1

        # 효과 측정값
        if delta is not None:
            try:
                p["impact_scores"].append(float(delta))
            except:
                pass

        if hits_b and hits_a is not None:
            try:
                reduction = (int(hits_b) - int(hits_a)) / int(hits_b) if int(hits_b) > 0 else 0
                p["hit_reductions"].append(reduction)
            except:
                pass

# ── 알림 패턴도 통합 ────────────────────────────────────────
alert_patterns = defaultdict(int)
if os.path.isdir(alerts_dir):
    for af in glob.glob(os.path.join(alerts_dir, "*.json")):
        try:
            with open(af) as f:
                ad = json.load(f)
            for alert in ad.get("alerts", []):
                pat = alert.get("pattern", "")
                if pat:
                    alert_patterns[pat] += 1
        except:
            pass

# 알림 패턴을 라이브러리에 추가 (기존 패턴과 매칭 시 보강)
for apat, count in alert_patterns.items():
    # 기존 패턴에서 매칭 찾기
    matched = False
    for pid, p in patterns.items():
        if apat.lower() in p["title"].lower() or apat.lower() in pid:
            p["occurrences"] = p.get("occurrences", 0) + count
            matched = True
            break
    if not matched:
        # 새 패턴으로 추가
        patterns[f"alert_{apat}"] = {
            "id":             f"alert_{apat}",
            "title":          f"실시간 경보: {apat}",
            "section":        "(스트림 모니터)",
            "before":         "",
            "after":          "",
            "target_pattern": apat,
            "change_type":    "alert_pattern",
            "severity":       "medium",
            "evidence_samples": [],
            "occurrences":    count,
            "applied_count":  0,
            "impact_scores":  [],
            "hit_reductions": [],
            "dates":          [],
            "is_known_good":  False,
            "impact_rating":  "unknown",
            "confidence":     0.0,
            "tags":           ["realtime", "alert"],
        }

# ── 패턴 평가 ──────────────────────────────────────────────
for pid, p in patterns.items():
    scores  = p["impact_scores"]
    reduces = p["hit_reductions"]
    applied = p["applied_count"]
    occur   = p["occurrences"]

    # 신뢰도 계산
    confidence = min(1.0, (applied / max(occur, 1)) * 0.6 +
                          (len(scores) / max(5, len(scores))) * 0.4)
    p["confidence"] = round(confidence, 2)

    # 평균 임팩트
    if scores:
        avg_impact = sum(scores) / len(scores)
        p["avg_impact"] = round(avg_impact, 3)
    else:
        p["avg_impact"] = None

    if reduces:
        avg_reduce = sum(reduces) / len(reduces)
        p["avg_hit_reduction"] = round(avg_reduce, 3)
    else:
        p["avg_hit_reduction"] = None

    # known_good 판정: 적용됨 + 긍정적 효과 or 높은 신뢰도
    is_good = (
        applied >= 1 and
        (p["avg_impact"] is None or p["avg_impact"] >= 0) and
        confidence >= 0.5
    )
    p["is_known_good"] = is_good

    # 임팩트 등급
    if p["avg_impact"] is not None:
        if p["avg_impact"] >= 0.5:
            p["impact_rating"] = "high"
        elif p["avg_impact"] >= 0.2:
            p["impact_rating"] = "medium"
        elif p["avg_impact"] >= 0:
            p["impact_rating"] = "low"
        else:
            p["impact_rating"] = "negative"
    elif applied >= 1:
        p["impact_rating"] = "applied_no_data"
    else:
        p["impact_rating"] = "not_applied"

    # 태그 자동 생성
    tags = []
    if p["severity"] == "high":
        tags.append("high-severity")
    if is_good:
        tags.append("known-good")
    if p["impact_rating"] == "high":
        tags.append("high-impact")
    if "git" in p["title"].lower() or "git" in pid:
        tags.append("git")
    if "exec" in p["title"].lower() or "exec" in pid:
        tags.append("exec")
    if "memory" in p["title"].lower() or "메모리" in p["title"]:
        tags.append("memory")
    if "discord" in p["title"].lower():
        tags.append("discord")
    if "gateway" in p["title"].lower() or "gateway" in pid:
        tags.append("gateway")
    if "realtime" in p.get("tags", []):
        tags.append("realtime")
    p["tags"] = list(set(tags))

# ── 라이브러리 저장 ────────────────────────────────────────
now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
sorted_patterns = sorted(
    patterns.values(),
    key=lambda x: (
        -int(x.get("is_known_good", False)),
        -x.get("applied_count", 0),
        -x.get("occurrences", 0)
    )
)

library = {
    "generated_at":   now,
    "total_patterns": len(patterns),
    "known_good":     sum(1 for p in patterns.values() if p.get("is_known_good")),
    "high_impact":    sum(1 for p in patterns.values() if p.get("impact_rating") == "high"),
    "patterns":       sorted_patterns,
}

os.makedirs(os.path.dirname(library_file), exist_ok=True)
with open(library_file, 'w') as f:
    json.dump(library, f, ensure_ascii=False, indent=2)

print(f"✅ 라이브러리 빌드 완료: {len(patterns)}개 패턴, "
      f"{library['known_good']}개 known-good")
PYEOF
}

# ── 패턴 목록 표시 ─────────────────────────────────────────
cmd_list() {
  local top="${1:-0}"  # 0 = 전체

  [[ ! -f "$LIBRARY_FILE" ]] && build_library "true"

  python3 - "$LIBRARY_FILE" "$top" <<'PYEOF'
import json, sys

lib_file = sys.argv[1]
top_n    = int(sys.argv[2])

try:
    with open(lib_file) as f:
        lib = json.load(f)
except:
    print("❌ 라이브러리 파일 없음. `sea patterns` 실행하여 빌드하세요.")
    sys.exit(1)

patterns = lib.get("patterns", [])
if top_n > 0:
    patterns = patterns[:top_n]

# 색상 ANSI
GOOD = '\033[0;32m'; WARN = '\033[1;33m'; BAD = '\033[0;31m'
CYAN = '\033[0;36m'; BOLD = '\033[1m'; RESET = '\033[0m'

print(f"{BOLD}📚 패턴 라이브러리{RESET} — {lib['total_patterns']}개 패턴, "
      f"{lib['known_good']}개 known-good, {lib['high_impact']}개 high-impact")
print(f"최종 업데이트: {lib.get('generated_at','?')}")
print()

for p in patterns:
    # 아이콘
    if p.get("is_known_good"):
        icon = f"{GOOD}✅{RESET}"
    elif p.get("impact_rating") == "negative":
        icon = f"{BAD}⚠️{RESET}"
    else:
        icon = f"{WARN}🔷{RESET}"

    impact_str = ""
    if p.get("avg_impact") is not None:
        sign = "+" if p["avg_impact"] >= 0 else ""
        impact_str = f" | 임팩트: {sign}{p['avg_impact']:.2f}"

    reduce_str = ""
    if p.get("avg_hit_reduction") is not None:
        reduce_str = f" | 감소율: {p['avg_hit_reduction']*100:.0f}%"

    tags_str = " ".join(f"[{t}]" for t in p.get("tags", [])[:3])

    print(f"{icon} {BOLD}{p['title']}{RESET}")
    print(f"    섹션: {p.get('section','?')} | "
          f"적용: {p.get('applied_count',0)}회 | "
          f"빈도: {p.get('occurrences',0)}회"
          f"{impact_str}{reduce_str}")
    if tags_str:
        print(f"    {CYAN}{tags_str}{RESET}")
    if p.get("evidence_samples"):
        ev = p["evidence_samples"][0][:80]
        print(f"    근거: {ev}")
    print()
PYEOF
}

# ── 키워드 검색 ────────────────────────────────────────────
cmd_search() {
  local keyword="${1:-}"
  [[ -z "$keyword" ]] && { echo "Usage: $0 --search <keyword>"; exit 1; }

  [[ ! -f "$LIBRARY_FILE" ]] && build_library "true"

  python3 - "$LIBRARY_FILE" "$keyword" <<'PYEOF'
import json, sys

lib_file = sys.argv[1]
kw       = sys.argv[2].lower()

try:
    with open(lib_file) as f:
        lib = json.load(f)
except:
    print("라이브러리 없음")
    sys.exit(1)

BOLD = '\033[1m'; RESET = '\033[0m'; CYAN = '\033[0;36m'

results = []
for p in lib.get("patterns", []):
    searchable = " ".join([
        p.get("title",""), p.get("section",""),
        p.get("before",""), p.get("after",""),
        p.get("target_pattern",""),
        " ".join(p.get("evidence_samples",[])),
        " ".join(p.get("tags",[])),
    ]).lower()
    if kw in searchable:
        results.append(p)

if not results:
    print(f"'{kw}' 검색 결과 없음")
    sys.exit(0)

print(f"{BOLD}🔍 '{kw}' 검색 결과: {len(results)}건{RESET}")
print()
for p in results:
    good = "✅" if p.get("is_known_good") else "🔷"
    print(f"{good} {BOLD}{p['title']}{RESET}")
    print(f"   {CYAN}{p.get('section','')}{RESET}")
    if p.get("after"):
        print(f"   → {p['after'][:100]}")
    print()
PYEOF
}

# ── 규칙 제안 ──────────────────────────────────────────────
cmd_suggest() {
  local text="${1:-}"
  [[ -z "$text" ]] && { echo "Usage: $0 --suggest '<text>'"; exit 1; }

  [[ ! -f "$LIBRARY_FILE" ]] && build_library "true"

  python3 - "$LIBRARY_FILE" <<PYEOF
import json, sys, re

with open("$LIBRARY_FILE") as f:
    lib = json.load(f)

query = """$text""".lower()
BOLD = '\033[1m'; RESET = '\033[0m'; GREEN = '\033[0;32m'

suggestions = []
for p in lib.get("patterns", []):
    score = 0

    # 패턴 정규식 매칭
    pat = p.get("target_pattern", "")
    if pat:
        try:
            if re.search(pat, query, re.IGNORECASE):
                score += 5
        except:
            pass

    # 키워드 매칭
    for word in p.get("title","").lower().split():
        if len(word) > 3 and word in query:
            score += 1

    for ev in p.get("evidence_samples", []):
        for word in ev.lower().split():
            if len(word) > 3 and word in query:
                score += 0.5

    if score > 0:
        suggestions.append((score, p))

suggestions.sort(key=lambda x: -x[0])

if not suggestions:
    print("라이브러리에서 관련 규칙을 찾을 수 없습니다.")
    print("새 패턴으로 기록하는 것을 권장합니다.")
else:
    print(f"{BOLD}💡 라이브러리 기반 규칙 제안{RESET}")
    print()
    for score, p in suggestions[:3]:
        good = "✅ " if p.get("is_known_good") else ""
        print(f"{good}{BOLD}{p['title']}{RESET} (관련도: {score:.1f})")
        if p.get("after"):
            print(f"  권장 규칙: {p['after'][:150]}")
        if p.get("section"):
            print(f"  대상 섹션: {p['section']}")
        if p.get("avg_impact") is not None:
            sign = "+" if p["avg_impact"] >= 0 else ""
            print(f"  측정 효과: {sign}{p['avg_impact']:.2f} quality_score")
        print()
PYEOF
}

# ── JSON 출력 ──────────────────────────────────────────────
cmd_json() {
  [[ ! -f "$LIBRARY_FILE" ]] && build_library "true"
  cat "$LIBRARY_FILE"
}

# ── 진입점 ─────────────────────────────────────────────────
MODE="list"
ARG=""
TOP_N=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build)         MODE="build"; shift ;;
    --list)          MODE="list"; shift ;;
    --json)          MODE="json"; shift ;;
    --search)        MODE="search"; ARG="${2:-}"; shift 2 ;;
    --suggest)       MODE="suggest"; ARG="${2:-}"; shift 2 ;;
    --top)           TOP_N="${2:-10}"; shift 2 ;;
    --help|-h)
      echo "Usage: $0 [--build] [--list] [--json] [--search <kw>] [--suggest <text>] [--top N]"
      exit 0 ;;
    *) echo "Unknown: $1" >&2; exit 1 ;;
  esac
done

case "$MODE" in
  build)   build_library "false" ;;
  list)    build_library "true" && cmd_list "$TOP_N" ;;
  json)    cmd_json ;;
  search)  cmd_search "$ARG" ;;
  suggest) cmd_suggest "$ARG" ;;
esac
