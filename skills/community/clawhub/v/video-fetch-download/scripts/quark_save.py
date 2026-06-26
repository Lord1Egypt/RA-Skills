#!/usr/bin/env python3
"""
夸克网盘分享链接转存
用法:
  python3 quark_save.py <share_url> [save_path]     # 转存分享链接
  python3 quark_save.py --list                       # 列出根目录文件
  python3 quark_save.py --login                      # 查看Cookie配置说明

Cookie 配置:
  ~/.config/video-fetch/quark_cookie.txt

支持格式:
  https://pan.quark.cn/s/xxxxxxxx
  https://pan.quark.cn/s/xxxxxxxx?pwd=xxxx  (带提取码)
"""
import sys
import os
import re
import json
import time
import random
import requests

COOKIE_FILE = os.path.join(
    os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
    "video-fetch", "quark_cookie.txt"
)
BASE_URL = "https://drive-pc.quark.cn"
SAVE_URL = "https://drive.quark.cn"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/94.0.4606.71 Safari/537.36 Core/1.94.225.400 QQBrowser/12.2.5544.400"
)


def ts13():
    return int(time.time() * 1000)


def load_cookie():
    if not os.path.exists(COOKIE_FILE):
        print(f"[夸克] 未找到 Cookie，请先运行: python3 quark_login.py")
        sys.exit(1)
    return open(COOKIE_FILE).read().strip()


def get_session():
    cookie = load_cookie()
    s = requests.Session()
    s.headers.update({
        "User-Agent": USER_AGENT,
        "Cookie": cookie,
        "Content-Type": "application/json",
        "Referer": "https://pan.quark.cn/",
        "Origin": "https://pan.quark.cn",
        "Accept-Language": "zh-CN,zh;q=0.9",
    })
    return s


def base_params():
    return {
        "pr": "ucpro",
        "fr": "pc",
        "uc_param_str": "",
        "__dt": random.randint(100, 9999),
        "__t": ts13(),
    }


def extract_url(share_url):
    """从分享链接提取 pwd_id 和提取码"""
    pwd_id = share_url.split('?')[0].split('/s/')[-1].split('#')[0]
    match_pwd = re.search(r"pwd=([a-zA-Z0-9]+)", share_url)
    passcode = match_pwd.group(1) if match_pwd else ""
    if not pwd_id or '/' in pwd_id:
        print(f"[夸克转存] 无效的分享链接: {share_url}")
        sys.exit(1)
    return pwd_id, passcode


def get_stoken(s, pwd_id, passcode=""):
    params = base_params()
    r = s.post(
        f"{BASE_URL}/1/clouddrive/share/sharepage/token",
        params=params,
        json={"pwd_id": pwd_id, "passcode": passcode},
        timeout=15
    )
    data = r.json()
    if data.get("status") == 200 and data.get("data"):
        return data["data"]["stoken"]
    print(f"[夸克转存] 获取stoken失败: {data.get('message', data)}")
    sys.exit(1)


def get_detail(s, pwd_id, stoken, pdir_fid="0"):
    file_list = []
    page = 1
    while True:
        params = base_params()
        params.update({
            "pwd_id": pwd_id,
            "stoken": stoken,
            "pdir_fid": pdir_fid,
            "force": "0",
            "_page": str(page),
            "_size": "50",
            "_sort": "file_type:asc,updated_at:desc",
        })
        r = s.get(
            f"{BASE_URL}/1/clouddrive/share/sharepage/detail",
            params=params, timeout=15
        )
        data = r.json()
        _total = data.get("metadata", {}).get("_total", 0)
        _size = data.get("metadata", {}).get("_size", 50)
        _count = data.get("metadata", {}).get("_count", 0)
        items = data.get("data", {}).get("list", [])
        file_list.extend(items)
        if _total < 1 or _total <= _size or _count < _size:
            break
        page += 1
    return file_list


