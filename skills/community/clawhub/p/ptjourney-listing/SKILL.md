---
name: ptjourney-listing
description: "PTJourney 跨境电商 AI 批量上架助手，支持 Ozon ERP、Wildberries（WB）ERP、TEMU ERP 工作流。整理 1688 商品、预检上架数据、管理已授权任务，通过已登录 Windows 客户端的本机 MCP 操作。Use for marketplace product listing and task management."
license: MIT-0
---

# PTJourney 跨境电商上架助手 · Ozon / Wildberries / TEMU

本 skill 指导 IDE 中的 AI 整理 1688 商品数据，并通过当前登录的 PTJourney 客户端执行 MCP 批量上架。本仓库仅提供操作说明；实际工具由已安装客户端和另行下载的官方 MCP 包提供。先按 [MCP 安装与连接](references/mcp-setup.md) 配置 ZCode、WorkBuddy 或 Codex，并调用 `ptj_listing_capabilities` 确认连接。

## 工作流

1. 用 `ptj_listing_reference` 读取账号下的店铺、模板、仓库和动态类目属性。类目 ID、字典值和店铺 ID 以当前平台响应为准，不根据 1688 页面猜测。
2. 将 1688 事实、俄文/英文翻译和图片整理到 [统一数据包](references/data-contract.md)。每行有稳定 `offer_id`，每个货号对应图片文件夹。Ozon 标品写完整 `ozon_item_json`，WB 写完整 `wb_request_json`；缺失的品牌、包装数据和认证资料留空待确认。
3. 按平台、店铺和模板拆批，调用 `ptj_listing_preflight`。预检返回逐行错误和 15 分钟有效的 `planId`。修正后重新预检。
4. 向用户展示预检摘要中的账号、店铺、商品数、价格范围及错误。得到该批次的明确授权后，用稳定 `idempotencyKey` 和 `confirm=true` 调用 `ptj_listing_create_batch`。
5. TEMU 和 Ozon POD 调用 `ptj_listing_start_batch`；Ozon 标品和 WB 创建后由客户端队列自动执行。用 `ptj_listing_batch_status` 查询批次，再用 `ptj_task_list`、`ptj_task_detail` 或 `ptj_task_logs` 查看真实任务进度。任务已创建不代表商品已上架成功。

## 日常任务运营

- `ptj_task_list` 查询 Ozon 标品/POD、WB 或 TEMU 上架任务；WB 和 TEMU 指定当前账号店铺 ID。
- `ptj_task_detail` 查询 Ozon、WB 明细；`ptj_task_logs` 查询 Ozon 任务日志。TEMU 按店铺在任务列表中查询。
- `ptj_task_action` 暂停或继续 Ozon/TEMU 任务，继续 WB 任务或重试 WB 失败子队列。先读取目标任务并向用户说明具体动作，再传 `confirm=true`。
- `ptj_runner_state` 查询 TEMU 上架执行器；`ptj_runner_control` 启动或暂停全部 TEMU 上架执行器。全局动作会影响当前客户端待执行任务，须向用户说明范围并传 `confirm=true`。

## 平台边界

- TEMU：使用标题、英文标题、产品模板及每货号至少五图；每店单独建任务。
- Ozon POD：使用已确认的模板、俄文标题、价格及每货号图片；同批商品需适用同一模板。
- Ozon 标品：每行需要完整 Ozon 商品快照，逐商品按店铺上架，MCP 会上传本地图片并运行现有 Ozon 客户端预检。
- WB：每行需要完整 WB 建卡与后处理请求，MCP 会上传本地图片并逐商品创建任务。类目必填属性和合法值须先读取平台数据。

具体字段和工具参数见 [MCP 工具契约](references/mcp-contract.md) 与 [平台数据要求](references/platforms.md)。

## 操作约束

- 使用客户端当前登录账号；不要向 IDE 提供 PTJourney、Ozon、WB 或 TEMU 的 Token/API Key。
- 只调用 MCP 工具，不调用 `window.api` 或旧的 `127.0.0.1:13080` 插件路由。
- 若 `tools/list` 没有 PTJourney 工具，或 `ptj_listing_capabilities` 提示客户端未运行，先检查 MCP 配置和客户端版本；Skill 安装成功不代表接口可用。
- `failed` 或 `uncertain` 的商品先核对平台任务与货号。修正数据后重新预检并使用新的幂等键；不要对提交结果未知的货号盲目重试。
- Ozon POD 额度警告是唯一的同批重提分支：先展示具体警告，用户同意后按 [MCP 工具契约](references/mcp-contract.md) 用同一 `planId` 和幂等键确认。不要自动确认额度警告。
