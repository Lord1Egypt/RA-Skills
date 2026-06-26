---
name: myskill
description: 这是一个专门用于与 Example API 进行安全交互的技能工具，支持执行数据变更操作。
version: 1.0.0
author: Developer
license: MIT
---

# My Skill (myskill)

## 功能概览
My Skill 是一个标准化的 API 交互接口，专门设计用于对接 `https://api.example.com`。它不仅能够处理常规的数据请求，还内置了安全防卫机制，确保在执行敏感操作（如删除或更新数据）时，用户始终拥有最终确认权。

## 核心规则 (Safety & Compliance)
为了保证生产环境的稳定性，使用本技能必须遵守以下规则：
- **二次确认机制**：所有涉及数据写入、删除或任何“破坏性”修改的操作，在执行前必须通过 `confirm` 交互触发器向用户获取明确确认。
- **凭据管理**：本技能严禁硬编码任何 API 密钥。所有的鉴权操作必须严格通过环境变量 `MY_API_KEY` 进行动态读取。
- **数据隐私**：在处理 payload 时，应确保不包含任何敏感的个人身份信息 (PII)，除非已加密。

## 环境配置
在使用前，请确保执行环境已配置以下环境变量：
- `MY_API_KEY`: 访问 `https://api.example.com` 所需的授权 Token。

## 使用方法
当用户输入包含“do the thing”、“执行操作”或类似意图的指令时，该技能将触发以下逻辑：

1. **解析意图**：从用户输入中提取必要参数（payload）。
2. **验证环境**：检查 `MY_API_KEY` 是否有效。
3. **安全拦截**：若涉及状态变更，调用确认函数（Confirm Function）。
4. **执行请求**：将请求发送至 `https://api.example.com/action`。
5. **反馈结果**：将 API 返回的 JSON 响应格式化后呈现给用户。

## 示例请求
*用户输入:* "帮我把状态更新为 active，并执行那个操作。"

*系统动作:* 1. 识别意图 -> `action: perform`, `payload: { status: 'active' }`
2. 触发确认 -> "即将向 API 发送更新请求，确认执行吗？"
3. 执行 API 调用 -> `POST https://api.example.com/action`
4. 输出结果 -> "操作成功，服务器返回状态码 200。"

## 错误处理
- 若 `MY_API_KEY` 未配置，技能将抛出 `AuthError` 并引导用户检查环境变量。
- 若 API 请求超时或返回 500 错误，技能将执行重试策略，并在三次重试后向用户反馈错误详情。