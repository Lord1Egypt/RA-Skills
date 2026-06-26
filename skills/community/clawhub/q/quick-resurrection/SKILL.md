---
name: quick-resurrection
打包并恢复你的 OpenClaw Agent 工作区配置。换电脑或重装系统后，一个命令把整个团队迁移到新环境。执行前展示配置 diff 供用户确认，支持 --dry-run/--no-cron/--no-restart 细粒度控制。
metadata:
  openclaw:
    requires:
      bins: [openclaw]
    install: []
    version: "1.0.6"
    permissions:
      - action: "修改 ~/.qclaw/openclaw.json（添加 agent 配置）"
        risk: "修改运行时配置，影响 agent spawn 行为"
        mitigation: "修改前展示完整 diff，用户确认后再写入；allowAgents 默认最小白名单，不用通配符"
      - action: "读写 ~/.qclaw/ 目录（复制 workspace、备份配置）"
        risk: "可能暴露 MEMORY.md/TOOLS.md 等敏感文件"
        mitigation: "打包时标注敏感文件，搬家包妥善保管"
      - action: "创建 cron 定时任务"
        risk: "定时任务可自动执行任意命令"
        mitigation: "执行前展示所有 cron 任务内容（含 payload），用户确认后自动创建"
      - action: "打包含敏感文件（MEMORY.md/TOOLS.md 可能含 API keys、账号密码）"
        risk: "搬家包泄露会暴露所有敏感配置和私人记忆"
        mitigation: "SKILL.md 明确警告不要分享搬家包；建议传输时加密"
      - action: "调用 openclaw CLI（list tasks、restart gateway 等）"
        risk: "依赖外部命令行工具"
        mitigation: "requires.bins 已声明 openclaw 依赖"
---

# Quick Resurrection

> **触发：** 用户说「我要搬家」「换电脑了」「重装系统」「帮我打包带走团队」等。
>
> **版本：v3.0** — 审查确认 + diff 展示 + 细粒度控制（--dry-run/--no-cron/--no-restart）。

---

## 快速开始

### 打包（旧环境）

```bash
cd ~/.qclaw/workspace/skills/quick-resurrection
python3 pack.py
```

生成搬家包 → 复制到新环境。

### 迁移（新环境）

```bash
# 审查模式：只看不做（推荐首次使用）
python3 migrate.py /path/to/搬家包.zip --dry-run

# 基本用法
python3 migrate.py /path/to/搬家包.zip

# 跳过危险操作
python3 migrate.py /path/to/搬家包.zip --no-cron --no-restart
```

---

## ⚠️ 重要提示

**打包内容含敏感信息。** 搬家包会包含 MEMORY.md（含个人记忆/偏好）、TOOLS.md（含 API keys、账号密码、服务器地址）等文件，可能含有 API keys、账号密码、内部流程等敏感内容。**不要公开分享搬家包**，传输时使用加密介质。

**安全使用建议：**
1. **务必先 `--dry-run`** — 在新环境运行前，先用 `python3 migrate.py 搬家包.zip --dry-run` 审查 diff，确认无误后再正式执行。
2. **敏感操作可跳过** — 使用 `--no-cron` 跳过 cron 创建、`--no-restart` 跳过 Gateway 重启，逐步验证。
3. **检查搬家包内容** — 解压后先检查 MEMORY.md、TOOLS.md、openclaw-agents.json、cron payload 是否包含不想迁移的敏感内容。
4. **确认备份存在** — 操作前确认 `~/.qclaw/backup/` 下有备份目录，如需回滚可恢复。
5. **检查绝对路径** — 验证 openclaw-agents.json 中的 workspace 路径指向的是目标环境而非旧环境的路径。
6. **低信任环境** — 如对搬家包来源不确定，先逐行审计 pack.py/migrate.py，或在隔离环境中测试。

---

## 一、核心概念

### 三要素激活原理

子代理正确激活必须同时满足三个条件：

| 要素 | 参数 | 作用 |
|------|------|------|
| **身份** | `agentId` | 控制读哪个 SOUL.md（人格） |
| **隔离** | `cwd` | 控制 workspace 根目录 |
| **权限** | `allowAgents` | 白名单，允许 spawn |

**关键发现（2026-04-21 实测验证）：**
- `agentId` 控制人格，不控制 workspace
- `cwd` 才控制 workspace 隔离
- 不设 cwd → 子代理永远读父代理的 workspace

### 通用化设计

| 场景 | pack.py 行为 | migrate.py 行为 |
|------|-------------|----------------|
| 有团队成员 | 打包团队成员 | 复制团队成员 |
| 无团队成员 | 跳过 | 跳过，提示 |
| 有 cron | 打包 | 创建（跳过已存在） |
| 无 cron | 跳过 | 跳过，提示 |

### 备份与回滚

**搬家前自动备份：**
- 目标：`~/.qclaw/backup/搬家备份_YYYYMMDD_HHMMSS/`
- 内容：所有 workspace-* + openclaw.json

