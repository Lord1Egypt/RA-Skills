#!/usr/bin/env python3
"""
poll_task.py — 轮询任务直到完成或失败
用法: python poll_task.py <task_id> [timeout_seconds]

状态流转: PENDING → TEXT_SUCCESS → FIRST_SUCCESS → SUCCESS
终止状态: SUCCESS / FIRST_SUCCESS / CREATE_TASK_FAILED / GENERATE_AUDIO_FAILED /
          CALLBACK_EXCEPTION / SENSITIVE_WORD_ERROR
"""
import os, sys, json, time, requests

API_KEY = os.environ.get("KIEAI_API_KEY")
if not API_KEY:
    print("错误: 请设置 KIEAI_API_KEY 环境变量", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://api.kie.ai"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

task_id = sys.argv[1] if len(sys.argv) > 1 else None
if not task_id:
    print("用法: python poll_task.py <task_id> [timeout_seconds]", file=sys.stderr)
    sys.exit(1)

timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 300
interval = 15

print(f"[轮询开始] task_id={task_id}", file=sys.stderr)

end_time = time.time() + timeout
while time.time() < end_time:
    resp = requests.get(
        f"{BASE_URL}/api/v1/generate/record-info?taskId={task_id}",
        headers=HEADERS, timeout=20, verify=True
    )
    data = resp.json()
    if data.get("code") != 200:
        print(f"[查询失败] {data}", file=sys.stderr)
        break
    result = data["data"]
    status = result.get("status")
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] 状态: {status}", file=sys.stderr)

    if status in ("SUCCESS", "FIRST_SUCCESS"):
        suno_data = (result.get("response") or {}).get("sunoData") or []
        for item in suno_data:
            print(f"歌曲: {item.get('title')}")
            print(f"音频: {item.get('audioUrl')}")
        output = {
            "success": True,
            "task_id": task_id,
            "status": status,
            "songs": [{"title": item.get("title"), "audioUrl": item.get("audioUrl")} for item in suno_data]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        break

    if status in ("CREATE_TASK_FAILED", "GENERATE_AUDIO_FAILED", "CALLBACK_EXCEPTION", "SENSITIVE_WORD_ERROR"):
        error = result.get("errorMessage") or status
        print(f"[失败] {status}: {error}", file=sys.stderr)
        print(json.dumps({"success": False, "error": f"{status}: {error}"}))
        break

    time.sleep(interval)
else:
    msg = f"任务 {task_id} 超过 {timeout}s 未完成"
    print(f"[超时] {msg}", file=sys.stderr)
    print(json.dumps({"success": False, "error": msg}))
