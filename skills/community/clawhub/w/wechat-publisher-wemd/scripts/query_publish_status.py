#!/usr/bin/env python3
import argparse
import json
import sys
from wechat_client import query_publish_status


def main() -> int:
    parser = argparse.ArgumentParser(description="Query WeChat publish status/result.")
    parser.add_argument("--publish-id", required=True, help="Publish task/job identifier")
    args = parser.parse_args()

    try:
        result = query_publish_status(args.publish_id)
        json.dump({
            "ok": True,
            "step": "query_publish_status",
            "publish_id": args.publish_id,
            "result": result,
        }, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except Exception as e:
        json.dump({
            "ok": False,
            "step": "query_publish_status",
            "publish_id": args.publish_id,
            "message": str(e),
        }, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
