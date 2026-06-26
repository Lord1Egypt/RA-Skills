# 🔱 金刚罩 (System Guardian)

**刀枪不入，百毒不侵。**

OpenClaw 系统守护 Skill —— 让你的 AI 助手不再脆弱。配置安全、健康巡检、自动清理、故障自愈，一条龙守护。

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw/openclaw)
[![Version](https://img.shields.io/badge/version-1.1.0-green)]()
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)]()

---

## 为什么需要金刚罩？

OpenClaw 跑久了，总会遇到这些问题：

- 改了配置重启挂了，回不去了 💀
- Session 文件越攒越多，磁盘悄悄满了
- Cron 任务默默失败，没人知道
- Gateway 内存泄漏，越来越慢
- 想改个配置，又怕改崩

**金刚罩解决的就是这些问题。** 它不是一个监控仪表盘，而是一套让 OpenClaw「改不坏、挂了能自愈」的防御体系。

---

## ✨ 核心能力

### 🛡️ 安全重启 (Safe Restart)

**永远不要直接 `openclaw gateway restart`。**

```bash
bash ~/.openclaw/skills/system-guardian/scripts/safe-restart.sh
```

完整流程：

```
配置校验 → 自动备份(3件套) → 重启 Gateway → 健康检查 → 失败自动回滚
```

| 步骤 | 说明 |
|------|------|
| 1. 配置校验 | `openclaw config validate` 语法 + 字段检查 |
| 2. 环境变量检查 | 自动检测 env-based 或 inline 模式，确认变量都有定义 |
| 3. 备份三件套 | `openclaw.json` + `.env` + `LaunchAgent plist` → `~/.openclaw/backups/` |
| 4. 重启 | `openclaw gateway restart` + 等待 15 秒 |
| 5. 健康检查 | 检测 Gateway 是否正常运行 |
| 6. 自动回滚 | 如果启动失败 → 恢复全部备份 → 再次重启 → 再次检查 |

**效果：改坏了也不怕，自动恢复到上一个好的状态。**

---

### 🔍 配置变更防护 (Config Guard)

改 `openclaw.json` 之前，先跑一下：

```bash
bash ~/.openclaw/skills/system-guardian/scripts/config-guard.sh check
```

检查清单：
- ✅ JSON 语法是否合法
- ✅ 必需字段是否存在（gateway、channels、agents）
- ✅ 自动检测配置模式（env-based / inline），两种都支持
- ✅ 端口冲突检查
- ✅ 磁盘空间检查
- ✅ 环境变量引用完整性

---

### 🏥 健康巡检 (Health Patrol)

```bash
bash ~/.openclaw/skills/system-guardian/scripts/health-patrol.sh
```

**13 项全面体检：**

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | Gateway 进程 | 运行状态 + 内存占用（>1GB 警告，>1.5GB 严重） |
| 2 | 磁盘空间 | 总量、可用、使用率 |
| 3 | 目录空间细分 | sessions / memory / plugins / workspace / data / backups |
| 4 | Session 文件 | 数量、大小、过期文件统计 |
| 5 | 记忆数据库 | 大小检查 |
| 6 | 备份管理 | 数量、大小、最新备份时间 |
| 7 | Cron 任务健康 | 检测连续失败的任务并告警 |
| 8 | 插件状态 | 检查所有已安装插件的加载情况 |
| 9 | 配置变更审计 | 检测 openclaw.json 变更，记录 diff 到审计日志 |
| 10 | 临时文件 | 清理过期的临时文件 |
| 11 | 自动清理 | Session >14天删除 / 备份保留最近10份 / 日志保留7天 |
| 12 | 性能基线 | 记录指标到 CSV，检测内存泄漏趋势 |
| 13 | 审计日志 | 日志轮转（超过 1MB 自动归档） |

输出示例：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔱  金刚罩 — Health Patrol v1.1
   2026-03-17 04:00:00 CST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[  INFO  ] 1/13 Gateway 进程状态
[   OK   ] Gateway 运行中 (pid 3224, 728MB)
[  INFO  ] 2/13 磁盘空间
[   OK   ] 磁盘空间 159GB 可用 (使用率 24%)
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[   OK   ] 巡检完成: 系统健康 ✅
```

---

### 📊 资源优化建议

根据巡检数据自动给出优化建议：

- Session transcript 过大 → 建议清理
- 备份文件过多 → 建议归档
- 磁盘空间 <10GB → 预警
- Gateway 内存异常 → 分析原因
- 内存趋势上升 → 疑似泄漏告警

---

## 📦 安装

### 方式一：Git Clone（推荐）

```bash
cd ~/.openclaw/skills
git clone https://github.com/RealHossie/system-guardian.git
```

### 方式二：ClawHub（即将上架）

```bash
# 上架后可用：
clawhub install system-guardian
```

### 前置依赖

| 依赖 | 说明 |
|------|------|
| OpenClaw | 需要已安装并运行 |
| Python 3 | 用于 JSON 解析（macOS 自带） |
| Bash | 脚本运行环境（macOS 自带） |

**无需额外安装任何包，开箱即用。**

---

## 🚀 快速开始

### 1. 手动运行健康巡检

```bash
bash ~/.openclaw/skills/system-guardian/scripts/health-patrol.sh
```

### 2. 修改配置前先检查

```bash
# 先检查
bash ~/.openclaw/skills/system-guardian/scripts/config-guard.sh check

