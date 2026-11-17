---
name: workbuddy-workspace-relay
description: 当用户要换电脑、切换设备或在另一台机器继续开发时，帮助把当前 WorkBuddy 项目和工作现场（未提交改动、Git、项目内配置、Agent 规则/Skill 与交接上下文）安全打包成加密工作包，或恢复已有 .wbpack 并接着上次工作。适用于“跨设备项目迁移/接力”“工作现场打包/恢复”“把项目和 Agent 上下文一起带走”等请求；不把单纯云同步、实时多人协作、普通 Git 同步或部署作为主要场景。
---

# WorkBuddy 项目续接

> 换电脑也能接着做：跨设备打包和恢复 WorkBuddy 工作现场。

## 产品概览

WorkBuddy 项目续接解决的是“换电脑后如何接着完成当前项目”，而不是多人实时协作或云端同步。它把当前 WorkBuddy 工作区、项目规则、未提交文件、项目内配置和 Agent 交接上下文封装为加密的 `.wbpack` 工作包，用户自行传输到另一台电脑后再恢复。

用户可能这样提出需求：

- “我要换电脑继续这个项目，帮我把当前工作现场带过去。”
- “把项目、未提交代码、Git 和 Agent 配置一起加密打包。”
- “我想在另一台电脑接着上次的进度开发。”
- “我有一个 `.wbpack`，帮我恢复并继续工作。”

## 交付结果

- 打包端：一个可传输的加密 `.wbpack` 文件。
- 接收端：一个不会覆盖既有目录的已恢复项目，以及可供 Agent 继续工作的 `HANDOFF.md`。

## 能力边界

默认保留源代码、文档、素材、数据库、`.git`、Agent 配置、项目内 Skill、项目规则、未提交修改和项目内 `.env` 文件；默认排除可重建依赖、缓存、构建产物、覆盖率、日志、系统临时文件、已有 `.wbpack` 和符号链接。

不迁移模型隐藏状态、原始会话进程、系统钥匙串、浏览器登录态、WorkBuddy 账号凭证或未公开的工作区切换接口；不负责云同步、实时多人协作、普通 Git 同步或部署。

## Agent 执行入口

触发后先读取 [`references/agent-workflow.md`](references/agent-workflow.md)，再按其中的双模式入口执行。不要仅凭文件是否存在猜测用户要打包还是恢复。

资源分工：

- [`references/agent-workflow.md`](references/agent-workflow.md)：交互顺序、打包/恢复流程、安全边界和失败处理。
- [`references/package-format.md`](references/package-format.md)：需要解释 `.wbpack` 结构或校验边界时读取。
- `scripts/relay.py`：确定性打包、age 加密、解密、归档校验、哈希校验和安全恢复。

## ClawHub 文本分发版

本分发版不携带 `age` 二进制文件。使用前请在目标设备自行安装并确认 `age` 已位于 `PATH` 中；Skill 不会自动下载、安装或替换系统工具。若目标设备需要随包提供二进制，请使用完整包，而不是本 ClawHub 文本版。
