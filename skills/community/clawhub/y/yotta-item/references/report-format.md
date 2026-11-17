# 报告契约与缺口类别（元题 yotta-item）

## 一、组卷报告（`assemble`）

Markdown 章节固定为：组卷结果（分节明细）→ 覆盖矩阵 → 难度分布 → 时间预算 →
缺口清单（仅在存在缺口时输出）→ 声明。

JSON 顶层字段（`schema_version 1.0`）：

| 字段 | 说明 |
|---|---|
| `title` | 卷名 |
| `seed` | 本次组卷使用的随机种子 |
| `sections[]` | 逐节：`id` / `title` / `type` / `count` / `points_each` / `selected`（题目 id 列表）/ `shortfall` / `knowledge_missing` / `difficulty_selected` / `difficulty_shortfall` |
| `paper` | 试卷对象（`schema_version` / `title` / `items[].id` / `items[].section`），可直接交给 `check` |
| `totals` | `count` / `points` / `minutes` |
| `coverage` | `required` / `covered` / `missing`（顶层必考考点） |
| `difficulty_summary` | 全卷各难度档题量 |
| `time_budget` | `limit` / `estimated` / `over` |
| `sources` | `subject` / `grade` / `item_sources`（题目来源标注集合） |
| `findings[]` | 缺口（见下表） |
| `disclaimer` | 免责声明 |

### 组卷缺口类别

| `code` | 严重级 | 含义 |
|---|---|---|
| `insufficient_items` | high | 某分节在题库中可选题目不足（含难度配额不足），给出缺口题数 |
| `coverage_gap` | medium | 分节必考考点或全卷 `coverage` 未被任何选中题目覆盖 |
| `time_over_budget` | medium | 选中题目预计作答时间超出蓝图限时 |

## 二、试卷校验（`check`）

Markdown 章节固定为：试卷校验 → 缺口清单 → 声明。

JSON 顶层字段：`title` / `sections` / `totals` / `coverage` / `difficulty_summary` /
`time_budget` / `findings` / `disclaimer`（与组卷报告同名同义）。

### 校验缺口类别

| `code` | 严重级 | 含义 |
|---|---|---|
| `unknown_item` | high | 试卷引用了题库中不存在的题目 id |
| `duplicate_item` | high | 同一题目在试卷中重复出现 |
| `total_points_mismatch` | high | 试卷总分与蓝图 `total_points` 不一致 |
| `section_missing` | medium | 蓝图某分节在试卷中没有任何题目 |
| `section_count_mismatch` | medium | 分节题量与蓝图 `count` 不一致 |
| `section_type_mismatch` | medium | 分节内出现题型与蓝图 `type` 不符的题 |
| `section_points_mismatch` | medium | 分节内出现分值 ≠ `points_each` 的题 |
| `difficulty_mismatch` | medium | 分节难度分布与蓝图 `difficulty` 配额不一致 |
| `coverage_gap` | medium | 分节必考考点或全卷 `coverage` 未被覆盖 |
| `time_over_budget` | medium | 预计作答时间超出限时 |
| `section_label_missing` | low | 题目未标注 `section`，无法逐节核对 |

每条 finding 都带 `evidence`（如题目 id、期望值、实际值、缺失考点），可直接贴进复核记录。

## 三、退出码

| 码 | 含义 |
|---|---|
| `0` | 正常（`check` 未触发闸门） |
| `1` | 触发 `--gate findings=<n>`；或 `assemble` 无法满足蓝图约束（存在缺口） |
| `2` | 输入错误（参数 / 输出路径等） |
| `3` | 题库、蓝图或试卷校验错误；输入文件不存在或 JSON 解析失败 |
| `4` | 运行时错误（文件读写等） |

## 四、接入 CI 的推荐用法

```bash
python3 scripts/yotta_item.py bank validate --bank bank.json
python3 scripts/yotta_item.py blueprint validate --blueprint blueprint.json --bank bank.json
python3 scripts/yotta_item.py assemble --bank bank.json --blueprint blueprint.json \
  --format json --out paper.json
python3 scripts/yotta_item.py check --bank bank.json --paper paper.json \
  --blueprint blueprint.json --gate findings=1 --format json --out review.json
```

`assemble` 存在缺口时本身就返回 1，不需要额外闸门即可阻断流水线。
