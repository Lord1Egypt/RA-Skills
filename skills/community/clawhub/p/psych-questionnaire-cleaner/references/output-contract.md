# Output contract

Use a new run directory. All delivered filenames, report prose, generated column names, log headers, rule descriptions, statuses, and exclusion reasons must be in Simplified Chinese. The original source file remains unchanged; when original columns are renamed in an output, include a reversible Chinese column-name map.

## 1. 清洗后分析数据

The Chinese-named analytical dataset should contain only rows retained after approved exclusions, plus:

- `稳定行标识`；
- 经授权且必要时保留的参与者或会话标识；
- 机械清洗后的题目值；
- 单独命名的反向计分衍生值；
- 分量表和总分，以及中文的计分状态字段；
- 每个作答质量指标的中文字段；
- `规律作答标记`、`规律作答类型`、`规律作答最长长度`、`规律作答题目范围`；
- `排除状态`、`排除规则`、`排除原因`。

Use the default filenames `清洗后分析数据.<format>` and `原始字段名与中文字段名对照表.<format>`. Do not silently replace raw questionnaire responses.

## 2. 排除记录

Write every excluded row to `排除记录.<format>` rather than discarding it. Include its stable row key, permitted participant/session identifier, triggered rule, Chinese exclusion reason, and all flags required for review. This file is an audit artifact, not part of the analysis dataset.

## 3. 审计日志

Provide `审计日志.<format>` with at least these Chinese headers:

```text
运行编号
时间戳
输入文件
输入哈希
行标识或适用范围
字段
操作
原值或原始汇总
新值或新汇总
规则编号
规则状态
规则来源
原因
```

For sensitive values, record a category or aggregate summary rather than the response itself.

## 4. 已解析清洗方案

Save the exact plan used as `已解析清洗方案.yaml` or `已解析清洗方案.json`. Its explanatory keys and values must be Chinese. Include software/tool version when available, the response-time median and bounds, all active thresholds, rule status, and source. Proposed-but-unused rules must remain visibly distinct from active rules.

## 5. 数据质量报告

Write `数据质量报告.md` in Simplified Chinese. It should state:

1. inputs and mode used;
2. row/column counts and identifier integrity;
3. structural issues and transformations;
4. missingness and out-of-range summaries;
5. counts for every quality indicator;
6. approved exclusions, with a count after each rule;
7. scoring coverage and unresolved scoring problems;
8. sensitivity results, if requested;
9. unresolved questions and limitations.

Report flagged and excluded counts separately. Avoid row-level sensitive data. State the response-time median, its inclusive lower and upper bounds, and the count excluded for response time and attention-check mismatches separately.

## 6. 核对检查

Before delivery, verify:

```text
输入行数 = 保留分析行数 + 已排除行数
```

Verify that `清洗后分析数据` and `排除记录` together reconcile to the input row count. Also verify unique stable row keys, reversible Chinese column-name mapping, rule-to-audit-log coverage, score formula spot checks, and deterministic rerun behavior.
