# 验证记录与已知边界

## 版本对应

| 项 | 版本 |
|---|---|
| 本 Skill 包 | **6.5.10**（文档修订，2026-10-29） |
| 运行包 | **6.5.4**（2026-10-28） |
| 真机验证 | UE 5.1.1 + UE 5.8.2 |

> 6.5.10 只改文档：未改 bridge、插件、DLL、命令实现。下面的运行包与真机数据
> 沿用 6.5.4；本次没有重新跑在线用例。

## 离线回归（运行包 6.5.4）

```text
820 passed / 95 skipped / 0 failed
```

- `95 skipped` 是需要真实编辑器的在线用例，不是失败；
- 离线覆盖：命令分发、参数校验、路径边界、幂等/锁、场景步骤、错误分类、
  fail-loud 分支；
- 移植包提供逐文件 SHA256 清单，可跨机比对。

## 真机矩阵（运行包 6.5.4）

| 项 | UE 5.1.1 | UE 5.8.2 |
|---|---|---|
| bridge 启动 / health | 通过 | 通过 |
| 会话锁冲突/释放 | 通过 | 通过 |
| 幂等重放/跨命令冲突 | 通过 | 通过 |
| 场景 command 步骤 | 通过 | 通过 |
| 场景高危命令拦截 | — | 通过 |
| AnimBP probe | 非 AnimBP 如实报 false | 真实 AnimBP 可读 |
| AnimBP read | 非 AnimBP fail-loud | 枚举 15 图；节点级未暴露，降级告警 |
| HTTP 413（9MB） | — | 通过 |
| stdio 34 工具 | — | 通过 |

## 本次实机冒烟（2026-10-29）

环境：Windows + UE **5.1.1-23901901**，引擎自带 Python 3.9.7，
运行包 **v6.5.4**，全新 `TP_BlankBP` 模板工程（非真实项目）。

| 步骤 | 结果 |
|---|---|
| `health` | `bridge_loaded=true`，engine 5.1.1 |
| `build_blueprint BP_Smoke` | `success=true` |
| `search_blueprint_nodes` | `BeginPlay` 命中事件候选；`PrintString` / `Delay` 未命中（引擎函数库不在 Python 包装内） |
| `apply_graph` BeginPlay→PrintString | 2 节点 / 1 连线，`verified=true`，`compiled=true` |
| `compile_and_diagnose` | `structured=true`，`compiled=true`，0 错误 |
| `get_pin_default_value` | `"Hello from skill test"`，`matched_by=guid` |
| `save_asset` | `saved=true`，22,749 bytes |
| `read_blueprint` L2 | 2 节点 / 1 连线；标题本地化（`事件开始运行` / `打印字符串`） |
| `verify_behavior` | `bHidden=false` → `verified=true`（`"False"` 因大小写失败，已记录） |
| `verify_scenario` | wait + log_contains，`verified=true`，JUnit 已写 |
| 任务账本 / 锁 / 撤销状态 | `task_begin/end`、`session_lock_*`、`agent_undo_status` 均可用 |

已知现象（不影响主路径）：

- 两个自启入口会各调一次 `start()`，第二个打印 `[Errno 10048] ... service stopped`；
  `/health` 正常，服务由第一个入口提供。
- `spawn_actor` 直接往 PIE 世界生成蓝图 Actor 返回 None；先放编辑器世界再 PIE 可正常
  BeginPlay（本次即用此路径验证）。
- 未采集实机截图（窗口失焦会导致 PIE 截图超时）；行为验证不依赖截图。

## 验证纪律

- 每个写操作读回比对，失败 `_fail_loud`；
- 编译走结构化诊断，不走日志正则猜；
- 场景 `verified` 只看断言/命令，截图失败只算证据失败；
- AnimBP 读不到节点时明确降级，不宣称节点可读；
- 移植包有逐文件 SHA256 清单，可跨机对比。

## 本次文档修订做了什么

- 元数据修正：明确本地 bridge 使用本机 token，无需外部 API Key；frontmatter
  声明 `requires_api_key: false`；
- 新增 `PITFALLS.md`（19 条蓝图陷阱 + 8 条构建/环境陷阱）与 `EXAMPLES.md`
  （6 个端到端示例）；
- `SKILL.md` 增加「何时不要用」「工具档位」，删除与 `COMMANDS.md` 重复的
  大表，商务/法务内容移到 `README.md`；
- 统一版本口径：删除内部 `skill v1.14.0` / `skill v2.0.1` 编号；
- 命令目录不再写死数量，改为以 `health.mcp_tool_count` / `tool_search` 为准。

## 没重跑的部分（如实说明）

- 本版未重跑完整 PIE 属性/截图场景，沿用 6.5.2–6.5.4 记录；
- 未新增 5.2–5.7 的真机记录（这些版本仍需自行重编译 bridge）；
- 未做跨机/跨网络（非 localhost）验证；bridge 无 TLS。

## 已知边界

- Windows only；
- UE 5.2–5.7 需自行重编译 bridge；
- 会话锁是协作式，不是编辑器强制锁；
- AnimBP 只读，写入未开放；
- 无 TLS；跨机使用需自建隧道；
- 复杂 PIE 场景请先在工程内小步试，再放进 `verify_scenario`。
