# 命令目录（按任务分组）

完整命令以运行包为准，本文只列 Agent 最常用的入口。**不要在提示词或脚本里
写死命令总数**：数量随版本增长，先 `health` 看 `mcp_tool_count`，或
`ue5_tool_search{query:"关键词"}` 发现。

调用形式二选一：

```json
{"tool":"ue5_read_blueprint","arguments":{"bp_path":"/Game/BP_Door","level":"L2"}}
{"command":"read_blueprint","params":{"bp_path":"/Game/BP_Door","level":"L2"}}
```

工具目录有三档：`gateway`（默认 12 个入口）、`core`（18 个）、`full`（34 个）。
不在 `tools/list` 里的能力，用 `ue5_tool_search` 发现后 `tools/call`，或走
`ue5_execute_command`。

## 读

| 命令 | 用途 |
|---|---|
| `health` | 引擎/项目/bridge 状态、工具档位 |
| `list_assets` | 列资产 |
| `read_blueprint` | L1/L2/full 读蓝图；`fields` 裁剪返回 |
| `read_variables` | 变量 |
| `read_cdo` | 类默认对象 |
| `read_nodes` | 节点 |
| `read_connections` | 连线 |
| `search_blueprint_nodes` | 按关键词查可调用节点 + 引脚签名 |
| `get_pin_default_value` | 读引脚默认值 |
| `get_node_by_guid` | 按 GUID 定位节点 |
| `find_actors` / `get_actor_properties` | 关卡 Actor |
| `logs_read` | 游标增量日志 |
| `datatable_read` | DataTable 行 |
| `class_probe` / `debug_reflect` | 类/反射探针 |
| `animbp_probe` / `animbp_read` | AnimBP 只读 |

## 写蓝图

| 命令 | 用途 |
|---|---|
| `build_blueprint` | 原子建资产（失败回滚） |
| `apply_graph` | 整图声明式写入（主路径） |
| `add_variable` | 加变量 |
| `add_component` / `remove_component` | 加/删组件 |
| `add_implemented_interface` | 加接口 |
| `add_event_dispatcher` | 加事件分发器 |
| `add_function_node` | 加函数调用节点 |
| `connect_pins` | 连线（拓扑验证） |
| `ue5_disconnect_pin` | 断线（MCP 工具；白名单无同名命令） |
| `ue5_delete_node` | 删节点（MCP 工具；白名单无同名命令） |
| `set_pin_default_value` | 改默认值 |
| `set_node_position` | 移动节点 |
| `add_cast_node` / `add_macro_node` / `add_switch_node` | 常用节点 |
| `set_class_default` | 改 CDO（**编译后**再改） |
| `save_asset` | 保存 |
| `delete_asset` | 删除（高危，需确认） |

## 编译 / 验证

| 命令 | 用途 |
|---|---|
| `compile_blueprint` | 编译 + 回读状态 |
| `compile_and_diagnose` | 结构化错误（带 `node_guid` / `pitfall_ref`） |
| `pie_start` / `pie_stop` / `pie_state` | PIE 生命周期 |
| `verify_behavior` | 运行时属性断言 |
| `verify_scenario` | 多步场景 + JUnit |
| `capture_viewport` / `capture_pie` | 截图证据 |
| `spawn_actor` / `set_actor_transform` | 运行时/关卡 Actor 操作 |

## 资产治理

| 命令 | 用途 |
|---|---|
| `batch_asset_ops` | 批量重命名/搬迁，默认 dry-run |
| `task_assets` | 任务资产账本 |
| `rollback_task_assets` | 回滚任务创建/删除的资产 |

## 任务 / 撤销

| 命令 | 用途 |
|---|---|
| `task_begin` / `task_step` / `task_end` | 任务账本 |
| `task_list` / `task_error` | 任务列表 / 错误记录 |
| `agent_undo_status` | 可回滚步数、下一步标题 |
| `agent_undo` | 回滚最近 N 个 agent 步 |

## 多 Agent

| 命令 | 用途 |
|---|---|
| `session_lock_acquire` | 抢显式资产锁 |
| `session_lock_release` | 释放 |
| `session_lock_status` | 查看 |
| `receipt_list` | 最近写回执 |
| `idempotency_key`（参数） | 重试不重复写 |

## 其他

材质：`material_create` / `material_add_expression` /
`material_connect_expressions` / `material_connect_property` /
`material_set_expression_property` / `material_compile` / `material_read` /
`material_instance_create` / `material_instance_set_parameter`

UMG：`widget_create` / `widget_add_child` / `widget_set_property` /
`widget_read_tree`

DataTable：`datatable_read` / `datatable_write_csv` / `datatable_create`

批量：`editor_batch`（白名单命令序列；场景验证不要放进来）

> 不确定命令名时先 `tool_search{query:"关键词"}`，不要猜参数。
