#!/usr/bin/env python3
"""即梦AI 任务查询"""
import sys, os, time, base64, argparse, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _jimeng import call_api, get_credentials

def query_task(task_id, req_key="jimeng_t2i_v40"):
    access_key, secret_key = get_credentials()
    if not access_key:
        print("Error: No credentials found. Add jimeng key first.")
        sys.exit(1)

    result = call_api("JimengT2IV40GetResult", {
        "req_key": req_key,
        "task_id": task_id
    }, access_key, secret_key)

    return result

def main():
    parser = argparse.ArgumentParser(description="即梦AI 任务查询")
    parser.add_argument("task_id", help="任务ID")
    parser.add_argument("req_key", nargs="?", default="jimeng_t2i_v40", help="req_key (默认 jimeng_t2i_v40)")
    parser.add_argument("--wait", action="store_true", help="等待完成")
    parser.add_argument("--interval", type=int, default=3, help="轮询间隔(秒)")
    args = parser.parse_args()

    if args.wait:
        print(f"Waiting for task {args.task_id} to complete... (Ctrl+C to stop)")
        for i in range(60):  # max 3 min
            result = query_task(args.task_id, args.req_key)
            status = result.get("Result", {}).get("data", {}).get("status", "unknown")
            print(f"[{i+1}] Status: {status}")
            if status == "done":
                data = result["Result"]["data"]
                if data.get("image_urls"):
                    print("\nImage URLs:")
                    for url in data["image_urls"]:
                        print(f"  {url}")
                if data.get("video_url"):
                    print(f"\nVideo URL: {data['video_url']}")
                if data.get("binary_data_base64"):
                    b64_list = data["binary_data_base64"]
                    print(f"\nBase64 images: {len(b64_list)}")
                    # Save first image
                    if b64_list and args.req_key.startswith("jimeng_t2i"):
                        img_data = base64.b64decode(b64_list[0])
                        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output.png")
                        with open(out_path, "wb") as f:
                            f.write(img_data)
                        print(f"Image saved to: {out_path}")
                return
            elif status == "failed":
                print(f"\nTask failed: {result}")
                return
            time.sleep(args.interval)
        print("Timeout waiting for task")
    else:
        result = query_task(args.task_id, args.req_key)
        status = result.get("Result", {}).get("data", {}).get("status", "unknown")
        print(f"Status: {status}")
        if status == "done":
            data = result["Result"]["data"]
            if data.get("image_urls"):
                print("\nImage URLs:")
                for url in data["image_urls"]:
                    print(f"  {url}")
            if data.get("video_url"):
                print(f"\nVideo URL: {data['video_url']}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
