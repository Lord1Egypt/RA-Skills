---
name: use-openclaw-manual
description: 配置 OpenClaw 前必须查阅官方文档的技能。当用户提到任何配置相关的话题（agent、session、channel、cron、通知、工具、workspace、gateway 等）时，立即使用此技能搜索本地文档。不要凭经验猜测——先查文档再设计方案。
compatibility:
  required_tools: git, curl, python3
  optional_tools: jq (测试框架), openclaw CLI (通知)
  optional_env: GITHUB_TOKEN (GitHub API 认证), OPENCLAW_MANUAL_PATH, DOC_NOTIFY_CHANNEL
  permissions: 本地文件读写 (~/.openclaw/workspace/docs/), GitHub API 访问
---

# use-openclaw-manual - 基于文档的 OpenClaw 配置技能

## 核心原则

**配置前必须查文档** —— 这是使用此技能的根本原因。OpenClaw 的配置字段、命令参数、渠道设置经常变化，凭经验操作容易出错。此技能确保你的配置方案基于最新官方文档，而非过时的记忆。

## 何时使用此技能

**触发场景**（看到以下任何关键词就应触发）：

| 关键词 | 查阅目录 | 优先级 |
|--------|---------|--------|
| agent, workspace, session | `concepts/`, `cli/agents.md` | P0 |
| cron, schedule, reminder, 定时 | `automation/cron.md`, `cli/cron.md` | P1 |
| discord, telegram, whatsapp, qqbot, 通知 | `channels/`, `automation/notifications.md` | P2 |
| tool, profile, browser, exec | `tools/`, `concepts/tools.md` | P1 |
| gateway, config, restart | `gateway/`, `cli/gateway.md` | P0 |
| memory, skill, 技能 | `concepts/memory.md`, `skills/` | P1 |

**不触发的场景**：
- 简单的文件操作（读/写/编辑工作区文件）
- 网络搜索（web_search, web_fetch）
- 与 OpenClaw 配置无关的任务

## 标准工作流程

收到配置需求后，按此流程操作：

```
1. 进入技能目录
   $ cd path/to/use-openclaw-manual/

2. 搜索文档
   $ ./run.sh --search "<关键词>"

3. 阅读相关文档
   $ ./run.sh --read "<文档路径>"

4. 设计方案（引用文档来源）
   "根据 <文档路径>，配置步骤如下：..."

5. 用户批准

6. 执行配置
```

**为什么必须引用文档来源**：让用户知道你的方案有官方依据，而非猜测。如果配置出错，也便于回溯是文档问题还是操作问题。

## 使用方法

### 首次配置

运行配置脚本完成权限设置和文档初始化：

```bash
# 进入技能目录
cd path/to/use-openclaw-manual/

# 运行配置脚本
./setup.sh
```

配置脚本会：
1. 检查必需依赖（git, curl, python3）
2. 添加执行权限到所有脚本
3. （可选）初始化官方文档

### 快速搜索

```bash
# 搜索关键词（默认搜索内容）
./run.sh --search "cron schedule"

# 指定搜索类型
./run.sh --search "agent" --type filename
./run.sh --search "notification" --type title

# 限制结果数量
./run.sh --search "discord" --limit 5
```

### 查阅文档

```bash
# 列出目录内容
./run.sh --list "automation"

# 阅读特定文档
./run.sh --read "automation/cron.md"
```

### 文档同步

```bash
# 增量同步（仅更新变更）
./run.sh --sync

# 仅检查更新（不同步）
./run.sh --check
```

### 查看统计

```bash
./run.sh --stats
```

### 帮助

```bash
./run.sh --help
```

### 查找技能安装位置

如果你不记得技能安装在哪里：

```bash
# 搜索技能目录
find ~ -name "use-openclaw-manual" -type d 2>/dev/null

# 或搜索 run.sh 文件
find ~ -path "*/use-openclaw-manual/run.sh" 2>/dev/null
```

找到后 `cd` 进入该目录即可使用。

## 详细文档

本技能提供以下详细文档：

| 文档 | 用途 | 何时读取 |
|------|------|---------|
| [references/scripts.md](references/scripts.md) | 脚本详细说明 | 首次使用或忘记参数时 |
| [references/troubleshooting.md](references/troubleshooting.md) | 故障排除指南 | 遇到错误或异常时 |

