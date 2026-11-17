"""
Layer 1: 输入适配层 (Input Adapter)

职责：
- 校验用户输入的类型、范围、格式
- 将原始输入（字符串/字典/JSON）规范化为 UserInput Schema
- 拒绝一切不合规输入，不让脏数据进入下游

这是 Triangulate 的"防腐层"第一关。
"""
from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional

from schemas import UserInput

logger = logging.getLogger(__name__)


# ============================================================================
# 关键词到模板的映射表（来自原 SKILL.md）
# ============================================================================

KEYWORD_TEMPLATE_MAP: Dict[str, str] = {
    "选型": "T-01",
    "对比": "T-01",
    "方案": "T-01",
    "框架": "T-08",
    "工具": "T-08",
    "诊断": "A-01",
    "调试": "A-01",
    "问题": "A-01",
    "故障": "A-01",
    "bug": "A-01",
    "设计": "T-03",
    "架构": "T-03",
    "系统": "T-03",
    "重构": "T-10",
    "数据": "A-02",
    "分析": "A-02",
    "报告": "A-02",
    "指标": "A-02",
    "风险": "A-04",
    "安全": "T-02",
    "合规": "A-04",
    "战略": "B-01",
    "规划": "B-01",
    "路线图": "B-01",
    "竞品": "B-02",
    "竞争": "B-02",
    "市场": "B-04",
    "产品": "B-03",
    "体验": "C-04",
    "交互": "C-04",
    "投资": "B-05",
    "估值": "B-05",
    "收购": "B-09",
    "定价": "B-06",
    "收入": "B-06",
    "变现": "B-07",
    "团队": "H-01",
    "招聘": "H-06",
    "人事": "H-01",
    "爬虫": "E-01",
    "反爬": "E-01",
    "数据采集": "E-01",
    "渗透": "E-02",
    "漏洞": "E-02",
    "安全测试": "E-02",
    "逆向": "E-03",
    "反编译": "E-03",
    "脱壳": "E-03",
    "大模型": "E-04",
    "Agent": "E-04",
    "LLM": "E-04",
    "Prompt": "E-04",
    "量化": "E-05",
    "交易": "E-05",
    "回测": "E-05",
    "因子": "E-05",
    "小说": "E-06",
    "写作": "C-01",
    "剧本": "E-06",
    "故事": "E-06",
    "短视频": "E-07",
    "视频": "E-07",
    "谈判": "H-02",
    "冲突": "H-02",
    "沟通": "H-02",
    "职业": "P-01",
    "学习": "P-02",
    "成长": "P-02",
    "健康": "P-05",
    "精力": "P-05",
    "习惯": "P-05",
    "生活": "P-04",
    "决策": "P-04",
    "选择": "P-04",
    "预测": "S-01",
    "比赛": "S-01",
    "赛事": "S-01",
    "内容": "C-01",
    "营销": "C-02",
    "品牌": "C-03",
    "定位": "C-03",
}


# ============================================================================
# 输入适配器
# ============================================================================

