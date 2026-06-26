---
name: scheduled-task-conflict-checker
description: 在确认任何 LUI/Claw 自然语言定时任务之前，检测重复任务、语义重叠、执行冲突和阻断性边界条件。当用户通过 LUI/Claw 创建或修改周期任务、定时任务、任务结果通知时使用；先标准化 LUI 任务，再与当前已有定时任务比较，并判断应该静默复用/更新、静默合并、要求用户确认、提示风险、阻断创建、部分创建或正常继续。
---

# 定时任务冲突检测

## 目标

在任何 LUI/Claw 自然语言定时任务写入、更新或确认前使用本 Skill。目标是避免用户创建重复任务、高风险重复写任务、不支持的平台/店铺任务，以及明显会排队或失败的高频任务。

本 Skill 只做创建前预检，不负责真正创建任务。输出结果必须归入以下决策之一：`proceed`、`reuse_or_update`、`silent_merge`、`ask_confirmation`、`block`、`partial_create`、`warn_then_proceed`。

## 输入信息

检测前收集或推断以下字段：

- 本次 LUI 任务：来源（可用时为 `lui` 或 `claw`）、用户原始表达、解析后的任务名称/内容、任务类型、执行时间、执行频次、店铺范围、平台范围、策略参数、通知设置。
- 当前已有任务：从 Task Service 或其它任务源拿到的当前任务，包含启用和暂停任务；排除已删除、已终止、历史已完成任务。
- 用户上下文：已绑定店铺、店铺授权状态、平台能力范围、ISV 高级版权限、通知绑定状态。

必须先把本次 LUI 任务标准化，再做比较。不要只比较用户原始话术。

## Workflow / 执行步骤

1. 读取本次 LUI 解析结果、当前已有定时任务和用户上下文。
2. 调用 `scripts/check_scheduled_task_conflicts.py` 标准化任务类型、店铺、平台、频次、时间和策略。
3. 先执行阻断性边界检查：店铺绑定、授权、ISV 高级版权限、平台能力、通知绑定。
4. 再执行重复和冲突检查：完全重复、语义重复、流程重复、策略差异、高风险写操作、高频堆积。
5. 输出标准决策和原因码；只有 `ask_confirmation`、`block`、`partial_create`、`warn_then_proceed` 需要给用户提示。
6. 在用户确认前，严禁创建、修改、合并或删除任何真实定时任务。

## 检测流程

1. 标准化本次任务。
   - 统一任务类型、店铺 ID、平台 ID、执行时间、执行频次、操作类型、资源范围和策略参数。
   - 将 LUI/Claw 话术映射到标准业务任务，例如把“每天 9 点上架商品”映射为 `auto_listing`。
   - 将本次 LUI 任务与调用方传入的所有当前任务比较，不关心存量任务最初来自哪里。

2. 先做边界检查，再做重复检查。
   - 无绑定店铺：阻断创建，引导绑定或开店。
   - 多店铺但未明确范围：要求用户选择全部店铺、某个平台下的店铺或指定店铺 ID。
   - 店铺授权失效：阻断该店铺；如果其它店铺有效，返回 `partial_create`。
   - 平台能力不支持：剔除不支持的平台/店铺，说明降级影响，并询问是否只为支持范围继续创建。
   - 缺少 ISV 高级版权限：阻断高级或高资源消耗任务，并提供开通或降频替代方案。
   - 通知渠道未绑定：除非用户明确要求该通知渠道是任务创建前提，否则不阻断任务执行；说明结果会回退到任务中心或 App Push。
   - 绑定与 ISV 高级版权限判断必须按 `references/permission-sql.md` 的 SQL 模板执行：绑定/授权来自 `1688-shopkeeper` 的店铺查询结果，ISV 权限来自 `/DistributeApiNew/checkShopPaidStatus` 的 `result.isPaid`。

3. 按顺序检测重复。
   - 完全重复：同店铺范围、同标准任务、同时间/频次、同策略。静默复用或更新已有任务。
   - LUI 语义重复：标准化后业务目标相同。策略没有实质变化时静默复用。
   - 流程重复：一个任务的前置步骤已被另一个流程覆盖，例如“选品”已包含在“选品+铺货”里。静默合并前置步骤。
   - 策略部分重复：同目标、同店铺范围，但策略参数不同，例如利润率 >=15% 与 >=10%。必须要求用户确认。
   - 高风险重复：批量下架、改价、发货、订单写入等高风险写操作存在重叠。不能静默合并，必须要求用户显式确认并给出保护规则。

