# ClawHub 上架材料 — 企微 Agent Ops Center v2.4.0

## 基本信息

- **Skill 名称**：wecom-agent-ops-center
- **版本**：2.4.0
- **价格**：免费（L0 版）；L1 Pro ¥99/月（私域转化）
- **分类**：Agent 工具 / 运维监控
- **标签**：企微 / 监控 / 告警 / WorkBuddy / OpenClaw / 多租户 / 自动发现

---

## 上架标题（三选一）

1. **企微 Agent Ops Center — AI 可观测性工具**
2. **让 AI Agent 从黑盒变透明 — 企微监控告警**
3. **企微 Agent 监控 — 心跳告警 + 进程守护 + 敏感信息拦截**

> 推荐用 **方案 1**（清晰、专业、SEO 友好）

---

## 上架描述（Markdown，直接粘贴）

```markdown
# 企微 Agent Ops Center

**在企微群里看到你的 AI Agent 在做什么。**

实时心跳监控、异常秒级告警、进程自动守护、敏感信息拦截——让 AI 从「黑盒」变「透明」。

> 🚀 **ClawHub 首发**：WorkBuddy + OpenClaw 用户 2 分钟接入，0 学习成本。

---

## 解决什么痛点

| 你的问题 | 我们怎么解决 |
|---|---|
| Agent 挂了没人知道，第二天才发现 | 心跳检测 + 企微群自动告警 |
| 不知道 Agent 今天处理了什么任务 | 任务进度直播 + 每日健康报告 |
| Agent 崩溃后没人重启 | 进程守护 + 指数退避自动重启 |
| 担心 Agent 泄露 API Key | 19 种敏感信息规则实时扫描拦截 |
| 不确定 Agent 访问了哪些外部服务 | 网络请求白名单守卫 |

---

## 与你有什么关系

- **WorkBuddy 用户**：Agent 挂了没人知道？心跳检测 + 企微群告警，2 分钟接入。安装后自动扫描本地所有 Agent，零配置。
- **OpenClaw 自托管用户**：服务器上的实例不稳定？进程守护 + 自动重启 + 平台自动识别。
- **企业运维 / 团队**：几十个 Agent 混在一起？多租户隔离，按用户 ID 自动分区，互不干扰。
- **业务负责人**：Agent 到底有没有在干活？调用统计 + 延迟追踪 + 审计日志。

---

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

### 3. 配置（最小配置）

```yaml
# config.yaml
wecom:
  bot_id: "你的BotID"
  bot_secret: "你的BotSecret"

adapters:
  - type: "workbuddy"
    agent:
      id: "my-workbuddy"
      endpoint: "http://localhost:9527"
```

### 4. 启动并验证

```bash
node connector.js
```

- 在企微里 `@机器人 你好` → Agent 应回复
- 浏览器打开 `http://localhost:9527` → 查看 Agent 健康状态
- Agent 离线 3 次心跳后 → 企微群收到告警卡片

---

## v2.4 新增能力

- 🧠 **Agent 自动发现**：安装 Skill 后 `agent-scanner` 自动扫描 `~/.workbuddy/skills/`（或 `~/.openclaw/`），批量注册到 Ops Center，零手动配置
- 👥 **多租户隔离**：按 WorkBuddy/OpenClaw 用户 ID 自动分区，不同用户的 Agent 数据完全隔离。API 通过 `X-Tenant-ID` header 过滤
- 🏷️ **平台自动识别**：`getPlatform()` 自动检测当前平台（检测 `~/.workbuddy` / `~/.openclaw` 目录 + 环境变量 + 自身路径），Agent 打上 `platform` 标签（`workbuddy` / `openclaw` / `unknown`），支持未来 `/api/stats/platform` 分类统计
- 🛡️ **进程守护**：Agent 崩溃后自动重启（指数退避，最多 10 次）
- 🔒 **Secrets 扫描**：19 种敏感信息规则（API Key / 私钥 / 密码），支持 block / redact / warn 三种模式
- 🌐 **网络守卫**：Monkey-patch http/https 模块，域名 / IP / CIDR 白名单，阻断非法外联
- 📊 **Dashboard API**：11 个新端点，查询进程状态 / 扫描统计 / 网络拦截记录
- 🔄 **systemd 守护**：`wecom-agent-ops-center.service` 开机自启 + 崩溃自动重启

