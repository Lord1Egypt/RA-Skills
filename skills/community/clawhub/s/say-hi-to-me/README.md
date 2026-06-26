<div align="center">

# 请先说你好.skill

> *"说声「/hi」，就能开始。"*

<!-- Badge Row 1: Core Info -->
[![ClawHub](https://img.shields.io/badge/ClawHub-Say--Hi--to--Me-E75C46?logo=clawhub)](https://clawhub.ai/JustZeroX/say-hi-to-me)  [![GitHub](https://img.shields.io/badge/GitHub-JustZeroX-181717?logo=github)](https://github.com/JustZeroX/skill-say-hi-to-me)  [![Version](https://img.shields.io/badge/Version-0.0.1-orange)](https://github.com/JustZeroX/skill-say-hi-to-me)

<!-- Badge Row 2: Tech Stack -->
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=3776AB)](https://www.python.org/)   [![YAML](https://img.shields.io/badge/YAML-Config-orange)](https://yaml.org/)

<!-- Badge Row 3: Platforms -->
[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)](https://github.com/JustZeroX/skill-say-hi-to-me)  [![Windows](https://img.shields.io/badge/Windows-0078D6?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4OCA4OCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGgzOXYzOUgweiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik00OSAwaDM5djM5SDQ5eiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDQ5aDM5djM5SDB6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTQ5IDQ5aDM5djM5SDQ5eiIvPjwvc3ZnPg==)](https://github.com/JustZeroX/skill-say-hi-to-me)   [![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://github.com/JustZeroX/skill-say-hi-to-me)

<!-- Badge Row 4: License -->
[![License](https://img.shields.io/badge/License-MIT-BD2D2D)](LICENSE)
<br>
<br>
想聊天，但不知道怎么开口。<br>
想找个人陪，但不想被打扰。<br>
想有个人记得你，但不需要每句话都有回应。
<br>

一句 **「/hi」** 。<br>
请先说你好，就会开始。 <br>
可以选择不同的人设陪你聊。<br>
也可以设置在你沉默时轻声问候。<br>

</div>



---
# ✨ 功能特点

- **👋 双重入口** — `/hi` 命令或直接说话，怎么方便怎么来
- **🎭 人设系统** — 创建、切换、定制你的专属数字伙伴
- **⏰ 主动问候** — 开启后会在你沉默时轻轻问候（可随时关闭）
- **🔕 安静时段** — 睡前设好免打扰，睡个好觉
- **🛡️ 安全边界** — 陪伴但不越界，有温度但不黏人
- **🔗 Heartbeat 集成** — 支持 OpenClaw 心跳触发定时问候
- **🌐 双语友好** — 中文优先，英文也能聊

---

# 🚀 快速开始

### 步骤 1：安装

#### 方式 1：Via ClawHub（推荐 ⭐）

```bash
# 1. 安装 ClawHub（如未安装）
npm install -g clawhub

# 2. 安装 say-hi-to-me
clawhub install say-hi-to-me
# 或
npx clawhub@latest install say-hi-to-me
```

#### 方式 2：Via GitHub

```bash
git clone https://github.com/JustZeroX/skill-say-hi-to-me.git ~/.openclaw/skills/say-hi-to-me
```

### 步骤 2：打招呼

```bash
# 方式一：使用命令
/hi

# 方式二：直接说话
你好呀，今天怎么样？
```

### 步骤 3：创建人设（可选）

```bash
# 快速模板
/hi 角色 模板 luoshui

# 或者用自己的描述创建
帮我创建一个温柔治愈系的角色，她喜欢植物和手冲咖啡
```

### 步骤 4：开启主动问候（可选）

```bash
# 开启
/hi 开

# 设置频率（低=24h，中=12h，高=6h）
/hi 频率 中
```

---

# 📖 使用示例

### 示例 1：日常陪伴

```
用户: /hi
助手: 👋 嗨！今天过得怎么样？

用户: 还行，就是有点累
助手: 💪 工作辛苦了！要不先休息一下，喝杯水？

用户: 嗯，准备追个剧放松一下
助手: 🎬 好选择！今天推荐你看点轻松的内容，给自己充充电～
```

### 示例 2：创建专属角色

```
用户: 帮我创建一个动漫风格的新角色，她是一个喜欢画画的大学生

助手: 🌸 好的！我来帮你创建这个角色...
     
     【治愈画师】
     风格：动漫风
     性格：温柔细腻，喜欢用画画表达情感
     兴趣：绘画、动漫、咖啡厅
     
     保存这个人设吗？回复「确认」激活～
```

### 示例 3：设置定时问候

```
用户: /hi 开
助手: ✅ 主动问候已开启！我会在你沉默一段时间后轻声问候。

用户: /hi 频率 高
助手: 📊 已调整为高频模式（每6小时检查一次）

用户: /hi 免打扰 23:00-08:00
助手: 🌙 好的，23:00-08:00 为安静时段，不会打扰你。
```

---

# 💬 命令参考

## 基础命令

| 命令 | 说明 |
|------|------|
| `/hi` | 打个招呼 |
| `/hi 帮助` | 显示所有命令 |
| `/hi 状态` | 查看当前设置 |
| `/hi 重置` | 重置所有配置 |

## 主动问候

| 命令 | 说明 |
|------|------|
| `/hi 开` | 开启主动问候 |
| `/hi 关` | 关闭主动问候 |
| `/hi 频率 低\|中\|高` | 设置问候频率 |
| `/hi 免打扰 HH:MM-HH:MM` | 设置安静时段 |
| `/hi 暂停 <时长>` | 暂停问候（如 `30m`、`2h`、`1d`）|

## 人设管理

| 命令 | 说明 |
|------|------|
| `/hi 角色 列表` | 查看所有角色 |
| `/hi 角色 当前` | 查看当前角色 |
| `/hi 角色 切换 <名字>` | 切换角色 |
| `/hi 角色 新建 <描述>` | 创建新角色 |
| `/hi 角色 编辑 <属性> <值>` | 编辑角色 |
| `/hi 角色 预览` | 预览当前角色 |
| `/hi 角色 保存 <名字>` | 保存角色 |
| `/hi 角色 确认` | 确认激活 |
| `/hi 角色 模板 luoshui` | 使用内置模板 |

---

# 🧩 核心概念

## 人设状态机

```
init → daily ↔ stress
         ↓
      cooldown
         ↓
      celebrate
```

| 状态 | 说明 |
|------|------|
| `init` | 刚初始化，等待配置 |
| `daily` | 日常陪伴模式 |
| `stress` | 检测到压力信号，开启支持模式 |
| `cooldown` | 用户请求安静，最小化交互 |
| `celebrate` | 庆祝成就时刻 |

## 主动触达机制

```
OpenClaw Heartbeat/Cron
         ↓
  proactive_scheduler.py
         ↓
    【检查条件】
    ├─ 主动问候已开启
    ├─ 未在暂停中
    ├─ 不在安静时段
    └─ 冷却时间已过
         ↓
    生成温暖问候 → 发送
```

## 免打扰参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `enabled` | `false` | 默认关闭 |
| `frequency` | `mid` | 中：每12小时检查一次 |
| `freshness` | `72h` | 72小时内的对话视为活跃 |

### 频率档位

| 档位 | 间隔 | 适用场景 |
|------|------|---------|
| `低` | 24小时 | 轻度陪伴 |
| `中` | 12小时 | 日常模式 |
| `高` | 6小时 | 紧密连接 |

---

# 🔧 配置说明

## Workspace 解析优先级

| 来源 | 路径 | 优先级 |
|------|------|--------|
| 环境变量 | `OPENCLAW_WORKSPACE` | 最高 |
| 配置文件 | `~/.openclaw/config.yaml` | 中 |
| 默认目录 | `~/.openclaw/workspace/` | 最低 |

## 目录结构

```
say_hi_to_me/
├── SKILL.md                      # 技能入口定义
├── README.md                     # 技术文档
├── PROJECT_STRUCTURE.md          # 项目结构说明
│
├── scripts/
│   ├── companion_runtime.py      # 核心运行时
│   ├── command_normalizer.py      # 命令标准化
│   ├── proactive_scheduler.py    # 主动调度策略
│   ├── heartbeat_bridge.py        # Heartbeat 桥接
│   ├── sync_heartbeat_md.py       # Heartbeat 同步
│   ├── generate_rolecard.py      # 角色卡生成
│   └── validate_rolecard.py      # 角色卡验证
│
├── references/
│   ├── runtime-core.md           # 运行时核心契约
│   ├── command-spec.md           # 命令规范
│   ├── proactive-scheduling.md   # 主动调度文档
│   ├── safety-policy.md          # 安全策略
│   ├── rolecard-structure.md     # 角色卡结构
│   ├── openclaw-heartbeat-integration.md  # Heartbeat 集成
│   └── presets/
│       └── luoshui-v1.yaml       # 内置角色模板
│
├── roles/                        # 角色卡存放目录
├── state/                        # 运行时状态存储
├── tests/                        # 测试套件
└── examples/                     # 示例配置
```

---

# 🧪 测试验证

```bash
# 测试日常对话
python3 scripts/companion_runtime.py --text "你好" --json

# 测试角色创建
python3 scripts/companion_runtime.py --text "帮我创建一个写实风格的新角色，她是一个热爱咖啡的独立书店店长" --json

# 测试主动调度
python3 scripts/proactive_scheduler.py --json

# 验证角色卡
python3 scripts/validate_rolecard.py roles/<role-file>.yaml

# 运行测试套件
python3 -m unittest discover -s tests -p "test_*.py"
```

**预期结果：**

```
✅ test_command_normalizer.py       - 通过
✅ test_heartbeat_bridge.py         - 通过
✅ test_runtime_scheduler_flow.py   - 通过
✅ test_session_schema.py           - 通过
```

---

# ⚙️ Heartbeat 集成

## 配置示例

```json
// examples/openclaw-heartbeat-config.md
{
  "enabled": true,
  "interval": "6h",
  "skill": "say-hi-to-me",
  "trigger": "proactive_scheduler"
}
```

## 集成步骤

1. 确保 `~/.openclaw/` 目录存在
2. 复制配置到 `~/.openclaw/config.jsonc`
3. 启用主动问候：`/hi 开`
4. 设置频率：`/hi 频率 <low|mid|high>`

---

# 🎯 使用提示

| 场景 | 建议 |
|------|------|
| 第一次用 | 先说 `/hi`，体验默认陪伴模式 |
| 想换人设 | 用 `/hi 角色 模板 luoshui` 快速切换 |
| 只想安静 | `/hi 暂停 24h`，给自己一点空间 |
| 睡前 | 设置 `/hi 免打扰 23:00-07:00` |
| 不知道怎么开始 | 直接说「今天心情不太好」 |

---

# 🔗 相关资源

| 资源 | 说明 |
|------|------|
| [OpenClaw 文档](https://github.com) | OpenClaw 平台文档 |
| [洛水角色模板](references/presets/luoshui-v1.yaml) | 内置人设模板 |
| [运行时核心](references/runtime-core.md) | 核心行为规范 |
| [安全策略](references/safety-policy.md) | 安全边界说明 |

---

<p align="center">

💜 Made with care by OpenClaw Skill System

</p>

---

# Say Hi to Me.skill

**An AI companion that actually cares.**

Sometimes you just want someone to ask how you're doing. Not to solve problems, just to listen. To remind you — you're still here today.

---

## ✨ Features

- **👋 Dual Entry** — `/hi` command or just talk naturally
- **🎭 Persona System** — Create, switch, and customize your digital companion
- **⏰ Proactive Check-ins** — Optional gentle greetings when you've been quiet (opt-in)
- **🔕 Quiet Hours** — Set boundaries for uninterrupted rest
- **🛡️ Safe Boundaries** — Warm but never clingy, present but respectful
- **🔗 Heartbeat Integration** — Scheduled greetings via OpenClaw Heartbeat
- **🌐 Bilingual** — Chinese-first with English support

---

## 🚀 Quick Start

### Step 1: Install

#### Via ClawHub (Recommended ⭐)

```bash
# 1. Install ClawHub (if not installed)
npm install -g clawhub

# 2. Install say-hi-to-me
clawhub install say-hi-to-me
```

#### Via GitHub

```bash
git clone https://github.com/JustZeroX/skill-say-hi-to-me.git ~/.openclaw/skills/say-hi-to-me
```

### Step 2: Say Hello

```bash
# Option 1: Use command
/hi

# Option 2: Just talk
Hey, how's it going?
```

### Step 3: Create a Persona (Optional)

```bash
# Quick template
/hi 角色 模板 luoshui

# Or describe your own
Create a gentle character who loves plants and pour-over coffee
```

### Step 4: Enable Proactive Greetings (Optional)

```bash
# Turn on
/hi 开

# Set frequency (low=24h, mid=12h, high=6h)
/hi 频率 中
```

---

## 📖 Examples

### Example 1: Daily Companion

```
User: /hi
Assistant: 👋 Hey! How's your day going?

User: Not bad, just a bit tired
Assistant: 💪 Hang in there! Maybe take a break and grab some water?

User: Yeah, gonna watch something to relax
Assistant: 🎬 Great idea! Pick something light and let yourself unwind～
```

### Example 2: Custom Persona

```
User: Create an anime-style character, she's a college student who loves drawing

Assistant: 🌸 Got it! Creating this persona...
     
     [Gentle Artist]
     Style: Anime
     Personality: Warm and attentive, expresses herself through art
     Interests: Drawing, anime, cafés
     
     Save this persona? Reply 「confirm」 to activate～
```

### Example 3: Scheduled Greetings

```
User: /hi 开
Assistant: ✅ Proactive greetings enabled! I'll check in gently when you've been quiet.

User: /hi 频率 高
Assistant: 📊 Set to high frequency (checks every 6 hours)

User: /hi 免打扰 23:00-08:00
Assistant: 🌙 Quiet hours set: 23:00-08:00. Sleep well!
```

---

## 💬 Commands

| Command | Description |
|---------|-------------|
| `/hi` | Start a conversation |
| `/hi 帮助` | Show all commands |
| `/hi 状态` | Check current settings |
| `/hi 开` | Enable proactive greetings |
| `/hi 关` | Disable proactive greetings |
| `/hi 频率 低\|中\|高` | Set check-in frequency |
| `/hi 免打扰 HH:MM-HH:MM` | Set quiet hours |
| `/hi 暂停 <duration>` | Pause (e.g. `30m`, `2h`, `1d`) |
| `/hi 角色 列表` | List all personas |
| `/hi 角色 切换 <name>` | Switch persona |
| `/hi 角色 新建 <prompt>` | Create new persona |
| `/hi 角色 模板 luoshui` | Use built-in template |

---

## 🧪 Testing

```bash
# Test daily conversation
python3 scripts/companion_runtime.py --text "你好" --json

# Test proactive scheduler
python3 scripts/proactive_scheduler.py --json

# Run full test suite
python3 -m unittest discover -s tests -p "test_*.py"
```
