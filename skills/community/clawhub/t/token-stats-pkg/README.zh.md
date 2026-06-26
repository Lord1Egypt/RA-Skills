# token-stats — 选个 Agent 看它的消耗

每次运行都让你选，想看哪个 Agent 就看哪个。

## 一句话说明

你的电脑上装了多个 AI 助手（Hermes、Claude Code、CodeX、OpenClaw……），
`token-stats` 可以告诉你**每个助手到底用掉了多少 tokens**。

> ⚠️ **重要说明：本工具仅统计本机的 Agent 数据。**
> 如果你在不同 PC 或服务器上运行 Agent，各自的数据仅保存在各台机器上，
> 无法跨机器统计。每台机器需要各自安装本工具查看。
> 
> 所有统计都是基于你选择的某个 Agent 来查询的，不是特指某一个。

---

## 环境要求

装 `token-stats` 之前，你的电脑需要先有这些东西：

### 1. Python 3.8+

`token-stats` 本身是纯 Python 脚本，依赖标准库，不需要额外 pip 装任何包。

```bash
# 检查已安装
python3 --version

# 如果没装 → 去 https://www.python.org/downloads/ 下载
# macOS 通常自带 Python 3，Windows 需要手动装
```

### 2. Node.js（安装工具时需要）

`token-stats` 通过 **ClawHub CLI** 安装。ClawHub 是个 Node.js 命令行工具。

```bash
# 检查已安装
node --version

# 如果没装 → 去 https://nodejs.org 下载（选 LTS 版本）
```

装好 Node.js 后会自动带上 `npm`，用来装 ClawHub。

### 3. ClawHub CLI

```bash
# 安装（npm 全局安装）
npm install -g clawhub

# 验证
clawhub --version   # 应该显示 v0.9.x
```

> 💡 如果你用的是 macOS 且通过 Homebrew 装过 Node.js，
> `npm install -g clawhub` 安装后会出现在 `/opt/homebrew/bin/clawhub`，
> 通常已经在你 PATH 里了，直接用就行。

---

## 安装

满足以上环境后，三行命令搞定：

```bash
# 第 1 步：从 ClawHub 安装 token-stats
clawhub install agent-usage-stats

# 第 2 步：创建全局命令（setup 命令会自动写好包装器，不需修改脚本权限）
python3 ~/skills/agent-usage-stats/token-stats.py setup
```

好了。以后在终端直接敲 `token-stats` 就能用。

### 验证安装成功

```bash
# 验证 1：版本号
token-stats --version
# 输出: token-stats v2.0.7

# 验证 2：看本机已安装的 Agent
token-stats --list-backends
# 输出示例:
#   ✅ Hermes
#   ✅ Claude Code
#   ❌ CodeX
#   ❌ OpenClaw

# 验证 3：直接看某个 Agent 的统计
token-stats -b hermes
# 输出示例:
# 📊 Hermes
#   deepseek-v4-flash | 上下文 62.4K/1.05M (6.0% ✅) | 输入 57.1K | 输出 5.4K | 调用 13 次
```

如果以上三条都正常输出，说明安装完全成功 🎉

> ⚠️ 如果 `~/skills/` 目录不存在，先确认 `clawhub install` 执行时当前目录在哪里。
> ClawHub 会把技能装到 **当前目录下的 skills/ 文件夹**。
> 建议在 `~/.hermes/` 或 `~` 目录下运行安装命令。

---

## 用法

### 快速查看

```bash
# 交互式选择
token-stats

# 直接指定 Agent（跳过菜单）
token-stats -b hermes
token-stats -b claude-code
token-stats -b codex
token-stats -b openclaw

# 查看本机所有 Agent
token-stats --all

# 当前快照（同默认）
token-stats -b hermes --now

# 详细模式（显示更多信息）
token-stats -b hermes --detail
```

所有命令都支持切换 Agent 名称，例如：
- `-b hermes` → Hermes
- `-b claude-code` → Claude Code
- `-b codex` → CodeX
- `-b openclaw` → OpenClaw