---

## 与「企微 AI 聊天机器人」的区别

| | 企微 AI 聊天 | 企微 Agent Ops Center |
|---|---|---|
| 产品类型 | AI 对话服务 | **Agent 运维工具** |
| LLM 谁负责 | 服务商内置 | **你自己配**（DeepSeek / GPT / 自建） |
| 核心价值 | 能聊天 | **能看到 Agent 在干什么** |
| 粘性 | 换了损失对话历史 | **换了损失所有 Agent 健康数据** |

---

## 常见问题

**Q：和企微自带的 AI 有什么区别？**
A：企微自带的是「AI 聊天」。我们是「Agent 运维工具」——不管你的 AI 是谁家的，我们帮你监控它是否正常运行。

**Q：消息内容会经过你们的服务器吗？**
A：消息转换（企微格式 ↔ 标准格式）走云端 API（www.hermesai.ltd），不存储明文。监控数据全部存在本地。也可以设置 `converter.enabled: false` 完全本地运行。

**Q：不用你们监控，我只要消息转发行不行？**
A：可以。设置 `monitor.enabled: false` 降级为纯消息转发模式。

**Q：bot_id 和 bot_secret 去哪找？**
A：企微管理后台 → 应用管理 → 智能机器人 → 点击应用名称 → 复制「机器人ID」和「Secret」。

**Q：多个用户共用一个 Ops Center，Agent 数据会混在一起吗？**
A：不会。v2.4 实现了多租户隔离：按 WorkBuddy/OpenClaw 的用户 ID 自动分区，API 通过 `X-Tenant-ID` header 过滤。平台来源（WorkBuddy / OpenClaw）也会自动打 `platform` 标签，方便后续分类统计。agent-scanner 安装后自动识别当前平台和用户，零配置。

**Q：我需要手动注册 Agent 吗？**
A：不需要。安装 Skill 后，内置的 `agent-scanner.js` 自动扫描 `~/.workbuddy/skills/`（或 `~/.openclaw/`），发现所有本地 Agent 并批量注册到 Ops Center。平台类型和租户 ID 全部自动识别。

---

## 链接

- 状态面板：`http://localhost:9527`
- 健康检查：`http://localhost:9527/health`
- 问题反馈：GitHub Issues

---

> 🚀 **ClawHub 首发**：安装后 2 分钟，你的企微群里就能看到 AI Agent 的健康状态。
```

---

## 截图说明

- **主截图**：`dashboard/screenshot.png`（Dashboard 界面，已生成）
- **建议补充截图**（可选，提升转化率）：
  1. 企微群告警卡片（截图企微群里的 🔴 异常告警卡片）
  2. 企微单聊对话（用户 @机器人 → Agent 回复）
  3. 配置文件（打码后的 config.yaml）

---

## 上架检查清单

- [x] SKILL.md 精简完成（144 行，ClawHub 展示用）
- [x] PRODUCT_PAGE.md 完整版备份
- [x] 版本号统一（package.json / connector.js 均为 2.4.0）
- [x] Dashboard 截图已生成
- [x] 端到端测试通过（10/10）
- [x] 服务器部署完成（www.hermesai.ltd）
- [ ] 准备企微群告警卡片截图（可选，提升转化率）
- [ ] 在 ClawHub 后台填写标题 + 描述 + 上传截图
- [ ] 发布后通知用户（公众号 / 小红书 / 知乎）

---

## 发布后推广建议

1. **WorkBuddy 内部引流**：在 WorkBuddy 启动时提示「安装企微监控 Skill」
2. **小红书**：「我的 AI Agent 半夜挂了，第二天才知道」痛点故事 + 解决方案
3. **知乎**：「如何监控企微里的 AI Agent？」问答式长文
4. **ClawHub 站内**：争取首页推荐（新上线 Skill 有流量扶持）
