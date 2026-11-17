# -*- coding: utf-8 -*-
"""版本检测与升级提醒模块 (#3跨平台版本提醒机制)

功能：
1. 跨平台来源识别 - 从 SKILL.json 读取 download_source（clawhub/github/skillhub/local_dev）
2. 每日版本检测 - 每天首次启动 Skill 时自动查询对应平台的最新版本
3. 版本号对比 - 语义化版本对比（支持 V1.0.4、V1.5 等多种格式）
4. 7 天强缓存 - 避免每次启动都请求网络，离线时直接跳过
5. 双通道提醒 - 控制台顶部蓝色横幅 + 右下角非阻塞弹窗
6. 紧急通知推送 - 通过 urgent_notice 字段推送不依赖版本号的紧急消息
7. 用户操作反馈 - 支持「稍后提醒（7天）」「跳过此版本」「立即前往升级」

远端 latest_version.json 格式（作者服务器静态文件）：
{
  "latest_version": "1.0.5",
  "release_notes": "修复网络波动下载卡死问题\\n新增版本自动提醒功能\\n优化崩溃分析准确率",
  "urgent_notice": "⚠️ 重要更新：免费期规则与付费体系已上线，老用户升级后立即享首月8折优惠！",
  "download_url": "https://clawhub.ai/liang030214/skills/mc-ecosystem-adapt-engine",
  "published_at": "2026-08-26T12:00:00+08:00"
}
"""

import json
import logging
import os
import time
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

# === 配置项 ===
# 版本检测频率：默认每天首次启动检查一次（可设为每 3 天：CHECK_INTERVAL_DAYS = 3）
CHECK_INTERVAL_DAYS = int(os.environ.get("MC_SKILL_VERSION_CHECK_INTERVAL", "1"))
# 远端缓存 TTL（秒）：7 天强缓存，避免频繁请求
REMOTE_CACHE_TTL_SECONDS = int(os.environ.get("MC_SKILL_VERSION_CACHE_TTL", str(7 * 24 * 3600)))
# 网络请求超时（秒）
REQUEST_TIMEOUT = int(os.environ.get("MC_SKILL_VERSION_TIMEOUT", "5"))
# 「稍后提醒」默认天数
REMIND_LATER_DAYS = 7

# 平台名称映射（用于显示）
PLATFORM_DISPLAY_NAMES = {
    "clawhub": "ClawHub",
    "github": "GitHub",
    "skillhub": "SkillHub",
    "local_dev": "本地开发版",
}

# 版本检查状态文件路径（与 auth_state.json 同目录）
def _get_state_file_path() -> Path:
    """获取版本检查状态文件路径"""
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir / "version_check_state.json"


def _load_skill_info() -> Dict[str, str]:
    """从 SKILL.json 读取下载来源、检查URL、当前版本号"""
    project_root = Path(__file__).resolve().parent.parent
    skill_json_path = project_root / "SKILL.json"
    defaults = {
        "download_source": "local_dev",
        "source_update_check_url": "",
        "version": "0.0.0",
    }
    try:
        with open(skill_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "download_source": data.get("download_source", "local_dev"),
            "source_update_check_url": data.get("source_update_check_url", ""),
            "version": str(data.get("version", "0.0.0")),
        }
    except Exception as e:
        logger.warning(f"[版本检测] 读取 SKILL.json 失败: {e}，使用默认值")
        return defaults


def _load_state() -> Dict[str, Any]:
    """加载版本检查状态（上次检查日期、跳过的版本、稍后提醒到期日等）"""
    state_path = _get_state_file_path()
    defaults = {
        "last_check_date": "",           # 上次检查日期 YYYY-MM-DD
        "cached_remote_info": None,      # 缓存的远端版本信息
        "cached_at_timestamp": 0,        # 缓存写入时间戳
        "skipped_version": "",           # 用户选择跳过的版本号
        "remind_later_until_date": "",   # 「稍后提醒」到期日 YYYY-MM-DD
        "last_shown_urgent_notice": "",  # 上次展示的紧急通知内容（防重复）
    }
    try:
        if state_path.exists():
            with open(state_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            defaults.update(loaded)
    except Exception as e:
        logger.warning(f"[版本检测] 加载状态文件失败: {e}，使用默认值")
    return defaults


def _save_state(state: Dict[str, Any]) -> None:
    """保存版本检查状态"""
    state_path = _get_state_file_path()
    try:
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"[版本检测] 保存状态文件失败: {e}")


