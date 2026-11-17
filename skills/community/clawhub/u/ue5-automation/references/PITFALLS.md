# 已知陷阱 Top 20+（症状 → 根因 → 修复）

> 用法：`compile_and_diagnose` 返回 `pitfall_ref` 时，直接跳到对应 ID；没有
> `pitfall_ref` 时按症状关键词查下表。这里是**修复用速查**，不是教程。

## 快速索引

| ID | 症状关键词 | 级别 |
|---|---|---|
| P01 | 蓝图编译过但事件不触发 / 拖不进场景 | 🔴 阻断 |
| P02 | `add_function_node` 返回 None / 节点没建 | 🔴 阻断 |
| P03 | 编译后 CDO 默认值被重置 | 🔴 阻断 |
| P04 | `connect_pins` 返回成功但没连上 | 🔴 阻断 |
| P05 | 跨调用节点引用变 None / 随机崩溃 | 🔴 阻断 |
| P06 | C++ 扩展运行时随机 Access Violation | 🔴 阻断 |
| P07 | `pin not found` / 引脚名对不上 | 🟡 警告 |
| P09 | `Variable ... type ... not found` | 🟡 警告 |
| P10 | `Referenced asset is null` | 🔴 阻断 |
| P11 | `Interface function not implemented` | 🟡 警告 |
| P12 | 蓝图 A ↔ B 循环依赖 | 🔴 阻断 |
| P13 | Tick 卡顿 / 帧率下降 | 🟡 警告 |
| P14 | 节点已废弃（deprecated） | 🟡 警告 |
| P17 | `/build` 成功但事件节点没建 | 🔴 阻断 |
| P18 | 同名节点只能改中一个 | 🟡 警告 |
| P19 | 照文档写 spec，节点建不出来 | 🟡 警告 |
| B1 | 中文路径 → MSVC C1083 | 🔴 阻断 |
| B2 | 编 5.8 找不到 VS 工具链 | 🟡 高 |
| B8 | `unreal.*` 报 GameThread / 元数据 unknown | 🟡 高 |
| B10 | 5.8 `pie_start` API 改名 | 🟡 高 |
| B11 | PIE 首张截图超时 | 🟡 中 |
| B15 | 编译错误提取为空 / 含旧错误 | 🔴 阻断 |
| B18 | 撤销步数为 0 / 标题为空 | 🔴 阻断 |
| B19 | 5.8 装了插件但服务没启动 | 🔴 阻断 |

---

## 蓝图陷阱

### P01 · 蓝图编译通过但事件不触发

**症状：** BeginPlay/Tick 不触发；蓝图拖不进场景。
**根因：** 用底层 `create_asset` 建蓝图，GeneratedClass 没注册，CDO 类型不对。
**修复：** 建蓝图一律用 `build_blueprint`（内部走原生 BlueprintFactory 流程），
不要自己用 `create_asset` 拼。

### P02 · 函数节点建不出来

**症状：** `add_function_node` 返回 None，没有引脚。
**根因：** 短类名无法被 `FindObject` 定位。
**修复：** 带完整类路径，如 `/Script/Engine.KismetSystemLibrary`；不确定就先
`search_blueprint_nodes`。

### P03 · 编译后 CDO 默认值被重置

**症状：** 先改 CDO 再编译，值丢了。
**根因：** 编译会重建 CDO，覆盖之前的 `set_editor_property`。
**修复：** 顺序改成“先编译，再取 `generated_class` 的 CDO 改值”。

### P04 · `connect_pins` 假阳性

**症状：** 返回成功，编辑器里没连线。
**根因：** 旧实现用“可行性验证”API 而不是“建立连接”API；类型不匹配时可能只
创建了隐式转换。
**修复：** 连线后用 `read_connections` 双向复核 `is_connected`；不要只信返回值。
新版本已修复底层实现，但验证纪律仍然保留。

### P05 · 跨调用节点引用丢失

