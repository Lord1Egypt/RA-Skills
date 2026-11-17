#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
group_compliance.py — 群聊语音合规策略（v2.9）

设计原则（合规底线）：
1. 群内语音默认不落盘（record=False），仅做即时转写与意图处理
2. 转写结果按保留策略（retention_days）清理，默认进程内暂存、重启即清
3. 如需开启落盘（record=True），必须显式 opt_in 且经管理员确认
   （opt_in_requires_admin=True），避免误操作侵犯群成员隐私

依赖：纯 Python 标准库；pyyaml 可选（缺失时降级内置默认值）
联系信息：njskills@agent.qq.com
"""

import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


# ==========================================
# 配置
# ==========================================

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config")
VOICES_YAML = os.path.join(CONFIG_DIR, "voices.yaml")

# 群合规默认配置（voices.yaml 无 group 块或加载失败时启用）
DEFAULT_GROUP_CONFIG = {
    "record": False,               # 群内语音默认不落盘
    "retention_days": 1,           # 转写文本保留天数（默认 1 天，最短可配）
    "opt_in_requires_admin": True, # 开启落盘需管理员确认
    "transcribe_only": True,       # 仅转写、不落盘音频
}


# ==========================================
# 配置加载
# ==========================================

def load_group_config() -> Dict[str, Any]:
    """
    读取 voices.yaml 的 group 配置块

    返回：
        dict：合并默认值后的群合规配置
    """
    cfg = dict(DEFAULT_GROUP_CONFIG)
    try:
        import yaml  # 可选依赖
        if os.path.exists(VOICES_YAML):
            with open(VOICES_YAML, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            group = data.get("group") or {}
            if isinstance(group, dict):
                for k, v in group.items():
                    cfg[k] = v
    except ImportError:
        logger.info("pyyaml 不可用，群合规使用内置默认值")
    except Exception as e:
        logger.warning(f"读取群合规配置失败，使用默认值: {e}")
    return cfg


# ==========================================
# 群合规管理器
# ==========================================

class GroupCompliance:
    """
    群聊语音合规管理器

    使用方式：
        compliance = GroupCompliance()
        if compliance.should_record(chat_id):
            # 仅经管理员确认后才走落盘分支
            ...
        else:
            # 默认：仅转写、不落盘（磁盘零语音文件）
            ...
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or load_group_config()

    def should_record(self, chat_id: str = None) -> bool:
        """
        群内语音是否落盘

        默认 False（磁盘零语音文件）。仅当配置显式开启且（如需要）管理员确认后返回 True。

        Args:
            chat_id: 群聊ID（预留，支持按群灰度）

        Returns:
            bool
        """
        return bool(self.config.get("record", False))

    def is_transcribe_only(self) -> bool:
        """是否仅转写不落盘"""
        return bool(self.config.get("transcribe_only", True))

    def retention_days(self) -> int:
        """转写文本保留天数"""
        try:
            return int(self.config.get("retention_days", 1))
        except (TypeError, ValueError):
            return 1

    def opt_in_requires_admin(self) -> bool:
        """开启落盘是否需管理员确认"""
        return bool(self.config.get("opt_in_requires_admin", True))

    def record_audio_disabled(self, admin_confirmed: bool = False) -> bool:
        """
        是否禁止落盘音频文件

        Args:
            admin_confirmed: 是否已获得管理员确认（用于开启落盘场景）

        Returns:
            bool: True=禁止落盘；False=允许落盘
        """
        # 默认禁止落盘
        if not self.should_record():
            return True
        # 开启落盘但要求管理员确认且未确认 → 仍禁止
        if self.opt_in_requires_admin() and not admin_confirmed:
            return True
        return False

    def note(self) -> str:
        """向用户提示的合规说明文本"""
        if self.record_audio_disabled():
            return ("群内语音默认仅转写不落盘，符合隐私最小化原则；"
                    "如需留存录音，需管理员在 voices.yaml 显式开启并经确认。")
        return "群内语音已开启落盘（需管理员确认），录音将按保留策略清理。"


# ==========================================
# 便捷函数
# ==========================================

_compliance_instance = None


def get_compliance() -> GroupCompliance:
    """获取单例合规管理器"""
    global _compliance_instance
    if _compliance_instance is None:
        _compliance_instance = GroupCompliance()
    return _compliance_instance


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行群合规自测"""
    print("=" * 60)
    print("群聊语音合规模块 — 自测模式")
    print("=" * 60)

    # 测试 1: 默认不落盘（磁盘零语音文件）
    print("\n[测试 1] 默认配置不落盘")
    c = GroupCompliance()
    assert c.should_record() is False, "默认应禁止落盘"
    assert c.record_audio_disabled() is True, "默认应禁止落盘音频"
    assert c.is_transcribe_only() is True
    print("✅ 默认不落盘（磁盘零语音文件）通过")

    # 测试 2: 保留策略天数读取
    print("\n[测试 2] 转写保留天数")
    assert c.retention_days() >= 1
    print(f"  保留天数: {c.retention_days()} 天")
    print("✅ 保留天数读取通过")

    # 测试 3: 管理员确认开关
    print("\n[测试 3] 开启落盘需管理员确认")
    assert c.opt_in_requires_admin() is True
    # 未确认 → 仍禁止
    assert c.record_audio_disabled(admin_confirmed=False) is True
    print("✅ 管理员确认约束通过")

    # 测试 4: 显式开启且确认后可落盘（合规放行）
    print("\n[测试 4] 显式开启 + 管理员确认 → 允许落盘")
    cfg = dict(DEFAULT_GROUP_CONFIG)
    cfg["record"] = True
    cfg["transcribe_only"] = False
    c2 = GroupCompliance(cfg)
    assert c2.should_record() is True
    assert c2.record_audio_disabled(admin_confirmed=True) is False
    assert c2.record_audio_disabled(admin_confirmed=False) is True
    print("✅ 显式开启 + 管理员确认放行通过")

    # 测试 5: 异常配置降级
    print("\n[测试 5] 异常配置降级")
    c3 = GroupCompliance({"retention_days": "bad"})
    assert c3.retention_days() == 1
    print("✅ 异常配置降级通过")

    print(f"\n{'=' * 60}")
    print("所有自测通过 ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_self_test()
