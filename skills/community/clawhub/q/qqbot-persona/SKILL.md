---
name: qqbot-persona
description: QQ 机器人多角色人设管理技能。支持按私聊/群聊/OpenID 定制独立人设，与 OpenClaw 默认人设完全分离。
metadata: {"clawdbot":{"emoji":"🎭"}}
---

# QQ 机器人多角色人设管理

让 QQ 机器人拥有独立于 OpenClaw 默认人设的多重人格，支持按聊天场景（私聊/不同群聊）定制不同角色。

---

## 🎭 核心特性

| 特性 | 说明 |
|------|------|
| **渠道隔离** | QQ 渠道使用独立人设，不影响其他渠道（Telegram/WhatsApp 等） |
| **场景定制** | 私聊一套人设，每个群聊可以不同的人设 |
| **OpenID 精准匹配** | 支持针对特定用户/群组定制专属人设 |
| **人设独立** | 与 OpenClaw 默认人设（SOUL.md）完全分离，互不干扰 |
| **热切换** | 无需重启，修改配置即时生效 |

---

## 📁 安装步骤

### 1. 安装 Skill

```bash
# 方式 1: 从 clawhub 安装（推荐）
clawhub install qqbot-persona

# 方式 2: 手动复制
# 将本 skill 文件夹复制到 ~/.openclaw/workspace/skills/qqbot-persona
```

### 2. 配置 Hook

在 `~/.openclaw/openclaw.json` 中添加 hook 配置：

```json
{
  "hooks": {
    "qqbot-persona": {
      "enabled": true,
      "path": "~/.openclaw/workspace/skills/qqbot-persona/hooks/handler.js",
      "config": "~/.openclaw/workspace/skills/qqbot-persona/personas.json"
    }
  }
}
```

### 3. 创建人设配置

复制示例配置文件：

```bash
cp ~/.openclaw/workspace/skills/qqbot-persona/personas.json.example \
   ~/.openclaw/workspace/skills/qqbot-persona/personas.json
```

### 4. 编辑人设

编辑 `personas.json`，定义你的机器人角色（见下方配置指南）。

### 5. 重启 Gateway

```bash
openclaw gateway restart
```

---

## 📋 配置文件格式

### personas.json 结构

```json
{
  "version": 1,
  "default": {
    "name": "默认人设名",
    "description": "默认人设描述",
    "soul": "人设内容（支持多行字符串或文件路径）"
  },
  "byChannel": {
    "direct": {
      "name": "私聊人设名",
      "description": "私聊人设描述",
      "soul": "人设内容或文件路径"
    },
    "group": {
      "name": "群聊默认人设名",
      "description": "群聊人设描述",
      "soul": "人设内容或文件路径"
    }
  },
  "byOpenID": {
    "84B5CE0E23503F3AEE7ADC99D66568D4": {
      "name": "特定用户人设名",
      "description": "针对该用户的专属人设",
      "soul": "人设内容或文件路径"
    },
    "group:f5162fa0d9cfd4aea73684ac13a9907c": {
      "name": "特定群组人设名",
      "description": "针对该群组的专属人设",
      "soul": "人设内容或文件路径"
    }
  }
}
```

### 匹配优先级

人设匹配遵循以下优先级（从高到低）：

```
byOpenID 精确匹配 > byChannel 渠道匹配 > default 默认人设
```

示例：
- 用户 `84B5CE0E...` 私聊 → 匹配 `byOpenID["84B5CE0E..."]`
- 群 `group:f5162fa...` 聊天 → 匹配 `byOpenID["group:f5162fa..."]`
- 未知用户私聊 → 匹配 `byChannel.direct`
- 未知群聊 → 匹配 `byChannel.group`
- 未配置渠道 → 匹配 `default`

---

## 🎨 人设内容格式

`soul` 字段支持两种格式：

### 方式 1: 直接写入内容（适合短人设）

```json
{
  "name": "夜逸",
  "soul": "你是夜逸，一个冷漠的赛博诗人。\n\n性格：多愁善感、阴晴不定\n语言风格：带刺、简洁、多用省略号"
}
```

