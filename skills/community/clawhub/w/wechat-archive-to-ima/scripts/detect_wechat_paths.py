#!/usr/bin/env python3
"""
detect_wechat_paths.py — 探测微信 PC 版数据目录
用法：
    python detect_wechat_paths.py                 # 打印环境清单
    python detect_wechat_paths.py --rank-contacts # 列出所有聊天对象的活跃度排行
"""
import argparse
import os
import re
import sys
from pathlib import Path


def user_home() -> Path:
    return Path(os.path.expanduser("~"))


def candidate_roots():
    """返回所有可能的微信数据根目录（按出现频率排序，实测 4.x 在用户主目录下）"""
    home = user_home()
    docs = home / "Documents"
    return [
        home / "xwechat_files",           # 4.x 默认（★ 最常见，实测在这）
        docs / "xwechat_files",          # 4.x 兼容
        docs / "WeChat Files",            # 3.x 默认
        Path("D:/xwechat_files"),
        Path("D:/WeChat Files"),
        Path("E:/WeChat Files"),
        Path("E:/xwechat_files"),
    ]


def detect_wechat_process():
    """粗略探测微信安装路径（Windows）"""
    if sys.platform != "win32":
        return None
    try:
        import winreg
        for sub in (r"Software\Tencent\Weixin", r"Software\Tencent\WeChat"):
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub)
                install_path, _ = winreg.QueryValueEx(key, "InstallPath")
                winreg.CloseKey(key)
                return install_path
            except FileNotFoundError:
                continue
    except Exception:
        pass
    return None


def find_account_dirs(root: Path):
    """在数据根目录下找账号子目录"""
    if not root.is_dir():
        return []
    accounts = []
    for sub in root.iterdir():
        if not sub.is_dir():
            continue
        name = sub.name
        # 跳过系统目录
        if name in ("All Users", "Applet", "WMPF", "Finderlive", "radium"):
            continue
        # 4.x: wxid_xxxx_hash 或 自定义名_hash
        # 3.x: 微信号 / 备注名
        accounts.append(sub)
    return accounts


def find_msg_dir(account_dir: Path):
    """在账号目录下找 msg / FileStorage 子目录"""
    candidates = [
        account_dir / "msg",
        account_dir / "FileStorage",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return None


def rank_contacts(msg_dir: Path):
    """
    列出 msg 下所有联系人子目录（attach/file），按文件数和最近修改时间排序
    返回 [(wxid, file_count, latest_mtime, size_bytes), ...]
    """
    contacts = {}
    for sub_name in ("attach", "file"):
        sub_dir = msg_dir / sub_name
        if not sub_dir.is_dir():
            continue
        for wxid_dir in sub_dir.iterdir():
            if not wxid_dir.is_dir():
                continue
            # msg/file 下是按月份分的（YYYY-MM），不是联系人，直接跳过
            if re.fullmatch(r"\d{4}-\d{2}", wxid_dir.name):
                continue
            cnt = 0
            latest = 0
            size = 0
            for fp in wxid_dir.rglob("*"):
                if fp.is_file():
                    cnt += 1
                    try:
                        st = fp.stat()
                        latest = max(latest, st.st_mtime)
                        size += st.st_size
                    except OSError:
                        pass
            if wxid_dir.name in contacts:
                old = contacts[wxid_dir.name]
                contacts[wxid_dir.name] = (
                    old[0] + cnt,
                    max(old[1], latest),
                    old[2] + size,
                )
            else:
                contacts[wxid_dir.name] = (cnt, latest, size)

    result = [
        (wxid, cnt, latest, size)
        for wxid, (cnt, latest, size) in contacts.items()
    ]
    # (wxid, cnt, latest, size)：先按文件数降序，再按最近修改时间降序
    result.sort(key=lambda x: (-x[1], -x[2]))
    return result


def human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rank-contacts", action="store_true",
                    help="列出聊天对象活跃度排行")
    ap.add_argument("--account", help="指定账号目录名（可选）")
    args = ap.parse_args()

    print("=" * 60)
    print("微信 PC 版环境探测")
    print("=" * 60)

    install = detect_wechat_process()
    if install:
        print(f"[安装路径] {install}")
    else:
        print("[安装路径] 未在注册表找到")

    found_roots = [r for r in candidate_roots() if r.is_dir()]
    if not found_roots:
        print("\n[!] 未找到任何微信数据目录。可能：")
        print("    1. 微信没在这台电脑登录过")
        print("    2. 数据目录被自定义到别处（让用户在微信设置→文件管理 里看）")
        sys.exit(1)

    for root in found_roots:
        print(f"\n[数据根] {root}")
        accounts = find_account_dirs(root)
        if not accounts:
            print("  （空目录）")
            continue
        for acc in accounts:
            msg = find_msg_dir(acc)
            marker = "✅" if msg else "⚠️"
            print(f"  {marker} 账号: {acc.name}")
            if msg:
                print(f"      msg目录: {msg}")
                # 总大小
                total = sum(
                    f.stat().st_size for f in msg.rglob("*") if f.is_file()
                )
                print(f"      附件总大小: {human_size(total)}")

                if args.rank_contacts:
                    print(f"\n      [聊天对象活跃度 TOP 20]")
                    print(f"      {'微信ID':<35} {'文件数':>6}  {'最近修改':<20} {'大小':>10}")
                    from datetime import datetime
                    for wxid, cnt, latest, size in rank_contacts(msg)[:20]:
                        lt = datetime.fromtimestamp(latest).strftime("%Y-%m-%d")
                        print(f"      {wxid:<35} {cnt:>6}  {lt:<20} {human_size(size):>10}")

    print("\n" + "=" * 60)
    print("下一步：")
    print("  1. 让用户在手机发起备份（见 SKILL.md 阶段 1）")
    print("  2. 用 --rank-contacts 输出，让用户指认目标联系人的 wxid")
    print("  3. 把该 wxid 传给 organize_attachments.py --contact")


if __name__ == "__main__":
    main()
