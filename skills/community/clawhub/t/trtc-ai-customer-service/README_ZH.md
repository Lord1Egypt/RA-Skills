# TRTC AI 电商客服 Skill

[English](README.md) | 简体中文

> 基于 [腾讯云 TRTC Conversational AI 解决方案](https://cloud.tencent.com/document/product/647/110584) 快速搭建生产级 AI 电商客服 Web 应用 — 语音与文字双通道、三语国际化、内置电商业务流程。

## 核心能力

| 能力 | 说明 |
|------|------|
| **实时语音** | 终端用户与云端 AI Bot 之间的双向 WebRTC 音频通信 |
| **文字降级** | 跳过 ASR，将键盘输入直接送达 LLM 处理链路 |
| **三语国际化** | 中文 / 粤语 / 英文全覆盖：UI、STT、TTS、SystemPrompt |
| **电商业务流** | 订单查询、退换货处理、物流追踪、优惠活动咨询 |
| **数字人可选** | 可选虚拟形象渲染，未配置时优雅降级为纯语音 |
| **会话生命周期** | 关键词触发告别、转人工、空闲超时自动结束 |
| **服务评分** | 会话结束后 4 维度评价 |

## 安装方式

本项目是一个**便携式 Agent Skill**（包含 `SKILL.md` + `scripts/` + `references/` + `assets/` 的标准结构）。安装到对应工具的 skills 目录即可被自动发现。

### OpenClaw

根据需要选择安装位置：

| 位置 | 作用域 | 命令 |
|------|--------|------|
| `<workspace>/skills/` | 当前工作区，优先级最高 | `git clone https://github.com/jerryang-cool/trtc-ai-customer-service-skill.git skills/trtc-ai-customer-service` |
| `~/.agents/skills/` | 个人级，跨工作区生效 | `git clone https://github.com/jerryang-cool/trtc-ai-customer-service-skill.git ~/.agents/skills/trtc-ai-customer-service` |
| `~/.openclaw/skills/` | 全局共享，所有 agent 可见 | `git clone https://github.com/jerryang-cool/trtc-ai-customer-service-skill.git ~/.openclaw/skills/trtc-ai-customer-service` |

安装后通过自然语言（如"帮我做个 AI 客服"）或斜杠命令 `/trtc-ai-customer-service` 调用。

> 更多信息参见 [OpenClaw Skills 官方文档](https://docs.openclaw.ai/zh-CN/tools/skills)。

### CodeBuddy

设置 → Skills → **导入 Skill**，选择本仓库目录。导入后，在对话中提及 *"AI 客服"*、*"电商客服"*、*"TRTC + AI"* 等关键词即自动激活。

### Claude Code

```bash
# 用户级（跨项目可用）
git clone <repo-url> ~/.claude/skills/trtc-ai-customer-service

# 或项目级（提交到仓库，团队共享）
git clone <repo-url> .claude/skills/trtc-ai-customer-service
```

Claude Code 通过 `description` 字段自动匹配触发。隐式调用（如"帮我做个 AI 客服"）或显式调用 `/trtc-ai-customer-service` 均可。

### OpenAI Codex CLI

```bash
# 用户级
git clone <repo-url> ~/.codex/skills/trtc-ai-customer-service

# 或项目级
git clone <repo-url> .agents/skills/trtc-ai-customer-service
```

Codex 在下次会话启动时自动检测新 skill。隐式调用（自然语言）或显式调用 `$trtc-ai-customer-service` 均可。

### Cursor

```bash
# 投放到 Cursor skills 目录
git clone <repo-url> ~/.cursor/skills/trtc-ai-customer-service
```

仓库内 `.cursor/rules/trtc-ai-customer-service.mdc` 遵循 2026 MDC 格式（Agent Requested 模式），Cursor 的 Agent 模式会按 description 按需加载。

> **从 `.cursorrules` 升级**：Cursor 自 2026 年起在 Agent 模式下静默忽略 `.cursorrules`。本 Skill 仅提供新的 `.cursor/rules/*.mdc` 格式。

## 快速开始

```bash
# 1. 生成新项目
python scripts/scaffold.py ./my-shop --name "云尚商城"

# 2. 启动（首次运行进入交互式密钥配置向导）
cd ./my-shop && ./start.sh

# 3. 浏览器访问 http://localhost:8080
```

## 架构

```
┌─────────────────────────────────┐
│  浏览器  (TRTC Web SDK v5)       │
│  WebRTC 音频 + 自定义消息         │
└──────────────┬──────────────────┘
               │
       ┌───────▼───────┐
       │   TRTC 房间    │
       │  ASR → LLM →  │  云端 AI 处理链路
       │      TTS       │  (后端零 LLM 调用)
       └───────┬────────┘
               │ OpenAPI (TC3-HMAC-SHA256)
       ┌───────▼────────┐
       │  Flask 后端     │  UserSig 签发
       │   (app.py)      │  + OpenAPI 中转
       └─────────────────┘
```

## 技术栈

| 层 | 技术 |
|----|------|
| 后端 | Python 3.8+ · Flask · tencentcloud-sdk-python |
| 前端 | 原生 JS · TRTC Web SDK v5 · CSS 自定义属性 |
| AI 引擎 | TRTC ConversationAI（云端 ASR → LLM → TTS） |
| 鉴权 | HMAC-SHA256 UserSig（仅服务端签发） |
| 配置 | YAML，通过 `envyaml` 支持环境变量插值 |

## 项目结构

```
trtc-ai-customer-service-skill/
├── SKILL.md              # Skill 入口 — 供 CodeBuddy / Claude Code / Codex CLI 识别
├── .cursor/
│   └── rules/
│       └── trtc-ai-customer-service.mdc  # Cursor 2026 MDC 格式
├── LICENSE               # MIT 许可证
├── CHANGELOG.md          # 版本历史
├── README.md             # English documentation
├── README_ZH.md          # 中文文档（本文件）
├── scripts/
│   └── scaffold.py       # 一键项目生成器
├── references/
│   ├── architecture.md   # 系统设计与后端集成
│   ├── config-guide.md   # 完整配置参考
│   └── frontend-guide.md # TRTC Web SDK 集成指南
└── assets/               # 脚手架附带的模板文件
```

## 参考链接

- [TRTC 控制台](https://console.cloud.tencent.com/trtc/app)
- [Conversational AI 解决方案](https://cloud.tencent.com/document/product/647/110584)
- [LLM 配置指南](https://cloud.tencent.com/document/product/647/115413)
- [TTS 音色配置指南](https://cloud.tencent.com/document/product/647/115414)

## 许可证

基于 [MIT 许可证](LICENSE) 发布。
