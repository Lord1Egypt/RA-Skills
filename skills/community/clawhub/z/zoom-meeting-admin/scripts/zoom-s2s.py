#!/usr/bin/env python3
"""
Zoom Server-to-Server OAuth REST API 调用脚本 (纯 Python，无外部依赖)
"""

import json
import os
import sys
import base64
import time
import urllib.request
import urllib.parse
import urllib.error
import argparse
from datetime import datetime, timezone

# =============================================================================
# 配置
# =============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(SCRIPT_DIR, "..", ".env")
TOKEN_CACHE = os.path.expanduser("~/.zoom-s2s-token.json")

ZOOM_ACCOUNT_ID = ""
ZOOM_CLIENT_ID = ""
ZOOM_CLIENT_SECRET = ""
ZOOM_USER_ID = ""

# =============================================================================
# .env 加载
# =============================================================================
def load_env():
    global ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, ZOOM_USER_ID
    if not os.path.exists(ENV_FILE):
        print(f"❌ .env 文件不存在: {ENV_FILE}", file=sys.stderr)
        sys.exit(1)
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                val = val.strip().strip('"').strip("'")
                if key == "ZOOM_ACCOUNT_ID":
                    ZOOM_ACCOUNT_ID = val
                elif key == "ZOOM_CLIENT_ID":
                    ZOOM_CLIENT_ID = val
                elif key == "ZOOM_CLIENT_SECRET":
                    ZOOM_CLIENT_SECRET = val
                elif key == "ZOOM_USER_ID":
                    ZOOM_USER_ID = val

# =============================================================================
# Token 管理
# =============================================================================
def get_token():
    cached_token = ""
    cached_expiry = 0

    if os.path.exists(TOKEN_CACHE):
        try:
            with open(TOKEN_CACHE) as f:
                d = json.load(f)
                cached_token = d.get("access_token", "")
                cached_expiry = d.get("expiry", 0)
        except Exception:
            pass

    # 检查缓存是否有效（提前5分钟过期）
    if cached_token and cached_expiry > (time.time() + 300):
        return cached_token

    # 获取新 Token
    creds = base64.b64encode(f"{ZOOM_CLIENT_ID}:{ZOOM_CLIENT_SECRET}".encode()).decode()
    url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={ZOOM_ACCOUNT_ID}"

    req = urllib.request.Request(url, data=b"", method="POST")
    req.add_header("Authorization", f"Basic {creds}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(f"❌ Token 获取失败 ({e.code}): {err}", file=sys.stderr)
        sys.exit(1)

    access_token = result.get("access_token", "")
    expires_in = result.get("expires_in", 3600)

    if not access_token:
        print("❌ Token 响应中无 access_token", file=sys.stderr)
        sys.exit(1)

    # 缓存，并收紧文件权限（仅当前用户可读写）
    with open(TOKEN_CACHE, "w") as f:
        json.dump({"access_token": access_token, "expiry": time.time() + expires_in - 300}, f)
    os.chmod(TOKEN_CACHE, 0o600)

    return access_token

# =============================================================================
# API 调用
# =============================================================================
def api_call(method, path, data=None):
    token = get_token()
    url = f"https://api.zoom.us/v2{path}"

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status == 204:
                return {"message": "OK (no content)"}
            result = json.loads(resp.read())
            return result
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        try:
            err_json = json.loads(err_body)
            return {"error": err_json}
        except Exception:
            return {"error": err_body}

# =============================================================================
# Actions
# =============================================================================

def list_meetings(user=None, page_size=10, meeting_type="upcoming"):
    user = user or ZOOM_USER_ID
    result = api_call("GET", f"/users/{urllib.parse.quote(user)}/meetings?page_size={page_size}&type={meeting_type}")
    return result

def get_meeting(meeting_id):
    return api_call("GET", f"/meetings/{meeting_id}")

def create_meeting(topic, start_time, duration=60, timezone="Asia/Shanghai", password=None,
                    recurrence_type=None, repeat_interval=1, weekly_days=None, end_times=None,
                    end_date_time=None, monthly_day=None, monthly_weeks=None):
    user = ZOOM_USER_ID
    payload = {
        "topic": topic,
        "type": 8 if recurrence_type else 2,
        "start_time": start_time,
        "duration": duration,
        "timezone": timezone,
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": False,
            "mute_upon_entry": False
        }
    }
    if password:
        payload["password"] = password
    if recurrence_type:
        rec = {"type": recurrence_type, "repeat_interval": repeat_interval}
        # type=1 (daily): 用 end_date_time / end_times 即可
        # type=2 (weekly): 必须给 weekly_days 字符串
        if recurrence_type == 2 and weekly_days is not None:
            rec["weekly_days"] = str(weekly_days)
        # type=3 (monthly): 二选一
        #   - monthly_day: 每月第几天（1-31，逗号分隔字符串，如 "15" 或 "1,15"）
        #   - monthly_weeks: 每月第几个周次（-1=最后, 1-4），配合 weekly_days
        if recurrence_type == 3:
            if monthly_day is not None:
                rec["monthly_day"] = str(monthly_day)
            elif monthly_weeks is not None:
                rec["monthly_weeks"] = int(monthly_weeks)
                if weekly_days is not None:
                    rec["weekly_days"] = str(weekly_days)
        if end_times is not None:
            rec["end_times"] = int(end_times)
        if end_date_time:
            rec["end_date_time"] = end_date_time
        payload["recurrence"] = rec
    return api_call("POST", f"/users/{urllib.parse.quote(user)}/meetings", payload)

def delete_meeting(meeting_id):
    return api_call("DELETE", f"/meetings/{meeting_id}")

