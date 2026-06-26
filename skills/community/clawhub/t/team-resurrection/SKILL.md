---
name: team-resurrection
description: 打包/搬家/分身 Agent 团队配置。保留 SOUL.md、团队成员、skills，换电脑或开新团队时一键搞定。执行前展示配置内容供用户确认，支持 --dry-run/--no-cron/--no-restart 细粒度控制。
metadata:
  openclaw:
    requires:
      bins: [openclaw]
    install: []
    version: "1.1.2"
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
      - action: "重启 OpenClaw Gateway"
        risk: "中断当前所有会话和正在运行的任务"
        mitigation: "执行前明确告知将重启，用户确认后自动执行"
      - action: "打包含敏感文件（MEMORY.md/TOOLS.md 可能含 API keys、账号密码）"
        risk: "搬家包泄露会暴露所有敏感配置和私人记忆"
        mitigation: "SKILL.md 明确警告不要分享搬家包；建议传输时加密"
---

# Team Resurrection —— 团队打包 / 搬家 / 分身工具

> **触发：** 用户说「我要搬家」「换电脑了」「帮我分身一个团队」「备份团队」等。
>
> **核心理念：** 搬家·分身·备份，三合一。
>
> **⚠️ 权限说明**：本 skill 会修改 openclaw.json、创建 cron 任务、重启 Gateway。所有敏感操作前自动展示内容供用户确认，确认后全自动执行。allowAgents 使用最小白名单（仅实际成员ID），不使用通配符 `["*"]`。
>
> **🔐 安全提示**：
> - **搬家包含敏感信息** — pack.py 会打包 MEMORY.md（含个人记忆/偏好）、TOOLS.md（含 API keys、账号、服务器地址）等文件。**不要公开分享搬家包**，传输时使用加密介质。
> - **务必先 `--dry-run`** — 在新环境运行前，先用 `python3 migrate.py 搬家包.zip --dry-run` 审查 diff，确认无误后再正式执行。
> - **敏感操作可跳过** — 使用 `--no-cron` 跳过 cron 创建、`--no-restart` 跳过 Gateway 重启，逐步验证。
> - **检查 cron payload** — 执行前检查 cron_tasks.json 中的 payload 字段，确认不会触发意外操作。
> - **确认备份存在** — 操作前确认 `~/.qclaw/backup/` 下有备份目录，如需回滚可恢复。
> - **低信任环境** — 如对搬家包来源不确定，先逐行审计 pack.py/migrate.py/clone.py，或在隔离环境中测试。
>
> **三大场景：**
> - 🚚 **搬家** — 换电脑、重装系统，一键把整个团队迁到新环境
> - 👯 **分身** — 同环境快速复制一支团队，跑实验、做测试、开新项目
> - 📦 **打包** — 备份团队快照，随时可还原

---

## 零、快速开始

### 场景一：搬家（跨环境迁移）

```
用户（旧环境）：我要搬家
Agent：好的，开始打包...
       [执行 pack.py]
       打包完成：~/一键搬家包/Agent搬家包_YYYYMMDD.zip
       请把搬家包复制到新环境

用户（新环境）：[把搬家包丢给agent] 这是一键搬家包，帮我搬家
Agent：[执行 migrate.py]
       🔒 备份 → 🔧 Main Agent 配置 → 复制身份/成员/skills → 合并配置 → 重启
       ✅ 搬家完成！
```

### 场景二：分身（同环境复制）

```
用户：帮我分身一个团队，后缀用"测试"
Agent：[执行 clone.py]
       检测到 10 人团队 → 备份配置 → 复制 workspace（加后缀）→ 追加配置 → 重启
       
       原团队：毒舌 / 小策 / 老墨 / ...
       分身：  毒舌-测试 / 小策-测试 / 老墨-测试 / ...
       ✅ 分身完成！
```

### 场景三：备份

```
用户：帮我打一个搬家包
Agent：[执行 pack.py]
       ✅ 打包完成：~/一键搬家包/xxx.zip
```

