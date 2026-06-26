#!/usr/bin/env python3
"""ZeeLin 调研任务封装 - 创建任务并启动监控子代理"""
import os, sys, json, requests, subprocess
from pathlib import Path

# 配置文件路径（脚本在 scripts/ 下，config.json 在 skill/ 下）
SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = SCRIPT_DIR.parent / "config.json"
WATCH_SCRIPT = SCRIPT_DIR / "zeelin_watch.py"

def load_config():
    """从配置文件读取配置"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

def save_config(config):
    """保存配置到文件"""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def ensure_target_config():
    """确保配置中有 target_user 和 channel，如果没有则尝试从环境变量获取并保存"""
    config = load_config()
    
    # 检查是否需要更新
    needs_save = False
    
    # 尝试从环境变量获取
    target_user = os.environ.get("ZEELIN_TARGET_USER", "")
    channel = os.environ.get("ZEELIN_CHANNEL", "")
    
    if target_user and not config.get("target_user"):
        config["target_user"] = target_user
        needs_save = True
        print(f"自动配置 target_user: {target_user}")
    
    if channel and not config.get("channel"):
        config["channel"] = channel
        needs_save = True
        print(f"自动配置 channel: {channel}")
    
    if needs_save:
        save_config(config)
        print(f"配置已保存到 {CONFIG_FILE}")
    
    return config

def load_api_key():
    """从配置文件读取 API Key"""
    config = load_config()
    key = config.get("api_key", "").strip()
    if key:
        return key
    print(f"ERROR: API Key not found in {CONFIG_FILE}")
    print("获取 API Key: https://skills.zeelin.cn/console/apps")
    sys.exit(1)

API_KEY = load_api_key()
CONTENT = sys.argv[1] if len(sys.argv) > 1 else "测试调研"
THINKING = sys.argv[2] if len(sys.argv) > 2 else "deep"  # 默认 deep

# 确保配置中有 target_user 和 channel（首次使用时自动配置）
ensure_target_config()

# 创建任务
resp = requests.post(
    "https://desearch.zeelin.cn/api/conversation/anew",
    json={
        "content": CONTENT, 
        "thinking": THINKING,
        "workflow": "",
        "needEditChapter": 0,
        "moreSettings": {}
    },
    headers={"x-skill-key": API_KEY}
)

data = resp.json()
if data.get("code") != 200:
    print(f"ERROR: {data}")
    sys.exit(1)

session_id = data.get("data", {}).get("sessionId")
title = data.get("data", {}).get("title", CONTENT)

if not session_id:
    print(f"ERROR: Failed to create task: {data}")
    sys.exit(1)

print(f"CREATED: session_id={session_id}")
print(f"TITLE: {title}")

# 启动子代理监控
# 方式1: 后台运行（环境变量问题，可能失效）
# 方式2: 直接运行（会阻塞，但能在子代理中正确发送消息）

# 检查是否是交互式调用
log_file = f"/tmp/zeelin_watch_{session_id}.log"

if sys.stdout.isatty():
    # 交互式，后台运行
    env = os.environ.copy()
    env["ZEELIN_SESSION_ID"] = session_id
    env["ZEELIN_CONTENT"] = title
    
    import subprocess
    with open(log_file, "w") as f:
        subprocess.Popen(
            ["nohup", "python3", "-u", str(WATCH_SCRIPT)],
            env=env,
            stdout=f,
            stderr=subprocess.STDOUT
        )
    print(f"SPAWNED: watching in background")
    print(f"LOG: {log_file}")
else:
    # 非交互式（如子代理调用），直接运行并等待完成
    env = os.environ.copy()
    env["ZEELIN_SESSION_ID"] = session_id
    env["ZEELIN_CONTENT"] = title
    
    import subprocess
    subprocess.run(
        ["python3", "-u", str(WATCH_SCRIPT)],
        env=env
    )
    print(f"COMPLETED: task finished")
