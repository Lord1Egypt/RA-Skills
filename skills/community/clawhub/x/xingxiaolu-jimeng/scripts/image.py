#!/usr/bin/env python3
"""即梦AI 文生图"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _jimeng import call_api, get_credentials

def main():
    parser = argparse.ArgumentParser(description="即梦AI 文生图")
    parser.add_argument("prompt", help="图像描述")
    parser.add_argument("--aspect", default="1:1", help="宽高比: 1:1, 3:4, 4:3, 16:9, 9:16 (默认 1:1)")
    parser.add_argument("--seed", type=int, default=-1, help="随机种子 (-1随机)")
    args = parser.parse_args()

    access_key, secret_key = get_credentials()
    if not access_key:
        print("Error: No credentials found. Add jimeng key first.")
        sys.exit(1)

    body = {
        "req_key": "jimeng_t2i_v40",
        "prompt": args.prompt,
        "aspect_ratio": args.aspect,
        "seed": args.seed
    }

    print(f"Generating image...")
    print(f"Prompt: {args.prompt}")
    result = call_api("JimengT2IV40SubmitTask", body, access_key, secret_key)

    if result.get("Result", {}).get("code") == 10000:
        task_id = result["Result"]["data"]["task_id"]
        print(f"\nTask submitted successfully!")
        print(f"Task ID: {task_id}")
        print(f"\nQuery with: python query.py {task_id}")
        return task_id
    else:
        print(f"\nError: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()
