---
name: wq-buddy
description: "Provides CLI tools (`wq`) and a specialized Alpha Miner sub-agent for WorldQuant BRAIN. Use for backtesting alpha expressions, searching BRAIN data fields, analyzing field characteristics, browsing datasets, querying operators, checking competition progress, and submitting alphas. For simple single-expression backtests, use CLI directly. For complex workflows (field exploration, batch backtesting, strategy iteration, submission management), spawn the Alpha Miner agent which has its own domain knowledge base."
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["wq"]
      config:
        - path: "~/.wq-buddy/config.json"
          access: "read-write"
          purpose: "存储BRAIN平台登录凭据和默认回测参数。平台仅支持Cookie会话认证，不支持OAuth/API Key。Token缓存4小时自动刷新。"
        - path: "~/.openclaw/openclaw.json"
          access: "read-write"
          purpose: "添加插件路径并重启Gateway"
      filesystem:
        - path: "~/.wq-buddy/alpha_workbench.db"
          access: "read-write"
          purpose: "存储Alpha回测结果和字段分析数据"
        - path: "~/.wq-buddy/.wq_token.json"
          access: "read-write"
          purpose: "缓存BRAIN平台登录会话Token（有效期4小时），自动刷新"
      credentials:
        - name: "BRAIN账号"
          type: "username_password"
          storage: "file"
          path: "~/.wq-buddy/config.json"
          purpose: "WorldQuant BRAIN平台登录凭据"
          note: "平台不支持OAuth/API Key，仅支持Cookie会话认证"
      install:
        - id: npm
          kind: node
          package: "wq-buddy"
          label: "Install via npm"
        - id: clawhub
          kind: clawhub
          slug: wq-buddy
          label: "Install via ClawHub"
---

# WQBuddy — WorldQuant BRAIN 工具与 Alpha Miner Agent

**项目仓库**: https://github.com/sebrinass/wq-buddy
**npm**: https://www.npmjs.com/package/wq-buddy

---

## 一、安装

**第 1 步：安装 npm 包**

```bash
npm install -g wq-buddy
```

**第 2 步：创建配置文件** `~/.wq-buddy/config.json`

```json
{
  "version": "v1.0.8",
  "credentials": {
    "username": "你的BRAIN账号",
    "password": "你的BRAIN密码"
  },
  "default_settings": {
    "instrument_type": "EQUITY",
    "region": "USA",
    "universe": "TOP3000",
    "delay": 1,
    "decay": 0,
    "neutralization": "INDUSTRY",
    "truncation": 0.08,
    "pasteurization": "ON",
    "unit_handling": "VERIFY",
    "nan_handling": "OFF",
    "language": "FASTEXPR"
  },
  "database": { "type": "sqlite", "path": "alpha_workbench.db" },
  "batch_settings": { "sleep_between_requests": 10, "max_retries": 3, "timeout_seconds": 300 }
}
```

**第 3 步：设置文件权限（保护密码）**

```bash
chmod 600 ~/.wq-buddy/config.json
```

> ⚠️ config.json 包含明文密码，必须设置权限为仅用户可读写。

**第 4 步：注册插件路径**

在 `~/.openclaw/openclaw.json` 的 `plugins.load.paths` 中添加 npm 全局安装路径（通常为 `~/.npm-global/lib/node_modules/wq-buddy`）。

**第 5 步：重启 Gateway**

```bash
openclaw gateway restart
```

---

## 二、使用方式

### 模式 A：轻量 — CLI 直接调用

适合：单条回测、简单搜索。直接调 `wq` 命令，不占额外上下文。

```bash
wq backtest "rank(ts_momentum(close, 60))"
wq search "operating cash flow"
wq analyze fnd2_ebitdm
wq stats
```

### 模式 B：专业 — 构建并 spawn Alpha Miner Agent

适合：字段勘探、批量回测（≥5 条）、策略迭代、提交全流程。需要构建一个**携带完整领域知识的专业 Agent**。

**构建方法**：

Alpha Miner Agent 不是一个空的通用 Agent。它的知识文件在 `wq-buddy` npm 包的 `agent/` 目录下。spawn 时，将以下文件作为 Agent 的知识来源注入：

1. **工作空间规则**：`{npm_global}/lib/node_modules/wq-buddy/agent/AGENTS.md`
2. **身份与价值观**：`{npm_global}/lib/node_modules/wq-buddy/agent/SOUL.md`
3. **安全红线**：`{npm_global}/lib/node_modules/wq-buddy/agent/SAFETY.md`
4. **工具清单**：`{npm_global}/lib/node_modules/wq-buddy/agent/TOOLS.md`
5. **经验记忆**：`{npm_global}/lib/node_modules/wq-buddy/agent/MEMORY.md`
6. **领域知识库**：`{npm_global}/lib/node_modules/wq-buddy/agent/knowledge/`（整个目录，含 wiki-purpose.md、wiki-schema.md、wiki-log.md、wiki/ 下的领域知识页面，含平台资源导航 platform-resources.md）

注意：`{npm_global}` 可通过 `npm root -g` 获取实际路径。

完整的 Agent 构建链路：AGENTS.md 会引导 Agent 依次加载 SOUL → SAFETY → TOOLS → MEMORY → knowledge/wiki/。这些文件共同构成 Alpha Miner 的专业能力——从字段分析到优化诊断到提交闭环。

**spawn 时的关键约束**：
- 给 Agent 的任务描述要**明确具体**——比如"分析 `fnd2_oper_income` 字段，然后用它构建 3 条动量类 Alpha 并回测"
- Alpha Miner 拥有独立的记忆系统（本地 SQLite），每次会话结束后经验自动沉淀到 MEMORY.md

---

## 三、决策路由

```
用户请求 Alpha 相关任务
│
├─ 单条表达式回测 → CLI: wq backtest "expr"
├─ 搜索一两个字段 → CLI: wq search "keyword"
├─ 快速查看统计 → CLI: wq stats
│
└─ 以下场景 → spawn Alpha Miner Agent：
   ├─ 批量回测（≥5 条表达式）
   ├─ 需要了解字段特性（覆盖率/频率/范围 六项分析）
   ├─ 需要优化诊断（Sharpe/Turnover/Fitness 不达标）
   ├─ 需要策略设计（从想法到可提交 Alpha 的全流程）
   └─ 需要管理提交状态（可提交→确认→已通过 闭环）
```
