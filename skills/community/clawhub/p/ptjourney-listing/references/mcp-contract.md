# PTJourney 批量上架 MCP 工具契约

新版客户端通过 stdio MCP 连接本机已登录的 PTJourney。安装方式见 [mcp-setup.md](mcp-setup.md)。连接后仍须用 `tools/list` 与 `ptj_listing_capabilities` 确认该客户端实际可用。

## 共同输入

批次输入包含 `platform`（`ozon_standard`、`ozon_pod`、`wb`、`temu`）、工作簿绝对路径、图片根目录绝对路径、目标店铺 ID 列表和任务名称。创建时另传批次幂等键。数据文件留在本机，不向 IDE 传登录凭据。单批最多 200 行、20 店；预检计划有效期 15 分钟。

统一工作簿允许混合平台，但执行时按平台、店铺和模板拆分。Ozon 标品与 Wildberries（WB） 逐商品建任务；TEMU 每店一任务；Ozon POD 一批可含多个店铺。

## 已开放的 MCP 工具

| 工具 | 作用 | 重要返回 |
| --- | --- | --- |
| `ptj_listing_capabilities` | 读取当前登录账号及四个平台输入要求 | 不返回 Token/API Key。 |
| `ptj_listing_reference` | 只读查询店铺、模板、仓库、Ozon 类目/属性/字典、WB 类目/属性 | `kind`、`platform` 及按需的店铺和类目 ID。 |
| `ptj_listing_preflight` | 解析 `products.xlsx`、图片目录并核对店铺归属、逐行必需字段 | 摘要、逐行错误、15 分钟有效 `planId`。 |
| `ptj_listing_create_batch` | 创建真实任务，按幂等键阻止重复提交 | `batchId`、逐任务 `taskId`、状态。 |
| `ptj_listing_start_batch` | 启动 TEMU 执行器或 Ozon POD 任务 | Ozon 标品和 WB 创建后自动进入队列。 |
| `ptj_listing_batch_status` | 查看客户端任务和可选平台明细 | `includeRemote=true` 时读取远端任务。 |
| `ptj_task_list` | 按平台分页查询上架任务 | Ozon 标品/POD共用 `platform=ozon`；WB、TEMU需当前账号店铺 ID。 |
| `ptj_task_detail` | 读取 Ozon 或 WB 任务明细 | TEMU上架任务用 `ptj_task_list` 按店铺查看。 |
| `ptj_task_logs` | 读取 Ozon 标品/POD 任务日志 | 支持分页与日志级别。 |
| `ptj_task_action` | Ozon/TEMU任务暂停与继续；WB继续与失败子队列重试 | `confirm=true`；TEMU必传店铺 ID；WB子队列可选 `confirm`、`media`、`price`、`stock`。 |
| `ptj_runner_state` | 读取 TEMU 上架执行器状态 | 只读。 |
| `ptj_runner_control` | 启动或暂停本机全部 TEMU 上架执行器 | 全局动作，需 `confirm=true`。 |

`create_batch` 会产生业务写入。先展示账号、店铺、商品数、价格范围并取得该批授权，再传 `confirm=true` 和稳定 `idempotencyKey`。客户端再次核对账号；本机桥接仅监听回环地址，用随机会话令牌鉴权，不使用旧浏览器插件通道。

任务管理也只通过客户端现有处理器执行。查询按当前登录账号进行；会改变任务状态的 `ptj_task_action` 与全局执行器控制要求明确目标和 `confirm=true`。返回会移除 Token、密钥及原始请求快照。不要把通用 IPC 名称当 MCP 工具直接调用。

若 Ozon POD 返回 `requiresOzonProductLimitConfirmation=1`，先向用户展示 `ozonProductLimitWarnings`。用户同意后，使用**同一** `planId` 和 `idempotencyKey` 再调用 `create_batch`，增加 `confirmOzonProductLimitWarning=true`。客户端仅允许对该额度警告明确失败的任务重提；其他已创建或结果未知的任务不会重复提交。

`created` 仅表示客户端任务创建成功，不代表平台商品成功。`uncertain` 表示提交结果未知，先到平台任务明细核对。当前没有自动重试失败项的 MCP 工具；修正数据后重新预检并用新幂等键提交明确失败的货号。
