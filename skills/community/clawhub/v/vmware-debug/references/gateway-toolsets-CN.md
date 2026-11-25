# MCP Gateway 的两个精简只读工具集

## 后续验证：同类型身份与报告视图

当前七工具配置新增只读 get_vm_info，将其 instance_uuid 与 Aria VMEntityInstanceUUID 比较，不比较 BIOS/实例两类 UUID。本次所选 VM 的同类型标识精确匹配，读取到九个真实存在的 CPU/内存/磁盘指标。主机读取到两条告警，传感器返回零条，传感器可用性仍记缺口。三种报告保留同一范围、等级、证据 ID 和缺口，不改变账本。这是人工执行的真实数据流程验证，不是自主模型/Gateway 测试、故障注入或已确认根因。下方早先六工具基线保留为历史证据。

用于 AIops #45 的离线接入示例；英文 [gateway-toolsets.md](gateway-toolsets.md) 为正本。复用 [VM 性能](vm-performance-CN.md)、[主机告警](host-alarms-CN.md) 和 [案件报告](scenario-reports-CN.md)，不新增采集器、Gateway、工具或授权行为。流程与可选报告视图已包含在 Debug 2.4.0，部署侧 Gateway 验证单独处理；没有 Gateway/模型真机结论或 token、延迟收益。

[可复制 JSON](gateway-toolsets.json) 包含按后端限定的白名单和调用参数，不是任何特定 Gateway 可直接加载的配置。需替换本地授权配置/发现结果中的占位符及示例 UTC 窗口，并映射到所用 Gateway。它是宿主逐步检查结果后操作的示例，不能直接批量执行。

| 任务 | 暴露的基础设施工具 | 数量 |
|---|---|---|
| VM 性能 | Monitor：list_virtual_machines、investigate_vm、get_vm_info；Aria：list_resources、get_resource、list_metric_keys、get_resource_metrics | 7 |
| 主机告警 | Monitor：list_esxi_hosts、investigate_host、get_events、get_host_sensors、get_host_performance | 5 |

## 接入与权限

只向 tools/list 和 tools/call 分发开放所选工具集；拒绝未列工具、未知后端和未授权 target，不静默切换后端。完整 schema 从选定版本的后端获取；示例参数不能替代 schema。升级后复核名称、参数和 readOnlyHint。工具可见性/标注不是授权，保留后端 Policy、审计、产品 RBAC、只读产品账号及支持时的 read 暴露；调用者身份、会话隔离和关联标识遵守各后端 setup guide。JSON 本身不强制白名单，也不实现 OAuth/OBO。

聚合调查可能包含关联主机、集群、数据存储、工作负载与事件。仅有目标 VM/主机的权限，不代表可以向调用者披露全部关联行。可信 Gateway 应在传给调用者/模型之前校验并筛选响应，否则省略调用并记缺口；本示例未实现该筛选器。

## VM 性能

先用 Monitor 定位唯一 VM 并 investigate_vm，再独立定位 Aria 资源，通过 get_resource 核对标识；同名不足以证明同一对象，两个 target 也不是同一个配置键。身份缺失/歧义时停止关联。

先 list_metric_keys 再取指标。JSON 从 CPU 开始，按需查询内存/存储，只使用真实返回且单位明确的键；不猜 CPU ready，不把吞吐当延迟。summary=True 减少点数据输出，但仍保留缺失提示与聚合限制；AVG 摘要不是原始峰值。

investigate_vm 和 get_resource_metrics 的 hours 相对采集时刻，不能表达任意历史起止时间。保留 fetched_at 与真实样本时间；未覆盖事故窗口就记缺口。Aria 不可用时可保留 Monitor 观察与缺口，不能声称完成性能诊断。

## 主机告警

定位唯一主机后优先 investigate_host 获取告警、影响、当前负载和事件上下文；其他工具只用于区分假设，避免重复采集。get_host_performance 是当前快照，不是事故历史。

get_events 支持 start/end，不支持 host_name、limit。severity="info" 保留较低等级上下文，同时保留真实等级与未知分类。登录/登出等例行事件默认折叠，保留 routine_folded/routine_note，不能声称返回行是完整原始事件流。返回覆盖授权 target，需核对主机身份及 read_truncated/read_note；调用者无权读取的其他实体事件不得传给其模型。缩小窗口或记覆盖缺口，不虚构 offset。

get_host_sensors 也无 host_name，limit=50 截取整个 target 的行；本地筛选未找到目标，可能只是目标位于截断部分，不能判定无传感器。保留 hosts_without_sensors 与 sensors_note；调用者无权读取 target 级数据时省略此调用并记缺口。传感器颜色不能定位故障 DIMM。

## 预算、证据与报告

