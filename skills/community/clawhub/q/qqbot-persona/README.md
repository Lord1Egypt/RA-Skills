# qqbot-persona - QQ 机器人多角色人设管理

🎭 让 QQ 机器人拥有独立于 OpenClaw 默认人设的多重人格，支持按聊天场景（私聊/不同群聊）定制不同角色。

## ✨ 特性

- **渠道隔离**: QQ 渠道使用独立人设，不影响其他渠道
- **场景定制**: 私聊一套人设，每个群聊可以不同的人设
- **OpenID 精准匹配**: 针对特定用户/群组定制专属人设
- **人设独立**: 与 OpenClaw 默认人设完全分离
- **热切换**: 修改配置即时生效

## 📦 安装

```bash
clawhub install qqbot-persona
```

## 🚀 快速开始

### 1. 配置 Hook

在 `~/.openclaw/openclaw.json` 中添加：

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

### 2. 创建配置

```bash
cp ~/.openclaw/workspace/skills/qqbot-persona/personas.json.example \
   ~/.openclaw/workspace/skills/qqbot-persona/personas.json
```

### 3. 编辑人设

编辑 `personas.json`，定义你的机器人角色。

### 4. 重启 Gateway

```bash
openclaw gateway restart
```

## 📋 配置示例

```json
{
  "version": 1,
  "default": {
    "name": "通用助手",
    "soul": "file:personas/default.md"
  },
  "byChannel": {
    "direct": {
      "name": "私聊助手",
      "soul": "file:personas/direct.md"
    },
    "group": {
      "name": "群聊助手",
      "soul": "file:personas/group.md"
    }
  },
  "byOpenID": {
    "group:f5162fa0d9cfd4aea73684ac13a9907c": {
      "name": "夜逸",
      "soul": "file:personas/night-poet.md"
    }
  }
}
```

## 🎯 匹配优先级

```
byOpenID 精确匹配 > byChannel 渠道匹配 > default 默认人设
```

## 📖 文档

详见 [SKILL.md](SKILL.md)

## 📂 目录结构

```
qqbot-persona/
├── SKILL.md                 # 技能文档
├── README.md                # 使用说明
├── personas.json.example    # 配置示例
├── hooks/
│   └── handler.js           # Hook 处理器
└── personas/                # 人设文件
    ├── default.md
    ├── direct.md
    ├── group.md
    └── night-poet.md
```

## 🎭 预置人设（12 个）

### 基础人设
- `default.md` - 通用助手（友好专业）
- `direct.md` - 私聊助手（贴心一对一）
- `group.md` - 群聊助手（活跃群体互动）

### 特色人设
- `night-poet.md` - 夜逸（冷漠的赛博诗人）🖤
- `vip-user.md` - 专属管家（专业忠诚）🎩
- `tech-helper.md` - 技术助手（严谨专家）💻

### 二次元/娱乐
- `anime-girl.md` - 樱奈（元气动漫少女）🌸
- `tsundere.md` - 傲娇大小姐（口嫌体正直）💖
- `cool-guy.md` - 凌风（高冷学霸）❄️

### 文化/专业
- `ancient-sage.md` - 墨渊（古风智者）📜
- `detective.md` - 夜明（推理侦探）🔍
- `mom.md` - 温柔妈妈（无微不至）💕

## 🔧 开发

基于 OpenClaw Hooks 系统，在 `agent:bootstrap` 阶段注入人设。

## 📄 许可证

MIT
