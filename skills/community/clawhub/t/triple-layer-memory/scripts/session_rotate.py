"""
session_rotate.py — Session 轮换触发器（兼容版）

目标：
1) 支持默认 OpenClaw（无 Mem0 / 无文件记忆）
2) 支持按上下文占用率触发（默认 80%）
3) 支持冷却去重，避免重复触发

输出协议：
- [ROTATE_NEEDED]
- [NEW_SESSION] 上下文达到80%，自动切换新会话
- [HANDOFF_HINT] ...
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_THRESHOLD_RATIO = 0.8
DEFAULT_COOLDOWN_MINUTES = 180


def load_state(state_file: Path) -> dict:
    if not state_file.exists():
        return {}
    try:
        return json.loads(state_file.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state_file: Path, state: dict) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def should_rotate(
    *,
    used_tokens: int,
    max_tokens: int,
    channel: str,
    threshold_ratio: float,
    cooldown_minutes: int,
    state_file: Path,
) -> tuple[bool, str, float]:
    if max_tokens <= 0:
        return False, "invalid_max_tokens", 0.0

    ratio = used_tokens / max_tokens
    if ratio < threshold_ratio:
        return False, f"ratio={ratio:.3f} < {threshold_ratio:.3f}", ratio

    state = load_state(state_file)
    last_trigger = state.get("lastSessionRotateTrigger")
    last_channel = state.get("lastSessionRotateChannel")

    if last_trigger and last_channel == channel:
        try:
            last_dt = datetime.fromisoformat(last_trigger)
            if datetime.now() - last_dt < timedelta(minutes=cooldown_minutes):
                return False, "cooldown", ratio
        except Exception:
            pass

    state["lastSessionRotateTrigger"] = datetime.now().isoformat()
    state["lastSessionRotateChannel"] = channel
    state["lastSessionRotateRatio"] = round(ratio, 4)
    save_state(state_file, state)
    return True, "threshold_reached", ratio


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Session rotate trigger by context ratio")
    parser.add_argument("used_tokens", type=int, help="Current used context tokens")
    parser.add_argument("max_tokens", type=int, help="Current max context tokens")
    parser.add_argument("channel", nargs="?", default="boss", help="Channel name")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD_RATIO, help="Rotate threshold ratio")
    parser.add_argument("--cooldown", type=int, default=DEFAULT_COOLDOWN_MINUTES, help="Cooldown minutes")
    parser.add_argument("--state-file", type=str, default="memory/heartbeat-state.json", help="State file path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    state_file = Path(args.state_file).expanduser().resolve()

    ok, reason, ratio = should_rotate(
        used_tokens=args.used_tokens,
        max_tokens=args.max_tokens,
        channel=args.channel,
        threshold_ratio=args.threshold,
        cooldown_minutes=args.cooldown,
        state_file=state_file,
    )

    if not ok:
        print(f"[ROTATE_NOT_NEEDED] {reason}")
        return

    print("[ROTATE_NEEDED]")
    print("[NEW_SESSION] 上下文达到80%，自动切换新会话")
    print(
        "[HANDOFF_HINT] 请在旧会话保留交接摘要（任务进度/关键决策/待办），"
        "新会话第一条消息粘贴该摘要。"
    )
    print(f"[ROTATE_RATIO] {ratio:.3f}")


if __name__ == "__main__":
    main()
