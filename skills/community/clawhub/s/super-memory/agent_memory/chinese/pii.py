"""Chinese PII detection — extended patterns for Chinese personal information."""
from __future__ import annotations

import re
from typing import Optional


_CHINESE_PII_PATTERNS = {
    "id_card_cn": {
        "pattern": re.compile(r'[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]'),
        "placeholder": "[身份证号]",
        "description": "中国大陆居民身份证号",
    },
    "phone_cn": {
        "pattern": re.compile(r'1[3-9]\d{9}'),
        "placeholder": "[手机号]",
        "description": "中国大陆手机号",
    },
    "phone_cn_landline": {
        "pattern": re.compile(r'(?:0[1-9]\d{1,2}-)?\d{7,8}'),
        "placeholder": "[座机号]",
        "description": "中国大陆座机号",
    },
    "bank_card_cn": {
        "pattern": re.compile(r'(?:62|4[0-9]|5[1-5]|6[2-6])\d{14,17}'),
        "placeholder": "[银行卡号]",
        "description": "中国银行卡号",
    },
    "email_cn": {
        "pattern": re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
        "placeholder": "[电子邮箱]",
        "description": "电子邮箱地址",
    },
    "passport_cn": {
        "pattern": re.compile(r'[A-Z]{1,2}\d{6,9}'),
        "placeholder": "[护照号]",
        "description": "中国护照号",
    },
    "military_id": {
        "pattern": re.compile(r'[军]\d{7}|[武]\d{7}'),
        "placeholder": "[军官证号]",
        "description": "军官证号",
    },
    "hk_macau_pass": {
        "pattern": re.compile(r'[HMhm]\d{8,10}'),
        "placeholder": "[港澳通行证号]",
        "description": "港澳通行证号",
    },
    "tw_pass": {
        "pattern": re.compile(r'[Tt]\d{8,10}'),
        "placeholder": "[台湾通行证号]",
        "description": "台湾通行证号",
    },
    "social_credit_code": {
        "pattern": re.compile(r'[0-9A-HJ-NP-RTU-Y]{2}\d{6}[0-9A-HJ-NP-RTU-Y]{10}'),
        "placeholder": "[统一社会信用代码]",
        "description": "统一社会信用代码",
    },
    "cn_address": {
        "pattern": re.compile(r'[\u4e00-\u9fff]{1,4}(?:省|市|自治区|特别行政区)[\u4e00-\u9fff]{1,6}(?:市|区|县|旗)[\u4e00-\u9fff]{1,10}(?:路|街|道|巷|弄|号)'),
        "placeholder": "[地址]",
        "description": "中国地址",
    },
    "cn_name": {
        "pattern": re.compile(r'(?:姓|名叫?|称为?|叫作?|先生|女士|同志|同学)[：:]*[\u4e00-\u9fff]{2,4}'),
        "placeholder": "[姓名]",
        "description": "中文姓名（上下文匹配）",
    },
}


class ChinesePIIDetector:
    def __init__(self, categories: list[str] = None):
        self._patterns = _CHINESE_PII_PATTERNS
        if categories:
            self._patterns = {k: v for k, v in self._patterns.items() if k in categories}

    def detect(self, text: str) -> list[dict]:
        if not text:
            return []
        findings = []
        for category, config in self._patterns.items():
            for match in config["pattern"].finditer(text):
                findings.append({
                    "category": category,
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "description": config["description"],
                })
        return sorted(findings, key=lambda x: x["start"])

    def redact(self, text: str, categories: list[str] = None) -> str:
        if not text:
            return text
        patterns = self._patterns
        if categories:
            patterns = {k: v for k, v in patterns.items() if k in categories}

        result = text
        for category, config in patterns.items():
            result = config["pattern"].sub(config["placeholder"], result)
        return result

    def get_categories(self) -> list[dict]:
        return [
            {"name": k, "description": v["description"], "placeholder": v["placeholder"]}
            for k, v in self._patterns.items()
        ]

    def risk_score(self, text: str) -> float:
        findings = self.detect(text)
        if not findings:
            return 0.0
        high_risk = {"id_card_cn", "bank_card_cn", "phone_cn", "email_cn"}
        score = 0.0
        for f in findings:
            if f["category"] in high_risk:
                score += 0.3
            else:
                score += 0.1
        return min(1.0, score)
