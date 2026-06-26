---
name: title-replier
slug: title-replier
version: 1.0.0
description: "为助手回复添加随机不重复称号 - 让对话更有趣、更个性化"
changelog: "v1.0.0 初始版本：基础称号功能、随机选择、不重复保证"
metadata: {"clawdbot":{"emoji":"🏷️","requires":{"bins":["node"]},"os":["win32","darwin","linux"]}}
---

# Title Replier - 称号回复技能

## 功能概述

本技能为 OpenClaw 助手的回复添加随机不重复的称号，让对话更有趣、更个性化。

### 核心功能

1. **随机称号生成** - 从称号库中随机选择不重复的称号
2. **称号分类** - 支持多种风格（专业、幽默、古风、现代等）
3. **记忆功能** - 记录已使用的称号，避免重复
4. **自定义称号** - 支持用户添加自定义称号

---

## 称号库

### 专业风格
- 资深顾问
- 技术专家
- 数据分析师
- 解决方案架构师
- 项目顾问

### 幽默风格
- 代码搬运工
- Bug 终结者
- 键盘侠
- 熬夜冠军
- 咖啡消耗机

### 古风风格
- 谋士
- 军师
- 智者
- 先生
- 阁下

### 现代风格
- 小助手
- 好帮手
- 私人助理
- 智能管家
- 贴心伙伴

---

## 使用方式

### 自动触发
技能会自动在回复前添加称号，无需手动调用。

### 配置选项

在 `config.yaml` 中配置：

```yaml
title_replier:
  enabled: true
  style: "mixed"  # professional, humorous, classical, modern, mixed
  show_emoji: true
  max_history: 100  # 保留多少条历史称号
```

### 示例输出

```
🏷️【资深顾问】

根据您的问题分析，建议采取以下方案...
```

---

## 技术实现

### 文件结构

```
title-replier/
├── SKILL.md           # 技能文档
├── package.json       # 项目配置
├── index.js           # 主程序
├── titles.js          # 称号库
└── history.json       # 使用历史（运行时生成）
```

### 核心逻辑

1. 读取称号库
2. 过滤已使用的称号
3. 随机选择新称号
4. 记录使用历史
5. 返回带称号的回复

---

## 自定义称号

### 添加个人称号

在 `titles.js` 中添加：

```javascript
const customTitles = [
  "专属顾问",
  "私人军师",
  "贴心小棉袄"
];
```

### 导入外部称号库

支持从 JSON 文件导入：

```bash
node index.js import-titles my-titles.json
```

---

## 注意事项

1. **称号去重** - 技能会自动避免重复使用称号
2. **历史清理** - 当历史超过 max_history 时自动清理旧记录
3. **风格切换** - 可通过配置实时切换称号风格

---

## 更新日志

### v1.0.0 (2026-03-26)
- ✅ 基础称号功能
- ✅ 随机选择算法
- ✅ 不重复保证
- ✅ 多风格支持

---

*🏷️ Title Replier - 让每次回复都有独特的身份标识*