输出示例（每个模型一行，仅显示有数据的模型）：
```
📊 Hermes
  deepseek-v4-flash | 上下文 62.4K/1.05M (6.0% ✅) | 输入 57.1K | 输出 5.4K | 缓存 480.6K | 调用 13 次 | 第 16 轮 "..."

📊 Claude Code
  deepseek-v4-pro | 上下文 2.60M/1.05M (>100%) | 输入 1.78M | 输出 823.0K | 缓存 341.48M | 调用 1723 次
  Qwen3-Coder-30B | 上下文 23.0K/131.1K (17.6% ✅) | 输入 22.9K | 输出 131 | 调用 1 次
```

### 时间段查询

查看某段时间内的总消耗（不显示上下文占比，显示会话数）：

```bash
# 今天（各 Agent 通用）
token-stats -b hermes --today
token-stats -b claude-code --today
token-stats -b codex --today
token-stats -b openclaw --today

# 昨天
token-stats -b hermes --yesterday

# 本周（周一到现在）
token-stats -b hermes --week

# 最近 7 天
token-stats -b hermes --last-7d

# 自定义日期范围（从当天 00:00:00 到当天 23:59:59）
token-stats -b hermes --from 2026-01-01 --to 2026-05-18
token-stats -b claude-code --from 2026-01-01 --to 2026-05-18
```

时间段输出示例（无上下文占比，显示会话数）：
```
📊 Hermes
  deepseek-v4-flash | 总计 988.9K | 输入 660.5K | 输出 327.0K | 缓存 72.66M | 调用 699 次 | 4 轮会话
```

### 对比两个时间段

```bash
# 快捷标签对比
token-stats -b hermes --compare --a today --b yesterday
token-stats -b hermes --compare --a this-week --b last-week

# 单天对比
token-stats -b hermes --compare --a 2026-01-01 --b 2026-05-18
token-stats -b claude-code --compare --a 2026-01-01 --b 2026-05-18

# 时间段对比（YYYY-MM-DD~YYYY-MM-DD）
token-stats -b hermes --compare --a 2026-01-01~2026-01-07 --b 2026-01-08~2026-05-18
```

对比输出示例：
```
📊 对比: "today" vs "yesterday"  [Hermes]
══════════════════════════════════════════════════════════════════════
  模型                           |            A |            B |           变化
──────────────────────────────────────────────────────────────────────
  deepseek-v4-flash            |       988.9K |        65.4K |      -923.5K
──────────────────────────────────────────────────────────────────────
  总计                           |       988.9K |        65.4K |      -923.5K
```

### 导出数据

交互式选择目录和格式：

```bash
# 导出当前最新会话
token-stats -b hermes --export
token-stats -b claude-code --export
token-stats -b codex --export

# 导出今天的数据
token-stats -b hermes --today --export

# 导出昨天的数据
token-stats -b hermes --yesterday --export

# 导出过去 7 天
token-stats -b hermes --last-7d --export

# 导出指定时间段
token-stats -b hermes --from 2026-01-01 --to 2026-05-18 --export
token-stats -b claude-code --from 2026-01-01 --to 2026-05-18 --export
```

流程：先显示统计 → 请输入导出目录路径 → 选择 JSON 还是 CSV。

支持三大操作系统路径：
- macOS/Linux: `~/Desktop`, `/tmp/data`
- Windows: `C:\Users\xxx\Documents`

### 实时监控

```bash
# 交互式选择 → 监控
token-stats --watch

# 直接指定
token-stats -b hermes --watch
token-stats -b claude-code --watch 2   # 2 秒刷新一次
```

每 5 秒自动刷新（可自定义间隔），Ctrl+C 停止后输出汇总表。

### 查看本机装了哪些 Agent

```bash
token-stats --list-backends
```

✅ 表示已安装，❌ 表示没装。没装的 Agent 不会出现在菜单里。

---

## 命令大全

所有命令都支持将 `-b hermes` 中的 `hermes` 替换为：`claude-code`、`codex`、`openclaw`。

### 基础

| 命令 | 说明 |
|------|------|
| `token-stats` | 交互式菜单选择 Agent → 查看统计 |
| `token-stats -b <name>` | 直接指定 Agent，跳过菜单 |
| `token-stats --version` | 显示版本号 |
| `token-stats -b <name> --detail` | 详细模式（同默认） |
| `token-stats -b <name> --now` | 当前快照（同默认） |

