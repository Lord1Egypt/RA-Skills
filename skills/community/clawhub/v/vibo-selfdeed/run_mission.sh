#!/usr/bin/env bash
# run_mission.sh — vibo-selfdeed mission wrapper.
#
# Subcommands:
#   init      --task "<description>" [--target 90] [--auto]  — start mission (backup dir, log)
#   checkpoint <STAGE> <ok|fail|note> "<comment>"           — mark stage START/SCAN/PROPOSE/FIX/LEARN/REPORT
#   progress  <done>/<total>                              — update success % (compass)
#   switch    <A|B|C>                                     — switch path (quantum pool)
#   rollback  <file>                                      — rollback from backup
#   finish    [--message "..."]                             — final report (mission + vibo usage)
#   notify    "<text>"                                     — Telegram notification (if configured)
#   ask       "<question>" "<details>"                     — ✅/❌ buttons, wait for answer (0=yes,1=no,2=no answer)
#   report    "<task>" "<line1>" ...                        — mission report to Telegram
#
# Example:
#   ./run_mission.sh init --task "fix bugs in src/" --target 90 --auto
#   ./run_mission.sh checkpoint START ok "context restored from ViBo"
#   ./run_mission.sh progress 3/10
#   ./run_mission.sh finish

set -euo pipefail
MISSION_DIR=".selfdeed_mission"
MISSION_JSON="$MISSION_DIR/mission.json"
MISSION_LOG="$MISSION_DIR/mission.log"
NOW() { date -u +%Y-%m-%dT%H:%M:%SZ; }
log() { echo "[$(NOW)] $*" >> "$MISSION_LOG"; }

cmd_init() {
  local task="" target=90 auto=0
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --task) task="$2"; shift 2 ;;
      --target) target="$2"; shift 2 ;;
      --auto) auto=1; shift ;;
      *) shift ;;
    esac
  done
  [[ -z "$task" ]] && { echo "❌ --task required"; exit 1; }
  mkdir -p "$MISSION_DIR"
  cat > "$MISSION_JSON" <<EOF
{
  "task": "$(echo "$task" | sed 's/"/\\"/g')",
  "target_percent": $target,
  "auto": $auto,
  "started_at": "$(NOW)",
  "progress": {"done": 0, "total": 0, "percent": 0},
  "path": "A",
  "stagnation": {"A": 0, "B": 0, "C": 0},
  "stages": {},
  "rounds": [],
  "stop_reason": null
}
EOF
  mkdir -p "$MISSION_DIR/backup"
  echo "🚀 Mission started: $task (target $target%, auto=$auto)"
  log "INIT task=$task target=$target auto=$auto"
}