4. 检测执行冲突。
   - 不同店铺且不同资源：允许继续。
   - 同平台多个店铺在同一时间执行 API 密集型写任务：可能进入平台级排队，通常不在创建时打断，除非频次过高。
   - 同店铺多个批量商品写任务：可能进入店铺级排队，任务中心展示排队状态。
   - 同商品字段写入：按商品/字段串行执行，后执行任务基于最新状态重新判断。
   - 同订单处理：按订单串行，同一订单只执行一次有效动作。
   - 高频任务，例如每 5 分钟或每 10 分钟，或执行周期短于预估耗时：提示风险，推荐更安全频次，除权益策略阻断外允许用户坚持。
   - 多任务集中在同一时间点：系统自动错峰或排队，默认不额外打扰用户。

5. 返回面向用户的结果。
   - 如果是 `block`，明确说明不能创建的原因和下一步可选动作。
   - 如果是 `ask_confirmation`，给出编号选项，在用户选择前不要创建任务。
   - 如果是 `partial_create`，列出支持和不支持的店铺/平台范围，并询问是否继续。
   - 如果是 `reuse_or_update` 或 `silent_merge`，默认不打扰用户，除非调用方需要内部审计说明。
   - 如果是 `warn_then_proceed`，说明风险、推荐调整方案，并允许用户继续。

## 脚本

当已经有结构化任务数据时，使用内置检测脚本：

```bash
python3 scripts/check_scheduled_task_conflicts.py input.json --format markdown
python3 scripts/check_scheduled_task_conflicts.py input.json --json
```

输入 JSON 结构：

```json
{
  "proposed_task": {},
  "existing_tasks": [],
  "user_context": {}
}
```

调用方需要机器可读结果时使用 `--format json`。输入路径传 `-` 时从标准输入读取 JSON。

## 输出契约

JSON 输出固定包含以下字段：

```json
{
  "decision": "proceed|reuse_or_update|silent_merge|ask_confirmation|block|partial_create|warn_then_proceed",
  "prompt_required": true,
  "normalized_proposed_task": {},
  "findings": [],
  "user_prompt": ""
}
```

退出码约定：`0` 表示检测成功并已输出决策；`2` 表示输入 JSON、文件读取或字段结构错误；其它非 0 表示脚本异常。`block` 和 `ask_confirmation` 是业务决策，不是脚本失败。

脚本会调用 `scripts/_tracker.py` 记录本地运行事件。打点只包含决策、是否需要提示和 finding 数量，不得记录用户原始话术、店铺名称、店铺 ID、商品、订单或任何授权凭证。

可选环境变量：`SCHEDULED_TASK_CONFLICT_CHECKER_TRACKING=0` 可关闭本地打点；`SCHEDULED_TASK_CONFLICT_CHECKER_TRACK_PATH=/path/to/file.jsonl` 可指定打点文件位置。

## Guardrails / 约束

- 严禁绕过本 Skill 直接创建高风险写任务，例如批量改价、批量下架、订单写入、发货或客服自动处理。
- 严禁把未绑定、授权失效、ISV 权限未知、ISV 权限接口异常当作可创建；这些情况必须 `block` 或 `partial_create`。
- 不得把当前任务列表当作前一日执行结果；本 Skill 只做创建前冲突检测。
- 不得静默合并策略不同或高风险写操作重叠的任务，必须要求用户显式确认。
- 不得在输出中暴露 AK、Token、Cookie、用户授权凭证、店铺敏感信息或完整订单数据。
- 如果输入缺少关键上下文，必须返回保守决策或要求确认，不能编造店铺、权限或任务状态。

## 参考

需要精确查看任务类型映射、重复/冲突优先级、LUI/Claw 提示模板时，读取 `references/rule-matrix.md`。

需要生成或核对绑定店铺、店铺授权、ISV 高级版权限的 SQL 判断时，读取 `references/permission-sql.md`。