**症状：** 第一次调用拿到的节点引用，第二次调用变 None；严重时随机崩溃。
**根因：** Python 侧 UObject 引用没有 UPROPERTY 保护，被 GC 回收。
**修复：** 同一张图的创建/连线/验证放在同一次调用里；主路径用 `apply_graph`
整图事务，不要跨轮次持有节点引用。

### P06 · C++ 扩展的 GC 野指针

**症状：** 运行时随机 Access Violation。
**根因：** `UObject*` 成员没加 `UPROPERTY()`，GC 追踪不到。
**修复：** 所有 UObject 成员加 `UPROPERTY()`；数组用 `TArray<TObjectPtr<...>>`。
（只影响自己写 C++ 扩展的用户。）

### P07 · 引脚名猜测失败

**症状：** `pin not found`。
**根因：** 引脚名随版本/节点类型变化；纯函数没有 exec 引脚。
**修复：** 连线前先 `search_blueprint_nodes` / `read_nodes` 拿实际引脚名，
不要凭记忆写。

### P09 · 变量类型找不到

**症状：** `Variable 'X' type 'TArray<FX>' not found`。
**根因：** 引用的结构体/枚举资产被移动、删除或未保存。
**修复：** 在 Content Browser 搜类型名；存在就 Refresh Nodes，不存在就重建
Structure/Enum，再编译。

### P10 · 引用资产丢失

**症状：** 节点引用为空；日志 `Referenced asset is null`。
**根因：** 资产被移动/删除/重命名，软引用解析不到。
**修复：** 用 Asset Registry 按名称找新路径并替换；确认已删除的资产要显式清理，
不要留空引用。

### P11 · 接口函数未实现

**症状：** 蓝图实现了接口但编译报缺函数。
**根因：** 接口升级后新增函数，蓝图里没有对应的 Function Override。
**修复：** 在事件图补缺失的接口函数实现（空实现也可以），再编译。

### P12 · 循环依赖

**症状：** A Cast/Spawn B，B 又 Cast/Spawn A；编译或加载卡住。
**根因：** 双向硬引用形成依赖环。
**修复：** 用 Interface 替代 Cast；用 Event Dispatcher 替代直接调用；或抽一个
中间蓝图/Subsystem 断开环。

### P13 · Tick 耗时过长

**症状：** 帧率下降，`stat game` 指向某个蓝图 Tick。
**根因：** Tick 里做 O(n) 遍历或重计算。
**修复：** 用 Timer 降频；大数据量用空间分区（Grid/Hash）；非 GT 工作考虑
AsyncTask/ParallelFor。

### P14 · 节点已废弃

**症状：** 编译/打开蓝图时提示 deprecated。
**根因：** 引擎升级后旧 API 被替换。
**修复：** 按提示和 Release Notes 找替代节点，替换后重新连线；不要忽略警告。

### P17 · 事件节点静默漏建

**症状：** 写入返回 `success=true`，但目标事件节点根本没建，编译还通过。
**根因：** 事件存在性判定把“本地化标题无关命中”当成已存在（例如把
`ReceiveActorBeginOverlap` 当成 `ReceiveActorEndOverlap`）。
**修复：** 写入后读回确认事件节点存在；检查返回的 `matched_by` / `candidates`；
新版本已修复判定逻辑，但“读回”仍是硬规则。

### P18 · 同名节点只能改中一个

**症状：** 图里有 3 个同名节点，只能改其中一个。
**根因：** 只用标题定位，同名场景不唯一。
**修复：** 先 `read_nodes` / `get_node_by_guid` 拿 32 位 GUID，再用 GUID 调
`set_pin_default_value` / `ue5_disconnect_pin` / `ue5_delete_node`。

### P19 · spec 字段名写错