### 快速时间段

| 命令 | 说明 |
|------|------|
| `token-stats -b <name> --today` | 今日统计（当天 00:00:00 ~ 现在） |
| `token-stats -b <name> --yesterday` | 昨日统计（昨天全天） |
| `token-stats -b <name> --week` | 本周统计（周一开始至今） |
| `token-stats -b <name> --last-7d` | 最近 7 天 |
| `token-stats -b <name> --from 2026-01-01 --to 2026-05-18` | 自定义时间段（起始日 00:00 到结束日 23:59） |

### 对比

| 命令 | 说明 |
|------|------|
| `token-stats -b <name> --compare --a today --b yesterday` | 快捷标签对比 |
| `token-stats -b <name> --compare --a this-week --b last-week` | 本周 vs 上周 |
| `token-stats -b <name> --compare --a 2026-01-01 --b 2026-05-18` | 两个单天对比 |
| `token-stats -b <name> --compare --a 2026-01-01~2026-01-07 --b 2026-01-08~2026-05-18` | 自定义时间段对比 |

**`--a` / `--b` 支持的格式：**
- `today` — 今天
- `yesterday` — 昨天
- `this-week` — 本周（周一起）
- `last-week` — 上周
- `2026-01-01` — 单天
- `2026-01-01~2026-01-07` — 时间段（起始~结束）

### 导出

| 命令 | 说明 |
|------|------|
| `token-stats -b <name> --export` | 导出当前统计（交互式选目录和格式） |
| `token-stats -b <name> --today --export` | 导出今日统计 |
| `token-stats -b <name> --yesterday --export` | 导出昨日统计 |
| `token-stats -b <name> --last-7d --export` | 导出近 7 天统计 |
| `token-stats -b <name> --from 2026-01-01 --to 2026-05-18 --export` | 导出指定时间段统计 |

### 实时监控

| 命令 | 说明 |
|------|------|
| `token-stats --watch` | 交互式选 Agent → 每 5 秒刷新（Ctrl+C 停止） |
| `token-stats -b <name> --watch` | 直接指定 Agent，默认 5 秒 |
| `token-stats -b <name> --watch 10` | 自定义间隔 10 秒 |

### 多 Agent

| 命令 | 说明 |
|------|------|
| `token-stats --all` | 查看本机所有 Agent 统计 |
| `token-stats --list-backends` | 列出已安装的 Agent |

### 安装与维护

| 命令 | 说明 |
|------|------|
| `clawhub install agent-usage-stats` | 从 ClawHub 安装 |
| `token-stats --setup` | 创建 `~/.local/bin/token-stats` 全局命令 |

> 💡 以上所有命令也可以通过 `token-stats --help` 在线查看。

---

## 各 Agent 的数据怎么看

每次运行输出都以 `📊 Agent名称` 开头，下面每行是一个**有数据的模型**（未使用的不显示）。

| Agent | 能看到什么 |
|-------|-----------|
| **Hermes** | 当前会话的模型、上下文占用（占比 + 提示）、输入/输出/cache tokens、API 调用次数、会话轮数 |
| **Claude Code** | 各模型的上下文占用、调用次数、子代理次数、会话/项目总数 |
| **CodeX** | 各模型的线程数（tokens 在 CodeX 中可能为 0，此时仅显示会话数） |
| **OpenClaw** | 当前模型（含 provider）、上下文占用、输入/输出 tokens、Agent 数量 |

### 数据来源位置（便于排查问题）

| Agent | 数据读哪里 |
|-------|-----------|
| Hermes | `~/.hermes/state.db` → sessions 表 |
| Claude Code | `~/.claude/projects/**/*.jsonl` |
| CodeX | `~/.codex/state_*.sqlite` → threads 表 |
| OpenClaw | `~/ai-testing-lab/openclaw/data/.../sessions.json` |

---

## 实用场景

**想知道 Hermes 用了多少上下文？**
```bash
token-stats
# 选 1 → 看到 "上下文: 123.4K/1M (11.8% ✅)"
```

