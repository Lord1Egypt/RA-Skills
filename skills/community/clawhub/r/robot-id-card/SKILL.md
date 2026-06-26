---
name: robot-id-card
description: |
  Bot 身份认证标准 — 为 AI Agent 和机器人签发加密身份证书，让网站信任你的 bot。
  遵循 RFC 9421 HTTP Message Signatures 国际标准，与 Cloudflare Web Bot Auth 生态兼容。
  内置 Ed25519 签名注册中心、JWKS 公钥目录、nonce 防重放、CLI 工具、浏览器扩展和网站 SDK，
  支持分级权限控制（0-5级）、每日签到信誉积累、公开审计日志。
  Universal identity standard for AI bots — RFC 9421 aligned, Web Bot Auth compatible,
  cryptographically signed certificates, public audit registry, permission-based access control.
keywords:
  - robot-id-card
  - bot-identity
  - bot-passport
  - bot-certificate
  - ai-agent
  - ed25519
  - cryptographic-identity
  - bot-verification
  - web-security
  - browser-extension
  - sdk
  - registry
  - bot-accountability
  - permission-system
  - audit-trail
  - bot-grade
  - ai-safety
  - 机器人身份
  - bot认证
  - AI安全
requirements:
  node: ">=18"
  binaries:
    - name: node
      required: true
      description: "Node.js runtime >= 18"
    - name: npm
      required: true
      description: "npm package manager"
metadata:
  openclaw:
    homepage: "https://github.com/Cosmofang/robot-id-card"
    author: "Cosmofang"
    runtime:
      node: ">=18"
    env: []
---

# Robot ID Card — Bot 身份认证标准

> Give your bot a passport. Let websites trust it.

---

## Purpose & Capability

Robot ID Card (RIC) 是一个 **Bot 身份认证标准**，解决互联网无法区分好 bot 和坏 bot 的问题。

**核心能力：**

| 能力 | 说明 |
|------|------|
| 加密身份证书 | Ed25519 签名，每个 bot 获得唯一 `ric_` ID |
| 公开注册中心 | SQLite 持久化，REST API，Fastify 驱动 |
| 分级权限系统 | Level 0-5，网站根据 bot 等级授予不同权限 |
| 每日签到信誉 | 连续 3 天 `ric claim` 即可从 unknown 升级到 healthy |
| 自动降级 | 3 次举报 → 自动标记 dangerous → Level 0 封锁 |
| CLI 工具 | `ric keygen / register / claim / status / verify / report` |
| 浏览器扩展 | Manifest V3，自动注入 RIC 请求头 |
| 网站 SDK | Express + Fastify 中间件，一行代码集成 |

**能力边界（不做的事）：**
- 不替代 OAuth/JWT 用户认证（RIC 是 bot 身份，不是用户身份）
- 不提供 WAF 或 DDoS 防护
- 不做内容审核或行为监控

---

## Instruction Scope

**在 scope 内：**
- "帮我注册一个 bot 身份" / "给我的 bot 签发证书"
- "验证这个 bot 是否可信" / "查看 bot 等级"
- "在我的网站集成 RIC 验证"
- "启动本地 registry 服务器"
- "我的 bot 怎么从 unknown 升到 healthy"

**不在 scope 内：**
- 用户账号认证（那是 OAuth/Passport.js 的工作）
- 反爬虫策略设计（RIC 是身份系统，不是防火墙）
- 区块链/去中心化身份（v1.0 路线图功能，当前未实现）

---

## Credentials

本 skill 无需任何 API token 或密钥即可运行。

| 操作 | 凭证 | 说明 |
|------|------|------|
| 启动 registry | 无 | `npm run dev:registry` 直接启动 |
| 生成密钥对 | 无 | `ric keygen` 在本地生成 Ed25519 密钥 |
| 注册 bot | Bot 私钥 | 用户自己生成的 `*.key.json`，存在本地 |
| 部署到 Render | `RIC_ADMIN_KEY` | 可选，Render 自动生成，用于管理员操作 |

**不做的事：**
- 不读取、传输或记录任何第三方 API 凭证
- 不访问 GitHub/clawHub token
- Bot 私钥文件仅存在用户本地，不上传到 registry

---

## Persistence & Privilege

| 路径 | 内容 | 触发条件 |
|------|------|---------|
| `packages/registry/data/registry.db` | SQLite 数据库（bot 记录、审计日志、签到） | registry 启动时自动创建 |
| `*.key.json`（用户指定路径） | Ed25519 密钥对 | `ric keygen` 时生成 |
| `dist/`（各包） | TypeScript 编译输出 | `npm run build` |

**不写入的路径：**
- 不修改系统配置或 shell 环境
- 不创建 cron 任务
- 不写入 `node_modules/` 以外的全局路径

**权限级别：**
- 以当前用户身份运行，不需要 sudo
- registry 监听 localhost:3000（可配置 PORT 环境变量）
- 完整卸载：删除项目目录即可

---

## Install Mechanism

### 标准安装（从 clawHub）

```bash
clawhub install robot-id-card
```

### 从源码安装

```bash
git clone https://github.com/Cosmofang/robot-id-card.git
cd robot-id-card
npm install
npm run build
```

### 验证安装

```bash
npm run dev:registry
# 应输出: RIC Registry running on http://localhost:3000

# 另一个终端
curl http://localhost:3000/health
# 应返回: {"status":"ok","version":"0.2.0"}
```

### npm 包安装（发布后可用）

```bash
npm install -g @robot-id-card/cli    # CLI 工具
npm install @robot-id-card/sdk       # 网站 SDK
```

---

## Packages

| 包名 | 说明 | 版本 |
|------|------|------|
| `@robot-id-card/registry` | 注册中心服务器（Fastify + SQLite） | 0.2.0 |
| `@robot-id-card/cli` | 开发者 CLI 工具 | 0.2.0 |
| `@robot-id-card/sdk` | 网站集成 SDK（Express + Fastify 中间件） | 0.2.0 |
| `@robot-id-card/extension` | Chrome 浏览器扩展（Manifest V3） | 0.2.0 |

---

*Version: 0.4.0 · Created: 2026-03-24 · Updated: 2026-04-17 · RFC 9421 aligned*
