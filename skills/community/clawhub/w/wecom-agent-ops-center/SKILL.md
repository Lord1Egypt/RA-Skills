---
name: wecom-agent-ops-center
display_name: 企微 Agent Ops Center
description: 企微 AI Agent 可观测性工具 — 心跳监控、进程守护、敏感信息扫描、网络白名单，2 分钟接入
version: 2.4.0
author: 咕嘟科技
homepage: https://hermesai.ltd
tags:
  - wecom
  - agent-monitoring
  - process-guard
  - observability
  - enterprise-wechat
  - AI-ops
  - websocket
  - multi-tenant
---

# 企微 Agent Ops Center

**在企微群里看到你的 AI Agent 在做什么。** 实时心跳监控、异常秒级告警、进程自动守护、敏感信息拦截——让 AI 从「黑盒」变「透明」。

WorkBuddy / OpenClaw 用户 2 分钟接入，0 学习成本。

## 解决什么痛点

| 你的问题 | 我们怎么解决 |
|-----------|----------------|
| Agent 挂了没人知道，第二天才发现 | 心跳检测 + 企微群自动告警 |
| 不知道 Agent 今天处理了什么任务 | 任务进度直播 + 每日健康报告 |
| Agent 崩溃后没人重启 | 进程守护 + 指数退避自动重启 |
| 担心 Agent 泄露 API Key | 19 种敏感信息规则实时扫描拦截 |
| 不确定 Agent 访问了哪些外部服务 | 网络请求白名单守卫 |
| 多个用户/团队的 Agent 数据混在一起 | 多租户隔离（按 WorkBuddy/OpenClaw 用户 ID 自动分区） |
| 分不清 Agent 来自哪个平台 | 自动识别平台来源（WorkBuddy / OpenClaw），支持分类统计 |

## v2.4 核心特性

- 🧠 **Agent 自动发现**：安装 Skill 后自动扫描 `~/.workbuddy/skills/` 下的所有 Agent，批量注册到 Ops Center，零手动配置
- 👥 **多租户隔离**：按 WorkBuddy/OpenClaw 用户 ID 自动分区，不同用户/团队的 Agent 数据完全隔离
- 🏷️ **平台自动识别**：自动检测当前平台（WorkBuddy / OpenClaw），Agent 打上 `platform` 标签，支持分类统计
- 🛡️ **进程守护**：Agent 崩溃后自动重启（指数退避，最多 10 次）
- 🔒 **Secrets 扫描**：19 种敏感信息规则（API Key / 私钥 / 密码），支持 block / redact / warn 三种模式
- 🌐 **网络守卫**：Monkey-patch http/https 模块，域名 / IP / CIDR 白名单，阻断非法外联

## 快速开始

### 1. 安装

```bash
# ClawHub 安装（推荐）
clawhub install wecom-agent-ops-center

# 或本地启动
git clone <repo> && cd wecom-agent-ops-center
npm install
```

### 2. 获取企微凭证

```
企微管理后台 → 应用管理 → 智能机器人
→ 创建应用（或选择已有）
→ 复制 Bot ID 和 Bot Secret
```

### 3. 配置

```bash
cp config.yaml.example config.yaml
# 编辑 config.yaml，填入 bot_id、bot_secret
```

**最小配置（WorkBuddy 用户）：**
```yaml
wecom:
  bot_id: "你的BotID"
  bot_secret: "你的BotSecret"
# agent-scanner 会自动扫描 ~/.workbuddy/skills/ 并批量注册！
```

**最小配置（OpenClaw 用户）：**
```yaml
wecom:
  bot_id: "你的BotID"
  bot_secret: "你的BotSecret"
# agent-scanner 会自动扫描 ~/.openclaw/ 并批量注册！
```

> 💡 **不需要手动注册 Agent**。安装后 scanner 自动扫描本地所有 Agent，批量上报到 Ops Center。平台类型（WorkBuddy/OpenClaw）和租户 ID（按用户隔离）全部自动识别。

