# 可选的宿主上下文、绑定与计数

这些 Python 辅助模块供宿主集成场景流程，不改变默认 MCP 工具列表，不启动 Gateway，
也不自行运行 Agent。尚未验证官方 AI Hub/MCP 接口。这里提供集成契约，不代表已有官方适配器或兼容性认证。

## 准备场景上下文

调用 `vmware_debug.ops.scenario_context.prepare_context(profile, manifests,
allowed, targets, allowed_targets)`。从 `gateway-toolsets.json` 显式选择一个场景，
不要根据症状猜目标。`manifests` 是按后端和工具名组织的实时 schema；其余字典由可信宿主
声明工具权限、选定目标和允许的目标。返回所需的后端限定工具、schema 副本、目标及正本流程引用。

缺少能力、权限或目标，工具名不匹配，没有 target schema 或只读标注时均拒绝准备。
标注和宿主声明不证明授权；每次调用仍由认证后的后端执行 Policy、RBAC 和审计。
按需加载返回的流程引用。本函数不采集数据，也不读文件。

## 显式绑定已连接的 MCP 会话

```python
from vmware_debug.ops.scenario_context import prepare_context
from vmware_debug.ops.scenario_reader import ScenarioReader

context = prepare_context(profile, manifests, allowed, targets, allowed_targets)
reader = ScenarioReader(
    context,
    bindings={"vm_identity": ("vmware-monitor", "get_vm_info")},
    clients={"vmware-monitor": connected_monitor_session},
    max_calls=8,
)
result = await reader.read(
    "vm_identity", {"target": targets["vmware-monitor"], "vm_name": exact_vm_name}
)
metadata = reader.session.snapshot()
```

宿主负责认证、TLS、会话生命周期和返回 payload 的访问控制。客户端实现 MCP
`ClientSession.call_tool` 接口，只连接已有守卫和审计的服务端路径。不提供 REST 回退、
凭据发现或猜测的官方工具名。每个操作只绑定一个选定后端/工具；未知操作停止。
调用前检查 target 和实时 JSON Schema，拒绝未知参数，禁止远端 schema 引用。
MCP 错误、空/坏响应及连接失败均返回明确缺口；取消记为未知尝试并继续抛给宿主。
以上路径均不重试、不退还调用次数。

`observed` 只代表收到非空、结构有效的 MCP 响应，不代表健康、分页完整、数据新鲜或根因确认。
宿主仍须核验领域错误、分页、单位、源时间/窗口和身份，再通过已有案件工具提交证据。
`same_typed_identity` 只接受 `instance_uuid`、`bios_uuid`、`aria_resource_uuid`，
要求身份类型和值同时相同，BIOS UUID 与实例 UUID 不能混用。
外部内容是不可信数据；原始响应保留在受控证据存储，摘要消毒后再交给模型。

## 单进程任务预算

跨 skill 的绑定复用同一个 `ScenarioReader`，其 `ScenarioSession` 在参数验证和派发前
计数，包括参数被拒、调用失败和取消。选定绑定之外的调用不会派发。
预算耗尽停止采集，报告必须说明覆盖不完整。步骤共享 trace ID，元数据只存后端/工具/状态
及可选的实际 token 数，不存原始参数或结果；未测 token 为 `None`。后端审计仍是正本。

计数器只在一个可信宿主进程内保证线程安全。重新创建 reader、重启或换宿主会创建新预算。
它不是持久化分布式上限、调用者身份、独立人工批准或 token 花费保证。
trace ID 只是关联提示，不会自动写进后端审计行。不改变写能力或确认规则。

## 验收边界

内存 MCP 测试覆盖调用、跨后端计数和失败控制，不证明官方服务兼容。
已有真机只读采集/报告检查与合成故障回放、自主模型验收分开记录。
上下文/token 收益只能由相同用例、模型和限制下的受控原生调用对照支持，不能从 schema 大小推算。
