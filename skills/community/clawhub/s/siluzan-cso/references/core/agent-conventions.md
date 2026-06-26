# Agent 执行规范（数据处理纪律唯一真相源）

> 本文件是 siluzan-cso Skill 下 AI 助手的**通用数据纪律**：加载纪律、数据处理协议、防工具死循环、交付自检。
> 各域 reference（`references/*.md`）只讲命令参数与字段口径，**不再重复**这些规则，需要处单行指向本文件。
> 脚本示例（`--json-out` + `node -e` 读盘）见 `references/core/tips.md`。

---

## 一、文档加载纪律

本 Skill 采用 **SKILL 路由 + references 按需加载**；**「按需」= 每个用户任务都要按需，不是整段对话只读一次**。

| 触发                                                             | 动作                                                                                                                                                                          |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **新的用户任务 / 同对话内换话题**（新账号、新平台、新报表/规划） | 按 `SKILL.md` 命令索引 **重新 Read** 该任务对应的 `references/<域>.md` 后再执行 CLI；**禁止**沿用上一任务的参数记忆——对话会被压缩，「读过」≠ 当前上下文仍含正确字段名与 flags |
| **上下文被压缩 / 记不清字段或命令**                              | 重读 `SKILL.md` 命令索引 + 当次任务 reference                                                                                                                                 |
| **CLI 返回 400 / 字段对不上**                                    | 回到对应 reference 核对参数名与口径，**勿猜**                                                                                                                                 |

所有 ID、命令 flags、业务数值以**当次 Read 的文档 + 当次 CLI 输出**为准；数值只来自本次 stdout 或脚本读盘结果，不引用对话记忆里的示例值。

---

## 二、数据处理协议（最高优先级，防工具死循环）

读取/列表/检索/详情类命令（`list-accounts`、`account-group list`、`persona list`、`rag list/query`、`report fetch/records`、`planning enterprises/content-types/list/get`、`task list/detail/comment list`、`list-members`）都支持 **`--json-out <路径>`**：业务数据落盘为唯一真相源，stdout 只回**一行摘要 + agentHint**。每条 `--json-out` 命令成功后**必须按顺序**处理，不要跳步：

1. **解析 stdout 一行摘要 JSON**：拿到 `outlineFile`、`writtenFiles[0]`、`manifestFile`、`agentHint`。摘要里**没有** `total` / `items` 等业务字段——**禁止对 stdout 写翻页循环**，业务数据只在 `writtenFiles[0]` 落盘文件里；**不要**硬编码 `<section>.json` 文件名，以摘要里的 `writtenFiles[]` / `manifestFile` 为准。
2. **【outline 门禁·先读完再动手】Read 当次产出的每个 `*.outline.txt`**（schema-only，通常 <2KB）确认字段树后**才可**写脚本。类型字面量是**最后一个不以 `//` 开头的行**（提取写法 `outlineRaw.trimEnd().split('\n').filter(l => !l.startsWith('//')).pop()`）。outline 是结构描述，**不是数据**，勿当 JSON `require`、勿贴给用户。**字段真相源 = 当次 outline**；SKILL.md / reference 里出现的字段名都是说明性示例，凡 outline 未确认的字段路径**禁止**凭印象写进脚本。
3. **编写并执行脚本**（`node -e` / `.mjs` / `python`）`readFileSync` / `require` 读 `writtenFiles[0]` 做筛选、聚合、计算；**永远不得**用宿主 Read / `cat` / `type` / `Get-Content` 打开落盘业务 `*.json`（可能 MB 级，会撑爆上下文）。
4. **交付物用代码写出**；向用户展示的数字须来自**脚本 stdout**，不在对话里手填、改数、心算汇总。

| 允许 Read 的文件                        | 必须用代码读取的文件                       |
| --------------------------------------- | ------------------------------------------ |
| `references/**/*.md`（Skill 文档）      | 所有 `--json-out` 业务 `*.json`            |
| 当次 `*.outline.txt`                    | manifest 中的路径索引（脚本 `JSON.parse`） |
| stdout 一行摘要、你刚写出的最终产物文件 | 用户提供的同构大 JSON                      |

**已有 JSON 不重跑**：用户已保存输出，或只问「怎么从一坨 JSON 里筛字段」时，**直接读本地文件**喂给脚本，不必为示例再执行业务命令。

**无结果即停**：用户指定的账号 / 知识库 / 任务 ID 查无结果时，**如实告知用户并停止**，禁止翻页 grep 自行换 ID 或反复重跑命令（会导致报错户、死循环）。

**中间结果一律落盘**：跨步骤数据不靠对话记忆；Windows 避免管道传 JSON，优先 `--json-out` + `node -e` 读文件。

---

## 三、`--json` 已移除

为杜绝整坨 JSON 打到 stdout 引发的翻页死循环，数据命令的 `--json` **已移除**，统一改用 `--json-out <目录或 *.json 文件>`。若仍传 `--json`，CLI 会 exit 1 并提示改用 `--json-out`（`workflow validate` 例外，其输出小、保留 `--json`）。写入/动作类命令（`publish`、`upload`、`persona create`、`account-group create/update/delete/...`、`task start/stop/...`、`planning generate/regenerate/...`）只输出简洁人类可读确认，无需 `--json-out`。

---

## 四、执行流程与交付自检

**计划 → 确认 → 执行 → 验证 → 预测**：

1. 按 §一 Read 当次任务 reference → 用 `-h` 确认命令 → 向用户输出操作计划。
2. 涉及写入/修改/删除的操作**必须先与用户确认**。
3. 按计划执行，说明每步意图。
4. 用成对的读命令复核写入结果；异步任务（`planning watch`、`task` 发布）按提示轮询直到完成/失败。
5. 报告 / 含数字话术交付前，**亲自 Read 最终产物**核对：数字来自脚本 stdout、账号 ID 与用户给定一致、无模板占位残留、空数据章节明确标注（禁止编造数字填坑）。
6. 全部完成后预测用户下一步操作。