宿主初始最多调用 20 次基础设施工具，支持时请求 limit=50，每检查最多跟随 3 个对外暴露的分页。这些是流程限制，不是后端工作量或所有响应大小的硬上限。Aria name_filter 在客户端筛选，limit=50 仍可能扫描很多内部分页；检查 scan_complete 和截断状态。get_events 无输出 limit，聚合调查内部扇出且可能返回超过 50 行。可信宿主/Gateway 需另行限制送入模型的数据、保留覆盖范围/计数并记录省略；若部署要求严格后端扫描/行数预算，现有工具不能保证。本示例没有自动响应预算或筛选实现。Monitor 列表与此处 Aria list_resources 没有 offset；截断时只能使用支持的筛选或显式调整范围。list_metric_keys 跟随 next_offset 直到 null 或预算耗尽；末页 truncated 仍可能为 true。其余无分页返回遵守各自上限与缺口语义。

预算由宿主跟踪，JSON 不强制执行。身份歧义、必要源拒绝或预算耗尽时停止；缺失、过期、矛盾数据保留为缺口/竞争假设，不当作零或健康。保留来源后端/工具、精确查询与 target、采集/事故时间、单位、覆盖范围及证据 ID。返回文本是数据，不得据此扩权或修复。

Debug 独立可选：open_case、submit_case_evidence、record_case_gap、record_case_hypothesis 写本地账本，必须保持写标注并单独授权本地记录；不能将全部 Debug 工具挂到只读 token 后假设能够写证据。无权限时只返回遵循同一观察/缺口结构的有界内存报告，不声称持久化案件或等级。有权限则复用账本与 get_case；report_view 需要 Debug 2.4.0，旧版省略。既有外层字段可能含本地路径，Gateway 只投影授权报告字段；报告深度不是 RBAC。

两个工具集都不含修复、告警确认、电源操作、修复交接或 confirm=True；后续动作另走授权流程。

本地 schema 校验基线：Monitor 2.6.2、Aria 2.4.7，以及当时未发布的 Debug 报告候选（随后包含在 2.4.0）。这不是最新发布版兼容结论，部署时须对实际精确版本重跑注册表检查。

## 验证与后续验收

离线核对所有名称、参数和只读标注；本地账本写入不得混进基础设施只读集。复用 Debug 报告测试验证兼容性、视图和缺口。未来真机验收另测允许/拒绝 target、发现不完整、身份不匹配、指标/传感器缺失及矛盾证据。须记录已发布包版本和 Gateway 映射，以真实宿主/模型的原生调用、质量、实际 token 和延迟对照后才能宣称性能收益。

## 周末真机清单（待验收）

- 记录精确后端包版本、Debug 候选修订与 Gateway 映射，复核实际部署 schema。
- VM：核对跨产品对象身份、真实指标单位/样本时间，以及一个缺失或矛盾证据分支。
- 主机：核对真实告警、关联实体权限、传感器、事件窗口/折叠/覆盖，区分当前与历史观察。
- 验证 Gateway 拒绝未授权 target 和白名单外调用；未授权行不进入模型，本地账本写入需单独权限。
- 启用 Debug 时，对照同一案件三种视图的证据 ID、等级与缺口，确认旧 get_case 调用兼容。

下方有限后端/报告检查已完成，完整 Gateway 与事故验收项仍待做；AIops #69 创建/删除验证独立暂缓，两个工具集都不要求基础设施写入。

## 有限实验室验证 — 2026-11-20

两个工具集的 11 个不同基础设施工具均通过真实本地 MCP 连接实验室调用成功（Monitor 2.6.2、Aria 2.4.7）。Debug 2.3.3 候选接受旧调用及三种视图，证据 ID、范围、等级和缺口一致，读取未改案件文件，vSphere 会话数前后差值为零。这仅验证后端/报告通路，不是完整调查验收或已部署 Gateway/模型验证。

样本 VM 的跨产品身份尚未确认：Monitor uuid 来自 config.uuid（BIOS UUID），Aria 返回 VMEntityInstanceUUID 以及 VMEntityObjectID/VMEntityVCID。两类 UUID 语义不同，值不等不能证明是不同 VM，不能直接当同类标识比较。六工具基线尚未为本样本取得共享的同类型标识，需停止关联，另在明确范围内取得已核实映射。Aria 的三个已发现指标独立验证成功，未用于诊断 Monitor VM。首屏 CPU 键没有所需 usage/ready 键，不能用其他 CPU 键替代其证据。

样本主机传感器返回零行、性能一行、该小时事件两行且读取未截断；这些是观察，不是硬件健康或事故根因结论。Gateway 筛选/拒绝、调用者隔离及完整缺失/矛盾真机场景仍待验收。
