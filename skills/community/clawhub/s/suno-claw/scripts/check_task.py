#!/usr/bin/env python3
"""
check_task.py — 查询单个任务状态
用法: python check_task.py <task_id>
"""
import os, sys, json, requests

API_KEY = os.environ.get("KIEAI_API_KEY")
if not API_KEY:
    print("错误: 请设置 KIEAI_API_KEY 环境变量", file=sys.stderr)
    sys.exit(1)

task_id = sys.argv[1] if len(sys.argv) > 1 else None
if not task_id:
    print("用法: python check_task.py <task_id>", file=sys.stderr)
    sys.exit(1)

resp = requests.get(
    f"https://api.kie.ai/api/v1/generate/record-info?taskId={task_id}",
    headers={"Authorization": f"Bearer {API_KEY}"},
    timeout=20,
    verify=True
)
data = resp.json()
print("code:", data.get("code"))
result = data.get("data", {})
print("status:", result.get("status"))
suno_data = (result.get("response") or {}).get("sunoData") or []
for i, item in enumerate(suno_data):
    print(f"歌曲{i+1}: title={item.get('title')}")
    print(f"  audioUrl={item.get('audioUrl')}")
    print(f"  videoUrl={item.get('videoUrl')}")