### 4. 启动

```bash
# 本地开发
node connector.js

# 服务器部署（推荐，开机自启）
sudo systemctl enable --now wecom-agent-ops-center
```

### 5. 验证

- 在企微里 `@机器人 你好` → Agent 应回复
- 浏览器打开 `http://localhost:9527` → 查看 Agent 健康状态
- Agent 离线 3 次心跳后 → 企微群收到告警卡片

## 命令行

```bash
node connector.js              # 启动（监控 + 消息转发）
node connector.js pair         # 生成 P2P 配对码
node connector.js join <CODE>  # 加入 P2P 配对
node connector.js status       # 查看连接状态
node connector.js peers       # 查看已配对节点
```

## 环境变量（免配置文件）

```bash
export WECOM_BOT_ID=xxx
export WECOM_BOT_SECRET=xxx
export AGENT_ENDPOINT=http://...
export MONITOR_NOTIFY_CHATID=群聊ID
node connector.js
```

## 常见问题

**Q：和企微自带的 AI 有什么区别？**
A：企微自带的是「AI 聊天」。我们是「Agent 运维工具」——不管你的 AI 是谁家的，我们帮你监控它是否正常运行。

**Q：我的 Agent 不是 HTTP 端点怎么办？**
A：只需提供一个 health check URL（返回 200 即可）。消息转发可以走其他方式，监控走 HTTP。

**Q：消息内容会经过你们的服务器吗？**
A：消息转换（企微格式 ↔ 标准格式）走云端 API（www.hermesai.ltd），不存储明文。监控数据全部存在本地。也可以设置 `converter.enabled: false` 完全本地运行。

**Q：不用你们监控，我只要消息转发行不行？**
A：可以。设置 `monitor.enabled: false` 降级为纯消息转发模式。

**Q：bot_id 和 bot_secret 去哪找？**
A：企微管理后台 → 应用管理 → 智能机器人 → 点击应用名称 → 复制「机器人ID」和「Secret」。

**Q：notify_chatid 怎么填？**
A：企微群里右键群名 → 复制群聊 ID（格式：`wrkSFfCgAA...`）。填到 config.yaml 的 `monitor.notify_chatid`。

**Q：端口 9527 被占用了怎么办？**
A：修改 config.yaml 的 `connector.port` 为其他端口（如 9528），重启即可。

**Q：多个用户共用一个 Ops Center，Agent 数据会混在一起吗？**
A：不会。系统按 WorkBuddy/OpenClaw 的用户 ID 自动做多租户隔离，每个用户只能看到自己的 Agent。平台来源（WorkBuddy / OpenClaw）也会自动打标签，方便分类统计。

## 技术栈

- **语言：** Node.js 18+
- **WebSocket：** `ws` 库（企微官方智能机器人协议）
- **监控：** 自建 AgentMonitor + NotifyEngine（无外部依赖）
- **持久化：** 本地 JSON 文件（StateStore）
- **消息转换：** 云端 API（www.hermesai.ltd）或本地降级

## 链接

- 状态面板：`http://localhost:9527`
- 健康检查：`http://localhost:9527/health`
- 云端转换 API：`https://www.hermesai.ltd/health`
- 问题反馈：GitHub Issues

---

> 🚀 **ClawHub 首发**：安装后 2 分钟，你的企微群里就能看到 AI Agent 的健康状态。

---
## 📬 更多资源

> 📬 更多 AI 企业落地实战案例 → 关注公众号：**咕嘟AI**  
> 💬 1v1 免费诊断（AI岗位匹配）→ 加微信：**GuduTech**  
> 🚀 完整 ACE 体系课 + AI 内容系统搭建 → https://hermesai.ltd  
>  
> 用 Ops Center 管好了企微 Agent？欢迎加微信分享你的部署经验 🤖
