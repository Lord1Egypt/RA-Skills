---
name: yotta-school-doc
slug: yotta-school-doc
version: 0.1.5
displayName: 公文校验·元公
summary: 本地、确定性的学校公文可信起草与校验：文种规则包 + 结构化事实 → 可复算文书骨架；对已有文稿检查必填要素、日期关系、附件、待补值、学生个人信息、过度承诺与会议待办；零依赖，不联网、不编造事实。
description: '学校公文校验（元公）—— 按版本化文种规则包（通知 / 告家长书 / 请示 / 报告 / 工作总结 / 会议纪要 / 工作方案 / 简报）生成可复算的文书骨架；check 子命令对已有文稿做确定性检查（必填字段 / 结构段 / 日期格式与先后关系 / 事实日期一致性 / 附件 / 未定占位值 / 学生个人信息 / 敏感表述 / 过度承诺 / 会议待办责任人与时间），支持 --gate findings=n 接入 CI；零依赖本地运行，不联网、不调用模型。触发：起草或检查学校通知 / 公文、核对日期 / 附件 / 学生信息、把学校公文结构检查接入自动化流程时。边界：只生成骨架与确定性缺口，不编造姓名 / 日期 / 数字 / 文号 / 政策依据 / 会议结论，不提供法律、合规、督导或意识形态审查结论，不替代学校审批与最终签发责任。'
tags: [学校公文, 公文校验, 通知, 告家长书, 会议纪要, 格式检查, 证据链, education, school document, 本地化]
category: education
subCategories: [edu-teaching-aid]
license: MIT
homepage: https://github.com/YottaMeta/yotta-school-doc
---
# 元公（yotta-school-doc）

本地、确定性的学校公文可信起草与校验技能。元公把「文种要求、事实输入与已有文稿」变成两件可复算的东西：

- 一份不编造事实的文书骨架；
- 一份带行号证据的确定性缺口清单。

可信契约：

- 缺失事实统一显示为 `〔待补〕`，并进入缺口清单；
- 日期支持 `YYYY-MM-DD` 与 `YYYY年M月D日`，内部归一化后比较；
- 同一事实 JSON + 同一规则包 = 同一骨架（仅生成时间变化）；
- 核心路径不联网、不调用模型，文稿与校情数据只在本机流转。

## 何时使用

- 先把通知、告家长书、请示、报告、工作总结、会议纪要、工作方案或简报的结构骨架搭起来；
- 用 `check` 核对已有文稿：标题、受文对象、成文单位、日期、联系方式、办理要求是否齐全；
- 核对日期格式、成文日期与截止日期是否倒置、文稿日期与事实清单是否一致；
- 核对附件引用、未定占位值、学生个人信息、过度承诺表述与会议待办；
- 把学校公文结构检查接入批处理或 CI（`--gate findings=n`）。

**Do NOT trigger**：

- 不生成完整成稿，也不编造姓名、日期、数字、文号、单位、政策依据或会议结论；
- 不提供法律、合规、督导或意识形态审查结论；
- 不替代学校审批链与最终签发责任：输出是骨架与缺口清单，最终定稿由学校负责人确认；
- 不联网、不调用模型、不上传学校文稿与校情数据；
- 不内置党政机关公文标准全文、真实学校模板或案例正文；需要润色时交给元真，需要统一呈现时交给元呈。

## 快速使用

```bash
# 生成规则包、事实 JSON 与骨架示例
python3 scripts/yotta_school_doc.py template --output-dir ./school-doc-template

# 按事实 JSON 生成文书骨架
python3 scripts/yotta_school_doc.py draft --type notice --facts facts.json

# 输出 JSON 骨架
python3 scripts/yotta_school_doc.py draft --type notice --facts facts.json --format json

# 检查已有文稿，缺口 ≥ 1 时让 CI 失败
python3 scripts/yotta_school_doc.py check --doc notice.md --type notice --facts facts.json --gate findings=1

# 查看内置文种
python3 scripts/yotta_school_doc.py types list

# 校验自定义规则包
python3 scripts/yotta_school_doc.py types validate --types school-types.json
```

退出码：`0` 正常 ｜ `1` 触发 `--gate` ｜ `2` 输入错误 ｜ `3` 文种或规则包错误 ｜ `4` 运行时错误。

## 输入与输出

- **文种规则包**：JSON，声明 `id` / `name` / `title_keywords` / `required_fields` / `required_sections` / `sensitive_terms` / `visibility_default`；
- **结构化事实**：JSON，声明 `doc_type` / `visibility` 与标题、单位、日期、受文对象、联系方式、正文要点、附件等；
- **骨架**：Markdown 或 JSON（`schema_version 1.0`，含 `document` / `facts` / `fields` / `body_points` / `attachments` / `findings` / `sources` / `disclaimer`）；
- **检查报告**：Markdown 或 JSON（含 `document` / `facts` / `checked` / `findings` / `summary` / `sources` / `disclaimer`）。

字段规范见 `references/types-format.md`；报告契约见 `references/report-format.md`。

## 检查项

| 缺口 | 含义 |
|---|---|
| `field_missing` | 必填字段在文稿中找不到 |
| `section_missing` | 必填结构段缺失 |
| `date_format_invalid` | 出现 `2026/9/24`、`2026.9.24` 等不符合约定格式的日期 |
| `date_order_invalid` | 成文日期晚于办理截止日期 |
| `fact_date_mismatch` | 文稿日期与事实清单不一致 |
| `attachment_missing` | 事实附件未在正文或附件清单中出现 |
| `attachment_unknown` | 文稿写了附件但事实清单没有 |
| `placeholder_present` | 文稿仍含 `〔待补〕`、未完成标记、`待定` 等未定值 |
| `privacy_risk` | 公开文书出现学生身份证号、手机号、邮箱或家庭住址等个人信息 |
| `action_item_incomplete` | 会议纪要待办缺少责任人或完成时间 |
| `sensitive_term_review` | 出现处分、开除、罚款、追责、承诺、保证等需人工复核的表述 |
| `overclaim_review` | 出现确保、全部、彻底、100% 等过度承诺 |

## 隐私与边界

- 本地运行：零网络、零模型；学校文稿、校情事实、参会人员信息只在本机流转；
- 个人信息识别只做规则命中提示，不做身份判断；命中即建议删改、脱敏或改走内部流转；
- 不内置 GB/T 9704 或任何标准全文、真实公文模板；内置规则只记录结构性字段与通用词；
- 输出为文书辅助与风险提示，不构成法律、合规、督导或意识形态审查结论；最终签发责任在学校。

详见 `references/privacy.md`。

## 家族协同

- **元真 yotta-humanize**：对学校作者写好的正文做中文文风润色；
- **元呈 yotta-present**：把骨架与检查报告渲染成统一格式；
- **元规 yotta-compliance**：需要条款级合规审查时另行使用，元公不代替它下结论；
- **元忆 yotta-memory**：按需保存规则包版本与检查摘要。

## 渐进披露

- 规则包与字段契约：`references/types-format.md`
- 骨架 / 检查报告契约与退出码：`references/report-format.md`
- 隐私与使用边界：`references/privacy.md`

按需读取，不必每次全读。