> **Agent 提示**：搜索时优先使用英文关键词（如 `notification`, `cron`, `gateway`），可获得更准确的搜索结果。

### 快速导航

- **了解脚本功能** → 读取 `references/scripts.md`
- **搜索无结果** → 读取 `references/troubleshooting.md` 的"搜索无结果"章节
- **同步失败** → 读取 `references/troubleshooting.md` 的"同步失败"章节
- **查看日志** → 读取 `references/troubleshooting.md` 的"日志分析"章节

## 环境变量

| 变量 | 默认值 | 必需 | 说明 |
|------|--------|------|------|
| `OPENCLAW_MANUAL_PATH` | `~/.openclaw/workspace/docs/openclaw_manual` | 否 | 文档存储路径 |
| `LAST_COMMIT_FILE` | `$OPENCLAW_MANUAL_PATH/.last-docs-commit` | 否 | 同步基线文件 |
| `DOC_UPDATE_LOG` | 技能目录内 `docs-update.log` | 否 | 同步日志 |
| `DOC_NOTIFY_CHANNEL` | `webchat` | 否 | 通知渠道（设为 `none` 禁用） |
| `GITHUB_TOKEN` | 无 | 否 | GitHub API Token（提高速率限制） |

### 运行时依赖

脚本执行前会自动检查以下工具：

- ✅ `git` - 文档同步（必需）
- ✅ `curl` - GitHub API 调用（必需）
- ✅ `python3` - JSON 解析（必需）
- ⚠️ `jq` - JSON 输出（可选，用于 `--json` 模式）
- ⚠️ `openclaw` CLI - 发送通知（可选，缺失时跳过通知）

如缺少必需依赖，脚本会报错并退出。

## 配置规范

### ✅ 必须做

- **配置前搜索文档** —— 即使你"记得"怎么配
- **引用文档来源** —— 在方案中说明依据
- **以文档为准** —— 文档与经验冲突时，相信文档
- **定期同步** —— 确保文档最新

### ❌ 禁止做

- 未查文档直接配置
- 凭猜测填写配置字段
- 忽略文档中的警告或注意事项
- 跳过用户批准步骤

## 示例场景

### 配置 Discord 通知

```
用户：帮我配置 Discord 通知

助手：
1. 进入技能目录
   $ cd path/to/use-openclaw-manual/

2. 搜索文档
   $ ./run.sh --search "discord notification"

3. 找到相关文档
   - channels/discord.md
   - automation/notifications.md

4. 设计方案（引用文档）
   "根据 channels/discord.md 第 3 节，配置步骤如下：..."

5. 用户批准后执行
```

### 配置定时任务

```
用户：设置一个每天早上 9 点运行的任务

助手：
1. 搜索文档
   $ ./run.sh --search "cron schedule every"

2. 查阅 automation/cron.md

3. 设计方案
   "根据 cron.md，使用 schedule.kind='every'，everyMs=86400000..."
```

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| 文档目录为空 | 未初始化 | `--init` |
| 搜索无结果 | 关键词不匹配 | 换关键词或检查是否已同步 |
| 同步失败 | 网络问题 | 检查网络，查看日志 |

详细故障排除见 [references/troubleshooting.md](references/troubleshooting.md)

## 脚本说明

详细脚本文档见 [references/scripts.md](references/scripts.md)

- `scripts/sync-docs.sh` - 文档同步
- `scripts/search-docs.sh` - 文档搜索
- `run.sh` - 入口脚本

## 文件结构

```
use-openclaw-manual/
├── SKILL.md                          # 技能说明（本文件）
├── run.sh                            # 入口脚本
├── scripts/
│   ├── sync-docs.sh                  # 文档同步
│   └── search-docs.sh                # 文档搜索
├── references/
│   ├── scripts.md                    # 脚本详细文档
│   └── troubleshooting.md            # 故障排除
└── .initialized                      # 初始化标记（自动创建）
```

## 相关资源

- 本地文档：`~/.openclaw/workspace/docs/openclaw_manual/`
- 官方文档：https://docs.openclaw.ai
- 社区：https://discord.com/invite/clawd

---

*版本：v2.0.0 | 最后更新：2026-03-11*
