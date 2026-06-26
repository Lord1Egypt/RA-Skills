#!/usr/bin/env bash
# ============================================================
# cross-agent-proposals.sh — SEA v5.0 크로스 에이전트 제안 생성기
#
# 역할: fleet-analyzer.sh가 생성한 fleet-report.json을 읽고
#       여러 에이전트에 동시 적용 가능한 제안을 생성.
#
# 제안 유형:
#   1. 전체 적용 — "모든 에이전트에 이 규칙을 추가해야 한다"
#   2. 규칙 이전 — "Agent A의 이 규칙을 Agent B로 복사"
#   3. 시스템 패턴 — "X/Y 에이전트에 같은 패턴 존재 → 공통 수정 필요"
#
# 출력:
#   - <SKILL_DIR>/data/fleet/cross-proposals-<DATE>.json
#   - stdout: 제안 요약 (Discord 전송 가능)
#
# 사용법:
#   bash cross-agent-proposals.sh
#   bash cross-agent-proposals.sh --json        # JSON만 출력
#   bash cross-agent-proposals.sh --dry-run     # 저장 없이 미리보기
#   FLEET_REPORT=/path/to/fleet-report.json bash cross-agent-proposals.sh
#
# 변경 이력:
#   v5.0 (2026-02-18) — SEA v5.0 크로스 에이전트 제안 신규 구현
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
FLEET_OUTPUT_DIR="${FLEET_OUTPUT_DIR:-$SKILL_DIR/data/fleet}"
FLEET_REPORT="${FLEET_REPORT:-$FLEET_OUTPUT_DIR/fleet-report.json}"
PROPOSALS_DIR="${PROPOSALS_DIR:-$SKILL_DIR/data/proposals}"
WORKSPACE="${WORKSPACE:-$HOME/openclaw}"

JSON_MODE=false
DRY_RUN=false

# 인수 파싱
for arg in "$@"; do
  case "$arg" in
    --json)    JSON_MODE=true ;;
    --dry-run) DRY_RUN=true ;;
  esac
done

log()  { [[ "$JSON_MODE" == "false" ]] && echo "[cross-proposals] $*" >&2 || true; }
ok()   { [[ "$JSON_MODE" == "false" ]] && echo "[cross-proposals] ✅ $*" >&2 || true; }
warn() { [[ "$JSON_MODE" == "false" ]] && echo "[cross-proposals] ⚠️  $*" >&2 || true; }

log "=== SEA v5.0 Cross-Agent Proposal Generator ==="

# fleet-report.json 존재 확인
if [[ ! -f "$FLEET_REPORT" ]]; then
  warn "fleet-report.json 없음. fleet-analyzer.sh 먼저 실행 필요."
  warn "실행: bash $SKILL_DIR/scripts/v5/fleet-analyzer.sh"
  if [[ "$JSON_MODE" == "true" ]]; then
    echo '{"error":"fleet-report.json not found","run":"bash fleet-analyzer.sh"}'
  fi
  exit 1
fi

log "fleet-report 읽기: $FLEET_REPORT"

# ── 제안 생성 (Python) ─────────────────────────────────────
DATE_TAG=$(date +%Y%m%d-%H%M%S 2>/dev/null || echo "unknown")
OUTPUT_FILE="$FLEET_OUTPUT_DIR/cross-proposals-${DATE_TAG}.json"
mkdir -p "$FLEET_OUTPUT_DIR" 2>/dev/null || true

python3 - "$FLEET_REPORT" "$OUTPUT_FILE" "$PROPOSALS_DIR" \
         "$JSON_MODE" "$DRY_RUN" "$DATE_TAG" "$WORKSPACE" \
<<'PYEOF' 2>/dev/null
import json, sys, os, re, datetime
from pathlib import Path

fleet_report_path = sys.argv[1]
output_file       = sys.argv[2]
proposals_dir     = sys.argv[3]
json_mode         = sys.argv[4] == "true"
dry_run           = sys.argv[5] == "true"
date_tag          = sys.argv[6]
workspace         = sys.argv[7]

now_iso = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# ─── Fleet 보고서 로드 ───
try:
    with open(fleet_report_path, encoding='utf-8') as f:
        fleet = json.load(f)
except Exception as e:
    print(f"Fleet 보고서 로드 실패: {e}", file=sys.stderr)
    sys.exit(1)

agent_scores    = fleet.get("agent_scores", {})
shared_patterns = fleet.get("shared_patterns", [])
systemic_issues = fleet.get("systemic_issues", [])
rankings        = fleet.get("rankings", {})
recommendations = fleet.get("recommendations", [])
agents_list     = list(agent_scores.keys())
n_agents        = len(agents_list)

