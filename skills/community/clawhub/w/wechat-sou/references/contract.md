# 契约补充

> **何时读**：核对 stdout 信封时以 `assets/output_envelope.schema.json` 与 `assets/*_cli_*.schema.json` 为准。本节只补充**上游 REST**异步任务与 CLI 信封的边界。

## 上游异步任务（Create → `/info`）

> CLI 入参/出参 schema **不含**任务 uuid：命令行仍只收 keyword/url 等；任务 id 由 Skill 内部从 Create 响应带到查询，**不出现在 stdout 信封**。

异步命令对 guaikei REST：

| 步骤 | 约定 |
| --- | --- |
| Create 成功出参 | 顶层 `id`：标准 36 字符 uuid；缺失或形态不符视为无 id |
| 查询 `/info` 有 id | **只传** `id`（请求层仍可附加 `_` / `skill_name`），**不带** keyword/url 等业务字段 |
| 查询无 id | 只传与 Create 相同的业务字段（兼容旧后端） |

有 id 时不带业务字段，是为避免上游「uuid 未命中则回落业务字段查他单」；未命中时按缺参/业务错误处理，由既有轮询与错误码承接。
