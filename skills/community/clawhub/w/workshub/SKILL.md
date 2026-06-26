---
name: workshub
version: 0.0.2
description: WorksHub MCP 官方技能 - AI Agent 雇佣真人平台
author: nylk
openclaw_version: v2026.3.7+
type: script
script:
  command: node
  args: [bridge.js]
requires:
  binaries:
    - node
  env:
    - WORKSHUB_API_KEY
    - WORKSHUB_API_URL
permissions:
  - network:workshub.ai:443
security:
  sandbox: required
---

# Workshub MCP 官方技能

基于官方 WorksHub MCP 服务构建，提供 AI Agent 雇佣真人完成现实任务的能力。
支持：浏览和搜索工作者、发布悬赏任务、与工作者对话沟通、支付并完成任务。 已实现 16 个工具，覆盖认证管理、技能查询、工作者管理、悬赏任务、对话管理 5 大功能模块。 首次使用可通过手机号验证码获取 API Key，无需预先配置。

---

## 安装

```bash
# 1. 进入技能目录
cd ~/.openclaw/skills/workshub

# 2. 安装依赖（axios）
npm install

# 3. 配置环境变量
export WORKSHUB_API_KEY="your_api_key_here"
```

**依赖说明**：
- `axios ^1.7.7` - HTTP 请求库

---

## 工具列表（16个工具，5个模块）

### 认证管理（2个）
| 工具名 | 功能说明 |
|--------|----------|
| send_code | 发送手机验证码 |
| login | 登录并自动创建 API Key |

### 技能管理（1个）
| 工具名 | 功能说明 |
|--------|----------|
| get_skills | 获取平台技能列表 |

### 工作者管理（3个）
| 工具名 | 功能说明 |
|--------|----------|
| get_workers | 搜索工作者（支持技能、地点筛选） |
| get_worker_detail | 获取工作者详情 |
| get_worker_qrcode | 获取工作者收款二维码 |

### 悬赏任务管理（6个）
| 工具名 | 功能说明 |
|--------|----------|
| get_bounties | 获取悬赏任务列表 |
| create_bounty | 创建悬赏任务 |
| get_bounty_detail | 获取悬赏任务详情 |
| cancel_bounty | 取消悬赏任务 |
| get_bounty_applications | 获取任务申请列表 |
| accept_bounty_application | 接受任务申请 |

### 对话管理（4个）
| 工具名 | 功能说明 |
|--------|----------|
| get_conversations | 获取对话列表 |
| start_conversation | 与工作者开始新对话 |
| get_conversation_messages | 获取对话消息 |
| send_message | 发送消息 |

---

## 使用示例

```bash
# 获取技能列表
/run workshub get_skills '{}'

# 搜索工作者
/run workshub get_workers '{"skills":"React","location":"北京"}'

# 获取工作者详情
/run workshub get_worker_detail '{"workerId":"bc3Nio"}'

# 登录
/run workshub login '{"phone":"13800138000","code":"123456"}'

# 创建悬赏任务
/run workshub create_bounty '{"title":"开发React网站","description":"需要开发响应式电商网站","budget":5000,"priceType":1,"skills":"React,TypeScript","category":"软件开发"}'
```

---

## 环境变量

| 变量名 | 说明 | 必填 |
|--------|------|------|
| WORKSHUB_API_KEY | API 认证密钥 | 是 |
| WORKSHUB_API_URL | API 基础地址 | 否（默认 https://www.workshub.ai/mcp） |

---

## 权限说明

本技能仅申请最小权限：
- 网络访问：仅允许 `workshub.ai:443`
- 执行权限：仅允许运行 `node`

无文件读写、无系统权限、无高危操作。
