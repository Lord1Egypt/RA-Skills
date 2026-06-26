#!/usr/bin/env python3
"""即梦AI 文生视频"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _jimeng import call_api, get_credentials

def main():
    parser = argparse.ArgumentParser(description="即梦AI 文生视频")
    parser.add_argument("prompt", help="视频描述")
    parser.add_argument("--duration", type=int, default=5, help="视频时长(秒): 5-10")
    parser.add_argument("--seed", type=int, default=-1, help="随机种子 (-1随机)")
    args = parser.parse_args()

    access_key, secret_key = get_credentials()
    if not access_key:
        print("Error: No credentials found. Add jimeng key first.")
        sys.exit(1)

    body = {
        "req_key": "jimeng_i2v_first_v30_1080",
        "prompt": args.prompt,
        "duration": args.duration,
        "seed": args.seed
    }

    print(f"Generating video...")
    print(f"Prompt: {args.prompt}")
    result = call_api("JimengTI2VV301080SubmitTask", body, access_key, secret_key)

    if result.get("Result", {}).get("code") == 10000:
        task_id = result["Result"]["data"]["task_id"]
        print(f"\nTask submitted successfully!")
        print(f"Task ID: {task_id}")
        print(f"\nQuery with: python query.py {task_id} jimeng_i2v_first_v30_1080")
        return task_id
    else:
        print(f"\nError: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()