def _parse_version(version_str: str) -> Tuple[int, ...]:
    """将版本号字符串解析为可比较的整数元组（语义化版本对比）
    
    支持格式：
      - "1.0.4" → (1, 0, 4)
      - "V1.5"  → (1, 5, 0)
      - "1.0.4-beta" → (1, 0, 4)
    """
    try:
        # 去掉前缀 V/v 和后缀 -alpha/-beta 等
        cleaned = version_str.strip().lstrip("Vv")
        if "-" in cleaned:
            cleaned = cleaned.split("-")[0]
        parts = cleaned.split(".")
        result = []
        for p in parts:
            # 只保留数字部分
            num = "".join(c for c in p if c.isdigit())
            result.append(int(num) if num else 0)
        # 补全为至少 3 位，避免 (1,5) < (1,0,4) 这种误判
        while len(result) < 3:
            result.append(0)
        return tuple(result)
    except Exception:
        logger.warning(f"[版本检测] 无法解析版本号: {version_str}，返回 (0,0,0)")
        return (0, 0, 0)


def _is_newer(remote_version: str, local_version: str) -> bool:
    """判断远端版本是否比本地版本新
    
    严格大于才返回 True（等于不算新版本）
    """
    rv = _parse_version(remote_version)
    lv = _parse_version(local_version)
    return rv > lv