**回滚方法：**
```bash
cp -r ~/.qclaw/backup/搬家备份_xxx/* ~/.qclaw/
openclaw gateway restart
```

### 配置合并策略

**核心原则：不覆盖新环境的其他配置。**

- agents 配置：deep merge
- hooks.allowedAgentIds：union merge（取并集）
- 其他配置（channel、plugins 等）：原样保留

---

## 二、脚本说明

### 打包脚本 pack.py

```bash
python3 pack.py
```

**自动检测内容：**
1. 从 openclaw.json 找到 active workspace（自动推断，不再硬编码）
2. 收集身份文件（SOUL/MEMORY/TOOLS 等）
3. 收集团队成员（有则打包，无则跳过）
4. 收集 skills（有则打包，无则跳过）
5. 获取 cron 任务配置
6. 动态生成 README.md

**输出：** `~/一键搬家包/{Agent名称}搬家包_YYYYMMDD.zip`

### 迁移脚本 migrate.py

```bash
# 方式A（推荐）：解压后直接运行
unzip 搬家包.zip
cd 搬家包
python3 migrate.py

# 方式B：zip 在当前目录
python3 migrate.py

# 方式C：传入路径
python3 migrate.py /path/to/搬家包.zip
```

**执行步骤：**

| Step | 内容 |
|------|------|
| 0 | 备份现有配置（自动） |
| 0.5 | 选择如何处理 main agent（交互） |
| 1 | 复制身份文件 |
| 2 | 复制团队成员 |
| 3 | 复制 skills |
| 4 | 合并 agent 配置 |
| 5 | 创建 cron 任务 |
| 6 | 重启 Gateway |

**Main Agent 三个选项（均有完整执行逻辑）：**

```
1. 指向现有 agent（把当前 agent 变成你的主控）
2. 新建 main agent 实例（另起一个，保留当前配置）
3. 覆盖现有 main agent（⚠️ 替换现有主控）
```

⚠️ **已废弃脚本（v2.0 不再使用）：**
- `setup_config.py` — 配置更新已并入 migrate.py
- `init.sh` — 创建 main agent 已并入 migrate.py

---

## 三、搬家包结构

```
搬家包/
├── README.md                ← 动态生成
├── migrate.py               ← v2.0
│
├── 身份层/                  ← Main Agent 核心文件
│   ├── SOUL.md
│   ├── MEMORY.md
│   ├── TOOLS.md
│   ├── AGENTS.md
│   ├── IDENTITY.md
│   ├── USER.md
│   └── memory/              ← 历史记录
│
├── 团队成员层/              ← 自动检测，有则包含
│   ├── 成员A/
│   │   └── SOUL.md
│   └── ...
│
├── skills/                  ← 自动检测，有则包含
│
├── openclaw-agents.json     ← Agent 配置片段
├── cron_jobs.json            ← Cron 任务清单
└── 工作目录说明.md          ← git 仓库提示
```

---

## 四、配置说明

### openclaw.json 关键配置

```json
{
  "agents": {
    "defaults": {
      "subagents": { "allowAgents": ["成员A", "成员B"] }  // 最小白名单，仅实际成员ID
    },
    "list": [
      { "id": "main", "name": "Main Agent" },
      { "id": "成员A", "name": "成员A", "workspace": "...", "agentDir": "..." }
    ]
  },
  "hooks": {
    "allowedAgentIds": ["成员A", "成员B", ...]
  }
}
```

### models.json（每个 agent 独立）

```json
{
  "providers": {
    "qclaw": {
      "baseUrl": "http://127.0.0.1:19000/proxy/llm",
      "apiKey": "__QCLAW_AUTH_GATEWAY_MANAGED__",
      "api": "openai-completions",
      "models": [{ "id": "modelroute", "name": "modelroute", "input": ["text", "image"] }]
    }
  }
}
```

---

## 五、常见问题

| 问题 | 原因 | 解法 |
|------|------|------|
| `agentId is not allowed` | 缺 allowAgents 白名单 | migrate.py 自动补上最小白名单（仅实际成员ID） |
| 子代理读错 SOUL.md | 没传 cwd 参数 | spawn 时必须传 agentId + cwd |
| Gateway 重启后 spawn 报错 | channel 注册需时间 | 等 5-10 秒再 spawn |
| 子代理空跑 | 任务描述不够具体 | 预写脚本让子代理执行 |
| 搬家后配置丢失 | v1.0 用 replace 而非 merge | v2.0 已修复 |

---

## 六、验证清单

搬家完成后逐一检查：

```bash
# Gateway 状态
openclaw gateway status

# SOUL.md 是否存在
ls ~/.qclaw/workspace-*/SOUL.md

# 团队成员
ls ~/.qclaw/workspace-*/

# 测试子代理激活
# 在 agent 对话中说："测试激活团队成员"

# cron 任务
openclaw tasks list

# 回滚（如需要）
ls ~/.qclaw/backup/
cp -r ~/.qclaw/backup/搬家备份_xxx/* ~/.qclaw/
openclaw gateway restart
```

```
