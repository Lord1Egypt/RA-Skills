---
name: wechat-claude-code-installer
description: 装好「微信 ↔ Claude Code 桥」并避开 6 个新手坑。用户说「装一下微信桥」/「微信里用 Claude Code」/「按那篇逛逛GitHub 文章配一下」/`/wechat-claude-code-installer` 时触发。包装上游 Wechat-ggGitHub/wechat-claude-code 的安装流程，提供 doctor.sh 体检 + install.sh 一键装 + fix-*.sh 6 坑修复脚本。仅 macOS 测过；其他 OS 仅文档参考。
metadata:
  type: skill
  scope: global
---

# WeChat ↔ Claude Code 一键安装 + 6 坑全过

把上游 [`Wechat-ggGitHub/wechat-claude-code`](https://github.com/Wechat-ggGitHub/wechat-claude-code) 的安装流程包装成一个可重复执行的 skill，**自动修掉**首次使用一定遇到的几个体验问题。

## 6 个坑速览

| # | 现象 | 修法（脚本） |
|---|---|---|
| 1 | cwd 设了不算数（daemon 用默认目录） | `scripts/fix-cwd.sh` |
| 2 | Claude 回复带"评估：xxx"元话术 | `scripts/fix-meta-talk.sh` |
| 3 | 闲置 5 分钟 daemon 假死 | `scripts/fix-caffeinate.sh` |
| 4 | `ANTHROPIC_BASE_URL` 默默继承本地代理 | `scripts/doctor.sh`（启动前提醒） |
| 5 | launchd 不死鸟（`kill -9` 杀不掉） | 用 `launchctl unload -w` |
| 6 | setup 卡在交互式输入 | `scripts/install.sh` 灌答案 |

## 触发方式

用户说以下任意一种：

- 「装一下微信桥」「微信里用 Claude Code」
- 「wechat-claude-code 安装」「按那篇逛逛GitHub 的文章配一下」
- `/wechat-claude-code-installer`

## 前置条件

- macOS（launchd 守护；其他 OS 上游也支持 systemd/nohup，但本 skill 修复脚本只测试过 macOS）
- Node.js ≥ 18
- 微信号一个（**强烈建议用个人小号**，不要用工作号）
- 已经在用 Claude Code

## 标准流程（4 步）

### 第 0 步：装前体检（必须先跑）

```bash
~/.claude/skills/wechat-claude-code-installer/scripts/doctor.sh
```

报告 6 项：Node 版本、是否已装、是否已绑、`ANTHROPIC_BASE_URL` 合规风险、OS 平台、**上游漂移检测**（v0.3 新增）。

**重点关注 4️⃣**：如果 `ANTHROPIC_BASE_URL` 指向本地代理（公司 LLM 网关），**所有微信对话会经此代理进入公司日志**——聊私事前请改 plist 切回个人 Anthropic 账号。

**新增第 6 项 — 上游漂移**：上游 wechat-claude-code 项目快速迭代（一周可能有 5-10 个 commit）。doctor 自动比对本地 vs 远程，发现漂移会建议你跑 `check-upstream.sh --since` 看具体新增哪些 commit。

### 第 1-2 步：一键安装（含扫码）

```bash
~/.claude/skills/wechat-claude-code-installer/scripts/install.sh "$HOME/Claude Code"
```

参数是 Claude Code 默认工作目录（路径含空格记得加引号）。脚本会：

1. 跑一遍 doctor（检查环境）
2. clone 上游项目到 `~/.claude/skills/wechat-claude-code/`
3. `npm install`
4. 弹出二维码，**扫码 + 微信里点确认绑定**
5. 自动灌入工作目录（绕过交互式卡死）

### 第 3 步：一键修复全部 6 坑

```bash
~/.claude/skills/wechat-claude-code-installer/scripts/fix-all.sh "$HOME/Claude Code"
```

或者按需单跑：

| 脚本 | 修复 |
|---|---|
| `fix-cwd.sh "$HOME/Claude Code"` | 坑 1：直接改 session.json |
| `fix-meta-talk.sh ["自定义 prompt"]` | 坑 2：覆盖 systemPrompt |
| `fix-caffeinate.sh` | 坑 3：plist 加 `caffeinate -i` |

### 第 4 步：起 daemon + 验证

```bash
cd ~/.claude/skills/wechat-claude-code && npm run daemon -- start
```

在微信里给 AI bot 发 `当前工作目录是哪里`，应回 `~/Claude Code` 且**不带元话术**。

## 日常使用（在微信里发）

| 发什么 | 作用 |
|---|---|
| `/help` | 内置帮助 |
| `/cwd <绝对路径>` | 切换工作目录 |
| `/clear` | 清当前会话 |
| `/status` | 查看状态 |
| `/model <名称>` | 切 Claude 模型 |
| `/prompt <内容>` | 设/改系统提示词 |
| `/skills` | 列已装 skill |
| 任意自然语言 | 转给本机 Claude Code |

发图、发 PDF、发语音都可以；Claude 生成的文件**直接推回微信**。

## 关掉 / 重启 daemon

```bash
# 临时关
cd ~/.claude/skills/wechat-claude-code && npm run daemon -- stop

# 永久关（重启后也不起；修第 5 个坑）
launchctl unload -w ~/Library/LaunchAgents/com.wechat-claude-code.bridge.plist

# 重新启用
launchctl load -w ~/Library/LaunchAgents/com.wechat-claude-code.bridge.plist
```

## 上游漂移检测（v0.3 新增）

上游 `Wechat-ggGitHub/wechat-claude-code` **迭代速度极快**（实测每周 5-10 个 commit），你装的版本一周后就可能落后了几个 fix。本 skill 6 个坑修法是基于上游 v1.0.0 + 特定 commit 范围，**上游修了某些坑后这些修法可能多余甚至冲突**。

```bash
# 看本地 vs 远程是否漂移
~/.claude/skills/wechat-claude-code-installer/scripts/check-upstream.sh

# 把当前装的版本 pin 为基线
~/.claude/skills/wechat-claude-code-installer/scripts/check-upstream.sh --pin

# 看 pin 以来上游所有 commit 列表
~/.claude/skills/wechat-claude-code-installer/scripts/check-upstream.sh --since
```

**建议节奏**：
- **每次跑 install.sh 后**——自动 pin 当时上游 commit
- **每周跑一次** `check-upstream.sh --since`——看上游加了哪些 commit
- 看到关键 fix（如"修了 cwd 问题"）→ 升级试装 → 验证 6 坑还要不要修 → 更新 pin

## 切换 API 端点（避开公司代理）

如果 doctor 报告 `ANTHROPIC_BASE_URL` 指向公司代理，且不希望微信对话经过公司日志：

```bash
PLIST=~/Library/LaunchAgents/com.wechat-claude-code.bridge.plist
python3 <<'PY'
import plistlib, os
p = os.path.expanduser("~/Library/LaunchAgents/com.wechat-claude-code.bridge.plist")
with open(p, 'rb') as f: d = plistlib.load(f)
env = d.setdefault('EnvironmentVariables', {})
env['ANTHROPIC_AUTH_TOKEN'] = 'sk-ant-api03-你的key'
env['ANTHROPIC_BASE_URL'] = 'https://api.anthropic.com/v1/'
with open(p, 'wb') as f: plistlib.dump(d, f)
print("done")
PY
launchctl unload ~/Library/LaunchAgents/com.wechat-claude-code.bridge.plist
launchctl load ~/Library/LaunchAgents/com.wechat-claude-code.bridge.plist
```

## 卸载

```bash
~/.claude/skills/wechat-claude-code-installer/scripts/uninstall.sh
```

完全清掉 daemon + 上游项目 + 数据目录。本 skill 自身保留。

## 风险与免责

1. **微信账号风险**：iLink AI 是腾讯官方通道，封号风险极低；但建议**首次绑个人小号**。
2. **数据流向**：所有微信消息 → 本机 daemon → 你的 `ANTHROPIC_BASE_URL` → Claude。doctor 第 4 步会提醒。
3. **本机权限**：daemon 等同"坐在你电脑前的人"——能跑命令、读文件、改文件。**不要把绑定的微信号借给别人**。
4. **本 skill 不修改上游代码**，所有改动都在 launchd plist + session.json，可随时回滚。
5. 上游 1.0.0 还在迭代；本 skill 修法基于 1.0.0，未来版本可能不需要。

## 参考

- 上游：[Wechat-ggGitHub/wechat-claude-code](https://github.com/Wechat-ggGitHub/wechat-claude-code)
- 灵感原文：「在你微信里用爽 Claude Code」（公众号「逛逛GitHub」，2026-06）

## License

MIT。本 skill 是上游项目的**安装与配置助手**，不重新分发上游代码。
