#!/usr/bin/env python3.12
"""
115网盘离线下载 - 使用 p115client
用法:
  python3.12 115_offline.py <url_or_magnet>        # 添加离线任务
  python3.12 115_offline.py <url> <folder_cid>     # 添加到指定目录
  python3.12 115_offline.py --list                 # 查看任务列表
"""
import sys
import os
import subprocess
import configparser
from p115client import P115Client


def get_rclone_config_path():
    """动态获取 rclone 配置文件路径，兼容所有用户和平台"""
    try:
        result = subprocess.run(
            ["rclone", "config", "file"],
            capture_output=True, text=True, check=True
        )
        # 输出格式: "Configuration file is stored at:\n/path/to/rclone.conf"
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.endswith(".conf") or line.endswith(".config"):
                return line
        # fallback: 最后一行非空
        lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
        return lines[-1] if lines else os.path.expanduser("~/.config/rclone/rclone.conf")
    except Exception:
        return os.path.expanduser("~/.config/rclone/rclone.conf")


def get_client():
    config_path = get_rclone_config_path()
    cfg = configparser.ConfigParser()
    cfg.read(config_path)
    if '115drive' not in cfg:
        raise Exception(
            "rclone 115drive 未配置，请先运行:\n"
            "  python3 scripts/115_qrlogin.py"
        )
    c = cfg['115drive']
    cookie = f"UID={c['uid']}; CID={c['cid']}; SEID={c['seid']}; KID={c['kid']}"
    return P115Client(cookie)


def offline_add(url, save_dir_id="0"):
    client = get_client()
    result = client.offline_add_url(url, pid=save_dir_id if save_dir_id != "0" else None)
    data = result.get('data', result)
    if result.get('state'):
        print(f"[115离线] 添加成功 ✓")
        print(f"  名称: {data.get('name', url[:60])}")
        print(f"  Hash: {data.get('info_hash', '-')}")
    else:
        print(f"[115离线] 添加失败: {result.get('error_msg', result)}")
        sys.exit(1)


def offline_list():
    client = get_client()
    result = client.offline_list()
    tasks = result.get('tasks', [])
    status_map = {0: '等待', 1: '下载中', 2: '完成', -1: '失败'}
    print(f"[115离线] 共 {len(tasks)} 个任务:")
    for t in tasks[:15]:
        status = status_map.get(t.get('status', 0), '未知')
        name = t.get('name', '')[:45]
        pct = t.get('percentDone', 0)
        print(f"  [{status}] {name} - {pct}%")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3.12 115_offline.py <url_or_magnet>")
        print("      python3.12 115_offline.py --list")
        sys.exit(1)
    if sys.argv[1] == "--list":
        offline_list()
    else:
        url = sys.argv[1]
        cid = sys.argv[2] if len(sys.argv) > 2 else "0"
        offline_add(url, cid)
