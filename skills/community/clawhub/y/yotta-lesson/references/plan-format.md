# 骨架与检查报告契约（元案 yotta-lesson）

## 一、教案骨架（Markdown）

1. 课题信息（学科 / 年级 / 课题 / 课时 × 每课时分钟 = 合计分钟）
2. 学习目标（逐条带课标来源）
3. 教学重难点与易错点
4. 教学环节与时间分配（表格：环节 / 时间 / 要点）
5. 板书与评价清单（可勾选）
6. 备课提示（映射包层面需要教师补充的点）
7. 来源与免责

## 二、骨架 JSON 顶层字段（`schema_version = 1.0`）

| 字段 | 说明 |
|---|---|
| `schema_version` | 契约版本 |
| `tool` | 固定为 `yotta-lesson` |
| `tool_version` | 引擎版本 |
| `generated_at` | 生成时间（UTC，唯一随运行变化的字段） |
| `lesson` | 课题信息：id / title / unit / subject / grade / periods / minutes_per_period / total_minutes |
| `objectives` | 学习目标数组（`knowledge` + `source`） |
| `key_points` | 教学重点 |
| `difficulties` | 教学难点 |
| `misconceptions` | 易错点 |
| `stages` | 环节数组（`id` / `name` / `minutes` / `focus`） |
| `checklist` | 评价清单（板书、反馈、作业等） |
| `findings` | 备课提示（映射包层面的缺口，如无易错点、课时被覆盖） |
| `sources` | 课标来源 |
| `disclaimer` | 固定免责声明 |

## 三、缺口检查报告

`check` 子命令对已有教案文本做确定性核对，输出 `findings` 数组（按 `kind` + `detail` 排序）：

| kind | 含义 | 处理建议 |
|---|---|---|
| `knowledge_missing` | 教案未出现映射包中的知识点原文 | 补知识点或改用映射包认可的名称 |
| `stage_missing` | 必填环节的关键词都未出现 | 补该环节，或调整 `check_keywords` |
| `source_missing` | 未标注课标来源 | 在教案中写明 `standard`（至少写明条目前半段） |
| `time_missing` | 未出现任何「N 分钟」标注 | 给各环节补时间 |
| `minutes_mismatch` | 标注的「合计 N 分钟」与 课时 × 每课时分钟 不一致 | 核对课时数或时间分配 |

检查报告 JSON 顶层字段：`schema_version`、`tool`、`tool_version`、`lesson`、`checked`、
`findings`、`summary`、`disclaimer`。

## 四、退出码与闸门

| 退出码 | 含义 |
|---|---|
| `0` | 正常（含未触发闸门） |
| `1` | `--gate findings=<n>`：缺口数量 ≥ n |
| `2` | 输入错误（文件缺失、教案文本缺失、非法输出路径） |
| `3` | 映射或配置错误（schema、必填字段、课时数、环节定义） |
| `4` | 运行时错误（文件系统等） |

## 五、复算与归档建议

- 归档四件：映射包、结构配置、教案骨架 JSON、教案正文；四件齐全才能复算同一结论；
- 教研组比对教案时，固定同一映射包与结构配置，差异才归因于教案本身；
- 骨架的 `findings` 与 `check` 的 `findings` 含义不同：前者是映射包层面的备课提示，后者是教案文本层面的缺口。
