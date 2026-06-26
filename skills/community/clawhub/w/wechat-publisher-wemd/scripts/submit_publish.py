#!/usr/bin/env python3
import argparse
import json
import sys
from wechat_client import WeChatSkillError, submit_publish


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit a confirmed WeChat draft for publish.")
    parser.add_argument("--draft-id", required=True, help="Draft/media identifier")
    parser.add_argument("--confirmed", action="store_true", help="Require explicit confirmation flag")
    args = parser.parse_args()

    try:
        if not args.confirmed:
            raise WeChatSkillError("Refusing publish without --confirmed")
        result = submit_publish(args.draft_id)
        json.dump({
            "ok": True,
            "step": "submit_publish",
            "draft_id": args.draft_id,
            "publish_id": result.get("publish_id"),
            "result": result,
        }, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except Exception as e:
        json.dump({
            "ok": False,
            "step": "submit_publish",
            "draft_id": args.draft_id,
            "message": str(e),
        }, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
