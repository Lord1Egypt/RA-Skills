# 覆盖范围与规则清单

元规把“覆盖级别”作为报告的第一等字段：`baseline_review` 表示可以输出该框架的独立 finding；
`mapping_only` 表示只把基础规则映射到该框架的主题，不输出该框架的独立合规结论。

## 1. 覆盖级别

| 级别 | 含义 | 报告行为 |
|---|---|---|
| `baseline_review` | 对基础框架执行确定性规则审查 | 可输出 finding；覆盖摘要状态为 `reviewed` |
| `mapping_only` | 只做主题映射 | 只显示 `框架:mapping_only` 标签；不输出独立结论 |

`mapping_only` 不得被描述为“已审查该框架”，也不得用于对外声称“通过某框架认证”。

## 2. 当前基础框架

| 规则包 | 框架 | 规则数 | 规则包版本 |
|---|---|---|---|
| `pipl` | `PIPL`（个人信息保护法） | 11 | `2026.09.1` |
| `data-export` | `DATA-EXPORT`（数据出境） | 4 | `2026.09.1` |

## 3. PIPL 规则清单

来源：中国人大网《中华人民共和国个人信息保护法》官方全文
（https://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html）。

| rule_id | 主题 | severity | 断言 | 来源条款 |
|---|---|---|---|---|
| `PIPL-NOTICE-001` | 未出现处理目的的告知表述 | medium | absent / document | 第十七条第一款第二项 |
| `PIPL-PURPOSE-002` | 未出现最小必要或影响最小约束 | medium | absent / document | 第六条 |
| `PIPL-BASIS-003` | 未出现处理个人信息的合法性依据 | medium | absent / document（置信 low） | 第十三条 |
| `PIPL-RETENTION-004` | 未出现个人信息保存期限说明 | medium | absent / document | 第十七条第一款第二项、第十九条 |
| `PIPL-RETENTION-005` | 保存期限达到或超过 3 年 | low | numeric_compare `gte 3` | 第十九条 |
| `PIPL-SENSITIVE-006` | 涉及敏感个人信息但未出现单独同意 | high | absent / document | 第二十八条、第二十九条 |
| `PIPL-MINOR-007` | 涉及不满十四周岁未成年人信息但未出现监护人同意 | high | absent / document | 第三十一条 |
| `PIPL-SHARE-008` | 对外提供个人信息但未出现单独同意 | high | absent / document | 第二十三条 |
| `PIPL-RIGHTS-009` | 未出现个人权利相关表述 | low | absent / document（置信 low） | 第十七条第一款第三项、第四十四条至第四十七条 |
| `PIPL-INCIDENT-010` | 未出现个人信息泄露补救与通知机制 | low | absent / document（置信 low） | 第五十一条第五项、第五十七条 |
| `PIPL-PIPIA-011` | 涉及影响评估情形但未出现个人信息保护影响评估 | medium | absent / document | 第五十五条 |

`PIPL-RETENTION-005` 只识别 `保存期限：N年` 形式，且只做阈值提示，不判断保存期限是否合法。

## 4. 数据出境规则清单

来源：《中华人民共和国个人信息保护法》第三十八条至第四十条；数据出境制度口径参照国家网信办
《促进和规范数据跨境流动规定》（2024-03-22，https://www.cac.gov.cn/2024-03/22/c_1712776611775634.htm）。
v0.1 未将人数阈值做成规则，相关阈值规则推迟到规则包 v2。

| rule_id | 主题 | severity | 断言 | 来源条款 |
|---|---|---|---|---|
| `EXPORT-SAFEGUARD-001` | 数据出境未出现安全评估、标准合同或保护认证 | high | absent / document | 第三十八条第一款 |
| `EXPORT-CONSENT-002` | 数据出境未出现单独同意 | high | absent / document | 第三十九条 |
| `EXPORT-NOTICE-003` | 数据出境未出现境外接收方告知 | medium | absent / document | 第三十九条 |
| `EXPORT-STORAGE-004` | 数据出境未出现境内存储说明 | low | absent / document（置信 low） | 第四十条 |

`EXPORT-STORAGE-004` 的适用性与“关键信息基础设施运营者”或“达到规定数量的处理者”身份有关，
规则只做概览性提示，必须人工核对适用性。

## 5. mapping_only 主题映射

### 5.1 pipl 包

| 框架 | 主题 | 映射规则数 |
|---|---|---|
| GDPR | breach_notification / children / data_subject_rights / dpia / lawful_basis / purpose_limitation / special_categories / storage_limitation | 10 |
| HIPAA | breach_notification / phi_context | 2 |
| SOC2 | incident_response / privacy_notice | 2 |
| PCI-DSS | account_data_context | 1 |
| ISO27001 | incident_management / retention_governance | 2 |
| 等保 | data_retention / emergency_response | 2 |

### 5.2 data-export 包

| 框架 | 主题 | 映射规则数 |
|---|---|---|
| GDPR | international_transfers | 3 |
| ISO27001 | data_residency / supplier_agreements | 2 |
| 等保 | data_residency / security_assessment | 2 |

映射只表示“该基础规则与这些框架主题相关”，不表示这些框架已经过审查。

## 6. 明确未覆盖

以下范围不在 v0.1 的 `baseline_review` 内：

1. **语义理解**：词形不同的同义表述可能漏检；absence 只判断检索词是否出现。
2. **文档级范围判断**：absence 的 `scope` 为 `document`，检索词出现在任何位置即视为已出现，
   不判断其是否适用于当前处理活动。
3. **否定句建模**：「不会对外提供」「未经同意不得处理」等否定表述仍可能触发候选匹配。
4. **中文数字解析**：「三年」「十万」等中文数字不解析、不换算。
5. **数据出境人数阈值**：100 万人以上、10 万人以上、1 万人敏感个人信息等阈值需要单位感知的
   数值原语，v0.1 不做跨单位换算，因而没有对应规则。
6. **其它框架的独立结论**：GDPR / HIPAA / SOC2 / PCI-DSS / ISO27001 / 等保 仅 `mapping_only`。
7. **非文本输入**：PDF / docx / 图片不直接解析，需先转成 UTF-8 文本或 Markdown。
8. **法律判断**：不判断合同效力、不预测诉讼结果、不替代律师或合规顾问。

## 7. 如何核对覆盖范围

```bash
# 列出实际装载的规则
python3 scripts/yotta_compliance.py rules list

# 只看某个框架
python3 scripts/yotta_compliance.py rules list --framework pipl

# 查看单条规则的来源与测试用例
python3 scripts/yotta_compliance.py rules show PIPL-NOTICE-001

# 校验规则包结构
python3 scripts/yotta_compliance.py rules validate --pack rules/pipl.json
python3 scripts/yotta_compliance.py rules validate --pack rules/data-export.json
```

Markdown 报告的「框架覆盖摘要」与 JSON 的 `framework_coverage` 反映实际装载结果；
两者是判断某框架是否进入本次审查的权威依据。

## 8. 更新规则包时的要求

- 升 `pack_version`，并同步更新本文件的规则清单与来源条款；
- 每条规则补齐正例、反例、边界例，并让 `test_ids` 与夹具逐项一致；
- 来源使用官方文本，写到条款号与 `https://` 链接；
- 重新运行规则包校验与全量契约测试；
- 规则包内容或行为发生变化时，随技能版本一起进入发布流程。
