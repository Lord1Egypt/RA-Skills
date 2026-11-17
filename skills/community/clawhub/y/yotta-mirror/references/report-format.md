# 报告与 JSON 契约（元镜 yotta-mirror）

## 一、Markdown 报告结构

1. 输入摘要（学生数 / 题目数 / 缺失单元格 / 是否匿名化 + 数据提示）
2. 逐题统计（满分、作答、缺失、平均分、得分率、满分人数、零分人数、知识点）
3. 知识点掌握（知识点、题号、样本量、掌握率、判定：薄弱 / 待巩固 / 掌握 / 数据不足）
4. 学生分层（A / B / C 人数与名单、临界生名单）
5. 薄弱点诊断（严重度 + 掌握率 + 阈值 + 样本量 + 证据题号）
6. 人工复核（低样本、无数据、缺失作答、临界生）
7. 免责声明

## 二、JSON 顶层字段（稳定契约，`schema_version = 1.0`）

| 字段 | 说明 |
|---|---|
| `schema_version` / `tool` / `tool_version` | 契约版本与引擎版本 |
| `generated_at` | 生成时间（UTC，唯一随运行变化的字段） |
| `input` | 学生数 / 题目数 / 缺失数 / 学生列名 / 是否匿名化 |
| `quality` | 数据质量：缺失计数与提示 |
| `items_stats` | 逐题统计数组 |
| `knowledge` | 知识点聚合数组（`name` / `items` / `respondents` / `rate` / `level`） |
| `layers` | 学生分层：`a` / `b` / `c` / `critical` 名单 |
| `diagnoses` | 薄弱点诊断（`knowledge` / `severity` / `rate` / `threshold` / `evidence`） |
| `review_items` | 人工复核清单（带 `reason` 与说明） |
| `summary` | 计数摘要 |
| `thresholds` | 本次实际使用的阈值（可复算依据） |
| `disclaimer` | 固定免责声明 |

`review_items[].reason` 取值：`item_no_data` / `item_low_sample` / `knowledge_low_sample` /
`student_missing_answers` / `critical_student`。

## 三、判定规则（确定性）

- 掌握率 = 该知识点涉及题目的得分总和 ÷ （各题有效作答人数 × 各题满分之和）；
- 判定：`rate < weak_below` → 薄弱；`rate >= solid_at_or_above` → 掌握；其余 → 待巩固；
- 严重度：薄弱且 `rate < weak_below × 0.75` → 高，否则 → 中；
- 样本量低于 `min_respondents` 的薄弱点不产出诊断，只进人工复核；
- 学生层：总分率 = 已作答题目得分 ÷ 已作答题目的满分之和；缺失作答的学生同时进复核清单；
- 临界生：总分率与某条分界线之差 ≤ `critical_margin`。

## 四、退出码与闸门

| 退出码 | 含义 |
|---|---|
| `0` | 分析完成；若给了 `--gate` 且未触发，同样为 0 |
| `1` | `--gate weak=<n>`：薄弱知识点数量 ≥ n |
| `2` | 输入错误（文件缺失、列/行不一致、重复学生、非数值、越界、非法输出路径） |
| `3` | 配置或映射错误（schema 版本、字段缺失、阈值不合法） |
| `4` | 运行时错误（文件系统等） |

CI 用法示例：

```bash
python3 scripts/yotta_mirror.py analyze --input scores.csv --items item-map.json --gate weak=3 || exit 1
```

## 五、复算与存档建议

- 存档时同时保留：原始成绩表、题目映射、阈值配置、输出 JSON（四件一致才能复算同一结论）；
- 报告需注明阈值来源（`thresholds` 字段已随 JSON 给出）；
- 分享版建议 `--anonymize` 后只保留结论、证据与复核清单。
