# 骨架与检查报告契约（元公 yotta-school-doc）

## 一、文书骨架 JSON（`schema_version = 1.0`）

| 字段 | 说明 |
|---|---|
| `schema_version` | 契约版本 |
| `tool` | 固定为 `yotta-school-doc` |
| `tool_version` | 引擎版本 |
| `generated_at` | 生成时间（UTC，唯一随运行变化的字段） |
| `document` | 文种、文种名、标题、默认可见范围 |
| `facts` | 事实入口摘要（文种与可见范围） |
| `fields` | 必填字段值；缺失时为 `〔待补〕` |
| `body_points` | 正文要点数组，按事实清单顺序输出 |
| `attachments` | 附件名数组 |
| `findings` | 骨架生成层面的缺口（字段缺失） |
| `sources` | 规则包标识与版本 |
| `disclaimer` | 固定免责声明 |

## 二、检查报告 JSON

| 字段 | 说明 |
|---|---|
| `schema_version` | 契约版本 |
| `tool` | 固定为 `yotta-school-doc` |
| `tool_version` | 引擎版本 |
| `document` | 文种、文种名、可见范围 |
| `facts` | 是否使用事实清单与事实文种 |
| `checked` | 已检查字段、结构段和识别到的日期 |
| `findings` | 缺口数组 |
| `summary` | 缺口数量 |
| `sources` | 规则包标识 |
| `disclaimer` | 固定免责声明 |

## 三、缺口类型

| kind | 默认严重级 | 含义 |
|---|---|---|
| `field_missing` | high | 必填字段未出现 |
| `section_missing` | high | 必填结构段未出现 |
| `date_format_invalid` | medium | 日期格式不符合约定 |
| `date_order_invalid` | high | 成文日期晚于办理截止日期 |
| `fact_date_mismatch` | medium | 文稿日期与事实清单不一致 |
| `attachment_missing` | high | 事实附件未在文稿中出现 |
| `attachment_unknown` | medium | 文稿写了附件但事实清单没有 |
| `placeholder_present` | medium | 文稿仍含未定占位值 |
| `privacy_risk` | high / medium | 发现可能的学生个人信息 |
| `action_item_incomplete` | medium | 会议纪要待办缺少责任人或时间 |
| `sensitive_term_review` | low | 出现需人工复核的表述 |
| `overclaim_review` | low | 可能过度承诺 |

每条缺口包含 `kind`、`severity`、`field`、`detail`、`suggestion`、`evidence`。
`evidence` 固定包含 `line` 与 `quote`；无法定位到原文时为空值。

## 四、退出码与闸门

| 退出码 | 含义 |
|---|---|
| `0` | 正常（含未触发闸门） |
| `1` | `--gate findings=<n>`：缺口数量 ≥ n |
| `2` | 输入错误（文件缺失、文稿缺失、非法输出路径） |
| `3` | 文种或规则包错误（schema、字段、结构段、日期冲突） |
| `4` | 运行时错误（文件系统等） |

## 五、复算与归档建议

- 归档四件：文种规则包、事实 JSON、骨架 JSON、最终文稿；
- 比对两次检查差异时固定同一规则包与事实清单；
- 骨架的 `findings` 与 `check` 的 `findings` 含义不同：前者是事实缺口，后者是文稿缺口；
- 日期和附件检查依赖事实清单；事实缺失时应先补事实，再判断文稿。