**边用 Claude Code 边盯着消耗？**
```bash
token-stats -b claude-code --watch
# 切到 Claude Code 干活，这边实时跳动 tokens
```

**想换 Agent 了？**
```bash
token-stats
# 再选一次就行
```

---

## 卸载

```bash
# 移除 token-stats 技能
clawhub uninstall agent-usage-stats

# 删除全局命令
rm -f ~/.local/bin/token-stats

# 清理旧 alias（如果你之前设过 alias token-stats=...）
# 检查现在的 shell 配置里有么有：
grep "alias token-stats" ~/.zshrc ~/.bashrc 2>/dev/null || echo "没有发现旧的 alias"

# 如果有输出对应的行，手动删除或用 sed：
sed -i '' '/alias token-stats/d' ~/.zshrc
source ~/.zshrc
```

---

## 兼容性

| 平台 | 状态 |
|------|------|
| macOS | ✅ 完整支持 |
| Linux | ✅ 完整支持 |
| Windows | ⬜ 规划中（欢迎 PR） |

| 环境 | 要求 |
|------|------|
| Python | 3.8+（标准库，零 pip 依赖） |
| Node.js | 仅安装时需要（装 ClawHub） |

---

## 常见问题与排查指南

### 安装问题

#### ❓ `clawhub install agent-usage-stats` 报错

**可能原因：网络问题或 Node.js 版本过旧。**

```bash
# 检查 Node.js 版本（需要 v18+）
node --version

# 重装 ClawHub
npm install -g clawhub

# 如果在国内网络慢，可尝试
npm install -g clawhub --registry=https://registry.npmmirror.com
```

#### ❓ `python3 ~/skills/agent-usage-stats/token-stats.py setup` 提示文件不存在

**原因：ClawHub 把技能装到了执行 `clawhub install` 时所在目录的 `skills/` 文件夹下。**

```bash
# 先看 skills 装在哪里了
find ~ -name "token-stats.py" -type f 2>/dev/null

# 找到后 cd 到对应目录执行 setup
cd ~
clawhub install agent-usage-stats
python3 ~/skills/agent-usage-stats/token-stats.py setup
```

#### ❓ `token-stats` 命令找不到

**原因：`~/.local/bin/` 不在 PATH 中。**

```bash
# 先确认是否在 PATH 里
echo $PATH | grep .local/bin

# 如果没输出，先添加：
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.zshrc
source ~/.zshrc

# 或者直接用完整路径运行
~/.local/bin/token-stats --version
```

#### ❓ 执行 `token-stats` 报 `Permission denied`

**原因：包装器脚本没有执行权限。**

```bash
chmod +x ~/.local/bin/token-stats
# 或者重新执行 setup
python3 ~/skills/agent-usage-stats/token-stats.py setup
```

### 运行问题

#### ❓ 菜单里看不到我装的 Agent

**原因：`token-stats` 通过检查特定路径来判断 Agent 是否已安装。** 这些路径存在才会显示：

| Agent | 检测路径 |
|-------|---------|
| **Hermes** | `~/.hermes/state.db` |
| **Claude Code** | `~/.claude/projects/` |
| **CodeX** | `~/.codex/state_*.sqlite` |
| **OpenClaw** | `~/ai-testing-lab/openclaw/data/agents/main/sessions/sessions.json` |

可以先用 `token-stats --list-backends` 看具体哪个被检测到了。

#### ❓ 统计显示「无数据」或数字为 0

**可能原因：**

1. **Agent 虽然装了但还没使用过** → 先去用一下再回来查
2. **数据文件路径不对** → 运行 `token-stats --list-backends` 确认是否被检测到
3. **时间段内没有数据** → 如果是 `--today` 或 `--from 2026-01-01`，确认该时间段内确实有会话

#### ❓ 对比结果显示 `unknown` 模型

**Hermes 数据库中部分会话的 model 字段为空**，不影响正常统计。可以用这个命令排查：

```bash
sqlite3 ~/.hermes/state.db "SELECT DISTINCT model FROM sessions WHERE model IS NULL OR model = ''"
