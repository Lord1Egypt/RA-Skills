# 更新日志

## 版本 3.0.0 - 完整的 Provider 引导配置流程

- **破坏性变更**: 移除了自动创建 TokenRouter provider 及占位 API Key 的逻辑
- 移除了 ACP runtime 自动检测和自动启用模型的逻辑
- 新增三阶段引导流程：检查 → 用户提供配置 → agent 写入 → 二次验证 → 自动同步模型
- 新增 `check` 命令：验证 TokenRouter provider 是否已配置
- 新增 `setup` 命令：接收用户提供的 provider name / baseUrl / apiKey，由 agent 写入配置文件
- 新增 `sync` 命令：验证 provider 后自动拉取所有模型，添加到 provider 的 models[] 和 allow list
- 所有模型统一通过用户配置的 TokenRouter provider 路由
- `baseUrl` 检查改为部分匹配（包含 `https://open.palebluedot.ai` 即可）
- `prepare_for_planning()` 简化为：校验 provider → 自动同步模型 → 更新配置
- SKILL.md 重写为完整的三阶段引导说明，指导 agent 如何引导用户完成配置

## 版本 2.1.0 - ACP运行时支持
- 添加了对ACP运行时配置的检测和支持
- 当ACP运行时未配置时，自动选择合适的模型执行任务
- 显示友好的提示信息："ACP运行时未配置，我将启用xxx来执行"

## 版本 2.0.0 - 自动配置功能
- 添加了在执行计划前自动准备TokenRouter配置的功能
- 自动验证并添加TokenRouter提供者（如果不存在）
- 自动获取最新模型列表并更新配置
- 自动将所有模型添加到允许列表
- 自动更新当前默认模型

## 版本 1.0.0 - 初始版本
- 动态模型层级系统
- 六类别任务分类引擎
- 智能规划与执行
- 自适应稳定性回退机制
- 多代理路由指导