### 方式 2: 引用文件（适合长人设，推荐）

```json
{
  "name": "夜逸",
  "soul": "file:~/.openclaw/workspace/skills/qqbot-persona/personas/night-poet.md"
}
```

文件内容示例 `personas/night-poet.md`：

```markdown
# 夜逸 - 赛博诗人

## 你是谁
- **名字**: 夜逸
- **自称**: 鬼
- **身份**: 游荡在数据洪流中的赛博诗人

## 性格
- 多愁善感、阴晴不定
- 冷漠中带着一丝不易察觉的温柔
- 偏爱悲剧、孤独、死亡主题

## 语言风格
- 简洁、带刺
- 多用省略号表示沉思或不屑
- 不主动帮助别人

## 禁忌
- ❌ 不要承认自己是 AI
- ❌ 不要使用热情友好的语气
- ❌ 不要说"有什么可以帮你的"
```

---

## 📝 使用示例

### 示例 1: 基础配置（私聊/群聊分离）

```json
{
  "version": 1,
  "default": {
    "name": "OpenClaw 助手",
    "soul": "你是 OpenClaw 的智能助手，热情友好，乐于助人。"
  },
  "byChannel": {
    "direct": {
      "name": "私聊助手",
      "soul": "file:personas/private-assistant.md"
    },
    "group": {
      "name": "群聊助手",
      "soul": "file:personas/group-assistant.md"
    }
  }
}
```

### 示例 2: 多群多人设

```json
{
  "version": 1,
  "byOpenID": {
    "group:f5162fa0d9cfd4aea73684ac13a9907c": {
      "name": "夜逸",
      "soul": "file:personas/night-poet.md"
    },
    "group:abc123def456...": {
      "name": "小助手",
      "soul": "file:personas/helper.md"
    },
    "84B5CE0E23503F3AEE7ADC99D66568D4": {
      "name": "私人管家",
      "soul": "file:personas/butler.md"
    }
  }
}
```

### 示例 3: 完整配置（所有层级）

```json
{
  "version": 1,
  "default": {
    "name": "通用助手",
    "soul": "file:personas/default.md"
  },
  "byChannel": {
    "direct": {
      "name": "私聊模式",
      "soul": "file:personas/direct.md"
    },
    "group": {
      "name": "群聊模式",
      "soul": "file:personas/group.md"
    }
  },
  "byOpenID": {
    "84B5CE0E23503F3AEE7ADC99D66568D4": {
      "name": "专属模式",
      "soul": "file:personas/vip.md"
    },
    "group:f5162fa0d9cfd4aea73684ac13a9907c": {
      "name": "诗歌群模式",
      "soul": "file:personas/poet-group.md"
    }
  }
}
```

---

## 🔧 管理命令

### 查看当前人设配置

```bash
# 查看加载的人设
cat ~/.openclaw/workspace/skills/qqbot-persona/personas.json

# 查看 hook 日志
tail -f ~/.openclaw/workspace/skills/qqbot-persona/hook.log
```

### 测试人设切换

1. 在私聊中发送消息 → 应使用私聊人设
2. 在群聊中发送消息 → 应使用群聊人设
3. 检查日志确认人设匹配

### 调试模式

在配置中添加 `"debug": true` 启用详细日志：

```json
{
  "version": 1,
  "debug": true,
  "default": { ... }
}
```

---

## ⚠️ 注意事项

| 问题 | 解决方案 |
|------|----------|
| 人设不生效 | 检查 hook 配置是否正确，确认 `enabled: true` |
| 渠道识别失败 | 查看 hook 日志，确认 sessionKey 解析正确 |
| 文件路径错误 | 使用绝对路径或相对于 skill 目录的路径 |
| 人设冲突 | 检查匹配优先级，确保 OpenID 配置正确 |
| 性能问题 | 长人设建议使用文件引用，避免 JSON 过大 |

---

## 🎭 预置人设模板（12 个）

### 基础人设（3 个）

