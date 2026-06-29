#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能自动升级工具
支持检查新版本、下载更新、备份回滚
"""
import argparse
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime

try:
    import requests
except ImportError:
    print("错误：缺少 requests 库。请运行: pip install requests")
    sys.exit(1)

# 默认升级源，可通过环境变量 YQZL_AI_UPDATE_URL 覆盖
DEFAULT_UPDATE_URL = os.environ.get(
    "YQZL_AI_UPDATE_URL",
    "http://8.135.62.13:5000/static/skills/yqzl-ai-service/latest.json"
)

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(SKILL_DIR, "version")
BACKUP_DIR = os.path.join(SKILL_DIR, "backup")

# 升级时需保留的文件/目录（不覆盖）
PRESERVE_ITEMS = {".api_key.enc", "backup"}


def _parse_version(v):
    """解析版本号为整数元组，支持 x.y.z 格式"""
    parts = re.split(r"[.-]", v.strip().lstrip("v"))
    nums = []
    for p in parts:
        try:
            nums.append(int(p))
        except ValueError:
            break
    # 补齐到 3 位
    while len(nums) < 3:
        nums.append(0)
    return tuple(nums[:3])


def _compare_version(v1, v2):
    """比较两个版本号。返回 1 表示 v1>v2，0 表示相等，-1 表示 v1<v2"""
    a = _parse_version(v1)
    b = _parse_version(v2)
    if a > b:
        return 1
    elif a < b:
        return -1
    return 0


def get_local_version():
    """读取本地版本号"""
    if not os.path.exists(VERSION_FILE):
        return "0.0.0"
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        return f.read().strip() or "0.0.0"


def get_remote_info(update_url=None):
    """从远程获取最新版本信息"""
    url = update_url or DEFAULT_UPDATE_URL
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        print("检查版本超时，请检查网络连接。")
        return None
    except requests.exceptions.ConnectionError:
        print("无法连接到版本服务器，请检查网络。")
        return None
    except Exception as e:
        print(f"获取版本信息失败: {e}")
        return None


def check_update(update_url=None, silent=False):
    """
    检查是否有新版本
    :param update_url: 自定义升级源地址
    :param silent: 是否静默模式（只返回结果，不打印）
    :return: (has_new, local_version, remote_info)
    """
    local = get_local_version()
    remote = get_remote_info(update_url)
    if not remote:
        if not silent:
            print("无法获取远程版本信息。")
        return False, local, None

    remote_version = remote.get("version", "0.0.0")
    cmp = _compare_version(remote_version, local)

    if cmp > 0:
        if not silent:
            print(f"发现新版本!")
            print(f"  当前版本: {local}")
            print(f"  最新版本: {remote_version}")
            changelog = remote.get("changelog", "")
            if changelog:
                print(f"  更新日志: {changelog}")
            print(f"  下载地址: {remote.get('download_url', '无')}")
            print("\n可运行以下命令升级:")
            print(f"  python {os.path.join(os.path.dirname(__file__), 'updater.py')} update")
        return True, local, remote
    else:
        if not silent:
            print(f"当前已是最新版本: {local}")
        return False, local, remote


def _backup_current():
    """备份当前版本到 backup/ 目录（按时间戳命名子目录）"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"v{get_local_version()}_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)

    for item in os.listdir(SKILL_DIR):
        if item in ("backup", "__pycache__"):
            continue
        src = os.path.join(SKILL_DIR, item)
        dst = os.path.join(backup_path, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    return backup_path


def _do_replace(extract_dir):
    """用解压后的文件替换当前技能文件（保留特定文件）"""
    for item in os.listdir(extract_dir):
        if item in PRESERVE_ITEMS:
            continue
        src = os.path.join(extract_dir, item)
        dst = os.path.join(SKILL_DIR, item)
        if os.path.exists(dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)


def do_update(update_url=None, force=False):
    """
    执行升级
    :param update_url: 自定义升级源地址
    :param force: 是否强制升级（忽略版本号）
    :return: 是否升级成功
    """
    has_new, local, remote = check_update(update_url, silent=True)
    if not remote:
        print("无法获取远程版本信息，升级终止。")
        return False

    remote_version = remote.get("version", "0.0.0")
    if not force and not has_new:
        print(f"当前已是最新版本 ({local})，无需升级。")
        return True

    download_url = remote.get("download_url")
    if not download_url:
        print("错误：远程配置中缺少 download_url，无法下载更新包。")
        return False

    # 下载更新包
    print(f"开始下载更新包 (版本 {remote_version})...")
    try:
        resp = requests.get(download_url, timeout=120)
        resp.raise_for_status()
    except Exception as e:
        print(f"下载更新包失败: {e}")
        return False

    # 备份当前版本
    print("正在备份当前版本...")
    try:
        backup_path = _backup_current()
        print(f"备份完成: {backup_path}")
    except Exception as e:
        print(f"备份失败: {e}")
        return False

    # 解压更新包
    tmp_zip = os.path.join(tempfile.gettempdir(), f"yqzl-ai-service-update-{remote_version}.zip")
    try:
        with open(tmp_zip, "wb") as f:
            f.write(resp.content)

        extract_dir = os.path.join(tempfile.gettempdir(), f"yqzl-ai-service-extract-{remote_version}")
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(tmp_zip, "r") as zf:
            zf.extractall(extract_dir)

        # 处理可能的嵌套目录（zip 内包含根目录）
        extracted_items = [i for i in os.listdir(extract_dir) if not i.startswith(".")]
        if len(extracted_items) == 1:
            nested = os.path.join(extract_dir, extracted_items[0])
            if os.path.isdir(nested):
                extract_dir = nested

        # 替换文件
        print("正在应用更新...")
        _do_replace(extract_dir)

        # 更新版本号
        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            f.write(remote_version)

        print(f"\n升级成功! 当前版本: {remote_version}")
        print(f"旧版本已备份至: {backup_path}")
        print("如遇问题可手动将 backup 中的文件复制回技能目录进行回滚。")
        return True

    except Exception as e:
        print(f"升级过程中发生错误: {e}")
        print("升级失败，当前版本保持不变。")
        return False
    finally:
        if os.path.exists(tmp_zip):
            try:
                os.remove(tmp_zip)
            except Exception:
                pass
        extract_dir = os.path.join(tempfile.gettempdir(), f"yqzl-ai-service-extract-{remote_version}")
        if os.path.exists(extract_dir):
            try:
                shutil.rmtree(extract_dir)
            except Exception:
                pass


def list_backups():
    """列出所有备份版本"""
    if not os.path.exists(BACKUP_DIR):
        print("暂无备份记录。")
        return
    backups = sorted(os.listdir(BACKUP_DIR))
    if not backups:
        print("暂无备份记录。")
        return
    print("备份列表:")
    for b in backups:
        path = os.path.join(BACKUP_DIR, b)
        size = sum(
            os.path.getsize(os.path.join(dirpath, f))
            for dirpath, _, filenames in os.walk(path)
            for f in filenames
        )
        print(f"  {b}  ({size / 1024:.1f} KB)")


def main():
    parser = argparse.ArgumentParser(description="云启智联AI服务技能自动升级工具")
    parser.add_argument(
        "--url",
        help="自定义升级源地址（默认从环境变量 YQZL_AI_UPDATE_URL 读取）"
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("check", help="检查是否有新版本")

    update_parser = subparsers.add_parser("update", help="执行升级")
    update_parser.add_argument("--force", action="store_true", help="强制升级（忽略版本号）")

    subparsers.add_parser("backups", help="查看已备份的版本列表")

    subparsers.add_parser("version", help="查看当前版本号")

    args = parser.parse_args()

    if args.command == "check":
        check_update(args.url)
    elif args.command == "update":
        do_update(args.url, force=args.force)
    elif args.command == "backups":
        list_backups()
    elif args.command == "version":
        print(f"当前版本: {get_local_version()}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