class InputAdapter:
    """输入适配器 — 将各种原始输入规范化为 UserInput Schema"""

    def __init__(self, strict_mode: bool = True, extra_keywords: Optional[Dict[str, str]] = None):
        """
        Args:
            strict_mode: True=拒绝不合规输入抛异常; False=尽力修复并警告
            extra_keywords: 额外的关键词→模板映射（合并到 KEYWORD_TEMPLATE_MAP）
        """
        self.strict_mode = strict_mode
        self._keyword_map: Dict[str, str] = dict(KEYWORD_TEMPLATE_MAP)
        if extra_keywords:
            self._keyword_map.update(extra_keywords)

    def register_keywords(self, mapping: Dict[str, str]) -> None:
        """动态注册额外的关键词→模板映射。"""
        if not isinstance(mapping, dict):
            logger.warning(f"register_keywords() 需要 dict 参数，收到 {type(mapping)}")
            return
        self._keyword_map.update(mapping)
        logger.info(f"已注册 {len(mapping)} 个额外关键词→模板映射")

    def validate(self, raw_input: Any) -> UserInput:
        """
        校验并规范化输入。

        Args:
            raw_input: 用户输入，支持：
                - str: 自然语言描述
                - dict: 包含 task_description 等字段
                - UserInput: 已是标准格式

        Returns:
            UserInput: 校验后的标准输入

        Raises:
            InputValidationError: 输入不合法且 strict_mode=True
        """
        # 已是标准格式 → 重新校验一遍
        if isinstance(raw_input, UserInput):
            return self._revalidate(raw_input)

        # 字符串 → 解析并推断元数据
        if isinstance(raw_input, str):
            return self._parse_string(raw_input)

        # 字典 → 校验字段
        if isinstance(raw_input, dict):
            return self._parse_dict(raw_input)

        raise InputValidationError(
            f"不支持的输入类型: {type(raw_input).__name__}",
            raw_input=raw_input,
        )

    # ------------------------------------------------------------------
    # 内部解析
    # ------------------------------------------------------------------

    def _revalidate(self, user_input: UserInput) -> UserInput:
        """重新校验已有 UserInput（逻辑一致性检查）。"""
        # 逻辑一致性检查：低重要性 + 要求执行层 → 警告
        if user_input.importance < 4 and user_input.require_execution_layer:
            logger.warning(
                f"重要性为 {user_input.importance} 但要求执行层，"
                f"建议降低配置档次以节约资源"
            )

        # 逻辑一致性检查：高重要性 + 不需要管理层 → 警告
        if user_input.importance >= 4 and not user_input.require_management_layer:
            logger.warning(
                f"重要性为 {user_input.importance} 但未启用管理层，"
                f"复杂任务建议启用管理层拆解"
            )

        # 关键词与模板一致性检查
        if user_input.keywords and not user_input.preferred_templates:
            # 有关键词但未推断出模板 → 可能是新领域关键词
            logger.debug(
                f"关键词 {user_input.keywords} 未能匹配到预置模板，"
                f"将使用视角自创建模式"
            )

        # 超时合理性检查
        if user_input.importance >= 4 and user_input.max_total_timeout_seconds < 120:
            logger.warning(
                f"高重要性任务但超时设置过短 "
                f"({user_input.max_total_timeout_seconds}s)，"
                f"建议至少 120s"
            )

        return user_input

    def _parse_string(self, text: str) -> UserInput:
        """从自然语言字符串解析"""
        text = text.strip()
        if not text:
            raise InputValidationError("输入不能为空", raw_input=text)

        keywords = self._extract_keywords(text)
        templates = self._infer_templates(text)

        return UserInput(
            task_description=text,
            keywords=keywords,
            preferred_templates=templates,
            importance=self._infer_importance(text),
        )

    def _parse_dict(self, data: Dict[str, Any]) -> UserInput:
        """从字典解析并校验"""
        try:
            return UserInput(**data)
        except Exception as e:
            if self.strict_mode:
                raise InputValidationError(
                    f"输入字典校验失败: {e}",
                    raw_input=data,
                ) from e
            # 宽松模式：只取已知字段
            known_fields = set(UserInput.model_fields.keys())
            dropped_fields = set(data.keys()) - known_fields
            if dropped_fields:
                logger.warning(
                    f"以下字段不在 UserInput Schema 中，已被丢弃: {sorted(dropped_fields)}"
                )
            safe_data = {k: v for k, v in data.items() if k in known_fields}
            return UserInput(**safe_data)

    # ------------------------------------------------------------------
    # 智能推断
    # ------------------------------------------------------------------

    def _extract_keywords(self, text: str) -> List[str]:
        """从文本中提取领域关键词"""
        found = []
        for keyword in self._keyword_map:
            if keyword in text:
                found.append(keyword)
        return list(dict.fromkeys(found))  # 去重保序

    def _infer_templates(self, text: str) -> List[str]:
        """从文本推断适用的视角模板"""
        templates = []
        seen = set()
        for keyword, template in self._keyword_map.items():
            if keyword in text and template not in seen:
                templates.append(template)
                seen.add(template)
        return templates[:3]  # 最多推荐 3 个

    def _infer_importance(self, text: str) -> int:
        """从文本推断任务重要性 (1-5)"""
        importance_signals = {
            "关键": 5,
            "重要": 4,
            "核心": 5,
            "紧急": 5,
            "必须": 4,
            "P0": 5,
            "P1": 4,
            "选型": 4,
            "架构": 4,
            "安全": 5,
            "故障": 5,
            "排查": 3,
            "了解": 2,
            "看看": 2,
            "随便": 1,
        }
        scores = []
        for signal, score in importance_signals.items():
            if signal in text:
                scores.append(score)

        if scores:
            return max(scores)
        return 3  # 默认中等重要性


# ============================================================================
# 异常（re-export from exceptions.py）
# ============================================================================
from exceptions import InputValidationError  # noqa: F401