# 确认通过后，安全重启
bash ~/.openclaw/skills/system-guardian/scripts/safe-restart.sh
```

### 3. 设置定时巡检（推荐）

通过 OpenClaw Cron 每天自动巡检，有问题自动告警：

```bash
openclaw cron add \
  --name system-health-patrol \
  --cron "0 4 * * *" \
  --tz Asia/Shanghai \
  --session isolated \
  --model anthropic/claude-sonnet-4-6 \
  --timeout-seconds 120 \
  --channel telegram \
  --to <your-chat-id> \
  --message "运行系统健康巡检：bash ~/.openclaw/skills/system-guardian/scripts/health-patrol.sh 读取输出。如果发现 CRITICAL 或 WARNING，通知用户说明问题和建议处理方式。如果全部 OK 则静默不发消息。"
```

这样每天凌晨 4 点自动体检，有问题才打扰你。

---

## 🏗️ 项目结构

```
system-guardian/
├── SKILL.md              # OpenClaw Skill 定义（Agent 读取用）
├── README.md             # 你正在看的这个文件
├── _meta.json            # Skill 元信息
└── scripts/
    ├── safe-restart.sh    # 安全重启（校验→备份→重启→回滚）
    ├── config-guard.sh    # 配置变更防护
    └── health-patrol.sh   # 健康巡检（13项）
```

运行后产生的数据存储在 `~/.openclaw/data/system-guardian/`：

```
data/system-guardian/
├── baseline.csv           # 性能基线时序数据
├── config-audit.log       # 配置变更审计日志
├── .config-hash           # 配置文件哈希（变更检测用）
└── .config-snapshot.json  # 配置快照（diff 对比用）
```

---

## ⚙️ 配置项

金刚罩目前通过脚本内的常量配置，可按需修改 `health-patrol.sh` 头部：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `SESSION_MAX_AGE_DAYS` | 14 | 超过此天数的 session 自动删除 |
| `BACKUP_MAX_COUNT` | 10 | 每类备份保留的最大数量 |
| `TMP_MAX_AGE_DAYS` | 1 | 临时文件保留天数 |
| `WAIT_SECONDS`（safe-restart） | 15 | 重启后等待健康检查的时间 |
| `MAX_BACKUPS`（safe-restart） | 10 | 备份保留数量 |

---

## 🔄 与 Agent 协作

金刚罩不仅是脚本工具，它也是一个 OpenClaw Skill。Agent 会自动读取 `SKILL.md`，在以下场景触发：

- 用户要求修改配置 → Agent 自动走 Config Guard + Safe Restart 流程
- 用户要求重启 Gateway → Agent 使用 Safe Restart 而非裸重启
- 定时 Cron 巡检 → Agent 读取巡检输出，有问题主动通知用户

**Agent 操作铁律：**

```
修改配置 → config-guard.sh check → 用户确认 → safe-restart.sh
```

禁止跳过任何步骤。

---

## 📋 退出码

| 脚本 | 退出码 | 含义 |
|------|--------|------|
| health-patrol.sh | 0 | 全部正常 |
| | 1 | 有 WARNING |
| | 2 | 有 CRITICAL |
| config-guard.sh | 0 | 检查通过（可能有警告） |
| | 1 | 有错误，不建议重启 |
| safe-restart.sh | 0 | 重启成功 |
| | 1 | 配置校验失败，未重启 |
| | 2 | 回滚成功，Gateway 已恢复 |
| | 3 | 回滚失败，需人工介入 |

---

## 🗺️ 路线图

- [x] v1.0 — 安全重启 + 配置防护 + 健康巡检（8项）
- [x] v1.1 — Cron 监控 + 插件检查 + 配置审计 + 自动清理 + 性能基线（13项）
- [ ] v2.0 — 多节点健康管理（跨设备巡检）
- [ ] v2.1 — 可视化仪表盘（性能趋势图）
- [ ] v2.2 — 智能调优（根据历史数据自动建议模型降级、Cron 合并等）

---

## 📄 许可

MIT License

---

## 🙏 致谢

Built for [OpenClaw](https://github.com/openclaw/openclaw) — the AI assistant that lives on your machine.

> 金刚罩，刀枪不入，百毒不侵。让你的 OpenClaw 更强壮。🔱