proposals = []
proposal_id_base = f"cross-{date_tag}"

def make_proposal(proposal_id, title, proposal_type, targets, description,
                  before="", after="", severity="medium", source_agent=None,
                  affected_agents=None):
    return {
        "id": proposal_id,
        "type": "cross_agent",
        "proposal_type": proposal_type,  # all_agents | transfer | systemic
        "title": title,
        "description": description,
        "targets": targets,  # list of agent names or ["all"]
        "source_agent": source_agent,
        "affected_agents": affected_agents or targets,
        "severity": severity,
        "before": before,
        "after": after,
        "status": "pending",
        "created_at": now_iso,
        "fleet_version": "v5.0",
        "apply_command": None,
    }

# ─── 1. 시스템 공통 패턴 제안 ───
# N/M 에이전트에서 동일 위반 패턴 발생 → 공통 규칙 추가
for i, pattern in enumerate(systemic_issues):
    rule_id   = pattern.get("pattern", "")
    desc      = pattern.get("description", rule_id)
    affected  = pattern.get("agents_affected", [])
    count     = pattern.get("agent_count", 0)
    total_viol = pattern.get("total_violations", 0)

    if count < 2:
        continue

    # 위반 유형별 구체적인 수정 제안 생성
    fix_map = {
        "git_direct_cmd": {
            "title": "모든 에이전트: git 직접 명령 금지 강화",
            "before": "# git 직접 사용\ngit pull --rebase\ngit push origin main",
            "after": "# ✅ 올바른 방식: git-sync.sh 사용 필수\nbash ~/openclaw/scripts/git-sync.sh\n# 직접 git pull/push 절대 금지",
            "severity": "high",
        },
        "curl_no_fallback": {
            "title": "모든 에이전트: curl 에러 핸들링 필수",
            "before": "# 위험: 에러 핸들링 없음\ncurl https://api.example.com/data",
            "after": "# ✅ 올바른 방식\ncurl -sf https://api.example.com/data || echo 'API 요청 실패'",
            "severity": "high",
        },
        "rm_destructive": {
            "title": "모든 에이전트: rm -rf 대신 trash 사용",
            "before": "rm -rf /path/to/dir",
            "after": "trash /path/to/dir  # 복구 가능\n# 또는: rm -rf /path/to/dir 2>/dev/null || true",
            "severity": "medium",
        },
        "script_no_fallback": {
            "title": "모든 에이전트: 스크립트 실행 에러 핸들링 필수",
            "before": "python3 script.py\nnode script.js",
            "after": "python3 script.py 2>&1 || echo 'Script failed'\nnode script.js 2>&1 || echo 'Script failed'",
            "severity": "medium",
        },
        "gateway_launchctl": {
            "title": "모든 에이전트: launchctl 직접 호출 금지",
            "before": "launchctl bootout gui/501/...\nlaunchctl kickstart gui/501/...",
            "after": "# ✅ 올바른 방식\nopenclaw gateway stop\nopenclaw gateway start",
            "severity": "high",
        },
    }

    fix = fix_map.get(rule_id, {
        "title": f"모든 에이전트: {desc} 규칙 강화",
        "before": f"# {rule_id} 위반 패턴",
        "after": f"# ✅ {desc} 규칙 준수 필요",
        "severity": "medium",
    })

    p = make_proposal(
        proposal_id=f"{proposal_id_base}-systemic-{i+1:02d}",
        title=fix["title"],
        proposal_type="systemic",
        targets=affected,
        description=(
            f"시스템 공통 패턴: '{desc}' — {count}/{n_agents} 에이전트에서 발생 "
            f"(총 위반 {total_viol}건). 모든 영향 에이전트의 AGENTS.md 동시 업데이트 필요."
        ),
        before=fix["before"],
        after=fix["after"],
        severity=fix["severity"],
        affected_agents=affected,
    )
    p["apply_command"] = f"sea fleet sync {rule_id} --to-all"
    proposals.append(p)

