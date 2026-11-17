---
slug: ue5-automation
name: ue5-automation
displayName: UE5 Blueprint Automation
version: 6.5.10
runtime_version: 6.5.4
summary: "UE5 Blueprint Automation (UE5 蓝图自动化): AI reads/writes Blueprint graphs, diagnoses compile errors, verifies PIE behavior, and undoes task-level changes. Windows + UE 5.1/5.8; requires the ue5-automation bridge."
description: "UE5 Blueprint Automation (UE5 蓝图自动化): let AI read/write UE5 Blueprint graphs, compile with structured node_guid diagnostics, verify PIE runtime behavior, and undo at task level. Requires the ue5-automation bridge/MCP; Windows, UE 5.1/5.8. 本地 bridge 使用本机 token，无需外部 API Key。"
license: Apache-2.0
icon: https://skillhub-1388575217.cos.accelerate.myqcloud.com/skill-icons/uploads/805989/e73274f659954dc38e2e9ede4189e872.png
requires_api_key: false
homepage: https://github.com/miracle1814/ue5-automation
tags:
  - unreal-engine
  - unreal-engine-5
  - ue5
  - ue5-blueprint
  - ue_automation
  - ue-automation
  - unreal-automation
  - blueprint
  - blueprint-automation
  - 虚幻引擎
  - mcp
  - game-development
  - windows
  - automation
---

# UE5 蓝图自动化

## English summary

`ue5-automation` is the operating contract for the **ue5-automation** bridge. It lets an
AI agent read a Blueprint, write a whole graph in one transaction, compile with
structured `node_guid` diagnostics, verify PIE runtime behavior, save the asset, and
undo at task level. It requires the local bridge on Windows (UE 5.1/5.8; prebuilt for
5.1/5.8). It is not a code generator and does not execute arbitrary Python.

**Use it when** you need an agent to inspect or edit UE5 Blueprint graphs, fix compile
errors with node-level anchors, or prove a runtime behavior in PIE. **Do not use it**
for C++ code generation, packaging, or pure art work.

## 中文说明

本 Skill 是 `ue5-automation` 的**操作契约**，不是运行包。真正读写 UE 编辑器的是
`ue5-automation` bridge（UE 插件 + 本机 HTTP/MCP 服务）。它负责让 Agent：

- 动手前先读清资产和图；
- 用整图事务写入，而不是一个节点一个节点地试；
- 写完后编译、读回、运行时验证；
- 失败时诚实报错，不把“命令返回 200”当成“蓝图已改对”；
- 多 Agent 并发时用幂等键/资产锁避免互相踩踏。

> **版本对应：** Skill 包 `6.5.10` ↔ 运行包 `6.5.4`。本次只更新文档，运行时不变。

