"""取用忌（Pipeline Step 4）。

依据格局确定理论用神/忌神（五行层面）。阴阳局/组合用神/五种神因 vault 无量化权重，
标 needs_formalization，不输出伪精细结论。
"""
from __future__ import annotations

from evidence import EvidenceRecord, load_vault_text, load_by_canonical
from paipan import GAN_WX, GAN

WX_NAME = ["木", "火", "土", "金", "水"]
YONGJI_RULES = ["YONGJI_THEORY"]


def _wx_list(idxs):
    return [WX_NAME[i] for i in idxs]


def yongji(pattern_name: str, day_master: int, vault_base: str | None = None):
    day_wx = GAN_WX[day_master]
    if pattern_name.startswith("身弱"):
        yong = [day_wx, (day_wx - 1) % 5]          # 比劫 + 印
        ji = [x for x in range(5) if x not in yong]
    elif pattern_name.startswith("身旺"):
        ji = [day_wx, (day_wx - 1) % 5]
        yong = [x for x in range(5) if x not in ji]
    elif pattern_name == "从弱":
        yong = [(day_wx + 2) % 5, (day_wx + 1) % 5, (day_wx + 3) % 5]  # 从克泄耗
        ji = [day_wx, (day_wx - 1) % 5]
    else:  # 从旺
        yong = [day_wx, (day_wx - 1) % 5]
        ji = [(day_wx + 2) % 5, (day_wx + 1) % 5, (day_wx + 3) % 5]

    vault_path, vault_text = load_by_canonical("天星密派 — 核心方法·格局七神阴阳局", vault_base)
    vault_ref = vault_path if vault_text else "VAULT_UNREADABLE"

    out = {
        "theory_yong": _wx_list(yong),
        "theory_ji": _wx_list(ji),
        "day_master": GAN[day_master],
    }
    rec = EvidenceRecord(
        step="yongji",
        input={"pattern": pattern_name, "day_master": GAN[day_master]},
        rules_used=YONGJI_RULES,
        intermediate_reasoning=(f"格局={pattern_name}；日主{GAN[day_master]}（{WX_NAME[day_wx]}）。"
                                f"理论用神={_wx_list(yong)}，理论忌神={_wx_list(ji)}。"),
        opposing_evidence="组合用神/五种神（理论·组合·阴阳）vault 无统一量化权重，未形式化。",
        output=out,
        confidence=0.85,
        vault_source=vault_ref,
        needs_formalization=True,
    )
    return rec
