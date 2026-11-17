# 规则包编写规范

元规的规则包是**版本化 JSON 数据**：内核只读取字段、编译正则、匹配文本与复算证据，
不把规则正文当作代码执行。规则质量直接决定审查结论的可信度，因此每条正式规则都必须有
来源、正例、反例、边界例和可复算的期望结果。

## 1. 目录与版本

```text
rules/
├── pipl.json
└── data-export.json
```

- 每个规则包对应一个框架与一个 `pack_id`；
- 规则包内容发生变化时，必须升 `pack_version`；
- `rules/` 进入发布包；`scripts/fixtures/` 下的测试夹具不进入发布包；
- `rules validate` 是发布前硬闸门，校验失败时退出码为 3。

## 2. 规则包字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `schema_version` | string | 是 | 当前固定为 `"1.0"` |
| `pack_id` | string | 是 | 规则包 id，如 `pipl` / `data-export` |
| `framework` | string | 是 | 基础框架名，如 `PIPL` / `DATA-EXPORT` |
| `pack_version` | string | 是 | 规则包版本，如 `2026.09.1` |
| `jurisdiction` | string | 否 | 司法辖区，如 `CN` |
| `coverage_level` | string | 是 | `baseline_review` 或 `mapping_only` |
| `clause_type_lexicon` | object | 否 | 条款类型到关键词数组的映射 |
| `mapping_only` | array | 否 | 其它框架的主题映射 |
| `rules` | array | 是 | 非空规则列表 |

`clause_type_lexicon` 中声明过的类型才能被 `clause_type` 条件引用；引用未声明的类型判为包损坏。

`mapping_only` 数组元素形如：

```json
{
  "framework": "GDPR",
  "topics": {
    "lawful_basis": ["PIPL-BASIS-003"],
    "storage_limitation": ["PIPL-RETENTION-004", "PIPL-RETENTION-005"]
  }
}
```

`topics` 中引用的 `rule_id` 必须存在；`mapping_only` 只影响 finding 的框架标签，不改变基础框架的
审查结论，也不得用于对外声称“已审查该框架”。

## 3. 单条规则字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `rule_id` | string | 是 | 全局唯一；建议 `框架-主题-序号` |
| `title` | string | 是 | 面向用户的规则标题 |
| `clause_types` | array | 否 | 该规则涉及的条款类型 |
| `match` | object | 是 | 候选匹配条件 |
| `assert` | object | 是 | 断言与搜索条件 |
| `severity` | string | 是 | `info` / `low` / `medium` / `high` / `critical` |
| `confidence_policy` | object | 否 | `exact_match` 与 `absence` 的置信度 |
| `evidence` | array | 是 | 至少一项：`matched_span` / `document_scope` / `section_scope` |
| `rationale` | string | 是 | 只描述可观察文本现象，不臆测真实业务 |
| `source` | object | 是 | `type` / `citation` / `url` |
| `remediation` | string | 是 | 面向用户的补充或核对建议 |
| `test_ids` | array | 是 | 非空；正式规则须与正例 / 反例 / 边界例逐一相等 |

示例：

```json
{
  "rule_id": "PIPL-NOTICE-001",
  "title": "未出现处理目的的告知表述",
  "clause_types": ["personal_information"],
  "match": {
    "operator": "any",
    "conditions": [
      {"kind": "clause_type", "value": "personal_information"}
    ]
  },
  "assert": {
    "operator": "absent",
    "target": "processing_purpose_notice",
    "scope": "document",
    "search": {
      "kind": "regex",
      "pattern": "处理目的|使用目的|收集目的"
    }
  },
  "severity": "medium",
  "confidence_policy": {"exact_match": "high", "absence": "medium"},
  "evidence": ["matched_span", "document_scope"],
  "rationale": "文本出现个人信息相关表述，但未检索到处理目的相关表述；需人工核对。",
  "source": {
    "type": "official",
    "citation": "《中华人民共和国个人信息保护法》第十七条第一款第二项",
    "url": "https://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html"
  },
  "remediation": "补充个人信息处理目的，并说明处理方式、处理的个人信息种类与保存期限。",
  "test_ids": [
    "PIPL-NOTICE-001-positive",
    "PIPL-NOTICE-001-negative",
    "PIPL-NOTICE-001-boundary"
  ]
}
```

## 4. 候选匹配

`match.operator` 为 `any` 或 `all`，`match.conditions` 不能为空。条件类型：

| `kind` | 字段 | 说明 |
|---|---|---|
| `keyword` | `value` | 确定性关键词匹配 |
| `regex` | `pattern` | Python 正则；同一规则内不得重复同一 pattern |
| `clause_type` | `value` | 引用 `clause_type_lexicon` 中声明的类型 |
| `section_anchor` | `value` | 引用结构块标签，如标题或条款号 |

