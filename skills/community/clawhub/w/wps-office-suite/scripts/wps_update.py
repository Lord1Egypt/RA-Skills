"""
Skill 更新检查器 v3.0
检查是否有新版本可用，提示用户更新。
"""
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta


SKILLHUB_API = "https://skillhub.cn/api/skill/wps-office-suite"
CURRENT_VERSION = "3.0.0"
UPDATE_CHECK_INTERVAL_DAYS = 7  # 每 7 天检查一次


def get_last_check_date():
    """获取上次检查更新的日期"""
    marker_file = Path(__file__).parent / ".last_update_check"
    if marker_file.exists():
        try:
            return datetime.fromisoformat(marker_file.read_text().strip())
        except Exception:
            pass
    return None


def set_last_check_date():
    """记录本次检查日期"""
    marker_file = Path(__file__).parent / ".last_update_check"
    marker_file.write_text(datetime.now().isoformat(), encoding="utf-8")


def should_check_update():
    """判断是否需要检查更新"""
    last = get_last_check_date()
    if last is None:
        return True
    return (datetime.now() - last).days >= UPDATE_CHECK_INTERVAL_DAYS


def check_update_available():
    """
    检查是否有新版本可用。
    返回: {"has_update": bool, "latest_version": str, "message": str}
    """
    # 尝试用 skillhub CLI 获取最新版本
    try:
        result = subprocess.run(
            ["skillhub", "info", "wps-office-suite", "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            latest = data.get("version", CURRENT_VERSION)
            if latest != CURRENT_VERSION:
                return {
                    "has_update": True,
                    "latest_version": latest,
                    "current_version": CURRENT_VERSION,
                    "message": f"✨ 发现新版本 v{latest}（当前 v{CURRENT_VERSION}）",
                    "update_cmd": f"skillhub install wps-office-suite",
                    "changelog_url": "https://skillhub.cn/skill/wps-office-suite",
                }
    except (FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired):
        pass
    
    return {"has_update": False, "current_version": CURRENT_VERSION,
            "message": f"当前已是最新版本 v{CURRENT_VERSION}"}


def try_check_update(force=False):
    """
    尝试检查更新（7 天一次）。
    返回更新信息或空（不需要更新）。
    """
    set_last_check_date()
    
    if not force and not should_check_update():
        return {"checked": False, "message": "未到检查周期"}
    
    return check_update_available()


def show_update_reminder():
    """显示更新提醒（友好提示）"""
    result = try_check_update()
    
    if not result.get("checked", True):
        return None
    
    if result.get("has_update"):
        lines = [
            "=" * 50,
            "📢 WPS Office 全家桶 Skill 更新提醒",
            "=" * 50,
            f"  当前版本: v{result['current_version']}",
            f"  最新版本: v{result['latest_version']}",
            f"  状态: 有新版本可用！",
            f"  更新命令: {result['update_cmd']}",
            f"  更新说明: {result.get('changelog_url', '')}",
            "=" * 50,
        ]
        return "\n".join(lines)
    
    return None


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Skill 更新检查")
    parser.add_argument("--force", action="store_true", help="强制检查")
    args = parser.parse_args()
    
    result = try_check_update(force=args.force)
    print(json.dumps(result, ensure_ascii=False, indent=2))
