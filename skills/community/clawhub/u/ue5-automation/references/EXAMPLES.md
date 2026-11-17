# 端到端示例（可直接照抄）

> 所有示例都假设 `health` 已通过、bridge 已连接。命令与 MCP 工具二选一即可；
> 这里统一用 `{"command":..., "params":...}` 形式，MCP 客户端可换成
> `{"tool":"ue5_...", "arguments":...}`。

## 1. 读懂一个蓝图

```json
{"command":"read_blueprint","params":{"bp_path":"/Game/Blueprints/BP_Door","level":"L1"}}
```

L1 只返回类信息、变量、CDO，适合先判断“这是什么”。需要节点和连线时再读 L2：

```json
{"command":"read_blueprint","params":{"bp_path":"/Game/Blueprints/BP_Door","level":"L2"}}
```

L2 结果在 `result.l2.graphs[]`，每个图有 `nodes[]` 和 `connections[]`；节点标题是
本地化的（如 `打印字符串`），定位用 `guid`。

大图不要一次全读：先用 L1 定位，再用 `read_nodes` / `get_node_by_guid` 按需读；
`read_blueprint` 支持 `fields` 裁剪返回字段。

## 2. 从零建蓝图并写入第一段逻辑

### 2.1 建空蓝图

```json
{"command":"build_blueprint","params":{
  "bp_name":"BP_Door",
  "pkg":"/Game/Blueprints/",
  "parent":"Actor"
}}
```

确认 `success=true`。失败时不要用 `create_asset` 绕过（会得到不可用蓝图，见
`PITFALLS.md` P01）。

### 2.2 查候选（可选）

```json
{"command":"search_blueprint_nodes","params":{
  "bp_path":"/Game/Blueprints/BP_Door",
  "query":"BeginPlay"
}}
```

确认事件候选可用。`search_blueprint_nodes` 对图内节点、蓝图自有函数/变量、
流程/事件目录可靠；引擎函数库（如 `KismetSystemLibrary`）在当前 Python 包装里
可能枚举不到，`PrintString` 搜不到不代表不存在。直接写完整类路径，写后
`read_nodes` 看实际引脚。

### 2.3 整图写入