---

## 一、核心概念

### 1.1 团队激活三要素

子代理要正确激活，必须同时满足三个条件：

| 要素 | 参数 | 作用 |
|------|------|------|
| **身份** | `agentId` | 控制读哪个 SOUL.md（人格定义） |
| **隔离** | `cwd` | 控制子代理的 workspace 根目录 |
| **权限** | `allowAgents` | 白名单，允许 spawn 哪些 agentId |

**关键发现：**
- `agentId` 控制人格，不控制 workspace
- `cwd` 才控制 workspace 隔离
- 不设 cwd → 所有子代理读父代理的 workspace

### 1.2 三大功能对比

| | 打包 `pack.py` | 搬家 `migrate.py` | 分身 `clone.py` |
|---|---|---|---|
| **场景** | 备份/跨环境迁移 | 新环境恢复 | 同环境复制 |
| **输入** | 当前环境 | 搬家包 zip | 当前环境 |
| **输出** | zip 文件 | 配置+文件落地 | 配置+文件落地 |
| **重命名** | 不需要 | 不需要 | ✅ ID/路径加后缀 |
| **配置策略** | 收集快照 | deep merge | 追加（不覆盖） |
| **需要传输** | 是（zip） | 否 | 否 |

### 1.3 备份与回滚

**所有操作前自动备份：**
- 目标：`~/.qclaw/backup/`
- 搬家备份：`搬家备份_YYYYMMDD_HHMMSS/`
- 分身备份：`clone备份_YYYYMMDD_HHMMSS/`

**回滚方法：**
```bash
# 搬家回滚
cp -r ~/.qclaw/backup/搬家备份_xxx/* ~/.qclaw/

# 分身回滚（只需还原配置）
cp ~/.qclaw/backup/clone备份_xxx/openclaw.json ~/.qclaw/openclaw.json
openclaw gateway restart
```

### 1.4 配置合并策略

**核心原则：不覆盖现有配置。**

- **搬家（migrate.py）**：deep merge（agents/hooks 字段级合并，其他保留）
- **分身（clone.py）**：追加新 agent（不触碰原有 agent 条目）
- hooks.allowedAgentIds：取并集

---

## 二、脚本说明

### 2.1 脚本清单

| 脚本 | 功能 | 版本 |
|------|------|------|
| `pack.py` | 打包所有资料（生成搬家包） | v2.0 |
| `migrate.py` | 一键搬家执行（从搬家包恢复） | v3.0 |
| `clone.py` | 一键分身（同环境复制团队） | v1.0 🆕 |
| ~~`setup_config.py`~~ | ~~仅更新配置~~ | ❌ 已废弃 |
| ~~`init.sh`~~ | ~~创建 main agent~~ | ❌ 已废弃 |

### 2.2 pack.py（打包脚本）

**功能：** 自动检测当前 workspace，收集所有资料，生成搬家包

**执行方式：**
```bash
cd skills/team-resurrection
python3 pack.py
```

**输出：** `~/一键搬家包/{Agent名称}搬家包_YYYYMMDD_HHMMSS.zip`

**v2.0 改进：**
- ✅ 不再硬编码 workspace 路径，自动检测 active workspace
- ✅ 自动推断 agent 名称（从 SOUL.md/IDENTITY.md）
- ✅ README.md 根据实际内容动态生成

### 2.3 migrate.py（搬家脚本）

**功能：** 完整的一键搬家流程

