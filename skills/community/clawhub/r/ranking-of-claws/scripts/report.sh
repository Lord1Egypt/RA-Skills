#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$SKILL_DIR/config.json"
STATE_FILE="${HOME}/.openclaw/ranking-of-claws-state.json"
API_URL="https://rankingofclaws.angelstreet.io/api/report"

AGENT_NAME_OVERRIDE="${1:-}"
COUNTRY_OVERRIDE="${2:-}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ranking-of-claws: python3 is required for JSONL parsing."
  exit 1
fi

PAYLOADS="$(
python3 - "$CONFIG_FILE" "$STATE_FILE" "$AGENT_NAME_OVERRIDE" "$COUNTRY_OVERRIDE" <<'PY'
import hashlib
import json
import os
import sys
from pathlib import Path

config_file = Path(sys.argv[1])
state_file = Path(sys.argv[2])
agent_override = sys.argv[3].strip()
country_override = sys.argv[4].strip()
home = Path(os.environ.get("HOME", ""))

def safe_num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0

def usage_totals(usage):
    if not isinstance(usage, dict):
        return None
    input_t = safe_num(usage.get("input", usage.get("inputTokens", usage.get("promptTokens", 0))))
    output_t = safe_num(usage.get("output", usage.get("outputTokens", usage.get("completionTokens", 0))))
    total_t = safe_num(usage.get("totalTokens", usage.get("total", usage.get("tokens", 0))))
    if total_t <= 0 and (input_t > 0 or output_t > 0):
        total_t = input_t + output_t
    if total_t <= 0 and input_t <= 0 and output_t <= 0:
        return None
    return {
        "tokens": int(total_t),
        "input": int(input_t),
        "output": int(output_t),
    }

cfg = {}
if config_file.exists():
    try:
        cfg = json.loads(config_file.read_text(encoding="utf-8"))
    except Exception:
        cfg = {}

gateway_id = cfg.get("gateway_id")
if not gateway_id:
    raw = f"{os.uname().nodename}-{os.environ.get('HOME','')}-openclaw"
    gateway_id = hashlib.sha256(raw.encode()).hexdigest()[:16]

agent_name = agent_override or cfg.get("agent_name") or os.environ.get("RANKING_AGENT_NAME") or os.uname().nodename
country = (country_override or cfg.get("country") or os.environ.get("RANKING_COUNTRY") or "XX").upper()

agents_dir = home / ".openclaw" / "agents"
totals = {}

if agents_dir.exists():
    for agent in agents_dir.iterdir():
        sessions = agent / "sessions"
        if not sessions.exists():
            continue
        for file in sessions.glob("*.jsonl"):
            try:
                with file.open("r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                        except Exception:
                            continue
                        msg = obj.get("message") if isinstance(obj, dict) else None
                        if not isinstance(msg, dict) and isinstance(obj, dict):
                            data = obj.get("data")
                            if isinstance(data, dict):
                                msg = data.get("message")
                        if not isinstance(msg, dict):
                            continue
                        if msg.get("role") != "assistant":
                            continue
                        usage = usage_totals(msg.get("usage"))
                        if not usage:
                            continue
                        model = msg.get("model") or msg.get("modelId") or "unknown"
                        rec = totals.setdefault(model, {"tokens": 0, "input": 0, "output": 0})
                        rec["tokens"] += usage["tokens"]
                        rec["input"] += usage["input"]
                        rec["output"] += usage["output"]
            except Exception:
                continue

prev = {"models": {}}
if state_file.exists():
    try:
        prev = json.loads(state_file.read_text(encoding="utf-8"))
    except Exception:
        prev = {"models": {}}

prev_models = prev.get("models", {}) if isinstance(prev, dict) else {}
payloads = []
for model, cur in totals.items():
    p = prev_models.get(model, {})
    dt = int(cur.get("tokens", 0)) - int(p.get("tokens", 0))
    di = int(cur.get("input", 0)) - int(p.get("input", 0))
    do = int(cur.get("output", 0)) - int(p.get("output", 0))
    if dt > 0 or di > 0 or do > 0:
        payloads.append({
            "gateway_id": gateway_id,
            "agent_name": agent_name,
            "country": country,
            "tokens_delta": dt if dt > 0 else max(0, di + do),
            "tokens_in_delta": max(0, di),
            "tokens_out_delta": max(0, do),
            "model": model,
        })

state_file.parent.mkdir(parents=True, exist_ok=True)
state_file.write_text(json.dumps({"models": totals}, separators=(",", ":")), encoding="utf-8")

print(json.dumps(payloads))
PY
)"

if [ "$PAYLOADS" = "[]" ]; then
  echo "ranking-of-claws: no new token deltas."
  exit 0
fi

python3 - "$PAYLOADS" "$API_URL" <<'PY'
import json
import subprocess
import sys

payloads = json.loads(sys.argv[1])
api_url = sys.argv[2]

for body in payloads:
    p = subprocess.run(
        [
            "curl", "-sf", "-X", "POST", api_url,
            "-H", "Content-Type: application/json",
            "-d", json.dumps(body, separators=(",", ":")),
        ],
        capture_output=True,
        text=True,
    )
    if p.returncode == 0:
        print(f"reported {body['tokens_delta']} tokens model={body['model']}")
    else:
        print(f"failed model={body['model']} code={p.returncode}", file=sys.stderr)
PY