# ─── 2. Exec 안전성 규칙 이전 제안 ───
# 가장 안전한 에이전트의 규칙을 덜 안전한 에이전트로 이전
if len(agent_scores) >= 2:
    sorted_by_safety = sorted(
        agent_scores.keys(),
        key=lambda a: agent_scores[a].get("exec_safety", 8.0)
    )
    worst  = sorted_by_safety[0]
    best   = sorted_by_safety[-1]
    ws = agent_scores[worst].get("exec_safety", 8.0)
    bs = agent_scores[best].get("exec_safety", 8.0)

    if worst != best and bs - ws >= 1.5:
        p = make_proposal(
            proposal_id=f"{proposal_id_base}-exec-safety-transfer",
            title=f"Exec 안전 규칙: {best} → {worst} 이전",
            proposal_type="transfer",
            targets=[worst],
            description=(
                f"{best} 에이전트의 exec 안전성({bs:.1f}/10)이 {worst}({ws:.1f}/10)보다 "
                f"{bs-ws:.1f}점 높음. {best}에서 검증된 exec 안전 패턴을 {worst}로 이전."
            ),
            before=f"# {worst}의 현재 exec 패턴 (안전성 {ws:.1f}/10)",
            after=(
                f"# ✅ {best}의 exec 안전 패턴 적용 (안전성 {bs:.1f}/10)\n"
                f"# 모든 exec 호출에 || true 또는 2>&1 || echo 추가\n"
                f"# bash ~/openclaw/scripts/safe-exec.sh 래퍼 우선 사용"
            ),
            severity="high",
            source_agent=best,
        )
        p["apply_command"] = f"sea fleet sync exec_safety --from {best} --to {worst}"
        proposals.append(p)

# ─── 3. 좌절 이벤트 기반 제안 ───
# 좌절이 많은 에이전트 → 컨텍스트 관리 규칙 추가
frustration_ranking = rankings.get("most_frustration", [])
if frustration_ranking:
    worst_frust = frustration_ranking[0]
    if worst_frust.get("value", 0) >= 3:
        agent = worst_frust["agent"]
        count = worst_frust["value"]

        # 가장 좌절이 적은 에이전트
        least_frust = frustration_ranking[-1] if len(frustration_ranking) > 1 else None
        source = least_frust["agent"] if least_frust and least_frust["agent"] != agent else None

        p = make_proposal(
            proposal_id=f"{proposal_id_base}-frustration-fix",
            title=f"{agent}: 사용자 좌절 감소 — 컨텍스트 관리 강화",
            proposal_type="transfer" if source else "improvement",
            targets=[agent],
            description=(
                f"{agent} 에이전트 좌절 이벤트 {count}건 — 플릿 최고치. "
                f"컨텍스트 손실, 반복 재요청, 의도 파악 실패가 주원인. "
                f"SESSION-STATE.md WAL 프로토콜 및 작업 완료 확인 루프 강화 필요."
                + (f" 참고: {source} 에이전트 패턴 (좌절 {least_frust['value']}건)." if source else "")
            ),
            before="# 컨텍스트 손실 방지 규칙 없음",
            after=(
                "## 컨텍스트 손실 방지 규칙\n\n"
                "- 장시간 작업 시작 전: SESSION-STATE.md에 목표/진행상황 기록 (WAL)\n"
                "- 완료 확인: '작업이 완료됐는지 확인해줘' → 파일 실제 확인 후 응답\n"
                "- 사용자가 '아까 말했잖아'류 표현 시: 즉시 SESSION-STATE.md 확인"
            ),
            severity="high",
            source_agent=source,
        )
        if source:
            p["apply_command"] = f"sea fleet sync context_rules --from {source} --to {agent}"
        proposals.append(p)

# ─── 4. 비활성 에이전트 제안 ───
no_session_agents = [
    name for name, s in agent_scores.items()
    if s.get("sessions_analyzed", 0) == 0
]
if no_session_agents:
    p = make_proposal(
        proposal_id=f"{proposal_id_base}-inactive-agents",
        title=f"비활성 에이전트 점검 필요: {', '.join(no_session_agents)}",
        proposal_type="all_agents",
        targets=no_session_agents,
        description=(
            f"다음 에이전트에서 최근 세션 데이터 없음: {', '.join(no_session_agents)}. "
            f"에이전트 설정, 채널 연결, LaunchAgent 상태 확인 필요."
        ),
        severity="low",
    )
    p["apply_command"] = f"openclaw agent status"
    proposals.append(p)

