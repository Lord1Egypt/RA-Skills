from __future__ import annotations

import argparse
import json

from utils import json_fail


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action_value", required=True)
    args = parser.parse_args()

    value = args.action_value.strip()
    if value.startswith("confirm_incremental:"):
        task_id = value.split(":", 1)[1]
        out({
            "success": True,
            "action": "confirm_incremental",
            "command": "confirm_incremental.py",
            "args": {"task_id": task_id},
        })
        return
    if value.startswith("cancel_incremental:"):
        task_id = value.split(":", 1)[1]
        out({
            "success": True,
            "action": "cancel_incremental",
            "command": "cancel_incremental.py",
            "args": {"task_id": task_id},
        })
        return
    out(json_fail("unknown_card_action", "无法识别 scan_updates 卡片动作。"))


if __name__ == "__main__":
    main()
