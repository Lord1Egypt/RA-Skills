# 报告契约

元规同时提供人类可读的 Markdown 报告与稳定的 JSON 契约。JSON 用于自动化、审计与二次处理，
字段语义不随文案样式调整而改变。

## 1. Markdown 报告

Markdown 报告固定包含七节，顺序不变：

| 节 | 内容 |
|---|---|
| 1. 输入摘要 | 来源、大小、行数、SHA-256、规则包 id / 版本 / 覆盖级别 / 规则数 |
| 2. 框架覆盖摘要 | 规则包、框架、覆盖级别、状态、规则数；`mapping_only` 单独说明 |
| 3. 风险汇总 | 输出 finding 数、全部 finding 数、按严重度计数、已检查 / 命中规则数 |
| 4. 逐条发现 | finding id、规则 id、标题、严重度、置信度、框架映射、条款类型、证据、说明、建议、来源 |
| 5. 未覆盖范围 | `mapping_only` 框架、PDF / docx 说明、`--include-safe` 时的未命中规则 |
| 6. 人工复核清单 | 低置信 finding 与无法验证的数值 / 日期项 |
| 7. 免责声明 | 固定声明：本工具提供基于确定性规则的条款审查建议与证据链，不构成法律意见 |

每条 finding 的证据展示规则：

- `matched_span` 显示原文 quote、行、列与 `section_id`；
- `document_scope` / `section_scope` 显示范围与起止行列，不显示伪造 quote；
- 单条 finding 最多展示 5 条证据；超出时追加 `evidence_note`，完整数量保留在 `evidence_total`。

## 2. JSON 顶层字段

```json
{
  "schema_version": "1.0",
  "tool": "yotta-compliance",
  "tool_version": "0.1.0",
  "generated_at": "2026-09-24T12:00:00Z",
  "input": {},
  "rule_packs": [],
  "framework_coverage": [],
  "summary": {},
  "findings": [],
  "review_items": [],
  "disclaimer": "本工具提供基于确定性规则的条款审查建议与证据链，不构成法律意见。"
}
```

| 字段 | 说明 |
|---|---|
| `schema_version` | JSON 契约版本，当前为 `1.0` |
| `tool` | 固定为 `yotta-compliance` |
| `tool_version` | 引擎版本 |
| `generated_at` | UTC ISO-8601 时间戳；这是重复运行唯一允许变化的字段 |
| `input` | 输入摘要，不回显原文 |
| `rule_packs` | 实际装载的规则包元信息与 SHA-256 |
| `framework_coverage` | 基础框架与 `mapping_only` 框架的覆盖摘要 |
| `summary` | 计数与可选已检查规则列表 |
| `findings` | 达到 `--min-severity` 的 finding 列表 |
| `review_items` | 低置信与无法验证项 |
| `disclaimer` | 固定免责声明 |

## 3. input

```json
{
  "kind": "file",
  "path": "D:\\work\\contract.md",
  "sha256": "…",
  "bytes": 1234,
  "lines": 56
}
```

| 字段 | 说明 |
|---|---|
| `kind` | `file` / `stdin` / `memory` |
| `path` | 文件输入时的绝对路径；stdin 时为 `null` |
| `sha256` | 输入 UTF-8 字节的 SHA-256 |
| `bytes` | UTF-8 字节数 |
| `lines` | 按 `\n` 计算的行数 |

报告不包含原文；如需复核，按 `path` 与 `sha256` 找回同一份输入。

## 4. rule_packs

```json
{
  "pack_id": "pipl",
  "framework": "PIPL",
  "pack_version": "2026.09.1",
  "coverage_level": "baseline_review",
  "sha256": "…",
  "rule_count": 11
}
```

`sha256` 用于确认报告引用的规则包版本未被替换；正式审查记录建议同时保存 `pack_id`、
`pack_version` 与 `sha256`。

## 5. framework_coverage

每个基础框架或 `mapping_only` 框架各占一项：

```json
{
  "framework": "GDPR",
  "coverage_level": "mapping_only",
  "status": "mapping_only",
  "pack_id": "pipl",
  "pack_version": "2026.09.1",
  "rule_count": 10,
  "topics": ["lawful_basis", "purpose_limitation"],
  "note": "仅主题映射，不等同于对该框架的合规审查。"
}
```

| 字段 | 说明 |
|---|---|
| `framework` | 框架名 |
| `coverage_level` | `baseline_review` 或 `mapping_only` |
| `status` | `reviewed` 或 `mapping_only` |
| `pack_id` | 产生该行的规则包 |
| `pack_version` | 规则包版本 |
| `rule_count` | 基础包为规则数；`mapping_only` 为映射条目数 |
| `topics` | 仅 `mapping_only` 提供 |
| `note` | 仅 `mapping_only` 提供 |

