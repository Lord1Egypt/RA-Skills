"""privacy/patterns.py — 统一 PII 模式定义

将 analyzer.py 和 compliance_guard.py 中的 PII 正则模式合并为单一来源。
每个模式包含 name, pattern, category, risk_level, description。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class PIIPattern:
    """单个 PII 检测模式的定义。"""
    name: str
    pattern: str
    category: str          # pii / financial / health / credential / emotional
    risk_level: str        # low / medium / high / critical
    description: str = ""

    @property
    def compiled(self) -> re.Pattern:
        """返回编译后的正则对象。"""
        return re.compile(self.pattern)


# ──────────────────────────────────────────────
# 统一模式注册表
# ──────────────────────────────────────────────

_ALL_PATTERNS: list[PIIPattern] = [
    # ── PII ──────────────────────────────────
    PIIPattern(
        name="phone_number",
        pattern=r'1[3-9]\d{9}|\+86[-\s]?\d{11}',
        category="pii",
        risk_level="medium",
        description="中国手机号码（含国际格式）",
    ),
    PIIPattern(
        name="email",
        pattern=r'[\w.+-]+@[\w-]+\.[\w.-]+',
        category="pii",
        risk_level="medium",
        description="电子邮件地址",
    ),
    PIIPattern(
        name="id_card",
        pattern=r'\b\d{17}[\dXx]\b',
        category="pii",
        risk_level="critical",
        description="中国居民身份证号",
    ),
    PIIPattern(
        name="bank_card",
        pattern=r'\b(4\d{15}|5[1-5]\d{14}|6\d{15,18})\b',
        category="pii",
        risk_level="critical",
        description="银行卡号（Visa/MasterCard/UnionPay 前缀匹配）",
    ),
    PIIPattern(
        name="credit_card",
        pattern=r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        category="pii",
        risk_level="critical",
        description="信用卡号",
    ),

    # ── Financial ────────────────────────────
    PIIPattern(
        name="salary",
        pattern=r'(?:薪资|工资|薪水|salary|compensation)(?:\s*(?:是|:|：))?\s*[\d,.万]+',
        category="financial",
        risk_level="high",
        description="薪资信息",
    ),
    PIIPattern(
        name="budget",
        pattern=r'(?:预算|budget|revenue|利润|profit)(?:\s*(?:是|:|：))?\s*\d',
        category="financial",
        risk_level="medium",
        description="预算/营收信息",
    ),
    PIIPattern(
        name="pricing",
        pattern=r'(?:价格|定价|pricing|报价|quote)(?:\s*(?:是|:|：))?\s*\d',
        category="financial",
        risk_level="medium",
        description="定价/报价信息",
    ),
    PIIPattern(
        name="monetary_amount",
        pattern=r'[¥$€£]\s*\d[\d,]+',
        category="financial",
        risk_level="medium",
        description="货币金额",
    ),

    # ── Health ───────────────────────────────
    PIIPattern(
        name="medical",
        pattern=r'(?i)(诊断|diagnos|疾病|disease|症状|symptom|药物|medication|处方|prescription|手术|住院)',
        category="health",
        risk_level="high",
        description="医疗诊断/药物信息",
    ),
    PIIPattern(
        name="mental_health",
        pattern=r'(?i)(抑郁|depress|焦虑|anxiety|心理|psycholog|治疗|therapy)',
        category="health",
        risk_level="critical",
        description="心理健康信息",
    ),

    # ── Credential ───────────────────────────
    PIIPattern(
        name="password",
        pattern=r'(?:password|密码|passwd|pwd)(?:\s*是)?\s*[:：=]\s*\S+',
        category="credential",
        risk_level="critical",
        description="密码/口令",
    ),
    PIIPattern(
        name="api_key",
        pattern=r'(?:api[_-]?key|secret|token)(?:\s*是)?\s*[:：=]\s*\S{8,}',
        category="credential",
        risk_level="critical",
        description="API 密钥/令牌",
    ),
    PIIPattern(
        name="auth_token",
        pattern=r'(?:Bearer|Authorization)\s+[\w.-]+',
        category="credential",
        risk_level="critical",
        description="认证令牌",
    ),

    # ── Emotional ────────────────────────────
    PIIPattern(
        name="deep_emotion",
        pattern=r'(?:我感到|我觉得|I feel|I think).{0,20}(?:孤独|lonely|绝望|hopeless|崩溃|breakdown)',
        category="emotional",
        risk_level="high",
        description="深层情感表达",
    ),
    PIIPattern(
        name="therapy",
        pattern=r'(?:心理咨询|therap|精神科|psychiatr)',
        category="emotional",
        risk_level="high",
        description="心理咨询/精神科相关",
    ),
]


# ──────────────────────────────────────────────
# 公共 API
# ──────────────────────────────────────────────

def get_all_patterns() -> list[PIIPattern]:
    """返回所有已注册的 PII 模式。"""
    return list(_ALL_PATTERNS)


def get_patterns_by_category(category: str) -> list[PIIPattern]:
    """按类别筛选模式。

    Args:
        category: 类别名（pii / financial / health / credential / emotional）

    Returns:
        匹配类别的模式列表。
    """
    return [p for p in _ALL_PATTERNS if p.category == category]
