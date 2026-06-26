# TradeMirrorOS（中文说明）

TradeMirrorOS 是一个面向交易记忆工作流的 Clawhub 最小技能包。

这个包刻意保持为 instruction-only：
保留能力路由、记忆架构与各子技能说明，但不再包含运行时代码、测试、同步脚本或远端传输流程。

- 公共仓库：<https://github.com/Topps-2025/TradeMirrorOS.git>
- 英文 README：[`README.md`](README.md)
- 对外介绍文案：[`PUBLIC_PAGE_COPY.zh-CN.md`](PUBLIC_PAGE_COPY.zh-CN.md) / [`PUBLIC_PAGE_COPY.md`](PUBLIC_PAGE_COPY.md)

## 这个包保留什么

- Finance Journal 的工作区路由能力
- 面向记录、计划、复盘、行为体检的 instruction-only 技能
- 长期交易记忆相关的架构与概念文档
- 轻量参考资料，如数据契约与进化逻辑说明

## 这个包不再包含什么

- 运行时代码
- 测试、示例与本地配置
- git 同步流程、push/pull 指令与提示模板
- 凭证相关操作与远端传输能力

## 核心结构

- `SKILL.md`：工作区总路由
- `finance-journal-orchestrator/`：记录编排与记忆 framing 技能
- `trade-plan-assistant/`：计划技能
- `trade-evolution-engine/`：复盘与自进化技能
- `behavior-health-reporter/`：行为体检技能
- `TRADE_MEMORY_ARCHITECTURE.md`：核心架构说明

## 安全默认值

- 这个包不应要求 secrets、tokens 或 git 凭证
- 任何文件修改、远端同步或发布动作都应由用户直接控制
- 私有账本、券商导出、`_runtime*` 与 `*.db` 文件不属于公开技能包