```json
{"command":"apply_graph","params":{
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

确认返回 `verified=true`。`success=true` 但 `verified=false` 时看 `errors` 和
`node_guids`，不要继续叠加修改。返回体里的 `node_guids` 已经把 spec id 映射到
32 位 GUID，后续读回/改值都用这个 GUID。

### 2.4 编译 + 读回 + 保存

```json
{"command":"compile_and_diagnose","params":{"bp_path":"/Game/Blueprints/BP_Door"}}
```

```json
{"command":"get_pin_default_value","params":{"bp_path":"/Game/Blueprints/BP_Door","node_id":"<node_guids.print>","pin_name":"InString"}}
```

```json
{"command":"save_asset","params":{"asset_path":"/Game/Blueprints/BP_Door"}}
```

编译看 `compiled=true`；读回应为 `Door opened`；保存后再确认文件落盘。

## 3. 修一个编译错误

### 3.1 拿结构化错误

```json
{"command":"compile_and_diagnose","params":{"bp_path":"/Game/Blueprints/BP_Door"}}
```

返回类似：

```json
{
  "success": false,
  "compiled": false,
  "errors": [{
    "code": "E-BP-REF-NULL-ASSET",
    "message": "Missing Asset /Game/Mesh/Cube",
    "asset": "/Game/Blueprints/BP_Door",
    "function": "OnOverlap",
    "node_guid": "A1B2C3D4E5F6...",
    "node_name": "Branch",
    "pin_hint": "Condition",
    "pitfall_ref": "PTN-010",
    "fix_hint": "扫描 Content Browser ..."
  }],
  "warnings": []
}
```

### 3.2 按 GUID 定位并修

```json
{"command":"get_node_by_guid","params":{
  "bp_path":"/Game/Blueprints/BP_Door",
  "node_guid":"A1B2C3D4E5F6..."
}}
```

```json
{"command":"set_pin_default_value","params":{
  "bp_path":"/Game/Blueprints/BP_Door",
  "node_id":"A1B2C3D4E5F6...",
  "pin_name":"Condition",
  "new_value":"true"
}}
```

### 3.3 重新编译并读回

```json
{"command":"compile_and_diagnose","params":{"bp_path":"/Game/Blueprints/BP_Door"}}
```

```json
{"command":"read_nodes","params":{"bp_path":"/Game/Blueprints/BP_Door"}}
```

最多 5 轮；同参数失败 2 次就停下换方向。修复期间不要 `save_asset`。

## 4. PIE 行为验证（不是只看编译）

```json
{"command":"verify_scenario","params":{
  "name":"door_opens",
  "start_pie":true,
  "pie_mode":"simulate",
  "steps":[
    {"type":"wait","seconds":0.5},
    {"type":"assert","actor_name":"BP_Door_1","property_name":"state","expected":"Open"},
    {"type":"log_contains","pattern":"Door opened","timeout":5},
    {"type":"screenshot","out_path":"door_scenario.png"}
  ]
}}
```

判据：

- `verified=true` 才是通过；
- 截图失败只算证据失败，不翻转 `verified`；
- 场景默认拒绝 `delete_asset` / `agent_undo` / `batch_asset_ops` /
  `apply_graph{replace}`；需要时显式 `allow_destructive=true`；
- 复杂场景拆小，总超时默认 300s。

单属性断言（bool 用小写；`match:"exact"` 大小写敏感）：

```json
{"command":"verify_behavior","params":{
  "actor_name":"BP_Door_1","property_name":"bHidden",
  "expected":"false","world":"pie","match":"exact","capture":false
}}
```

## 5. 用户说“撤回刚才的改动”

```json
{"command":"agent_undo_status","params":{}}
```

返回 `agent_undoable`、`next_title`、`next_is_agent`、`redo_count`。

```json
{"command":"agent_undo","params":{"count":1}}
```

读返回：

- `undone`：实际撤掉的步数；
- `titles`：撤掉的事务标题；
- `stopped_reason`：为什么提前停（最常见是“中间用户手动改过”）。

`undone < 请求数` 时，把 `stopped_reason` 用人话转述给用户，不要假装全撤了。
资产创建/删除不在撤销栈。

## 6. 两个 Agent 同时改一个工程

```json
{"command":"task_begin","params":{"goal":"给传送门加进入提示"}}
```

```json
{"command":"session_lock_acquire","params":{
  "owner":"agent-a",
  "assets":["/Game/Blueprints/BP_Portal"],
  "ttl":600
}}
```

```json
{"command":"apply_graph","params":{
  "bp_path":"/Game/Blueprints/BP_Portal",
  "replace":false,
  "idempotency_key":"portal-hint-v1",
  "graph_spec":{
    "graph":"EventGraph",
    "nodes":[
      {"id":"overlap","kind":"event","target":"ReceiveActorBeginOverlap"},
      {"id":"print","kind":"function",
       "class":"/Script/Engine.KismetSystemLibrary",
       "target":"PrintString"}
    ],
    "edges":[{"from":"overlap.then","to":"print.execute"}],
    "pin_defaults":{"print.InString":"Enter portal"}
  }
}}
```

> `replace=false` 只适用于空图；如果 `BP_Portal` 的 EventGraph 已有内容，先
> `read_blueprint` 看现状，确认后再用 `replace=true`，否则工具会拒绝写入。

```json
{"command":"session_lock_release","params":{
  "owner":"agent-a",
  "assets":["/Game/Blueprints/BP_Portal"]
}}
```

```json
{"command":"task_end","params":{"status":"success","summary":"传送门进入时打印提示"}}
```

约定：

- 冲突返回 `asset_locked` / `session_lock`，不要重试同一资产；
- 同 `idempotency_key` + 同命令/参数会重放上次成功结果，不会重复写；
- 同 key 换命令返回 `idempotency_conflict`；
- 锁是协作式，所有写操作走 `execute_command` 才经过锁层。
