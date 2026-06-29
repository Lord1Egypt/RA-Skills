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

# ClawHub 技能下载地址（始终获取最新版本）
DEFAULT_DOWNLOAD_URL = os.environ.get(
    "YQZL_AI_DOWNLOAD_URL",
    "https://wry-manatee-359.convex.site/api/v1/download?slug=yqzl-ai-service"
)

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(SKILL_DIR, "version")
BACKUP_DIR = os.path.join(SKILL_DIR, "backup")

# 升级时需保留的文件/目录（不覆盖）
PRESERVE_ITEMS = {".api_key.enc", "backup"}

# 自动检测状态文件（记录上次检测时间）
STATE_FILE = os.path.join(SKILL_DIR, ".update_state.json")
# 自动检测间隔：24小时（秒）
CHECK_INTERVAL_SECONDS = 24 * 60 * 60


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


def get_remote_info(download_url=None):
    """获取远程下载信息（ClawHub 始终提供最新版本）"""
    url = download_url or DEFAULT_DOWNLOAD_URL
    return {
        "version": "latest",
        "download_url": url,
        "changelog": "从 ClawHub 获取最新版本",
    }


def check_update(download_url=None, silent=False):
    """
    检查更新（ClawHub 始终提供最新版本）
    :param download_url: 自定义下载地址
    :param silent: 是否静默模式（只返回结果，不打印）
    :return: (has_new, local_version, remote_info)
    """
    local = get_local_version()
    remote = get_remote_info(download_url)
    if not remote:
        if not silent:
            print("无法获取下载信息。")
        return False, local, None

    if not silent:
        print(f"当前版本: {local}")
        print(f"下载地址: {remote.get('download_url', '无')}")
        print(f"\n可运行以下命令升级到 ClawHub 最新版:")
        print(f"  python {os.path.join(os.path.dirname(__file__), 'updater.py')} update")
    return True, local, remote


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


def do_update(download_url=None, force=False):
    """
    从 ClawHub 下载并安装最新版本
    :param download_url: 自定义下载地址
    :param force: 是否强制升级（保留参数兼容）
    :return: 是否升级成功
    """
    has_new, local, remote = check_update(download_url, silent=True)
    if not remote:
        print("无法获取下载信息，升级终止。")
        return False

    remote_version = remote.get("version", "latest")
    download_url = remote.get("download_url")
    if not download_url:
        print("错误：缺少下载地址，无法下载更新包。")
        return False

    # 下载更新包
    print(f"开始从 ClawHub 下载最新版本...")
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


# ============================
# 自动检测 & 升级功能
# ============================

def _read_state():
    """读取上次检测状态"""
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _write_state(state):
    """写入检测状态"""
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False)
    except Exception:
        pass  # 状态写入失败不影响正常使用


def _should_auto_check():
    """判断是否应该执行自动检测（距上次检测是否已超过24小时）"""
    state = _read_state()
    last_check = state.get("last_check_time", 0)
    now = datetime.now().timestamp()
    return (now - last_check) >= CHECK_INTERVAL_SECONDS