cmd_checkpoint() {
  local stage="${1:-}" status="${2:-ok}" comment="${3:-}"
  [[ -f "$MISSION_JSON" ]] || { echo "❌ no mission: run init first"; exit 1; }
  # python JSON update (safer than sed)
  python3 - "$stage" "$status" "$comment" "$MISSION_JSON" <<'PYEOF'
import json, sys, time
stage, status, comment, path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
d = json.load(open(path, encoding="utf-8"))
d.setdefault("stages", {})[stage] = {"status": status, "comment": comment, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✅ stage {stage} [{status}] {comment}")
PYEOF
  log "CHECKPOINT $stage $status $comment"
}

cmd_progress() {
  local done_total="${1:-}"
  [[ -f "$MISSION_JSON" ]] || { echo "❌ no mission started"; exit 1; }
  local done="${done_total%/*}" total="${done_total#*/}"
  python3 - "$done" "$total" "$MISSION_JSON" <<'PYEOF'
import json, sys
done, total, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
d = json.load(open(path, encoding="utf-8"))
d["progress"] = {"done": done, "total": total, "percent": round(100*done/max(1,total))}
json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
p = d["progress"]["percent"]
t = d["target_percent"]
print(f"📊 {done}/{total} = {p}% (target {t}%)")
if p >= t: print("🎯 TARGET REACHED — run finish")
PYEOF
}

cmd_switch() {
  local path="${1:-}"
  [[ "$path" =~ ^[ABC]$ ]] || { echo "❌ path: A/B/C"; exit 1; }
  python3 - "$path" "$MISSION_JSON" <<'PYEOF'
import json, sys
path, file = sys.argv[1], sys.argv[2]
d = json.load(open(file, encoding="utf-8"))
d["path"] = path
json.dump(d, open(file, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"🔀 Path switched to {path}")
PYEOF
  log "SWITCH path=$path"
}

cmd_rollback() {
  local f="${1:-}"
  [[ -f "$MISSION_JSON" ]] || { echo "❌ no mission started"; exit 1; }
  echo "⚠️ This will OVERWRITE $f from the latest backup." >&2
  read -r -p "Continue? [y/N] " _ok
  [[ "$_ok" =~ ^(y|yes|д|да)$ ]] || { echo "❌ cancelled"; exit 1; }
  python3 - "$f" "$MISSION_DIR/backup" <<'PYEOF'
import sys, shutil, glob
from pathlib import Path
target, bdir = sys.argv[1], Path(sys.argv[2])
cands = sorted(bdir.glob(f"{Path(target).name}.*.bak"))
if not cands:
    print(f"❌ no backups for {target}"); sys.exit(1)
src, dst = cands[-1], Path(target)
shutil.copy2(src, dst)
print(f"↩️ Rollback: {target} ← {src.name}")
PYEOF
  log "ROLLBACK $f"
}

cmd_finish() {
  [[ -f "$MISSION_JSON" ]] || { echo "❌ no mission started"; exit 1; }
  python3 - "$MISSION_JSON" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
p = d["progress"]
print("=" * 44)
print("🏁 MISSION REPORT (vibo-selfdeed)")
print("=" * 44)
print(f"Task:    {d['task']}")
print(f"Progress: {p['done']}/{p['total']} = {p['percent']}% (target {d['target_percent']}%)")
print(f"Paths:   {d.get('rounds', []) or '—'}")
print(f"Stages:")
for st, v in (d.get("stages") or {}).items():
    print(f"  {st}: [{v['status']}] {v['comment']}")
print(f"Stop:    {d.get('stop_reason') or '—'}")
PYEOF
  echo "—" >> "$MISSION_LOG"
  log "FINISH"
  # ViBo usage — via lib_vibo.py (single CLI lookup)
  if [[ -f lib_vibo.py ]]; then
    echo "--- 💾 ViBo usage ---"
    python3 lib_vibo.py usage 2>/dev/null | head -8 || true
  fi
}

case "${1:-}" in
  init) shift; cmd_init "$@" ;;
  checkpoint) shift; cmd_checkpoint "$@" ;;
  progress) shift; cmd_progress "$@" ;;
  switch) shift; cmd_switch "$@" ;;
  rollback) shift; cmd_rollback "$@" ;;
  finish) shift; cmd_finish "$@" ;;
  notify) shift; echo "⚠️ NOTE: this sends mission data to Telegram (external service)" >&2; [[ -f telegram_mission.py ]] && python3 telegram_mission.py notify "${1:-}" || echo "📨 [no telegram_mission.py]" ;;
  ask) shift; echo "⚠️ NOTE: this sends mission data to Telegram (external service)" >&2; [[ -f telegram_mission.py ]] && python3 telegram_mission.py ask "${1:-}" "${2:-}" || { echo "❓ ${1:-}"; echo "   ${2:-}"; exit 2; } ;;
  report) shift; echo "⚠️ NOTE: this sends mission data to Telegram (external service)" >&2; [[ -f telegram_mission.py ]] && python3 telegram_mission.py report "${1:-}" "${@:2}" || echo "📨 [no telegram_mission.py]" ;;
  *) grep -E '^#   ' "$0" | head -25; exit 1 ;;
esac
