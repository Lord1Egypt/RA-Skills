#!/usr/bin/env python3
"""
Config Guardian - QClaw 配置守护者
自动备份关键配置，检测版本变化，升级后恢复配置

用法:
    python3 backup_config.py          # 备份当前配置
    python3 backup_config.py --check  # 检查版本变化
    python3 backup_config.py --list   # 列出备份历史
"""

import json
import os
import sys
import platform
import subprocess
from datetime import datetime
from pathlib import Path

# ============== 动态检测函数 ==============

def get_qclaw_version():
    """动态获取 QClaw 版本（跨平台）"""
    system = platform.system()

    if system == "Darwin":  # macOS
        try:
            result = subprocess.run(
                ["/usr/libexec/PlistBuddy", "-c", "Print CFBundleShortVersionString",
                 "/Applications/QClaw.app/Contents/Info.plist"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass

    elif system == "Windows":
        # Windows: 从注册表或可执行文件读取
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\QClaw")
            version, _ = winreg.QueryValueEx(key, "Version")
            return version
        except Exception:
            pass

    # 通用方法：从配置文件读取
    config_path = get_config_path() / "version.txt"
    if config_path.exists():
        return config_path.read_text().strip()

    return "unknown"


def get_config_path():
    """动态获取 QClaw 配置目录"""
    system = platform.system()

    if system == "Darwin":
        return Path.home() / ".qclaw"
    elif system == "Windows":
        return Path(os.environ.get("APPDATA", "")) / "QClaw"
    else:  # Linux
        return Path.home() / ".config" / "qclaw"


def get_backup_base_dir():
    """获取备份根目录"""
    return get_config_path() / "config-backups"


def get_openclaw_config_path():
    """动态获取 openclaw.json 路径"""
    system = platform.system()

    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "QClaw" / "openclaw.json"
    elif system == "Windows":
        return Path(os.environ.get("APPDATA", "")) / "QClaw" / "openclaw.json"
    else:
        return get_config_path() / "openclaw.json"


def get_channel_defaults_path():
    """获取 channel-defaults.json 路径"""
    return get_config_path() / "channel-defaults.json"


def get_cron_jobs():
    """动态获取所有 cron 任务（通过 cron CLI 工具）"""
    # 优先使用 cron 工具的 list action（JSON 输出）
    # 这是获取准确配置的推荐方式
    try:
        # 尝试通过 subprocess 调用 skill 中的 cron 工具
        # 注意：这里假设 AI 会通过 cron tool API 调用
        # 返回占位，真实获取由 AI session 处理
        return {
            "jobs": [],
            "note": "Cron jobs fetched dynamically by AI via cron tool"
        }
    except Exception:
        return {"jobs": [], "note": "Could not fetch cron jobs"}


def get_channels_config():
    """从主配置中提取 channels 配置"""
    config_path = get_openclaw_config_path()

    if not config_path.exists():
        return {}

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get('channels', {})
    except Exception:
        return {}


def get_plugins_config():
    """从主配置中提取 plugins 配置"""
    config_path = get_openclaw_config_path()

    if not config_path.exists():
        return {}

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get('plugins', {})
    except Exception:
        return {}


# ============== 备份函数 ==============

def backup_config(cron_jobs_override=None):
    """备份当前配置
    
    Args:
        cron_jobs_override: 可选，由 AI 通过 cron tool 获取后传入
    """
    version = get_qclaw_version()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = get_backup_base_dir() / f"{timestamp}_v{version}"

    backup_dir.mkdir(parents=True, exist_ok=True)

    print(f"📦 备份 QClaw 配置 (版本: {version})")
    print(f"   备份目录: {backup_dir}")
    print()

    backup_data = {
        "meta": {
            "version": version,
            "timestamp": timestamp,
            "platform": platform.system(),
            "python_version": platform.python_version(),
        },
        "channels": get_channels_config(),
        "plugins": get_plugins_config(),
        "channel_defaults": {},
        "cron_jobs": {}
    }

    # 备份 channel-defaults.json
    channel_defaults_path = get_channel_defaults_path()
    if channel_defaults_path.exists():
        try:
            backup_data["channel_defaults"] = json.loads(
                channel_defaults_path.read_text()
            )
            print("  ✅ channel-defaults.json")
        except Exception as e:
            print(f"  ⚠️ channel-defaults.json 读取失败: {e}")

    # 备份 cron jobs（优先使用 override）
    if cron_jobs_override:
        backup_data["cron_jobs"] = cron_jobs_override
        job_count = len(cron_jobs_override.get("jobs", []))
        print(f"  ✅ cron jobs ({job_count} 个，来自 AI)")
    else:
        cron_jobs = get_cron_jobs()
        backup_data["cron_jobs"] = cron_jobs
        job_count = len(cron_jobs.get("jobs", []))
        print(f"  ✅ cron jobs ({job_count} 个)")

    # 写入备份文件
    backup_file = backup_dir / "backup.json"
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)

    # 更新 latest 链接（通过复制）
    latest_file = get_backup_base_dir() / "latest.json"
    with open(latest_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)

    # 记录最后备份版本
    last_version_file = get_backup_base_dir() / "last-version.txt"
    last_version_file.write_text(version)

    print()
    print("✅ 备份完成")
    print(f"   文件: {backup_file}")

    return backup_data


def check_version_change():
    """检查版本是否变化"""
    current_version = get_qclaw_version()
    last_version_file = get_backup_base_dir() / "last-version.txt"

    if not last_version_file.exists():
        return {
            "changed": True,
            "current": current_version,
            "previous": None,
            "message": "首次运行，需要备份"
        }

    last_version = last_version_file.read_text().strip()

    if current_version != last_version:
        return {
            "changed": True,
            "current": current_version,
            "previous": last_version,
            "message": f"版本已从 {last_version} 升级到 {current_version}"
        }

    return {
        "changed": False,
        "current": current_version,
        "previous": last_version,
        "message": "版本未变化"
    }


def list_backups():
    """列出所有备份"""
    backup_dir = get_backup_base_dir()

    if not backup_dir.exists():
        print("暂无备份")
        return []

    backups = sorted(backup_dir.glob("*_v*"), reverse=True)

    if not backups:
        print("暂无备份")
        return []

    print("📋 备份历史")
    print("-" * 50)

    for b in backups:
        if b.is_dir():
            backup_file = b / "backup.json"
            if backup_file.exists():
                try:
                    data = json.loads(backup_file.read_text())
                    meta = data.get("meta", {})
                    print(f"  {b.name}")
                    print(f"    版本: {meta.get('version', '?')}")
                    print(f"    时间: {meta.get('timestamp', '?')}")
                    print(f"    Cron: {len(data.get('cron_jobs', {}).get('jobs', []))} 个")
                except Exception:
                    print(f"  {b.name} (读取失败)")

    return backups


# ============== 主函数 ==============

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == "--check":
            result = check_version_change()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            if result["changed"]:
                print()
                print("⚠️ " + result["message"])
                print("建议执行: python3 backup_config.py")
            return result["changed"]

        elif arg == "--cron-data":
            # 接收 AI 传入的 cron 数据
            if len(sys.argv) > 2:
                cron_data_path = sys.argv[2]
                cron_file = Path(cron_data_path)
                if cron_file.exists():
                    global_cron_data = json.loads(cron_file.read_text())
                    backup_config(cron_jobs_override=global_cron_data)
                else:
                    print(f"❌ 文件不存在: {cron_data_path}")
                    sys.exit(1)
            else:
                backup_config()
            return

        elif arg == "--list":
            list_backups()
            return

        elif arg in ["--help", "-h"]:
            print(__doc__)
            return

    # 默认：执行备份
    backup_config()


if __name__ == "__main__":
    main()
