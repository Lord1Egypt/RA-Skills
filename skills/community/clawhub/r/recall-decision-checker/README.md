# recall-decision-checker · 医疗器械召回级别判定器

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> AI-assisted decision-support CLI. NOT legal advice, **not a compliance proof** — verify against official texts. Text verified: 2026-09-26.

## What it does
Determines the **recall level and notification deadline** per official rules: **《医疗器械召回管理办法》(总局令 第29号)** — based on `harm_level` (severe/reversible/none, required) and `use_phase` (on_market/in_use/sold, optional).

- 一级（severe）→ 1 日内通知；二级（reversible）→ 3 日内；三级（none）→ 7 日内；均须向省局报告。
- **Insufficient input → strict presumption**: `use_phase=in_use/sold` → warning that the notification scope must also cover distributors and users, and in-use units need follow-up per the recall plan (`rc=1`). It never silently skips in-market obligations.
- Invalid enum values are rejected (`rc=2`) — garbage `harm_level` is NOT silently treated as Level III.

## Install & run (zero-dependency, Python 3.8+)
```bash
python recall-decision-checker.py --demo
python recall-decision-checker.py --harm_level severe                 # Level 1, 1-day, rc=1
python recall-decision-checker.py --harm_level reversible             # Level 2, 3-day, rc=0
python recall-decision-checker.py --harm_level severe --use_phase sold  # in-market notice warning, rc=1
python recall-decision-checker.py --harm_level garbage                # invalid enum → rc=2
```

## Output
Deterministic JSON IR with `rc` (0=ok / 1=with warnings / 2=insufficient or invalid input), `recall_level`, `notify_within_days`, `obligations`, `warnings`, `evidence`, and `aigc_mark` (GB 45438-2025 metadata, `is_generated: true`). Decision support only — final determination rests with the regulator.

## Compliance & IP
- LGD-Powered badge · theory TH-MED-003 · ambassador 诺康@MED 域首席发声人
- 中文文档见 `SKILL.md`。本工具为决策支持，须人工复核，最终以监管机构认定为准。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `recall-decision-checker.py` | **未在 LICENSE 中识别** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在代码许可覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依其自身许可使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 SynomosAI. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块：**A 段公共段逐字复制、未删改；B 段资产参数段按本包真值填写**；发布 / 重提前须照最新版本复核。）

## 家族合集
| 环节 | 工具 | 大使 |
|---|---|---|
| 非临床研究 | non-clinical-checker | 诺康 |
| 上市后不良事件 | pms-vigilance-intake | 诺康 |
| 召回 | recall-decision-checker | 诺康 |
| 标签 | label-compliance-checker | 诺康 |
| 进出口 | import-export-router | 诺衡 |