**症状：** 照文档写 events/functions，节点建不出来，报错却指向“函数不存在”。
**根因：** 文档键名与实现键名不一致（`name` vs `event_name`，
`target_class` vs `function_path`）。
**修复：** 以运行包当前 schema 为准；events 用 `event_name`，functions 用
`function_name` + `function_path`；两者都缺时工具会 fail-loud 并回传实收 keys。

---

## 构建 / 环境陷阱

### B1 · 中文路径导致 MSVC C1083

**症状：** PCH 中间文件路径乱码，编译开局失败。
**根因：** GBK 码页与 MSVC/UBT 路径编码不一致；UE 官方要求纯 ASCII 路径。
**修复：** 仓库和项目放到纯 ASCII 路径（如 `D:/ue5-automation`）。

### B2 · 多引擎编译找不到工具链

**症状：** 编 5.8 报找不到 VS2019 14.29 工具链，21 秒失败。
**根因：** 用户级 `BuildConfiguration.xml` 钉死了旧 `CompilerVersion`。
**修复：** 临时挪开 `%APPDATA%`、`Documents`、`%APPDATA%\Local` 下三份
`UnrealBuildTool\BuildConfiguration.xml`，编译后恢复；长期按引擎版本分开管理。

### B8 · `unreal.*` 只能在 GameThread 调用

**症状：** `/health` 里 `engine_version` / `project_dir` 是 unknown；截图目录 404。
**根因：** HTTP/uvicorn 线程直接调 `unreal.*`，异常被吞成空值。
**修复：** 所有 UE API 走 GT 队列（bridge 已内置）；自己写扩展时不要从 HTTP
线程直接调 `unreal.*`。

### B10 · UE 5.8 的 PIE API 改名

**症状：** `editor_play_in_editor` 在 5.8 不存在。
**根因：** 5.8 改为 `EditorRequestBeginPlay()` / `EditorRequestEndPlay()` /
`IsInPlayInEditor()`。
**修复：** 用运行包内置的 `pie_start` / `pie_stop`，不要自己调旧 API；改 API 前
先 grep 引擎头文件。

### B11 · PIE 首张截图超时

**症状：** `capture_pie` 报文件不存在，几秒后文件自己出现。
**根因：** PIE 预热 + 截图延迟一帧 + PNG 编码，首张可能超过 2s。
**修复：** 工具已放宽轮询到 8s；仍失败就把编辑器调到前台重试，不要返回白图。

### B15 · 编译错误提取为空或含旧错误

**症状：** 编译失败但 `errors=[]`；或修好后仍看到上一轮错误。
**根因：** 中文/英文引擎日志格式不同；日志异步落盘；tail 窗口含历史行。
**修复：** 看 `compiled` 收敛，不只看 `errors`；结合 `structured` /
`errors_scope` / `warnings`；结构化通道异常时工具会 sleep 后重读一次。

### B18 · 撤销步数为 0

**症状：** 明明在事务里写，`agent_undo_status` 却报 `undo_count=0`；标题为空。
**根因：** `GetUndoCount()` 是“已撤销、可重做”的条数，不是可撤销数；可撤销数 =
`GetQueueLength() - GetUndoCount()`；下一步标题在队列末位。
**修复：** 只信 `agent_undo_status` 的 `agent_undoable` / `next_title` /
`redo_count`；不要自己读 `GetUndoCount`。

### B19 · UE 5.8 项目 init 不执行

**症状：** 插件 DLL 已加载，但 8889 没监听；5.1 同布局正常。
**根因：** 5.8 起不再执行项目自身 `Content/Python/init_unreal.py`。
**修复：** 自启挂到插件侧
`Plugins/ue5-automation-extras/Content/Python/init_unreal.py`；
`ue5_bridge.start()` 幂等，重复调用无害。

---

## 一句话纪律

- 看到 `success=true` 先找 `verified`；
- 同名节点先拿 GUID；
- 连线后必读回；
- 编译只看 `compiled`，不要被 `errors` 列表带偏；
- 失败就回滚，不要在同一份错误 spec 上重试。
