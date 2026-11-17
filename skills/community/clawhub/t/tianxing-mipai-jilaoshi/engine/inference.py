"""体系融合断语（Pipeline Step 7，天星密派统一口径）。

把前面各步的确定性结果（格局 / 用忌 / 大运 / 流年）按天星密派主干 + 补充融合为统一断语。
硬性约束：只翻译 / 组织已有 evidence_chain，不创造新结论。
六亲应事十二诀 / 应事律 / 发散律 因 vault 无统一量化权重，标 needs_formalization。
"""
from __future__ import annotations

from evidence import EvidenceRecord, load_by_canonical, search_atoms

INFER_RULES = ["TX-INFER-001", "TX-INFER-002", "TX-INFER-003", "TX-TERM-000"]

INFER_CANON = [
    "天星密派 — 六亲十神应事十二诀",
    "天星密派 — 能量流·计算规律·空亡论",
    "天星密派 — 应事律·发散律与名人案例",
    "天星密派 — 全书总纲与体系地图",
]


def inference(records: list, theme: str = "通用全览", vault_base: str | None = None):
    by_step = {r.step: r for r in records}
    pat = by_step["pattern"].output
    yj = by_step["yongji"].output
    dy = by_step["dayun"].output
    ln = by_step["liunian"].output

    # 加载天星密派补充知识仅用于追溯，不参与结论生成
    paths = []
    for c in INFER_CANON:
        p, t = load_by_canonical(c, vault_base)
        paths.append(p if t else "VAULT_UNREADABLE")
    vault_ref = ";".join(paths)

    # 原子库速查层：断事前先检索与主题相关的极简规则，作为快速校验
    atoms, atom_path = search_atoms(theme, vault_base)
    atom_ref = atom_path if atoms else "ATOM_LIB_UNREADABLE"
    quickref = []
    for a in atoms:
        b = a["body"]
        quickref.append(
            f"【{a['domain']}】{a['title']}：{b[:48]}{'…' if len(b) > 48 else ''}"
            f"（边界：{a['boundary']}；反例：{a['counter']}）来源 {a['source']}"
        )
    vault_ref = vault_ref + " | 原子库:" + atom_ref

    fused = {
        "theme": theme,
        "pattern": pat["pattern"],
        "theory_yong": yj["theory_yong"],
        "theory_ji": yj["theory_ji"],
        "current_dayun": dy.get("current_label"),
        "near_liunian": [
            f"{it['year']}{it['label']}:{','.join(it['actions'])}"
            for it in ln["items"] if it["actions"]
        ],
        "remark": "六亲应事十二诀 / 应事律 / 发散律无统一量化权重，未形式化，交人工或后续规则形式化。",
        "atom_quickref": quickref,
    }
    reasoning = (
        f"主干（格局={pat['pattern']}，用神={yj['theory_yong']}，忌神={yj['theory_ji']}）"
        f"结合大运 {dy.get('current_label')} 与近五年流年作用，按天星密派口径融合。"
        f"六亲 / 应事律细分标 NEEDS_RULE_FORMALIZATION。"
        f"断语生成前已检索原子库速查层命中 {len(atoms)} 条规则（见 atom_quickref），"
        f"须与速查层交叉校验后再组织结论。"
    )

    rec = EvidenceRecord(
        step="inference",
        input={"theme": theme, "steps": list(by_step.keys())},
        rules_used=INFER_RULES,
        intermediate_reasoning=reasoning,
        opposing_evidence="六亲应事十二诀、应事律、发散律、阴阳神五种神在 vault 中无统一量化权重，本步不产出细分断语。",
        output=fused,
        confidence=0.8,
        vault_source=vault_ref,
        needs_formalization=True,
    )
    return rec
