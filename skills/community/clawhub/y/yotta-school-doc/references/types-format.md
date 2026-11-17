# 文种规则包与事实清单契约（元公 yotta-school-doc）

## 一、文种规则包 JSON

规则包顶层字段：

| 字段 | 必填 | 说明 |
|---|---|---|
| `schema_version` | 是 | 固定为 `1.0` |
| `pack_version` | 否 | 规则包版本标识，进入输出 `sources` |
| `types` | 是 | 文种数组，至少一项 |

每个文种字段：

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | 唯一文种标识，如 `notice` |
| `name` | 是 | 中文文种名，如「通知」 |
| `title_keywords` | 是 | 标题识别关键词数组 |
| `required_fields` | 是 | 必填字段数组，必须是引擎支持的字段 |
| `required_sections` | 是 | 必填结构段数组 |
| `sensitive_terms` | 否 | 需人工复核的表述词；缺省使用内置词 |
| `visibility_default` | 否 | `public` 或 `internal`，缺省 `public` |

## 二、结构段

每个结构段至少声明以下一种识别方式：

| 字段 | 说明 |
|---|---|
| `keywords` | 字符串数组，命中任一词即视为存在 |
| `min_lines` | 正整数，正文有效行数达到该值即视为存在 |
| `date_required` | 布尔值，文稿中出现任一可识别日期即视为存在 |

示例：

```json
{
  "id": "date",
  "name": "成文日期",
  "date_required": true
}
```

## 三、内置文种

| id | 中文名 | 关键必填字段 |
|---|---|---|
| `notice` | 通知 | 标题 / 成文单位 / 成文日期 / 受文对象 / 办理截止 / 联系方式 |
| `parents_letter` | 告家长书 | 标题 / 成文单位 / 成文日期 / 家长对象 / 反馈截止 / 联系方式 / 附件 |
| `request` | 请示 | 标题 / 成文单位 / 成文日期 / 主送对象 / 请示事项 / 理由 / 联系方式 |
| `report` | 报告 | 标题 / 成文单位 / 成文日期 / 主送对象 / 工作概述 / 下一步 / 联系方式 |
| `summary` | 工作总结 | 标题 / 成文单位 / 成文日期 / 工作概述 / 下一步 / 联系方式 |
| `minutes` | 会议纪要 | 标题 / 成文单位 / 会议日期 / 参会人员 / 议定事项 / 待办事项 |
| `plan` | 工作方案 | 标题 / 成文单位 / 成文日期 / 目标 / 步骤 / 责任人 / 时间安排 / 联系方式 |
| `briefing` | 简报 | 标题 / 成文单位 / 成文日期 / 工作概述 / 亮点 / 联系方式 |

## 四、事实清单 JSON

```json
{
  "schema_version": "1.0",
  "doc_type": "notice",
  "visibility": "public",
  "title": "关于开展秋季运动会的通知",
  "issuer": "示例中学",
  "published_date": "2026-09-24",
  "audience": "各年级组、各班级",
  "action_deadline": "2026-09-30",
  "contact": "教务处（010-00000000）",
  "body_points": ["运动会时间与地点", "报名办法", "安全工作要求"],
  "attachments": ["报名表.xlsx"],
  "approval": {"reviewer": "校务会", "approved_date": "2026-09-23"}
}
```

- `body_points` 与 `attachments` 必须是字符串数组；
- `visibility` 只允许 `public` 或 `internal`；
- 日期字段可使用 ISO 或中文写法，内部归一化；
- 缺失必填字段生成 `〔待补〕` 与 `field_missing`，不会自动补事实。

## 五、自定义规则包

学校可复制 `template` 命令生成的 `types.json`，按校情调整必填字段、结构关键词、敏感词与默认可见范围。
引擎只读取声明式数据，不执行表达式；规则包不进入文稿输出，也不会联网更新。
