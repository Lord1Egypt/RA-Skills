"""64 卦推演引擎 — 领域无关"""
import json
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parent.parent
HEX_TABLE_PATH = ROOT / "data" / "hexagram_64.json"

_TABLE = None


def _load_table() -> Dict:
    global _TABLE
    if _TABLE is None:
        with open(HEX_TABLE_PATH, encoding="utf-8") as f:
            _TABLE = json.load(f)
    return _TABLE


def yao_to_bits(yao_dict: Dict[str, float], threshold: float = 0.5,
                order=None) -> str:
    """6 维爻位 → 6 位二进制字符串

    Args:
        yao_dict: {"攻防": 0.6, "士气": 0.5, ...}
        threshold: 阴阳判定阈值
        order: 爻位排序（默认按经验库格式：上爻→下爻）

    Returns:
        "111011" 这样的字符串
    """
    if order is None:
        order = ["赔率", "交锋", "主客场", "伤停", "士气", "攻防"]
    bits = ""
    for k in order:
        v = yao_dict.get(k, 0.5)
        bits += "1" if v > threshold else "0"
    return bits


def lookup(bits: str) -> Dict:
    """查 64 卦表"""
    table = _load_table()
    return table.get(bits, {
        "bits": bits,
        "gua_name": "未知",
        "football_meaning": "无对应卦象",
        "verdict": "数据不足，慎入",
    })


def yang_count(bits: str) -> int:
    return bits.count("1")


def changing_lines(yao_dict: Dict[str, float], lo=0.4, hi=0.6) -> int:
    """变爻数 — 临界带的爻位个数"""
    return sum(1 for v in yao_dict.values() if lo <= v <= hi)


def risk_count(yao_dict: Dict[str, float], lo=0.3, hi=0.85) -> int:
    """风险点 — 极端值个数"""
    return sum(1 for v in yao_dict.values() if v < lo or v > hi)


def recognize(yao_dict: Dict[str, float]) -> Dict:
    """完整推演：爻位 → 卦象 → 综合"""
    bits = yao_to_bits(yao_dict)
    hex_data = lookup(bits)
    yang = yang_count(bits)
    return {
        "bits": bits,
        "yang_count": yang,
        "yin_count": 6 - yang,
        "hexagram_name": hex_data.get("gua_name"),
        "football_meaning": hex_data.get("football_meaning", ""),
        "verdict": hex_data.get("verdict", ""),
        "yao_summary": yao_dict,
        "changing_count": changing_lines(yao_dict),
        "risk_count": risk_count(yao_dict),
    }
