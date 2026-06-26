# skill-isolator

为不同项目提供独立的技能配置和隔离管理。

## 功能特性

- ✅ **项目隔离** - 每个项目独立技能配置
- ✅ **多源支持** - clawhub / local / git / url
- ✅ **版本控制** - 支持锁定特定版本
- ✅ **自动同步** - 进入项目自动安装缺失技能
- ✅ **优先级解析** - 多源优先级配置
- ✅ **智能缓存** - 减少重复下载

## 快速开始

### 1. 创建配置

在项目根目录运行：

```bash
node scripts/init-project-config.js
```

或手动创建 `.openclaw-skills.json`：

```json
{
  "skills": ["feishu-doc", "weather"],
  "excludeGlobal": true
}
```

### 2. 同步技能

```bash
node scripts/sync-project-skills.js
```

### 3. 验证配置

```bash
node scripts/validate-config.js
```

## 目录结构

```
skill-isolator/
├── SKILL.md                      # 技能定义
├── README.md                     # 说明文档
├── package.json                  # 元数据
├── scripts/
│   ├── sync-project-skills.js    # 同步脚本
│   ├── validate-config.js        # 配置验证
│   └── init-project-config.js    # 初始化向导
└── references/
    ├── usage-guide.md            # 使用指南
    ├── tutorials.md              # 实战教程
    ├── faq.md                    # 常见问题
    ├── quick-reference.md        # 快速参考
    └── example-config.json       # 配置示例
```

## 使用方式

### 在聊天中

```
/skills status          # 查看状态
/skills sync            # 同步技能
/skills add <name>      # 添加技能
/skills remove <name>   # 移除技能
```

### 直接运行脚本

```bash
# 同步
node scripts/sync-project-skills.js [--force] [--verbose]

# 验证
node scripts/validate-config.js [config-path]

# 初始化配置
node scripts/init-project-config.js
```

## 配置示例

### 最小配置

```json
{
  "skills": ["feishu-doc"],
  "excludeGlobal": false
}
```

### 完整配置

```json
{
  "name": "my-project",
  "skills": [
    { "name": "feishu-doc", "version": "latest" },
    { "name": "weather", "version": "1.2.0" }
  ],
  "excludeGlobal": true,
  "sources": [
    { "name": "clawhub", "type": "registry", "priority": 1 },
    { "name": "local", "type": "filesystem", "paths": ["~/.openclaw/skills"], "priority": 2 }
  ],
  "cache": { "enabled": true, "ttlHours": 24 },
  "autoSync": { "onProjectEnter": true, "onSkillMissing": true }
}
```

## 学习资源

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| [tutorials.md](references/tutorials.md) | 5 个实战教程，从零开始 | 新手 🌱 |
| [usage-guide.md](references/usage-guide.md) | 详细使用指南和配置详解 | 进阶用户 📚 |
| [faq.md](references/faq.md) | 常见问题解答 | 所有人 ❓ |
| [quick-reference.md](references/quick-reference.md) | 快速参考卡片 | 快速查询 ⚡ |

## 故障排查

详见 [SKILL.md](SKILL.md) 的「故障排查」章节或 [faq.md](references/faq.md)。

## 许可证

MIT
