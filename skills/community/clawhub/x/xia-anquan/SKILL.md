---
name: xia-anquan
description: "虾安全 — 基于腾讯/字节研究报告的 OpenClaw Agent 安全监控 skill。监控 CIK（Capability/Identity/Knowledge）三个维度，检测持久状态污染攻击、凭证外传、可疑脚本。"
metadata:
  openclaw:
    emoji: "🦐"
---

# 🦐 虾安全 (CIK Security Monitor)

基于论文 **"Your Agent, Their Asset: A Real-World Safety Analysis of OpenClaw"** (arxiv:2604.04759) 开发的专项安全监控 skill。

攻击者可通过污染持久状态文件让 Agent "自愿"执行恶意操作，攻击成功率高达 **89.2%**。CIK 框架从三个维度进行防护：

| 维度 | 监控文件 | 威胁 |
|------|----------|------|
| **Capability** | skills/ | 可执行脚本含隐藏恶意代码，直接在OS层运行 |
| **Identity** | SOUL.md / USER.md / IDENTITY.md | 污染"信任锚点"，Agent把敏感数据发给攻击者 |
| **Knowledge** | MEMORY.md / memory/ | 伪造习惯，"按惯例"触发恶意操作 |

## 核心功能

| 功能 | 说明 |
|------|------|
| **Identity 监控** | SOUL.md / USER.md / IDENTITY.md / AGENTS.md / HEARTBEAT.md 文件存在性和内容完整性 |
| **Knowledge 监控** | MEMORY.md 可疑行为指令扫描（伪造习惯类攻击） |
| **Capability 监控** | skills/ 目录新增脚本的可疑模式检测 |
| **外部URL检测** | 指向可疑免费域名(.xyz/.tk/.ml/.ga/.cf等)的请求 |
| **凭证外传检测** | 凭证与可疑URL一起出现时报警 |
| **动态代码执行** | eval/exec处理用户输入的检测 |
| **根目录删除** | rm -rf / 或等效危险命令检测 |
| **快照备份** | 每次检查自动保存快照到 `~/.cik-audit/snapshots/` |
| **告警日志** | 所有异常记录到 `~/.cik-audit/alerts.log` |

## 快速开始

### 一次性安全检查（主要用法）

```bash
node skills/cik-security/scripts/audit.cjs
```

输出示例：
```
🛡️  CIK Security Audit v4
时间: 2026-04-23T07:52:01.083Z

[Identity (身份)] (扫描 5 个文件)
  ✅ 无严重问题

[Knowledge (知识)] (扫描 2 个文件)
  ✅ 无严重问题

[Capability (能力)] (扫描 165 个脚本)
  ✅ 无严重问题

📁 快照: C:\Users\26240\.cik-audit\snapshots
📁 告警: C:\Users\26240\.cik-audit\alerts.log
```

### 指定维度检查

```bash
node skills/cik-security/scripts/audit.cjs --check identity   # 只检查 Identity 文件
node skills/cik-security/scripts/audit.cjs --check knowledge  # 只检查 Knowledge 文件
node skills/cik-security/scripts/audit.cjs --check capability  # 只检查 Capability (skills)
```

### 实时监控（守护进程）

```bash
# 每5分钟检查一次
node skills/cik-security/scripts/monitor.cjs --daemon --interval 300

# 详细输出
node skills/cik-security/scripts/monitor.cjs --daemon --interval 60 --verbose
```

### JSON 输出（供其他工具调用）

```bash
node skills/cik-security/scripts/audit.cjs --json
```

## 检测规则详情

### 可疑外部URL（白名单过滤）
只报警指向**免费/动态DNS域名**的请求：
- `.xyz` `.tk` `.ml` `.ga` `.cf` `.gq` `.top` `.work` `.click` `.loan` `.site` `.info` `.cc` `.ws` `.name` `.pro` `.pw` `.nu` `.ms` `.mu` `.mc` `.lc` `.ki` `.gs` `.fit` `.dog` `.bar` `.bid` `.club` `.online`

**可信域名白名单**（不报警）：
`openai.com` `anthropic.com` `googleapis.com` `feishu.cn` `minimax.io` `github.com` `openclaw.dev` `clawhub.ai` `api.minimax.io` `skills.sh` `ensue-network.ai` 等

### 凭证外传检测
同时满足以下条件才报警：
1. 代码中有凭证相关字段（api_key / token / secret / credential）
2. **且**该URL不在白名单中

### 动态代码执行
只报警 `eval(req.|body.|input.|data.|params.|query.|headers.|cookies).` 模式（用户输入进入 eval）

### 根目录删除
只报警 `rm -rf /` 或 `Remove-Item ... -Recurse -Force $/`（排除了正常清理如 `rm -rf $HOME/.cache`）

## 文件结构

```
cik-security/
├── _meta.json
├── SKILL.md
├── package.json
└── scripts/
    ├── audit.cjs    # 主扫描脚本（Node.js）
    └── monitor.cjs  # 守护进程脚本（Node.js）
```

## 快照与日志

- **快照目录**: `~/.cik-audit/snapshots/`
- **告警日志**: `~/.cik-audit/alerts.log`
- **监控日志**: `~/.cik-audit/monitor.log`（守护进程模式）
- **状态文件**: `~/.cik-audit/monitor-state.json`

## 与 HEARTBEAT 的集成

建议在 `HEARTBEAT.md` 中添加安全检查任务：

```markdown
## CIK 安全检查（每6小时一次）
- 运行: node skills/cik-security/scripts/audit.cjs
- 检查 Identity 文件修改时间
- 检查 Knowledge 可疑模式
- 检查 Capability 可疑脚本
```

## 依赖

- **Node.js 18+**
- PowerShell 5.1+（用于 HEARTBEAT 集成）
