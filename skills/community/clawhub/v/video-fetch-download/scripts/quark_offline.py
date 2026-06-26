#!/usr/bin/env python3
"""
夸克网盘离线下载
用法:
  python3 quark_offline.py <magnet_or_url>   # 添加离线任务
  python3 quark_offline.py --list            # 查看任务列表
  python3 quark_offline.py --login           # 显示登录说明

Cookie 配置:
  将夸克网盘 Cookie 写入 ~/.config/video-fetch/quark_cookie.txt
  Cookie 格式: __pus=xxx; __puus=xxx; ...
"""
import sys
import os
import json
import time
import requests

COOKIE_FILE = os.path.join(
    os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
    "video-fetch", "quark_cookie.txt"
)

BASE_URL = "https://drive-pc.quark.cn"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) quark-cloud-drive/3.14.2 Chrome/112.0.5615.165 "
    "Electron/24.1.3.8 Safari/537.36 Channel/pckk_other_ch"
)


def load_cookie():
    if not os.path.exists(COOKIE_FILE):
        print(f"[夸克] 未找到 Cookie 文件: {COOKIE_FILE}")
        print("请运行: python3 quark_offline.py --login 查看配置说明")
        sys.exit(1)
    with open(COOKIE_FILE) as f:
        cookie = f.read().strip()
    if not cookie:
        print(f"[夸克] Cookie 文件为空: {COOKIE_FILE}")
        sys.exit(1)
    return cookie


def get_session():
    cookie = load_cookie()
    s = requests.Session()
    s.headers.update({
        "User-Agent": USER_AGENT,
        "Cookie": cookie,
        "Content-Type": "application/json",
        "Referer": "https://pan.quark.cn/",
    })
    return s


def get_user_info():
    s = get_session()
    r = s.get(f"{BASE_URL}/1/clouddrive/config",
              params={"pr": "ucpro", "fr": "pc", "uc_param_str": ""})
    r.raise_for_status()
    data = r.json()
    if data.get("code") == 0:
        return data.get("data", {})
    return None


def offline_add(url, save_fid="0"):
    s = get_session()
    # 1. 获取任务ID
    payload = {
        "fid": save_fid,
        "fetch_url": url,
        "scene": "manual",
        "uc_param_str": ""
    }
    r = s.post(
        f"{BASE_URL}/1/clouddrive/task",
        params={"pr": "ucpro", "fr": "pc"},
        json=payload
    )
    r.raise_for_status()
    result = r.json()
    if result.get("code") != 0:
        # 尝试离线下载接口
        payload2 = {
            "fid": save_fid,
            "url": url,
        }
        r2 = s.post(
            f"{BASE_URL}/1/clouddrive/offline/download",
            params={"pr": "ucpro", "fr": "pc"},
            json=payload2
        )
        r2.raise_for_status()
        result = r2.json()

    if result.get("code") == 0:
        task_id = result.get("data", {}).get("task_id", "")
        print(f"[夸克离线] 添加成功 ✓")
        print(f"  任务ID: {task_id}")
        print(f"  响应: {result.get('message', 'ok')}")
    else:
        print(f"[夸克离线] 添加失败: code={result.get('code')} msg={result.get('message')}")
        print(f"  完整响应: {result}")
        sys.exit(1)


def offline_list():
    s = get_session()
    r = s.get(
        f"{BASE_URL}/1/clouddrive/offline/download",
        params={"pr": "ucpro", "fr": "pc", "page": 1, "size": 20}
    )
    r.raise_for_status()
    result = r.json()
    if result.get("code") != 0:
        print(f"[夸克离线] 获取列表失败: {result}")
        sys.exit(1)
    tasks = result.get("data", {}).get("task_list", [])
    status_map = {0: "等待", 1: "下载中", 2: "完成", 3: "失败"}
    print(f"[夸克离线] 共 {len(tasks)} 个任务:")
    for t in tasks:
        status = status_map.get(t.get("status", 0), "未知")
        name = t.get("file_name", t.get("url", ""))[:45]
        pct = t.get("percent", 0)
        print(f"  [{status}] {name} - {pct}%")


def show_login_help():
    print("""
[夸克网盘 Cookie 获取方法]

1. 浏览器打开 https://pan.quark.cn 并登录
2. 按 F12 打开开发者工具
3. 切换到 Network 标签，刷新页面
4. 找任意一个 quark.cn 的请求，点击查看 Request Headers
5. 复制 Cookie 字段的完整内容
6. 保存到文件:

mkdir -p ~/.config/video-fetch
echo '<粘贴Cookie内容>' > ~/.config/video-fetch/quark_cookie.txt

注意: Cookie 有效期通常较长，失效后重新获取即可。
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 quark_offline.py <magnet_or_url>")
        print("      python3 quark_offline.py --list")
        print("      python3 quark_offline.py --login")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "--list":
        offline_list()
    elif cmd == "--login":
        show_login_help()
    else:
        fid = sys.argv[2] if len(sys.argv) > 2 else "0"
        offline_add(cmd, fid)