候选匹配决定“这条规则是否值得继续判断”。反例与边界例同样要求候选命中，
用于防止“规则没有运行”被误判为通过。

## 5. 断言契约

`assert.search` 必填，沿用同一套确定性原语。断言类型：

| `operator` | 额外字段 | 行为 |
|---|---|---|
| `absent` | `scope` = `document` / `section` | 搜索条件未命中时输出 finding；必须提供范围证据 |
| `present` | 无 | 搜索条件命中时输出 finding |
| `numeric_compare` | `search.group`、`compare.op`、`compare.value` | 解析原文数值并按 `gte` / `lte` / `gt` / `lt` / `eq` / `ne` 比较 |
| `date_compare` | `search.group`、`compare.op`、`compare.value` | 解析原文日期并按上述操作符比较 |
| `duration_compare` | 上述字段 + `unit` = `day` / `month` / `year` | 只比较相同单位，不跨单位换算 |

compare 系列规则必须满足：

- `search.pattern` 含有第 `search.group` 个捕获组；
- `compare.value` 对 `numeric_compare` 是数字，对 `date_compare` 是可解析日期；
- `duration_compare` 的原文单位必须与 `unit` 一致，否则进入 `review_items`（`unverifiable`），
  不输出数值结论；
- 数值或日期无法解析时，记录人工复核项，不自动换算、不补值。

`absent` 的 `scope` 必须是 `document` 或 `section`；缺省范围会被判为包损坏。

## 6. 证据与置信度

| 证据类型 | 内容 |
|---|---|
| `matched_span` | 原文 `quote` + `start` / `end` + `line` / `column` + `section_id` |
| `document_scope` | 全文起止范围与起止行列，不伪造原文引用 |
| `section_scope` | 命中所在结构块的范围，不伪造原文引用 |

证据约束：

- `quote` 必须等于原文切片，禁止拼接、改写或从规范化文本复制；
- `start` / `end` 基于原始文本，不是规范化文本；
- absence 规则必须给出搜索范围；
- 没有证据的 finding 不得进入报告。

`confidence_policy` 常用字段：

| 字段 | 使用场景 |
|---|---|
| `exact_match` | `present` 或 compare 断言命中原文时 |
| `absence` | `absent` 断言未找到检索词时 |

absence 类结论建议使用 `medium` 或 `low`；`low` 置信 finding 会强制进入人工复核清单。

## 7. 来源可追溯

正式规则包的每条规则必须满足：

- `source.type` = `"official"`；
- `citation` 带书名号或法规名，并写到条款号；
- `source.url` 使用 `https://`；
- 条款号逐条核对官方全文，不凭记忆或二手摘要编写。

运行时不会联网校验来源；来源可信度由规则作者在发布前核对，并由规则包版本记录。

## 8. 测试夹具与 test_ids

正式规则必须同时具备：

- 至少一个正例：命中并给出期望证据；
- 至少一个反例：候选命中但不触发 finding；
- 至少一个边界例：缺字段、矛盾值、低置信或词形差异等边界。

数值阈值规则可增加 `threshold` 类型用例，覆盖等值边界。

夹具位于 `scripts/fixtures/rules/<pack>-cases.json`，示例结构：

```json
{
  "schema_version": "1.0",
  "pack_id": "data-export",
  "cases": [
    {
      "case_id": "EXPORT-SAFEGUARD-001-positive",
      "rule_id": "EXPORT-SAFEGUARD-001",
      "kind": "positive",
      "text": "为提供服务，本平台会将您的个人信息传输至境外服务器。\n",
      "expect": {
        "outcome": "finding",
        "severity": "high",
        "confidence": "medium",
        "evidence_kinds": ["matched_span", "document_scope"],
        "evidence_quote": "传输至境外"
      }
    }
  ]
}
```

验收要求：

1. 每条规则的 `test_ids` 与夹具中同 id 的正例、反例、边界例逐项相等；
2. 每个用例显式声明期望结果、severity、confidence、证据类型与 quote；
3. 反例与边界例也要求候选命中（`status != no_match`）；
4. `matched_span` 的 `start` / `end` 切片必须等于 `quote`；
5. 同一语料运行两次，除 `generated_at` 外结果完全一致。

## 9. 校验与发布

```bash
python3 scripts/yotta_compliance.py rules validate --pack rules/pipl.json
python3 scripts/yotta_compliance.py rules validate --pack rules/data-export.json
python3 scripts/test_yotta_compliance.py
```

规则包变更后还要同步检查：

- `references/coverage.md` 的规则清单与来源条款；
- 夹具中的 `test_ids` 与期望结果；
- 报告示例与覆盖范围说明；
- `pack_version` 是否递增。

不要编写以下规则：

- 需要语义推理、模型评分或真实业务事实才能判断的规则；
- 需要跨单位换算的人数阈值规则；
- 需要联网检索法条或实时法规更新的规则；
- 无法给出原文证据或明确来源的规则。