def get_user(user=None):
    user = user or ZOOM_USER_ID
    return api_call("GET", f"/users/{urllib.parse.quote(user)}")

def list_users(page_size=30):
    return api_call("GET", f"/users?page_size={page_size}")

def list_recordings(user=None, page_size=10):
    user = user or ZOOM_USER_ID
    return api_call("GET", f"/users/{urllib.parse.quote(user)}/recordings?page_size={page_size}")

def help():
    print("""
用法: zoom-s2s.py <action> [参数...]

可用 Action:
  list_meetings   [user] [page_size] [type]     列出会议 (type: upcoming/past/live)
  get_meeting     <meeting_id>                  获取单个会议详情
  create_meeting  <topic> <start_time> <duration> [timezone] [password]
                  [recurrence_type] [repeat_interval] [weekly_days] [end_times] [end_date_time]
                  [monthly_day] [monthly_weeks]
                                                  创建会议 (start_time: YYYY-MM-DDTHH:MM:SS)
                                                  支持周期性会议：
                                                    recurrence_type=1 每日
                                                    recurrence_type=2 每周，weekly_days Zoom 编码："1"=周日 "2"=周一 ... "7"=周六（如 "2" 周一 或 "3,5" 周二+周四）
                                                    recurrence_type=3 每月，每月几号 monthly_day="1-31"（如 "15" 或 "1,15"）
                                                                    或 每月第几个周次 monthly_weeks=-1..4 + weekly_days
  delete_meeting  <meeting_id> --yes              删除会议（需 --yes 确认）
  get_user        [user_id]                     获取用户信息
  list_users      [page_size]                   列出账户下所有用户
  recordings      [user_id] [page_size]         获取云录像
  help                                            显示本帮助

示例:
  # 列出即将到来的会议
  python3 zoom-s2s.py list_meetings service@uperform.cn 10 upcoming

  # 创建明天早上10点会议
  python3 zoom-s2s.py create_meeting "煎饼果子讨论会" "2026-05-05T10:00:00" 60 Asia/Shanghai

  # 创建周期性会议（每周一 20:00 EDT，7次，2小时；weekly_days="2" = Zoom 编码周一）
  python3 zoom-s2s.py create_meeting "北美龙虾 AI 数字员工系列第 2 期" "2026-08-18T20:00:00" 120 America/New_York "" 2 1 2 7

  # 创建月度会议（每月 15 号 10:00，共 12 次）
  python3 zoom-s2s.py create_meeting "月度复盘" "2026-08-15T10:00:00" 60 Asia/Shanghai "" 3 1 15 12

  # 创建月度会议（每月第 2 个周二 20:00，共 6 次）
  python3 zoom-s2s.py create_meeting "月度董事会" "2026-08-25T20:00:00" 60 America/New_York "" 3 1 2 6 "" "" 2

  # 获取云录像
  python3 zoom-s2s.py recordings service@uperform.cn 10
""")

# =============================================================================
# Main
# =============================================================================
def main():
    load_env()

    if len(sys.argv) < 2:
        help()
        sys.exit(0)

    action = sys.argv[1].lower()
    args = sys.argv[2:]

    if action == "list_meetings":
        user = args[0] if len(args) > 0 else ZOOM_USER_ID
        page_size = int(args[1]) if len(args) > 1 else 10
        meeting_type = args[2] if len(args) > 2 else "upcoming"
        result = list_meetings(user, page_size, meeting_type)

    elif action == "get_meeting":
        if len(args) < 1:
            print("❌ 需要 meeting_id", file=sys.stderr)
            sys.exit(1)
        result = get_meeting(args[0])

    elif action == "create_meeting":
        if len(args) < 2:
            print("❌ 需要 topic 和 start_time", file=sys.stderr)
            sys.exit(1)
        topic = args[0]
        start_time = args[1]
        duration = int(args[2]) if len(args) > 2 else 60
        timezone = args[3] if len(args) > 3 else "Asia/Shanghai"
        password = args[4] if len(args) > 4 else None
        recurrence_type = int(args[5]) if len(args) > 5 else None
        repeat_interval = int(args[6]) if len(args) > 6 else 1
        weekly_days = args[7] if len(args) > 7 else None
        end_times = int(args[8]) if len(args) > 8 else None
        end_date_time = args[9] if len(args) > 9 else None
        monthly_day = args[10] if len(args) > 10 else None
        monthly_weeks = int(args[11]) if len(args) > 11 else None
        result = create_meeting(topic, start_time, duration, timezone, password,
                               recurrence_type, repeat_interval, weekly_days, end_times,
                               end_date_time, monthly_day, monthly_weeks)

    elif action == "delete_meeting":
        if len(args) < 1:
            print("❌ 需要 meeting_id", file=sys.stderr)
            sys.exit(1)
        if "--yes" not in args:
            print(f"⚠️  即将删除会议 {args[0]}，此操作不可撤销。", file=sys.stderr)
            print(f"   请添加 --yes 参数以确认执行，例如：", file=sys.stderr)
            print(f"   python3 zoom-s2s.py delete_meeting {args[0]} --yes", file=sys.stderr)
            sys.exit(1)
        result = delete_meeting(args[0])

    elif action == "get_user":
        user = args[0] if len(args) > 0 else None
        result = get_user(user)

    elif action == "list_users":
        page_size = int(args[0]) if len(args) > 0 else 30
        result = list_users(page_size)

    elif action == "recordings":
        user = args[0] if len(args) > 0 else None
        page_size = int(args[1]) if len(args) > 1 else 10
        result = list_recordings(user, page_size)

    elif action in ("help", "--help", "-h"):
        help()
        sys.exit(0)

    else:
        print(f"❌ 未知 action: {action}", file=sys.stderr)
        help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()