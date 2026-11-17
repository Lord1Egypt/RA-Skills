# uas-ops-checker · 无人机运营合规分类判定器

> AI-assisted decision-support CLI. **NOT legal advice**, **not a compliance proof** — verify against official texts. Text verified: 2026-09-26.


## What it does
Classifies a UAS operation grade per official rules: **《无人驾驶航空器飞行管理暂行条例》(国务院令761号, 2024-01-01施行) 第6/12/16/31/32条 + CCAR-92** (clause numbers pending manual verification — see `clause_review_checklist` in the output; official texts prevail).

- Grades: 微型 / 轻型 / 小型 / 中型 / 大型.
- **Insufficient input → strict presumption (从严推定)**: with only one weight argument the tool returns the **most obligation-heavy grade** among the physically possible ones, states the possible range in `warnings`, and sets `rc=1`. It never silently returns a lenient grade.
- **Out of scope**: airspace class (friendly / controlled), operator qualifications, insurance, foreign-related or commercial-operation extra review.

## Install & run (zero-dependency, Python 3.8+)
```bash
python uas-ops-checker.py --demo                     # 3 built-in smoke cases
python uas-ops-checker.py --mtow 5                    # single arg → strict presumption, rc=1
python uas-ops-checker.py --mtow 5 --empty_weight 4    # complete args → 轻型, rc=0
```

## Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `grade_basis`, `possible_grades`, `warnings`, `clause_review_checklist`, and `aigc_mark` (GB 45438-2025 metadata; `is_generated: true`, label basis noted as pending verification).

Real excerpt (`python uas-ops-checker.py --mtow 5`, arrays folded for readability; values verbatim):

```json
{
  "tool": "uas-ops-checker",
  "input": {"mtow": "5"},
  "result": {
    "grade": "小型",
    "grade_basis": "从严推定（输入不完整）",
    "possible_grades": ["微型", "轻型", "小型"],
    "obligations": ["操控员执照（视具体机型）", "实名登记", "强制责任保险", "在适飞空域外飞行需申请"],
    "evidence": ["暂行条例 第6条", "暂行条例 第16条", "CCAR-92"],
    "warnings": ["…3 条（输入不完整 / 分类不确定按从严推定 / 该等级需额外审查）"]
  },
  "rc": 1,
  "clause_review_checklist": ["…7 条（条款号 + 用途 + 待人工核对）"],
  "aigc_mark": {"standard": "GB 45438-2025", "is_generated": true, "generator": "uas-ops-checker@SynomosAI",
                "content_type": "decision_support_output", "label_note": "标识口径待核"}
}
```

## Theory hook (证据语义澄清)
分类即空中治理的出生登记。依 LGD 证据语义界定：**Evidence（证据）＝治理状态转换的可验证依据，非行为日志**；识别信息报送 / 飞行动态上传属**行为日志**，本工具不把日志当证据。域站位件：TH-UAS-001。

## 条款号待人工核对清单 / Clause review checklist
| 条款 / 数值 | 用途 | 状态 |
|---|---|---|
| 暂行条例 第6条 | 分类（微型/轻型/小型/中型/大型）规则来源 | 待人工核对 |
| 暂行条例 第12条 | 微型/轻型的实名登记与适飞空域内免执照义务 | 待人工核对 |
| 暂行条例 第16条 | 小型的执照/登记/保险义务（原实现引用） | 待人工核对 |
| 暂行条例 第31条 / 第32条 | 中型/大型的运营合格证、适航、飞行活动申请 | 待人工核对 |
| CCAR-92 | 分类参数与运行要求 | 待人工核对 |
| GB 45438-2025 | AIGC 标识字段 `aigc_mark` | 待人工核对 |
| 阈值 0.25 / 4 / 7 / 15 / 25 / 150 (kg) | 分类级联断点取值 | 待人工核对 |

## Pointers (verified live 2026-09-26)
- Theory ledger repo: https://github.com/zhaoxinghua09-cell/lgd-theory
- Reference implementation: https://github.com/zhaoxinghua09-cell/uibc-core
- Skill library index: https://github.com/zhaoxinghua09-cell/agent-skills
- LGD 理论总账 REGISTRY 在线页：(地址待补) · UAS 域速查页：(地址待补)

## License & attribution
**Layered licence — the code licence does NOT cover the docs or the theory text.**

| Layer | Carrier | Licence |
|---|---|---|
| Code | `uas-ops-checker.py` | **MIT** |
| Docs & theory text | this `README.md`, `SKILL.md`, the 「理论依据」 section and all theory wording | **Not covered by MIT**: all rights reserved |

```
© 2026 SynomosAI. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : uibc-core = Apache-2.0 (see repo LICENSE)
                    本文本与理论表述不在 Apache-2.0 覆盖范围内
引用格式 (cite as)      : uibc-core/CITATION.cff · concept DOI 10.5281/zenodo.22821834
首次公开锚 (first public): 2026-09-17 13:31:45 UTC (commit cb6f11b)
                    外锚 (external anchor): Sigstore Rekor logIndex 2883389783
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**。）
**本包补充**：`uas-ops-checker.py` = MIT；本 `README.md` / `SKILL.md` 及其中理论文本不在任何代码许可覆盖范围内。

## 家族合集
| 域 | 工具 | 大使 | 目录 |
|---|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/uas-ops-checker |
| AUT 驾驶 | aut-grade-checker | 诺卫 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/aut-grade-checker |
| DAT 数据 | data-grade-checker | 诺源 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/data-grade-checker |
| BIO 生物 | hgrac-route-checker | 诺康 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/hgrac-route-checker |
| FIN 金融 | fin-ai-classifier | 诺丰 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/fin-ai-classifier |
| LAW 法律 | evid-four-check | 诺律 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/evid-four-check |

---
诺卫@UAS 域首席发声人 · TH-UAS-001 · SynomosAI（AI 辅助生成，非自然人）
