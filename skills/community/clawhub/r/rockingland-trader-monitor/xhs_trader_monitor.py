#!/usr/bin/env python3
"""
小红书用户帖子关键词监测
每天检查指定用户的最新帖子，标题含关键词时微信推送提醒。

使用前请按 SKILL.md 配置说明填入你自己的信息。
MCP 生命周期由脚本自己管理（启动→监测→关闭）。
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ==========================
# ⚠️ 用户配置区 — 使用前必须修改
# ==========================

# 1. 微信推送目标 ID（openclaw-weixin 通道）
#    获取方式：openclaw message list-accounts --channel openclaw-weixin
TARGET_ID = "YOUR_WECHAT_ID@im.wechat"

# 2. 小红书目标用户 ID（从用户主页 URL 或分享链接中获取）
USER_ID = "YOUR_XHS_USER_ID"

# 3. xsec_token（从用户主页任意帖子的 feed 数据中获取 xsecToken）
USER_XSEC = "YOUR_XSEC_TOKEN"

# 4. 监测关键词列表（帖子标题含任一关键词即触发推送）
KEYWORDS = ["棱镜球", "炫彩蛋", "同乘蛋", "祝福项坠"]

# ==========================
# 以下为通用逻辑，通常无需修改
# ==========================

# 脚本目录（skill 的 scripts/ 目录）
SCRIPT_DIR = Path(__file__).parent.resolve()

# 状态文件（记录已通知的帖子 ID，避免重复推送）
STATE_FILE = Path("xhs_trader_state.json")

# 日志文件
MCP_LOG = Path("xhs_trader.log")


def log(msg):
    print(msg)
    try:
        MCP_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(MCP_LOG, 'a', encoding='utf-8') as f:
            ts = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


def start_mcp():
    """启动 MCP 服务"""
    env = os.environ.copy()
    env['PATH'] = '/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
    env['MCP_URL'] = 'http://localhost:18060/mcp'
    
    # 先确保停止旧的
    stop_mcp()
    time.sleep(2)
    
    # 启动
    proc = subprocess.Popen(
        [str(SCRIPT_DIR / "start-mcp.sh"), "--headless=true"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
        cwd=str(SCRIPT_DIR)
    )
    
    # 等待服务就绪
    for _ in range(30):
        try:
            result = subprocess.run(
                ["curl", "--noproxy", "*", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                 "-X", "POST", "http://localhost:18060/mcp",
                 "-H", "Content-Type: application/json",
                 "-d", '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"healthcheck","version":"1.0"}}}'],
                capture_output=True, text=True, timeout=5
            )
            if result.stdout.strip() == "200":
                log("  ✅ MCP 服务已就绪")
                return True
        except:
            pass
        time.sleep(1)
    
    log("  ❌ MCP 服务启动超时")
    return False


def stop_mcp():
    """停止 MCP 服务"""
    env = os.environ.copy()
    env['PATH'] = '/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
    subprocess.run(
        [str(SCRIPT_DIR / "stop-mcp.sh")],
        capture_output=True, timeout=30,
        env=env, cwd=str(SCRIPT_DIR)
    )


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"notified_ids": [], "last_check": None}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE) if os.path.dirname(STATE_FILE) else ".", exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def mcp_call(tool, args_dict):
    try:
        env = os.environ.copy()
        env['PATH'] = '/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
        env['MCP_URL'] = 'http://localhost:18060/mcp'
        
        args_json = json.dumps(args_dict, ensure_ascii=False)
        
        result = subprocess.run(
            [str(SCRIPT_DIR / "mcp-call.sh"), tool, args_json],
            capture_output=True, text=True, timeout=60, env=env,
            cwd=str(SCRIPT_DIR)
        )
        
        if result.returncode != 0:
            log(f"  MCP调用错误: {result.stderr[:200]}")
            return None
        
        return json.loads(result.stdout)
    except Exception as e:
        log(f"  MCP调用失败: {e}")
        return None


def get_user_latest_feeds():
    result = mcp_call("user_profile", {
        "user_id": USER_ID,
        "xsec_token": USER_XSEC
    })
    
    if not result or "result" not in result:
        return []
    
    content = result["result"].get("content", [])
    if not content:
        return []
    
    text_content = content[0].get("text", "")
    try:
        data = json.loads(text_content)
    except:
        return []
    
    return data.get("feeds", [])


def check_keywords_in_feed(feed):
    title = feed.get("noteCard", {}).get("displayTitle", "")
    matched = []
    for kw in KEYWORDS:
        if kw in title:
            matched.append(kw)
    return matched, title


def send_weixin(message):
    try:
        env = os.environ.copy()
        env['HOME'] = str(Path.home())
        env['PATH'] = '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
        
        cmd = [
            "openclaw", "message", "send",
            "--channel", "openclaw-weixin",
            "--target", TARGET_ID,
            "--message", message
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=env)
        return result.returncode == 0 or "✅ Sent" in result.stderr
    except Exception as e:
        log(f"  微信推送失败: {e}")
        return False


def main():
    now = datetime.now(timezone(timedelta(hours=8)))
    log(f"🔍 [{now.strftime('%H:%M')}] 检查目标用户更新...")
    
    # 1. 启动 MCP
    if not start_mcp():
        log("  ❌ MCP 启动失败，本次跳过")
        stop_mcp()
        sys.exit(1)
    
    try:
        # 2. 获取帖子
        state = load_state()
        feeds = get_user_latest_feeds()
        
        if not feeds:
            log("  ❌ 无法获取帖子列表")
            return
        
        # 3. 检查最新帖子
        today_str = now.strftime("%m.%d")
        found = False
        
        for feed in feeds[:5]:
            feed_id = feed.get("id", "")
            title = feed.get("noteCard", {}).get("displayTitle", "")
            
            if not title.startswith(today_str):
                continue
            
            matched, title = check_keywords_in_feed(feed)
            
            if matched:
                if feed_id in state["notified_ids"]:
                    log(f"  ⏭️ 已通知过: {title}")
                    continue
                
                msg = f"🎯 上新提醒！\n\n{title}\n\n检测到关键词：{'、'.join(matched)}\n\n快去查看 👀"
                
                log(f"  🚨 发现关键词！{matched}")
                if send_weixin(msg):
                    log("  ✅ 微信推送成功")
                    state["notified_ids"].append(feed_id)
                    found = True
                else:
                    log("  ❌ 微信推送失败")
        
        state["last_check"] = now.isoformat()
        save_state(state)
        
        if not found:
            log("  ✅ 本轮无目标商品")
    
    finally:
        # 4. 无论如何都关闭 MCP
        stop_mcp()
        log("  🧹 MCP 已关闭")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"错误: {e}")
        import traceback
        traceback.print_exc()
        # 确保 MCP 关闭
        stop_mcp()
        sys.exit(1)