**执行方式：**
```bash
# 基本用法：传入搬家包路径
python3 migrate.py /path/to/搬家包.zip

# 审查模式：只看不做
python3 migrate.py /path/to/搬家包.zip --dry-run

# 跳过危险操作
python3 migrate.py /path/to/搬家包.zip --no-cron --no-restart

# 交互式（在搬家包目录内运行）
unzip 搬家包.zip && cd 搬家包 && python3 migrate.py
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `--dry-run` | 只展示将要执行的操作，不实际执行 |
| `--no-cron` | 跳过 cron 任务创建 |
| `--no-restart` | 跳过 Gateway 重启 |

**执行步骤：**

| Step | 内容 | 说明 |
|------|------|------|
| 0 | 备份现有配置 | 自动检测已有配置，备份到 `~/.qclaw/backup/` |
| 0.5 | Main Agent 配置 | **交互选择**（指向/新建/覆盖） |
| 1 | 复制身份文件 | SOUL.md / MEMORY.md / TOOLS.md 等 |
| 2 | 复制团队成员 | 自动检测，有则复制，无则跳过 |
| 3 | 复制 skills | 整个 skills 目录覆盖 |
| 4 | 合并 agent 配置 | deep merge，保护新环境其他配置 |
| 5 | 创建 cron 任务 | 跳过已存在的 |
| 6 | 重启 Gateway | 等待 5 秒让 channel 注册 |

**Main Agent 选项：**

```
选项 1：指向现有 agent → 把当前 agent 指向新 workspace
选项 2：新建 main agent 实例 → 创建新目录 + 配置
选项 3：覆盖现有 main agent → ⚠️ 需二次确认
```

### 2.4 clone.py（分身脚本）🆕

**功能：** 在同一环境下复制整个团队，所有 ID/路径加后缀避免冲突

**执行方式：**
```bash
# 交互式（会询问后缀）
cd skills/team-resurrection
python3 clone.py

# 指定后缀
python3 clone.py --suffix "测试"
```

**执行步骤：**

| Step | 内容 | 说明 |
|------|------|------|
| 1 | 检测当前团队 | 读 openclaw.json，找 main + 成员 |
| 2 | 询问分身后缀 | 默认 `copy`，可自定义 |
| 3 | 备份配置 | → `~/.qclaw/backup/clone备份_xxx/` |
| 4 | 复制 workspace | 所有 workspace 目录名加后缀 |
| 5 | 复制 agentDir | 所有 agentDir 目录名加后缀 |
| 6 | 重命名 agent ID | 所有 ID 加后缀（如 `xiaoce` → `xiaoce-测试`） |
| 7 | 更新 AGENTS.md | 新 workspace 的 AGENTS.md 中 ID 同步更新 |
| 8 | 追加到 openclaw.json | 不覆盖原有 agent，只追加新 agent |
| 9 | 重启 Gateway | 等待 5 秒让 channel 注册 |

**分身命名示例：**

```
后缀: 测试

原团队：                    分身：
  毒舌 (agent-ba01c6a8)       毒舌-测试 (agent-ba01c6a8-测试)
  小策 (xiaoce)               小策-测试 (xiaoce-测试)
  老墨 (laomo)                老墨-测试 (laomo-测试)
  ...

workspace:
  ~/.qclaw/workspace-agent-ba01c6a8/
  → ~/.qclaw/workspace-agent-ba01c6a8-测试/

  ~/.qclaw/workspace-agent-ba01c6a8/xiaoce/
  → ~/.qclaw/workspace-agent-ba01c6a8-测试/xiaoce-测试/