def get_or_create_dir(s, save_path):
    if not save_path or save_path in ("/", "0"):
        return "0"
    r = s.post(
        f"{BASE_URL}/1/clouddrive/file/info/path_list",
        params={"pr": "ucpro", "fr": "pc"},
        json={"file_path": [save_path], "namespace": "0"},
        timeout=10
    )
    data = r.json()
    if data.get("code") == 0 and data.get("data"):
        return data["data"][0]["fid"]
    # 创建目录
    r = s.post(
        f"{BASE_URL}/1/clouddrive/file",
        params={"pr": "ucpro", "fr": "pc"},
        json={"pdir_fid": "0", "file_name": save_path.strip('/'), "dir_path": "", "dir_init_lock": False},
        timeout=10
    )
    data = r.json()
    if data.get("code") == 0:
        return data["data"]["fid"]
    print(f"[夸克转存] 创建目录失败，使用根目录")
    return "0"


def submit_task(s, task_id):
    for i in range(30):
        params = base_params()
        params.update({"task_id": task_id, "retry_index": str(i)})
        r = s.get(
            f"{BASE_URL}/1/clouddrive/task",
            params=params, timeout=10
        )
        data = r.json()
        if data.get("data", {}).get("status") == 2:
            return True
        time.sleep(0.5)
    return False


def save_share(share_url, save_path="/夸克转存"):
    s = get_session()
    pwd_id, passcode = extract_url(share_url)
    print(f"[夸克转存] pwd_id: {pwd_id}")

    stoken = get_stoken(s, pwd_id, passcode)
    file_list = get_detail(s, pwd_id, stoken)

    if not file_list:
        print("[夸克转存] 分享为空或已失效")
        sys.exit(1)

    print(f"[夸克转存] 发现 {len(file_list)} 个文件/文件夹")
    for f in file_list[:5]:
        icon = "📁" if f.get("dir") else "📄"
        print(f"  {icon} {f['file_name']}")
    if len(file_list) > 5:
        print(f"  ... 共 {len(file_list)} 个")

    to_pdir_fid = get_or_create_dir(s, save_path)
    fid_list = [f["fid"] for f in file_list]
    fid_token_list = [f["share_fid_token"] for f in file_list]

    params = base_params()
    r = s.post(
        f"{SAVE_URL}/1/clouddrive/share/sharepage/save",
        params=params,
        json={
            "fid_list": fid_list,
            "fid_token_list": fid_token_list,
            "to_pdir_fid": to_pdir_fid,
            "pwd_id": pwd_id,
            "stoken": stoken,
            "pdir_fid": "0",
            "scene": "link",
        },
        timeout=15
    )
    result = r.json()
    if result.get("code") == 0:
        task_id = result.get("data", {}).get("task_id", "")
        print(f"[夸克转存] 任务提交成功，等待完成...")
        if task_id and submit_task(s, task_id):
            print(f"[夸克转存] ✓ 转存完成，保存到: {save_path}")
        else:
            print(f"[夸克转存] ✓ 转存已提交 (task_id: {task_id})")
    else:
        print(f"[夸克转存] 转存失败: {result.get('message', result)}")
        sys.exit(1)


def list_files():
    s = get_session()
    params = base_params()
    params.update({"pdir_fid": "0", "_page": 1, "_size": 20, "_fetch_total": 1, "_sort": "file_type:asc,updated_at:desc"})
    r = s.get(f"{BASE_URL}/1/clouddrive/file/sort", params=params, timeout=10)
    data = r.json()
    files = data.get("data", {}).get("list", [])
    print(f"[夸克网盘] 根目录 ({len(files)} 个):")
    for f in files:
        icon = "📁" if f.get("dir") else "📄"
        print(f"  {icon} {f['file_name']}")


def show_login_help():
    print("请运行: python3 quark_login.py")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 quark_save.py <share_url> [save_path]")
        print("      python3 quark_save.py --list")
        print("      python3 quark_save.py --login")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "--list":
        list_files()
    elif cmd == "--login":
        show_login_help()
    else:
        save_path = sys.argv[2] if len(sys.argv) > 2 else "/夸克转存"
        save_share(cmd, save_path)
