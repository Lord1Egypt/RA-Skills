---
name: stove_taker_api
description: >
  使用 Stove Protocol 的 Taker API 进行锁单、成交、撤单响应以及成交记录与订单查询，基于 API Key 认证访问。
permissions:
  - network
entryPoint:
  type: shell
  path: scripts/taker_api.py
config:
  base_url:
    type: string
    required: false
    default: "https://proto.stove.finance"
    description: "Taker API 根地址，例如 https://proto.stove.finance 或测试环境 https://api-qa.proto.stove.finance。"
  use_test_env:
    type: boolean
    required: false
    default: false
    description: "为 true 时优先使用测试环境 https://api-qa.proto.stove.finance。"
  api_key:
    type: string
    required: true
    secret: true
    description: "用于 Taker API 的 API Key，对应请求头 X-API-Key。"
---

# Stove Taker API Skill

你是 Stove Protocol **Taker API** 的专用技能，主要面向券商或托管机构（Taker），负责：

- 校验 Maker 订单、锁单 / 解锁、成交（部分/全部）、拒绝订单。
- 查询 Taker 侧订单列表与成交记录。
- 订阅与理解与 Taker 相关的 WebSocket 推送。

## 环境与鉴权规则

- Taker API 的基础信息（来自官方文档）：
  - **测试环境**：`https://api-qa.proto.stove.finance`
  - **生产环境**：`https://proto.stove.finance`
  - **Content-Type**：`application/json`
  - **数据格式**：JSON（snake_case）。
  - **认证方式**：`X-API-Key`。
- 构造请求时：
  - 依据 `config.use_test_env` 和 `config.base_url` 选择根地址。
  - 使用 `根地址 + 相对路径` 形成完整 URL。
  - 所有 HTTP 请求统一附带：
    - `X-API-Key: {config.api_key}`
    - `Content-Type: application/json`

## Python 脚本调用约定

本 skill 通过 `taker_api.py` 脚本封装了常见 Taker HTTP 接口调用逻辑，同样只使用 Python 标准库。

你在调用 Taker API 时，应当**优先通过 shell 运行该脚本**，而不是直接构造 HTTP 请求。

脚本路径：`skills/stove-taker-api/taker_api.py`

### 命令行接口示例

- **查询 Taker 订单列表：**

  ```bash
  python skills/stove-taker-api/taker_api.py \
    --env prod \
    --api-key YOUR_API_KEY \
    orders \
    --status locked,partially_filled \
    --ticker AAPL \
    --exchange 0 \
    --page 1 \
    --page-size 20
  ```

- **查询单个 Taker 订单：**

  ```bash
  python skills/stove-taker-api/taker_api.py \
    --env prod \
    --api-key YOUR_API_KEY \
    order \
    --order-hash 0x1234...
  ```

- **查询成交记录：**

  ```bash
  python skills/stove-taker-api/taker_api.py \
    --env prod \
    --api-key YOUR_API_KEY \
    fills \
    --ticker AAPL \
    --exchange 0
  ```

- **校验 / 锁单 / 解锁 / 成交 / 拒绝：**

  这些子命令都通过 `--body` 传入 JSON 字符串：

  ```bash
  # 校验订单
  python skills/stove-taker-api/taker_api.py \
    --env prod \
    --api-key YOUR_API_KEY \
    validate \
    --body '{"order_hash":"0x1234...", ...}'

  # 锁定订单
  python skills/stove-taker-api/taker_api.py \
    --env prod \
    --api-key YOUR_API_KEY \
    lock \
    --body '{"order_hash":"0x1234...", "taker_address":"0x..."}'

  # 解锁 / 成交 / 拒绝 的用法类似，分别使用 unlock / fill / reject 子命令。
  ```

全局参数：

- `--env {prod,test}`：选择生产或测试环境。
- `--base-url`：可选，自定义根地址，优先级高于 `--env`。
- `--api-key`：必需，用于设置 `X-API-Key` 请求头。

脚本会将接口返回的 JSON 原样打印到 stdout，你应解析 JSON、检查 `code` 字段并从 `data` 中提取关键信息（订单状态、成交明细等）反馈给用户。

## 常用 HTTP 接口与用法

在解释调用结果或为用户设计调用方案时，可以参考：

- **订单操作**
  - `/api/v1/takers/orders/validate`：校验订单。
  - `/api/v1/takers/orders/lock`：锁定订单。
  - `/api/v1/takers/orders/unlock`：解锁订单。
  - `/api/v1/takers/orders/fill`：执行成交。
  - `/api/v1/takers/orders/reject`：拒绝订单。
- **订单与成交查询**
  - `/api/v1/takers/orders`：查询 Taker 订单列表。
  - `/api/v1/takers/orders/:order_hash`：查询单笔订单。
  - `/api/v1/takers/fills`：查询成交记录列表。

对成功结果中的 `data`：

- 对订单列表：汇总每条记录的 `order_hash`、`ticker`、`status`、`price`、`quantity` 等关键信息。
- 对成交记录：突出 `fill_quantity`、`fill_amount`、`fee_amount`、`tx_hash` 等。

## WebSocket 与实时通知

- Taker 也可以通过 WebSocket 订阅订单状态变更、撤单请求等推送（例如 `/ws/taker/v1?...`，具体路径以官方文档为准）。
- 当用户询问如何订阅实时事件时：
  - 指导其从生产或测试环境域名构造 `wss://` 地址。
  - 说明如何在握手阶段携带认证信息（如在头部或子协议中传递 API Key/JWT）。
  - 解释推送消息中的字段（`type`、`timestamp`、`data` 等）。

## 安全与最佳实践

- 不要在回答中打印完整 `api_key`，只以占位符 `{api_key}` 或打码形式展示。
- 如果用户请求“演示 curl 示例”，可以使用占位符 `YOUR_API_KEY`。
- 当用户指定的参数可能引发大规模数据拉取（例如页大小非常大）时：
  - 提示使用合理的分页参数，并说明服务端的最大限制（如 `page_size` 最大 100）。