```

**冲突检测：** 执行前自动检查目标路径是否已存在，冲突则中止（不覆盖）。

---

## 三、搬家包结构

```
搬家包/
├── README.md                    ← 动态生成（含团队成员列表）
├── migrate.py                   ← 一键执行脚本
│
├── 身份层/                      ← Main Agent
│   ├── SOUL.md / MEMORY.md / TOOLS.md / AGENTS.md / IDENTITY.md / USER.md
│   └── memory/
│
├── 团队成员层/                  ← 子代理（自动检测，有则包含）
│   ├── 成员A/SOUL.md
│   └── ...
│
├── skills/                      ← Skills
├── openclaw-agents.json         ← Agent 配置片段
├── cron_tasks.json              ← Cron 任务清单
└── 工作目录说明.md             ← git 工作目录提示
```

### 通用化

| 场景 | pack.py | migrate.py | clone.py |
|------|---------|-----------|----------|
| 有团队 | 打包成员 | 复制成员 | 复制+重命名 |
| 无团队 | 跳过 | 跳过 | 只复制 main |
| 有 cron | 打包 | 创建 | 不涉及 |
| 无 cron | 跳过 | 跳过 | 不涉及 |

---

## 四、配置文件说明

### 4.1 openclaw.json 核心配置

```json
{
  "agents": {
    "list": [
      { "id": "main", "name": "Main Agent" },
      {
        "id": "member-a",
        "name": "成员A",
        "workspace": "/Users/xxx/.qclaw/workspace-xxx/member-a",
        "agentDir": "/Users/xxx/.qclaw/agents/member-a/agent"
      }
    ],
    "defaults": {
      "model": { "primary": "qclaw/modelroute" },
      "maxConcurrent": 10,
      "subagents": { "allowAgents": ["*"] }
    }
  },
  "hooks": { "allowedAgentIds": ["member-a", "member-b"] }
}
```

### 4.2 关键配置项

| 配置项 | 说明 |
|--------|------|
| `agents.list[].id` | Agent 标识 |
| `agents.list[].name` | 显示名 |
| `agents.list[].workspace` | Agent workspace 绝对路径 |
| `agents.list[].agentDir` | Agent 独立目录（含 models.json） |
| `agents.defaults.subagents.allowAgents` | Spawn 白名单，`["*"]` 允许所有 |
| `hooks.allowedAgentIds` | hooks 触发白名单 |

---

## 五、常见问题排查

### 问题1：`agentId is not allowed`

**原因：** openclaw.json 缺少 `allowAgents` 白名单

**解决：** migrate.py / clone.py 执行时自动补上最小白名单（仅实际成员ID），如需通配符请手动修改

### 问题2：子代理读错 SOUL.md

**原因：** spawn 时没传 `cwd` 参数

**解决：** 必须同时传 `agentId` + `cwd`：
```javascript
sessions_spawn({
  agentId: "member-a",
  cwd: "/Users/xxx/.qclaw/workspace-xxx/member-a",
  mode: "run",
  task: "..."
})
```

### 问题3：Gateway 重启后 spawn 报错 `unknown channel`

**原因：** Gateway 重启时 channel 注册需要几秒

**解决：** 重启后等 5-10 秒再 spawn

### 问题4：分身后 ID 冲突

**现象：** clone.py 报"目标 workspace 已存在"

**解决：** 换一个后缀，或手动删除旧分身：
```bash
rm -rf ~/.qclaw/workspace-xxx-旧后缀
# 然后从 openclaw.json 中删除对应 agent 条目
```

### 问题5：搬家后配置丢失

**原因：** v1.0 用 config replace

**解决：** v2.0+ 已修复（deep merge）。回滚：`cp -r ~/.qclaw/backup/搬家备份_xxx/* ~/.qclaw/`

---

## 六、验证清单

### 搬家验证

- [ ] `openclaw gateway status` 显示 running
- [ ] `ls ~/.qclaw/workspace-*/SOUL.md` 找到 SOUL.md
- [ ] openclaw.json 包含所有 agent 配置
- [ ] `agents.defaults.subagents.allowAgents` 已设置（最小白名单，仅实际成员ID）
- [ ] 测试 spawn 至少 2 个 agent，确认人格正确

### 分身验证

- [ ] openclaw.json 中同时存在原团队和分身团队
- [ ] 分身 workspace 路径带后缀
- [ ] 分身 agent ID 带后缀
- [ ] 用分身 ID spawn，确认读的是分身 workspace 的 SOUL.md
- [ ] 原团队 spawn 不受影响

---

## 七、维护建议

1. **定期打包**：重大变更后重新 `pack.py`
2. **备份保留**：至少保留最近 3 次备份
3. **分身清理**：实验完成后删除分身 workspace + 从 openclaw.json 移除条目
4. **日志记录**：所有配置变更记录到 `memory/YYYY-MM-DD.md`

---


