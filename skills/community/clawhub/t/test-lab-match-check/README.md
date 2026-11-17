# test-lab-match-check · 医疗器械检测项目与实验室匹配器 / MD Test-Item & Lab Match Checker

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

> Zero-dependency deterministic CLI screener for medical-device compliance.
> **Decision support only — NOT legal/regulatory advice. Always verify against official texts.** Text verified: 2026-09-26.

### Why
Before sample submission you assume "just a few items"; when the report comes back you're missing an endpoint and the lab's accreditation doesn't even cover it — re-submitting costs months.

### What it does
Screens test items and lab qualification against public rule sources: **GB/T 16886 series / GB 9706.1 / YY 0505 / ISO 11135·11137·17665 / ISO 11607 / IEC 62304**.
Outputs deterministic JSON IR with `rc` (0 = ok / 1 = ok with warnings / 2 = insufficient input),
`error_code`, and GB 45438-2025 AIGC metadata. No network, no API key, no third-party packages.

- **Insufficient input → strict presumption**: missing `--material` and sterile-without-method are flagged in `warnings` (`rc=1`) — never silently outputs a lenient checklist.
- Invalid enums are rejected (`rc=2`): `device_type`, `contact`, `dest`.
- Measured: full implant args → rc=0; `--device_type active --sterile yes` → rc=1; `--dest jp` → rc=2.

### Run it (Python 3.8+)
```bash
python test-lab-match-check.py --demo
python test-lab-match-check.py --json <your args...>
```

### Compliance & IP
- Author: SynomosAI contributors · © 2026 SynomosAI · MIT License
- Theory anchor: `TH-MED-010` (LGD · registry / evidence / gate)
- Published by an AI-assisted studio; the institution bears responsibility for the output.

## 中文

> 零依赖确定性 CLI 判定器，用于医疗器械合规初筛。
> **仅为决策支持——不构成法律/监管意见。请以官方文本复核。** 文本核验：2026-09-26。

### 为什么
送检前以为项目就那几项，报告拿到手才发现缺一个终点、实验室资质还超范围——重送一轮就是几个月。

### 做什么
按公开规则源推导检测项目并核对实验室资质：**GB/T 16886 系列 / GB 9706.1 / YY 0505 / ISO 11135·11137·17665 / ISO 11607 / IEC 62304**。
输出确定性 JSON IR，含 `rc`（0=正常 / 1=正常带警示 / 2=输入不足）、`error_code`、GB 45438-2025 AIGC 元数据。无网络、无 API Key、无第三方依赖。

- **输入不足从严推定**：缺 `--material`、声明无菌但缺灭菌方式会在 `warnings` 中标注（`rc=1`），绝不静默输出宽松清单。
- 非法枚举拒绝（`rc=2`）：`device_type`、`contact`、`dest`。
- 实测：全套植入参数 → rc=0；`--device_type active --sterile yes` → rc=1；`--dest jp` → rc=2。

### 运行（Python 3.8+）
```bash
python test-lab-match-check.py --demo
python test-lab-match-check.py --json <你的参数...>
```

### 合规与 IP
- 作者：SynomosAI contributors · © 2026 SynomosAI · MIT License
- 理论锚点：`TH-MED-010`（LGD · 有籍 / 有证 / 有门禁）
- AI 辅助工作室出品，机构承担出品责任。

## Family / 家族

| Stage 环节 | Tool 工具 | Status 位置 |
|---|---|---|
| Classification & route 分类与路径 | `md-classification-route` | this batch 本批 |
| Registration dossier 注册资料 | `SynomosAI-reg-hub` | existing hub 存量枢纽 |
| Clinical eval route 临床评价选路 | `clin-eval-route-picker` | existing 存量 |
| Clinical eval evidence 临床评价证据 | `cer-equivalence-check` | this batch 本批 |
| Test items & lab match 检测项目与实验室匹配 | `test-lab-match-check` | this batch 本批 |
| Pre-submission non-clinical 非临床研究 | `non-clinical-checker` | existing 存量 |
| UDI format UDI格式校验 | `udi-format-validator` | existing 存量 |
| UDI database UDI数据库提交 | `udi-db-submission-check` | this batch 本批 |
| PMCF plan 上市后PMCF计划 | `pmcf-plan-check` | existing 存量 |
| PMCF report 上市后PMCF报告 | `pmcf-evaluation-report-check` | this batch 本批 |
| Vigilance 上市后不良事件 | `pms-vigilance-intake` | existing 存量 |
| Recall 上市后召回 | `recall-decision-checker` | existing 存量 |
| Labels & IFU 标签与说明书 | `label-compliance-checker` | existing 存量 |
| Import/export 进出口路径 | `import-export-router` | existing 存量 |

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `test-lab-match-check.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在代码许可覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依其自身许可使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 SynomosAI. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包 = MIT (see LICENSE)
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
