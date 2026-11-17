---
name: ptbrowser-mcp
description: "PTBrowser 浏览器环境管理 AI Skill。通过已登录 Windows 客户端的本机 MCP 管理独立 Chromium profiles、环境、分组、代理、扩展和回收区。Use for PTBrowser profile and browser environment management; not third-party webpage automation."
license: MIT-0
---

# PTBrowser 浏览器环境管理 · Chromium Profiles MCP

本 skill 连接当前 Windows 用户已登录的 PTBrowser 客户端。先按 [连接说明](references/setup.md) 配置 stdio MCP 服务；`tools/list` 应返回 `ptb_` 开头的工具。Skill 只是操作说明，实际动作由客户端执行。

## 使用方法

1. 调用 `ptb_auth_status`，确认客户端已登录；若应用锁已开启，请用户在客户端解锁。
2. 先用对应的 `*_list` 工具读取真实 ID 与当前状态，再执行创建、修改、启动、关闭、归档或恢复。
3. 变更状态的工具在展示目标和效果并获得用户授权后传 `confirm=true`；永久删除尤其要核对回收区条目 ID。
4. 调用后重新读取状态，确认最终结果。启动环境可能受套餐额度、代理检查和多设备租约限制。

若创建或修改请求超时，先用列表工具核对实际状态，不要立即重复提交，尤其是批量创建。

工具名、入参 schema 和说明由客户端的 MCP `tools/list` 实时提供，勿推测字段。环境配置修改需提供完整配置和 `riskAcknowledged=true`，可先读取环境当前值。批量创建通过 `ptb_environment_batch_create` 的 `rows` 参数提交结构化数据，每次最多 100 个。

客户端使用本机随机令牌桥接，不要读取或分享会话文件中的 token。`ptb_` 工具管理 PTBrowser 自身的环境与配置；不会代替用户在第三方网站执行登录、上架或批量网页操作。