`mapping_only` 行不得被解读为已完成该框架的审查。

## 6. summary

```json
{
  "findings_total": 3,
  "findings_total_all": 11,
  "by_severity": {"info": 0, "low": 4, "medium": 4, "high": 3, "critical": 0},
  "by_confidence": {"low": 4, "medium": 7, "high": 0},
  "rules_checked": 15,
  "rules_matched": 13,
  "review_items": 4,
  "checked_rules": []
}
```

| 字段 | 说明 |
|---|---|
| `findings_total` | 达到 `--min-severity` 的 finding 数 |
| `findings_total_all` | 过滤前 finding 总数 |
| `by_severity` | 全部 finding 的严重度计数 |
| `by_confidence` | 全部 finding 的置信度计数 |
| `rules_checked` | 本次运行实际检查的规则数 |
| `rules_matched` | 候选命中的规则数，含 matched / matched_no_finding |
| `review_items` | 人工复核项数量 |
| `checked_rules` | 仅在 `--include-safe` 时提供 |

`checked_rules` 每项形如：

```json
{
  "rule_id": "PIPL-SENSITIVE-006",
  "pack_id": "pipl",
  "status": "no_match"
}
```

`status` 取值：

| 值 | 含义 |
|---|---|
| `no_match` | 候选未命中，规则未继续求值 |
| `matched` | 求值后输出 finding |
| `matched_no_finding` | 候选命中，但断言未输出 finding 或进入人工复核 |

## 7. findings

```json
{
  "finding_id": "F-0001",
  "rule_id": "PIPL-NOTICE-001",
  "title": "未出现处理目的的告知表述",
  "severity": "medium",
  "confidence": "medium",
  "framework_mapping": ["PIPL", "GDPR:mapping_only"],
  "clause_types": ["personal_information"],
  "evidence": [
    {
      "kind": "matched_span",
      "quote": "个人信息",
      "start": 12,
      "end": 16,
      "line": 3,
      "column": 5,
      "section_id": "para-2"
    },
    {
      "kind": "document_scope",
      "start": 0,
      "end": 120,
      "line": 1,
      "column": 1,
      "end_line": 9,
      "end_column": 12,
      "section_id": null,
      "scope_label": "全文范围"
    }
  ],
  "evidence_total": 5,
  "evidence_note": "仅显示前 5 条证据，共 8 条。",
  "rationale": "规则说明只描述可观察文本现象。",
  "remediation": "面向用户的补充或核对建议。",
  "source": {
    "type": "official",
    "citation": "《中华人民共和国个人信息保护法》第十七条第一款第二项",
    "url": "https://www.npc.gov.cn/"
  }
}
```

| 字段 | 说明 |
|---|---|
| `finding_id` | 在本次报告中从 `F-0001` 起连续编号 |
| `rule_id` / `title` | 命中的规则 |
| `severity` | `info` / `low` / `medium` / `high` / `critical` |
| `confidence` | `low` / `medium` / `high` |
| `framework_mapping` | 基础框架 + 命中的 `框架:mapping_only` 标签 |
| `clause_types` | 规则声明的条款类型 |
| `evidence` | 原文证据数组；`quote` 必须等于原文切片 |
| `evidence_total` | 证据总数；超过 5 条时仅前 5 条进入 `evidence` |
| `evidence_note` | 证据被截断时出现 |
| `rationale` / `remediation` | 规则说明与建议动作 |
| `source` | 规则来源与链接 |

finding 按严重度降序、`rule_id`、证据起始位置排序，保证同一输入结果稳定。

## 8. review_items

低置信 finding 与无法验证的 compare 结果进入人工复核清单：

```json
{
  "kind": "low_confidence",
  "rule_id": "PIPL-BASIS-003",
  "pack_id": null,
  "finding_id": "F-0005",
  "reason": "低置信结论，必须人工核验后才能采信。"
}
```

| `kind` | 触发条件 |
|---|---|
| `low_confidence` | finding 的 `confidence=low` |
| `unverifiable` | 数值 / 日期无法解析，或时长单位与规则声明不一致 |

`unverifiable` 不输出数值结论，也不伪造原文引用。

## 9. CLI 行为与退出码

- Markdown 是默认格式；`--format json` 输出 JSON；
- `--out` 缺省时只写 stdout；`--out` 写入成功时在 stderr 输出目标路径；
- `--gate` 达到阈值时返回 1；`--gate off` 不触发闸门；
- `--min-severity` 只过滤 `findings`，不改变全部 finding 的汇总计数；
- 输入错误返回 2；规则包错误返回 3；用法错误返回 4。

## 10. 确定性

同一输入、同一规则包、同一参数重复运行时，除 `generated_at` 外，JSON 结果必须完全一致。
审计场景建议使用 `--format json`，并保留输入 SHA-256、规则包 SHA-256 与报告文件。
