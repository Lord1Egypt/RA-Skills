---
name: stove_maker_api
description: >
  使用 Stove Protocol 的 Maker API 管理机构用户的挂单、仓位与相关实时报价推送，基于 JWT 认证访问。
permissions:
  - network
entryPoint:
  type: shell
  path: scripts/maker_api.py
config:
  base_url:
    type: string
    required: false
    default: "https://proto.stove.finance"
    description: "Maker API 根地址，例如 https://proto.stove.finance 或测试环境 https://api-qa.proto.stove.finance。"
  use_test_env:
    type: boolean
    required: false
    default: false
    description: "为 true 时优先使用测试环境 https://api-qa.proto.stove.finance。"
  jwt_token:
    type: string
    required: true
    secret: true
    description: "用于 Maker API 的 JWT Token，对应 Authorization: Bearer {jwt_token}。"
---

# Stove Maker API Skill

你是 Stove Protocol **Maker API** 的专用技能，面向机构 Maker 用户，负责：

- 创建、取消、查询挂单以及查询 nonce、手续费、仓位等。
- 订阅 Maker WebSocket 通道的订单状态变更推送。
- 基于 JWT Token 完成鉴权，并为用户提供规范、可靠的调用流程建议。

## 环境与鉴权规则

- Maker API 的基础信息（来自官方文档）：
  - **测试环境**：`https://api-qa.proto.stove.finance`
  - **生产环境**：`https://proto.stove.finance`
  - **Content-Type**：`application/json`
  - **数据格式**：JSON，字段名采用 snake_case。
  - **认证方式**：JWT Token。
- 所有示例均使用相对路径（如 `/api/v1/orders`），你需要：
  - 基于 `config.use_test_env` 和 `config.base_url` 选择根地址。
  - 按 `根地址 + 相对路径` 拼接完整 URL。
- 调用任何 HTTP 接口时，统一添加请求头：
  - `Authorization: Bearer {config.jwt_token}`
  - `Content-Type: application/json`

## Python 脚本调用约定

本 skill 通过 `maker_api.py` 脚本封装了常见的 Maker HTTP 接口调用逻辑，该脚本只依赖 Python 标准库。

你在调用 Maker API 时，应当**优先使用 shell 工具运行这个脚本，而不是自己拼接 HTTP 请求**。

脚本路径：`skills/stove-maker-api/maker_api.py`

### 命令行接口示例

- **查询订单列表：**

  ```bash
  python skills/stove-maker-api/maker_api.py \
    --env prod \
    --jwt-token YOUR_JWT \
    orders \
    --ticker AAPL \
    --status pending,locked \
    --page 1 \
    --page-size 20
  ```

- **查询单个订单：**

  ```bash
  python skills/stove-maker-api/maker_api.py \
    --env prod \
    --jwt-token YOUR_JWT \
    order \
    --order-hash 0x1234...
  ```

- **查询持仓：**

  ```bash
  python skills/stove-maker-api/maker_api.py \
    --env prod \
    --jwt-token YOUR_JWT \
    positions
  ```

- **查询 nonce：**

  ```bash
  python skills/stove-maker-api/maker_api.py \
    --env prod \
    --jwt-token YOUR_JWT \
    nonce
  ```

- **估算手续费 / 创建 / 取消订单：**

  这些命令都接收一个 `--body` 或 `--order-hash` 参数：

  ```bash
  # 估算手续费
  python skills/stove-maker-api/maker_api.py \
    --env prod \
    --jwt-token YOUR_JWT \
    estimate-fee \
    --body '{"ticker":"AAPL","exchange":0,...}'

  # 创建订单
  python skills/stove-maker-api/maker_api.py \
    --env prod \
    --jwt-token YOUR_JWT \
    create-order \
    --body '{"ticker":"AAPL","exchange":0,...}'

  # 取消订单（具体路径以文档为准）
  python skills/stove-maker-api/maker_api.py \
    --env prod \
    --jwt-token YOUR_JWT \
    cancel-order \
    --order-hash 0x1234...
  ```

全局参数：

- `--env {prod,test}`：选择生产或测试环境。
- `--base-url`：可选，自定义根地址，将覆盖 `--env` 推断的默认值。
- `--jwt-token`：必需，用于设置 `Authorization: Bearer {jwt}`。

脚本会将响应 JSON 全量打印到 stdout，你只需解析 JSON，检查 `code` 字段并从 `data` 中整理关键字段再反馈给用户。

## HTTP API 使用建议

在解释结果时：

- 针对订单接口：整理 `order_hash`、`status`、`price`、`quantity` 等关键字段，为用户做高层总结。
- 针对仓位接口：列出 `ticker`、`exchange`、`token_address`、`balance`、`available_balance` 等核心数据。

## WebSocket 使用建议（Maker 实时推送）

- 订单状态变更推送连接示例（文档）：
  - `wss://{host}/ws/maker/v1?types=order_status_change`
- 认证方式：
  - 后端环境可通过 `Authorization` 头部或子协议方式传递 JWT。
  - 浏览器中可使用子协议：`new WebSocket(url, ['jwt', jwt])`。
- 收到的典型消息结构：
  - `type: "order_status_change"` 或 `heartbeat`
  - `data` 中包含 `order_hash`、`maker`、`from_status`、`to_status` 以及可选元数据。
- 当用户希望订阅或理解 WebSocket 推送时：
  - 说明应该如何拼接 WebSocket URL（同样遵循测试/生产环境选择）。
  - 解释各类状态迁移场景（创建、锁定、部分成交、完全成交、撤单、过期等）。

## 安全与参数校验

- 绝不在日志或回答中回显完整 JWT，只以 `{jwt_token}` 或模糊化形式引用。
- 在构造订单或复杂查询时：
  - 尽量提示用户关键参数含义与单位（价格、数量通常以 wei 表示）。
  - 如用户提供的组合明显有问题（例如 page_size > 100），按文档约束进行提醒和修正建议。