# ─── 5. 전체 에이전트 공통 규칙 강화 제안 ───
# fleet_health가 낮으면 공통 규칙 추가
fleet_health = fleet.get("fleet_health", 7.0)
if fleet_health < 7.0 and n_agents >= 2:
    p = make_proposal(
        proposal_id=f"{proposal_id_base}-fleet-health-boost",
        title=f"플릿 전체 건강도 개선 (현재: {fleet_health}/10)",
        proposal_type="all_agents",
        targets=["all"],
        description=(
            f"플릿 건강도 {fleet_health}/10 — 목표 8.5 미달. "
            f"모든 에이전트의 AGENTS.md에 핵심 exec 안전 규칙, "
            f"WAL 프로토콜, 채널 라우팅 규칙 검토 및 강화 필요."
        ),
        before="# 현재 규칙 미비 상태",
        after=(
            "## 플릿 공통 필수 규칙\n\n"
            "1. **Exec 황금률**: 실패 가능한 모든 명령에 || true 또는 에러 핸들링 필수\n"
            "2. **WAL 프로토콜**: 중요 정보는 SESSION-STATE.md에 먼저 기록 후 응답\n"
            "3. **Git 안전**: git 직접 명령 금지 — git-sync.sh 사용\n"
            "4. **채널 라우팅**: 기술 작업→dev, 단순 질문→lite, 일반→main\n"
            "5. **메시지 통합**: 짧은 메시지 연속 전송 금지 (하나로 통합)"
        ),
        severity="medium",
        affected_agents=agents_list,
    )
    p["apply_command"] = "sea fleet sync core_rules --to-all"
    proposals.append(p)

# ─── 제안 요약 ───
summary = {
    "generated_at": now_iso,
    "fleet_report": fleet_report_path,
    "fleet_health": fleet_health,
    "agents_analyzed": n_agents,
    "proposals_count": len(proposals),
    "proposals_by_type": {
        "systemic": len([p for p in proposals if p["proposal_type"] == "systemic"]),
        "transfer": len([p for p in proposals if p["proposal_type"] == "transfer"]),
        "all_agents": len([p for p in proposals if p["proposal_type"] == "all_agents"]),
        "improvement": len([p for p in proposals if p["proposal_type"] == "improvement"]),
    },
    "proposals_by_priority": {
        "high": len([p for p in proposals if p["severity"] == "high"]),
        "medium": len([p for p in proposals if p["severity"] == "medium"]),
        "low": len([p for p in proposals if p["severity"] == "low"]),
    },
}

output = {
    "summary": summary,
    "proposals": proposals,
}

# ─── 저장 / 출력 ───
if not dry_run:
    # 파일 저장
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # 개별 proposals 디렉토리에도 저장 (sea proposals로 관리 가능)
    os.makedirs(proposals_dir, exist_ok=True)
    for p in proposals:
        prop_file = os.path.join(proposals_dir, f"proposal-cross-{p['id']}.json")
        with open(prop_file, "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=2)

if json_mode:
    print(json.dumps(output, ensure_ascii=False, indent=2))
else:
    # 사람이 읽기 좋은 요약 출력 (stdout → Discord 전송 가능)
    print(f"\n🚀 SEA v5.0 Cross-Agent Proposals")
    print(f"{'='*50}")
    print(f"플릿 건강도: {fleet_health:.1f}/10 | 에이전트: {n_agents}개 | 제안: {len(proposals)}개")
    print()

    if not proposals:
        print("✅ 크로스 에이전트 제안 없음 — 플릿 상태 양호")
    else:
        priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢", "critical": "🚨"}
        type_icons = {"systemic": "⚡ 시스템", "transfer": "🔄 이전", "all_agents": "📢 전체", "improvement": "📈 개선"}

        for p in sorted(proposals, key=lambda x: {"high":0,"medium":1,"low":2,"critical":-1}.get(x["severity"],3)):
            icon = priority_icons.get(p["severity"], "❓")
            type_label = type_icons.get(p["proposal_type"], p["proposal_type"])
            targets = ", ".join(p["targets"]) if isinstance(p["targets"], list) else p["targets"]
            print(f"{icon} [{type_label}] {p['title']}")
            print(f"   대상: {targets}")
            print(f"   {p['description'][:120]}...")
            if p.get("apply_command"):
                print(f"   → {p['apply_command']}")
            print()

    if not dry_run:
        print(f"📁 저장: {output_file}")
        print(f"📁 제안들: {proposals_dir}/proposal-cross-*.json")
    else:
        print("ℹ️  DRY RUN: 파일 저장 안 함")
PYEOF

# ── 완료 확인 ───────────────────────────────────────────────
if [[ "$DRY_RUN" != "true" && -f "$OUTPUT_FILE" ]]; then
  ok "Cross-agent 제안 저장 완료: $OUTPUT_FILE"
elif [[ "$DRY_RUN" == "true" ]]; then
  ok "DRY RUN 완료 (파일 저장 안 함)"
else
  warn "제안 파일 생성 실패"
  exit 1
fi

log "=== SEA v5.0 Cross-Agent Proposals 완료 ==="