def _fetch_remote_info(check_url: str) -> Optional[Dict[str, Any]]:
    """从 check_url 获取远端版本信息（带超时和异常处理）
    
    返回格式：
    {
        "latest_version": "1.0.5",
        "release_notes": "...",
        "urgent_notice": "⚠️ ...",
        "download_url": "https://...",
        "published_at": "..."
    }
    """
    if not check_url or check_url.startswith("https://example.com/"):
        # 占位URL，直接跳过
        logger.info("[版本检测] 检查URL为占位符，跳过联网检测")
        return None

    # V1.0.5 修复：离线模式下跳过版本检查
    from config import OFFLINE_MODE
    if OFFLINE_MODE:
        logger.info("[版本检测] 离线模式，跳过联网版本检查")
        return None

    try:
        import urllib.request
        import urllib.error
        import ssl  # V1.0.5 修复：显式 SSL 上下文

        req = urllib.request.Request(
            check_url,
            headers={
                "User-Agent": f"MCSkill-VersionChecker/1.0",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT, context=ssl.create_default_context()) as resp:
            body = resp.read().decode("utf-8")
            data = json.loads(body)
            # 基本字段校验
            if "latest_version" not in data:
                logger.warning(f"[版本检测] 远端返回缺少 latest_version 字段: {data}")
                return None
            return data
    except Exception as e:
        logger.info(f"[版本检测] 联网查询失败: {type(e).__name__}: {e}，跳过本次检查")
        return None


def _should_check_today(state: Dict[str, Any]) -> bool:
    """根据 CHECK_INTERVAL_DAYS 判断今天是否需要检查"""
    today_str = date.today().isoformat()
    last_check = state.get("last_check_date", "")
    if not last_check:
        return True  # 从未检查过，需要检查
    try:
        last_date = date.fromisoformat(last_check)
        today = date.today()
        days_passed = (today - last_date).days
        return days_passed >= CHECK_INTERVAL_DAYS
    except Exception:
        return True


def _is_cache_valid(state: Dict[str, Any]) -> bool:
    """判断缓存是否在有效期内"""
    cached_at = state.get("cached_at_timestamp", 0)
    if not cached_at:
        return False
    age_seconds = time.time() - cached_at
    return age_seconds <= REMOTE_CACHE_TTL_SECONDS


def _check_remind_later_expired(state: Dict[str, Any]) -> bool:
    """判断「稍后提醒」是否已到期（到期=需要显示）"""
    remind_until = state.get("remind_later_until_date", "")
    if not remind_until:
        return True  # 没有设置稍后提醒，直接显示
    try:
        until_date = date.fromisoformat(remind_until)
        return date.today() >= until_date
    except Exception:
        return True


def _is_version_skipped(state: Dict[str, Any], remote_version: str) -> bool:
    """判断该版本是否被用户标记为跳过"""
    return state.get("skipped_version", "") == remote_version


def check_for_updates(force: bool = False) -> Optional[Dict[str, Any]]:
    """主入口：检查是否有新版本
    
    Args:
        force: 强制立即检查（忽略频率限制，但仍尊重缓存）
    
    Returns:
        如果需要提醒用户升级，返回字典：
        {
            "type": "update" | "urgent_notice",
            "download_source": "clawhub",
            "platform_display_name": "ClawHub",
            "current_version": "1.0.4",
            "remote_version": "1.0.5",
            "release_notes": "修复了...\\n新增了...",
            "urgent_notice": "⚠️ 紧急通知...",  # 可能为空字符串
            "download_url": "https://clawhub.ai/liang030214/skills/mc-ecosystem-adapt-engine",
        }
        如果不需要提醒，返回 None
    """
    skill_info = _load_skill_info()
    download_source = skill_info["download_source"]
    check_url = skill_info["source_update_check_url"]
    local_version = skill_info["version"]
    platform_name = PLATFORM_DISPLAY_NAMES.get(download_source, download_source)

    state = _load_state()

    # 本地开发版默认不提示（避免干扰调试），除非 force=True
    if download_source == "local_dev" and not force:
        logger.info("[版本检测] 本地开发版，跳过版本提醒")
        return None

    # 判断今天是否需要检查
    if not force and not _should_check_today(state):
        logger.info("[版本检测] 未到检查频率，跳过")
        return None

    # 更新「上次检查日期」为今天（无论联网成功与否，都避免下次再进）
    state["last_check_date"] = date.today().isoformat()

    # 优先用缓存
    remote_info = None
    if _is_cache_valid(state):
        remote_info = state.get("cached_remote_info")
        logger.info(f"[版本检测] 使用缓存版本信息（年龄 {int((time.time() - state['cached_at_timestamp'])/3600)}h）")

    # 缓存无效则联网
    if remote_info is None:
        remote_info = _fetch_remote_info(check_url)
        if remote_info is not None:
            # 写入缓存
            state["cached_remote_info"] = remote_info
            state["cached_at_timestamp"] = int(time.time())

    _save_state(state)

    if remote_info is None:
        # 离线或失败，啥也不做
        return None

    remote_version = str(remote_info.get("latest_version", "0.0.0"))
    release_notes = str(remote_info.get("release_notes", ""))
    urgent_notice = str(remote_info.get("urgent_notice", ""))
    download_url = str(remote_info.get("download_url", ""))

    # === 第一优先级：紧急通知（urgent_notice）===
    # 只要有新的 urgent_notice 且和上次显示的不一样，就必须显示（哪怕版本号不变）
    last_urgent = state.get("last_shown_urgent_notice", "")
    has_new_urgent = bool(urgent_notice) and urgent_notice != last_urgent

    if has_new_urgent:
        state["last_shown_urgent_notice"] = urgent_notice
        _save_state(state)
        return {
            "type": "urgent_notice",
            "download_source": download_source,
            "platform_display_name": platform_name,
            "current_version": local_version,
            "remote_version": remote_version,
            "release_notes": release_notes,
            "urgent_notice": urgent_notice,
            "download_url": download_url,
        }

    # === 第二优先级：版本升级提醒 ===
    if not _is_newer(remote_version, local_version):
        # 版本号没有更新
        return None

    # 检查是否被跳过或稍后提醒
    if _is_version_skipped(state, remote_version):
        logger.info(f"[版本检测] 版本 {remote_version} 被用户标记为跳过，不提醒")
        return None
    if not _check_remind_later_expired(state):
        logger.info("[版本检测] 在「稍后提醒」期限内，不提醒")
        return None

    return {
        "type": "update",
        "download_source": download_source,
        "platform_display_name": platform_name,
        "current_version": local_version,
        "remote_version": remote_version,
        "release_notes": release_notes,
        "urgent_notice": urgent_notice,
        "download_url": download_url,
    }


# === 用户操作回写函数（供 UI 调用）===

def skip_version(version: str) -> None:
    """用户选择「跳过此版本」"""
    state = _load_state()
    state["skipped_version"] = version
    _save_state(state)
    logger.info(f"[版本检测] 用户跳过版本: {version}")


def remind_me_later(days: int = REMIND_LATER_DAYS) -> None:
    """用户选择「稍后提醒」，默认 N 天后再提示"""
    state = _load_state()
    until = (date.today() + timedelta(days=days)).isoformat()
    state["remind_later_until_date"] = until
    _save_state(state)
    logger.info(f"[版本检测] 用户选择稍后提醒，{days} 天后（{until}）再次提示")


def dismiss_banner_temporarily() -> None:
    """临时关闭横幅（本次会话不再显示，下次启动重新判断）
    
    实现方式：不写入持久化文件，仅由调用方在内存中标记
    """
    logger.info("[版本检测] 用户临时关闭升级横幅（本次会话有效）")


def get_check_summary() -> Dict[str, Any]:
    """获取当前版本检测状态摘要（供调试和 F14 报表使用）"""
    skill_info = _load_skill_info()
    state = _load_state()
    cache_age_hours = 0
    if state.get("cached_at_timestamp"):
        cache_age_hours = int((time.time() - state["cached_at_timestamp"]) // 3600)
    return {
        "download_source": skill_info["download_source"],
        "platform_name": PLATFORM_DISPLAY_NAMES.get(skill_info["download_source"], skill_info["download_source"]),
        "current_version": skill_info["version"],
        "check_url": skill_info["source_update_check_url"],
        "last_check_date": state.get("last_check_date", "从未检查"),
        "cache_age_hours": cache_age_hours,
        "cache_valid": _is_cache_valid(state),
        "skipped_version": state.get("skipped_version", "无"),
        "remind_later_until": state.get("remind_later_until_date", "无"),
        "check_interval_days": CHECK_INTERVAL_DAYS,
    }
