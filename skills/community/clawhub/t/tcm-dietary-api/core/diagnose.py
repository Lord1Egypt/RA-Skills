"""
core/diagnose.py — 辨证引擎 API 客户端

POST /api/diagnose → 症状 → 证型 + 食疗方案

Usage:
    from core.diagnose import diagnose
    result = diagnose(["头晕", "乏力", "失眠"])  # 免费
"""

import json
import urllib.request
import urllib.error
from . import API_BASE, api_key, _api_request


def diagnose(symptoms: list, language: str = "zh", gender: str = "") -> dict:
    """
    TCM 辨证分析.

    将症状和可选性别通过 HTTPS 发送到 api.tcmplate.com 处理.
    请勿在 symptoms 中包含姓名、身份证号等个人身份信息.

    Args:
        symptoms: 症状列表, 建议 3 个以上用于准确辨证
        language: "zh" (中文) 或 "en" (English)
        gender: 可选, "male" / "female" / ""

    Returns:
        {
            "constitution": {"type": "阳虚质", "name_en": "Yang Deficiency", "confidence": 0.89},
            "syndrome": {"pattern": "心肾不交", "organ": "心"},
            "recommended_foods": [...],
            "foods_to_avoid": [...],
            "tea_recipes": [...],
            "exercises": [...],
            "meal_plan": [...],
        }

    Raises:
        RuntimeError: API 返回非 200
        urllib.error.HTTPError: 429 = 日限额, 403 = 无效 key
    """
    return _api_request("POST", "/api/diagnose", {
        "symptoms": symptoms,
        "language": language,
        "gender": gender,
    })