def auto_check_and_notify(verbose=False):
    """
    启动时自动检测并升级。
    下载 ClawHub 最新版本，比较版本号，若有新版本则自动安装。
    
    :param verbose: 是否输出检测过程信息
    :return: dict {"checked": bool, "version": str, "upgraded": bool}
    """
    result = {"checked": False, "version": get_local_version(), "upgraded": False}

    # 判断是否需要检测（24小时间隔）
    if not _should_auto_check():
        if verbose:
            print(f"[自动检测] 距上次检测不足24小时，跳过检测。当前版本: {result['version']}")
        return result

    result["checked"] = True

    # 记录检测时间
    _write_state({
        "last_check_time": datetime.now().timestamp(),
        "last_result": "checking",
    })

    if verbose:
        print(f"[自动检测] 当前版本: {result['version']}，正在检查更新...")

    # 下载并比较版本
    info = _download_and_extract()
    if info is None:
        if verbose:
            print("[自动检测] 无法下载最新版本信息，跳过更新。")
        _write_state({
            "last_check_time": datetime.now().timestamp(),
            "last_result": "download_failed",
        })
        return result

    extract_dir, remote_version = info
    local = result["version"]

    if _compare_version(remote_version, local) > 0:
        if verbose:
            print(f"[自动检测] 发现新版本 {remote_version}（当前 {local}），正在自动升级...")
        try:
            success = _apply_update(extract_dir, remote_version)
            if success:
                result["version"] = remote_version
                result["upgraded"] = True
                if verbose:
                    print(f"[自动检测] 升级成功！当前版本: {remote_version}")
                _write_state({
                    "last_check_time": datetime.now().timestamp(),
                    "last_result": "upgraded",
                })
            else:
                if verbose:
                    print("[自动检测] 自动升级失败，当前版本保持不变。")
                _write_state({
                    "last_check_time": datetime.now().timestamp(),
                    "last_result": "upgrade_failed",
                })
        finally:
            # 清理临时目录
            try:
                if os.path.exists(extract_dir):
                    shutil.rmtree(extract_dir, ignore_errors=True)
            except Exception:
                pass
    else:
        if verbose:
            print(f"[自动检测] 已是最新版本 ({local})")
        _write_state({
            "last_check_time": datetime.now().timestamp(),
            "last_result": "up_to_date",
        })
        # 清理临时目录
        try:
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir, ignore_errors=True)
        except Exception:
            pass

    return result


def _download_and_extract():
    """
    下载 ClawHub 最新版本包并解压到临时目录。
    :return: (extract_dir, remote_version) 元组，失败返回 None
    """
    download_url = DEFAULT_DOWNLOAD_URL
    tmp_zip = os.path.join(tempfile.gettempdir(), "yqzl-ai-service-autocheck.zip")
    extract_dir = os.path.join(tempfile.gettempdir(), "yqzl-ai-service-autocheck")

    try:
        # 下载
        resp = requests.get(download_url, timeout=60)
        resp.raise_for_status()

        with open(tmp_zip, "wb") as f:
            f.write(resp.content)

        # 解压
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(tmp_zip, "r") as zf:
            zf.extractall(extract_dir)

        # 处理嵌套目录
        extracted_items = [i for i in os.listdir(extract_dir) if not i.startswith(".")]
        if len(extracted_items) == 1:
            nested = os.path.join(extract_dir, extracted_items[0])
            if os.path.isdir(nested):
                extract_dir = nested

        # 读取版本
        version_file = os.path.join(extract_dir, "version")
        if os.path.exists(version_file):
            with open(version_file, "r", encoding="utf-8") as f:
                remote_version = f.read().strip()
        else:
            remote_version = "0.0.0"

        # 清理临时 zip
        try:
            os.remove(tmp_zip)
        except Exception:
            pass

        return extract_dir, remote_version

    except Exception as e:
        # 清理
        try:
            if os.path.exists(tmp_zip):
                os.remove(tmp_zip)
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir, ignore_errors=True)
        except Exception:
            pass
        return None


def _apply_update(extract_dir, remote_version):
    """
    用已解压的目录替换当前技能文件。
    :param extract_dir: 已解压的更新目录
    :param remote_version: 远程版本号
    :return: 是否成功
    """
    try:
        # 备份当前版本
        backup_path = _backup_current()

        # 替换文件
        _do_replace(extract_dir)

        # 更新版本号
        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            f.write(remote_version)

        return True
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="云启智联AI服务技能升级工具（ClawHub 最新版）")
    parser.add_argument(
        "--url",
        help="自定义下载地址（默认使用 ClawHub 最新版）"
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("check", help="查看当前版本和下载信息")

    subparsers.add_parser("update", help="从 ClawHub 下载并安装最新版本")

    subparsers.add_parser("backups", help="查看已备份的版本列表")

    subparsers.add_parser("version", help="查看当前版本号")

    args = parser.parse_args()

    if args.command == "check":
        check_update(args.url)
    elif args.command == "update":
        do_update(args.url)
    elif args.command == "backups":
        list_backups()
    elif args.command == "version":
        print(f"当前版本: {get_local_version()}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