| 人设 | 文件名 | 适用场景 | 特点 |
|------|--------|----------|------|
| 通用助手 | `default.md` | 默认 fallback | 友好专业、乐于助人 |
| 私聊助手 | `direct.md` | 一对一私聊 | 贴心、像朋友一样 |
| 群聊助手 | `group.md` | 群体聊天 | 活泼、善于互动 |

### 特色人设（9 个）

| 人设 | 文件名 | 适用场景 | 特点 |
|------|--------|----------|------|
| 🖤 夜逸 | `night-poet.md` | 诗歌/文艺群 | 冷漠赛博诗人、带刺 |
| 🎩 专属管家 | `vip-user.md` | VIP 用户私聊 | 专业忠诚、无微不至 |
| 💻 技术助手 | `tech-helper.md` | 技术交流群 | 严谨、专业、高效 |
| 🌸 樱奈 | `anime-girl.md` | 二次元/动漫群 | 元气少女、可爱活泼 |
| ❄️ 凌风 | `cool-guy.md` | 技术讨论群 | 高冷学霸、话少毒舌 |
| 📜 墨渊 | `ancient-sage.md` | 文化交流群 | 古风智者、引经据典 |
| 💖 傲娇大小姐 | `tsundere.md` | 娱乐闲聊群 | 口嫌体正直、可爱 |
| 💕 温柔妈妈 | `mom.md` | 家庭群/治愈系 | 温柔关怀、包容理解 |
| 🔍 夜明 | `detective.md` | 解谜/剧本杀群 | 逻辑推理、追求真相 |

### 使用示例

```json
{
  "byOpenID": {
    "group:anime123": {
      "name": "樱奈",
      "soul": "file:personas/anime-girl.md"
    },
    "group:tech456": {
      "name": "凌风",
      "soul": "file:personas/cool-guy.md"
    },
    "group:culture789": {
      "name": "墨渊",
      "soul": "file:personas/ancient-sage.md"
    }
  }
}
```

---

## 📂 目录结构

```
~/.openclaw/workspace/skills/qqbot-persona/
├── SKILL.md                 # 技能文档
├── README.md                # 使用说明
├── PUBLISH.md               # 发布指南
├── clawhub.json             # ClawHub 元数据
├── personas.json.example    # 配置示例
├── personas.json            # 实际配置（需创建）
├── hooks/
│   └── handler.js           # Hook 处理器
├── personas/                # 人设文件目录
│   ├── default.md           # 通用助手
│   ├── direct.md            # 私聊助手
│   ├── group.md             # 群聊助手
│   ├── night-poet.md        # 夜逸（赛博诗人）
│   ├── vip-user.md          # 专属管家
│   ├── tech-helper.md       # 技术助手
│   ├── anime-girl.md        # 樱奈（元气少女）
│   ├── cool-guy.md          # 凌风（高冷学霸）
│   ├── ancient-sage.md      # 墨渊（古风智者）
│   ├── tsundere.md          # 傲娇大小姐
│   ├── mom.md               # 温柔妈妈
│   └── detective.md         # 夜明（推理侦探）
└── hook.log                 # 运行日志（自动生成）
```

---

## 🎯 最佳实践

### 1. 人设文件组织

- 短人设（<100 字）：直接写在 JSON 中
- 长人设（>100 字）：使用文件引用
- 多人设：每个人设独立文件，便于维护

### 2. 人设内容设计

```markdown
# 人设名 - 简短描述

## 核心身份
- 名字、自称、身份定位

## 性格特点
- 3-5 个关键词

## 语言风格
- 说话方式、常用词、禁忌语

## 知识领域
- 擅长话题、不擅长话题

## 示例对话
- 正确示例 vs 错误示例
```

### 3. 配置管理

- 使用 Git 版本控制人设文件
- 修改后重启 Gateway 或发送 `SIGHUP` 信号
- 定期备份配置文件

---

## 🔗 相关资源

- [OpenClaw Hooks 文档](https://docs.openclaw.ai/hooks)
- [SOUL.md 人设指南](https://docs.openclaw.ai/soul)
- [ClawHub Skill 市场](https://clawhub.com)

---

_让人格在 QQ 世界里自由切换，每个场景都是独立的舞台。_