![UE5 蓝图自动化工作流总览](https://skillhub-1388575217.cos.accelerate.myqcloud.com/skill-overview-images/uploads/805989/ff18d2dcd40c4d1c86aa5159671584d0.png)

> 读 → 写 → 编译 → 验证 → 收尾；`verified=true` 才算通过。

## 何时使用

当用户提出以下需求时使用：

- “帮我读一下这个蓝图 / 变量 / 节点 / 连线”
- “给这个蓝图加一段逻辑 / 连一条线 / 改默认值”
- “从零建一个蓝图 / 加组件 / 加接口 / 加事件”
- “编译报错了，帮我定位是哪个节点”
- “跑一下 PIE，确认这个属性/日志/画面真的对”
- “撤回刚才的改动 / 这个任务改了哪些资产”

触发词：UE5、Unreal、蓝图、Blueprint、蓝图节点、PIE、UMG、Material、DataTable、
Gameplay、蓝图自动化、UE 编辑器。

## 何时不要用

以下场景不属于本 Skill，强行使用只会得到假成功或半成品：

- **C++ 代码生成、模块重构、Build.cs / 反射宏调整** → 用 C++ 工具链或 IDE，本 Skill 只操作蓝图/资产层。
- **打包、签名、上架、CI 分发** → 用 UAT 或专门的打包 Skill。
- **纯美术创作、材质外观设计、动画制作** → 本 Skill 能读写资产，但不代替创作工具。
- **没有安装 bridge、编辑器未启动、MCP 未连接** → 先按安装文档部署；不要假装工具可用。
- **需要执行任意 Python / 任意控制台命令** → 本 Skill 明确不支持，也不应尝试绕过白名单。
- **非 Windows 主机** → bridge 是 Win64 插件，其他平台不支持。

## 5 分钟最小成功路径

如果只想先确认“这东西真能用”，按下面跑一遍。

**Step 1 · health**

```json
{"command":"health","params":{}}
```

确认返回 `engine_version` / `bridge_loaded`。

**Step 2 · 建一个空蓝图**

```json
{"command":"build_blueprint","params":{"bp_name":"BP_Smoke","pkg":"/Game/Test/","parent":"Actor"}}
```

确认返回 `success=true`。

**Step 3 · 查候选（可选）**

```json
{"command":"search_blueprint_nodes","params":{"bp_path":"/Game/Test/BP_Smoke","query":"BeginPlay"}}
```

确认能返回事件候选。`search_blueprint_nodes` 对图内节点、蓝图自有函数/变量、
流程/事件目录可靠；引擎函数库（如 `KismetSystemLibrary`）在当前 Python 包装里
可能枚举不到——`PrintString` 搜不到不代表不存在，直接写完整类路径，写后
`read_nodes` 看实际引脚。

**Step 4 · 写入 BeginPlay → PrintString**

```json
{"command":"apply_graph","params":{
  "bp_path":"/Game/Test/BP_Smoke",
  "replace":true,
  "graph_spec":{
    "graph":"EventGraph",
    "nodes":[
      {"id":"begin","kind":"event","target":"ReceiveBeginPlay"},
      {"id":"print","kind":"function",
       "class":"/Script/Engine.KismetSystemLibrary",
       "target":"PrintString"}
    ],
    "edges":[{"from":"begin.then","to":"print.execute"}],
    "pin_defaults":{"print.InString":"Hello"}
  }
}}
```

确认返回 `verified=true`。

**Step 5 · 编译**

```json
{"command":"compile_and_diagnose","params":{"bp_path":"/Game/Test/BP_Smoke"}}
```

确认 `compiled=true`。

**Step 6 · 读回**

```json
{"command":"get_pin_default_value","params":{"bp_path":"/Game/Test/BP_Smoke","node_id":"<node_guids.print>","pin_name":"InString"}}
```

从 Step 4 返回体 `node_guids` 取 `print` 的 GUID，读回应为 `Hello`。

**Step 7 · 保存**

```json
{"command":"save_asset","params":{"asset_path":"/Game/Test/BP_Smoke"}}
```

确认文件落盘。

这条路径覆盖了“建资产 → 查节点 → 整图写入 → 编译 → 读回 → 保存”的核心闭环。

## 前置条件

| 项 | 要求 |
|---|---|
| 系统 | Windows 10/11 x64（bridge 是 Win64 插件） |
| 引擎 | UE 5.1.x 开箱可用；5.8.x 有预编译 DLL；5.2–5.7 需按源码重编译 |
| 编辑器 | 启用 `Python Editor Script Plugin` 与 `Editor Scripting Utilities` |
| 运行包 | 已安装 `ue5-automation` 插件、宿主脚本与 bridge（v6.5.4） |
| MCP | 已连接本机 `http://127.0.0.1:8889/mcp`，或已配置 stdio 代理 |
| 权限 | 用户明确授权写入当前 UE 工程 |

如果 `health` / `ue5_check_health` 不可用，**不要假装工具已连接**；先让用户按
`references/INSTALL-WINDOWS.md` 安装运行包并启动编辑器。

## 工具档位（先确认再调用）

运行包默认是 **gateway 档**，`tools/list` 只返回 12 个入口：

`ue5_check_health`、`ue5_tool_search`、`ue5_execute_command`、`ue5_read_blueprint`、
`ue5_search_blueprint_nodes`、`ue5_apply_blueprint_graph`、`ue5_compile_and_diagnose`、
`ue5_screenshot`、`ue5_verify_behavior`、`ue5_verify_scenario`、`ue5_task_begin`、
`ue5_task_end`。

另外两档（重启编辑器生效）：

- `UE5_MCP_CORE_TOOLS=1` → 18 个高频工具；
- `UE5_MCP_ALL_TOOLS=1` 或 `UE5_MCP_PROFILE=full` → 全量 34 个。

`health` 返回 `mcp_tool_profile` 与 `mcp_tool_count`。如果某个工具不在
`tools/list` 里，用 `ue5_tool_search{query}` 发现后直接 `tools/call`，或走
`ue5_execute_command{command, params}`；**不要因为目录里没看到就断言能力不存在**。

命令白名单 101 条（v6.5.4），数量随版本增长。**以 `health.mcp_tool_count` 和
`ue5_tool_search` 的结果为准，不要背数字。**

## 第一条规则：先检查工具可用性

在写任何资产之前，先调用：

```json
{"tool":"ue5_check_health","arguments":{}}
```

或：

```json
{"command":"health","params":{}}
```

预期返回包含 `engine_version`、`project_name`、`bridge_loaded`。如果失败：

1. 明确告诉用户“bridge 未连接/插件未加载”；
2. 不要继续写操作；
3. 按 `references/INSTALL-WINDOWS.md` 排查。

## 标准工作流

### 1. 读：先看清再动手

```json
{"tool":"ue5_read_blueprint",
 "arguments":{"bp_path":"/Game/Blueprints/BP_Door","level":"L2"}}
```

- L1：类信息、变量、CDO；
- L2：节点与连线；返回结构是 `result.l2.graphs[].nodes` / `.connections`；
  节点标题是本地化的（如 `打印字符串`），定位用 `guid`；
- `fields` 可裁剪返回字段，避免大图把上下文撑爆。

写图前还要查可调用节点和引脚签名：

```json
{"tool":"ue5_search_blueprint_nodes",
 "arguments":{"bp_path":"/Game/Blueprints/BP_Door","query":"Open","limit":20}}
```

### 2. 写：整图事务优先

主路径是 `apply_graph` / `ue5_apply_blueprint_graph`：

```json
{"tool":"ue5_apply_blueprint_graph",
 "arguments":{
   "bp_path":"/Game/Blueprints/BP_Door",
   "replace":true,
   "graph_spec":{
     "graph":"EventGraph",
     "nodes":[
       {"id":"begin","kind":"event","target":"ReceiveBeginPlay"},
       {"id":"print","kind":"function",
        "class":"/Script/Engine.KismetSystemLibrary",
        "target":"PrintString"}
     ],
     "edges":[{"from":"begin.then","to":"print.execute"}],
     "pin_defaults":{"print.InString":"Door opened"}
   }
 }}
```

硬规则：

- **超过 2 个节点的新图一律走 `apply_graph`**；`connect_pins`（命令）/
  `ue5_disconnect_pin`、`ue5_delete_node`（MCP 工具）只用于单点手术。
- `pin_defaults` 是**图级**字段，键为 `"<节点id>.<引脚名>"`；写在单个节点里不会生效。
- 函数节点必须带完整类路径（如 `/Script/Engine.KismetSystemLibrary`），
  只写 `KismetSystemLibrary` 在 5.8 上会定位失败。
- 节点引用优先用 32 位十六进制 GUID；用标题时不能有歧义。
- `replace=true` 才会替换已有图；空图首次写入也要显式确认。
- 返回值必须包含 `verified=true`；失败会回滚并返回错误，**不要重试同一份错误 spec**。
- 编译失败 ≠ 重写：图内容正确但编译不过时，走编译修复循环，不要推倒重来。

### 3. 编译：看结构化诊断

```json
{"tool":"ue5_compile_and_diagnose",
 "arguments":{"bp_path":"/Game/Blueprints/BP_Door"}}
```

每个错误尽量带：资产、函数/图、节点标题、`node_guid`、引脚提示、规则库
`pitfall_ref/fix_hint`。下次修改用 `node_guid` 定位，不要靠标题猜。

修复循环：

- 最多连续 5 轮；同参数重复失败 2 次提前熔断；
- 修复期间**不要 `save_asset`**，确认前所有改动只在内存里；
- 修复成功后必须 read-back，编译通过 ≠ 图是对的；
- `errors=[]` 不等于没有错误，结合 `warnings` 和 `compiled` 判断；
- 结果 Unknown（Live Coding 等）要如实说“不知道成没成”，不要报成失败。

### 4. 验证：编译通过不等于行为正确

运行时属性断言：

```json
{"tool":"ue5_verify_behavior",
 "arguments":{"actor_name":"BP_Door_1","property_name":"state",
              "expected":"Open","world":"pie","match":"exact"}}
```

多步场景（wait / assert / log_contains / screenshot / command）：

```json
{"tool":"ue5_verify_scenario",
 "arguments":{
   "name":"door_opens",
   "start_pie":true,
   "pie_mode":"simulate",
   "steps":[
     {"type":"wait","seconds":0.5},
     {"type":"assert","actor_name":"BP_Door_1","property_name":"state",
      "expected":"Open"},
     {"type":"log_contains","pattern":"Door opened","timeout":5},
     {"type":"screenshot","out_path":"door_scenario.png"}
   ]
 }}
```

- `verified=true` 才是通过；截图失败只算证据失败，不翻转 `verified`；
- `match:"exact"` 大小写敏感；bool 用小写 `true` / `false`（写 `"False"` 会判失败）；
- 场景默认禁止 `delete_asset`、`agent_undo`、`batch_asset_ops`、`apply_graph{replace}`
  等高危命令；需要时显式 `allow_destructive=true`；
- 总超时默认 300s，上限 1800s；
- 视觉验证先看 `camera_source`：`fallback` 机位的构图不能作为结论；
- `source="pie"` 在 PIE 未运行时会明确报错，不要拿编辑器画面冒充运行证据。

### 5. 收尾：保存 + 任务账本

```json
{"command":"task_begin","params":{"goal":"给门加 BeginPlay 打印"}}
{"command":"task_end","params":{"status":"success","summary":"..."}}
```

- 写命令会自动留一个可撤销的 UE 事务步；
- `task_begin` 在动手前调用；写操作之后再开任务，收尾会因无证据标 `unverified`；
- `agent_undo_status` 看可回滚步数，`agent_undo` 回滚最近 N 个 agent 步；
- 回滚遇到用户操作会立即停，不会跳过用户改动；
- 资产创建/删除**不在**撤销栈：回滚不会删新建蓝图，也不会恢复已删资产；
- 没有编译/写入/截图记录的任务，收尾会被标 `unverified`；先验证再声称成功。

## 多 Agent 协作

两个 Agent 同时写同一个蓝图时：

1. 写命令带 `session_id`（会话标识）；
2. 先 `session_lock_acquire{owner, assets:[...], ttl:600}`；
3. 冲突会返回 `asset_locked` / `session_lock`，不要重试同一资产；
4. 写完 `session_lock_release`，或等 TTL 过期；
5. 网络重试带 `idempotency_key`：同 key + 同命令/参数会重放上次成功结果，
   不会重复写；同 key 换命令会 `idempotency_conflict`。

锁是协作式，不是编辑器强制锁。所有写操作走 `execute_command` 才能经过锁层。

## 安全与授权

执行以下操作前必须得到用户明确同意：

- 删除资产；
- 批量重命名/搬迁；
- 替换已有图（`apply_graph{replace:true}`）；
- 保存/覆盖工程资产；
- 向工程写入新资产；
- 启停 PIE；
- 撤销用户已有操作。

只读查询（health/read/list/logs）不需要额外确认。其余边界：

- bridge 只监听 `127.0.0.1`，需要 `X-Skill-Token`；
- 没有默认 token；token 存在本机 `%APPDATA%\ue5_bridge\token`；
- 命令白名单，不允许任意代码执行；
- 资产路径只允许 `/Game/`；
- 删除/批量操作默认 dry-run 或需要 `confirm`；
- 不向外部服务上传工程内容；日志读取有允许根。

## 失败时怎么做

- **不要**把 `success=true` 当成“用户的目标已完成”；看 `verified`。
- 编译失败：先 `compile_and_diagnose`，按 `node_guid` 定位，再改。
- 写图失败：读回 `verified=false` 时不要继续叠加修改；先回滚/修正 spec。
- 工具不可用：明确说“MCP/bridge 未连接”，不要编造结果。
- 资产不存在：`asset_load` / `asset_not_found` 是明确失败，不要创建同名替代品
  除非用户要求。

## 边界

- Windows only；UE 5.2–5.7 需自行重编译 bridge；
- AnimBP 只读：能枚举图，节点级属性在部分版本未暴露；写入通道未开放；
- 场景真机验证覆盖 5.1/5.8 的 command/wait/断言；复杂 PIE 场景请先在工程内小步试；
- 无 TLS；跨机使用需自建隧道；
- UE 5.8 起项目自身 `Content/Python/init_unreal.py` 不再自动执行，自启依赖插件侧 init。

## 参考

- 安装与客户端配置：`references/INSTALL-WINDOWS.md`
- 命令目录：`references/COMMANDS.md`
- 端到端示例：`references/EXAMPLES.md`
- 已知陷阱（Top 20+）：`references/PITFALLS.md`
- 常见故障：`references/TROUBLESHOOTING.md`
- 安全模型：`references/SECURITY.md`
- 验证记录：`references/VERIFICATION.md`
- 项目主页：https://github.com/miracle1814/ue5-automation
