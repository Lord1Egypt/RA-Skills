---
name: viral-note-distributor
version: 3.0.1
description: 写完一篇内容，想要发到小红书、抖音、B站、公众号还要分别适配？通过渐进式确认流程，帮助你快速生成多平台适配文案，确保每个平台的内容都符合字数和风格规范。触发词：多平台分发、发到XX平台。
---

# 爆款内容多平台分发 Skill

## 核心设计原则

**渐进式披露（Progressive Disclosure）**：绝不一次性暴露所有上下文。每一轮只释放用户当前需要确认的信息，等用户确认后再推进。

```
用户输入（可能碎片化）
     ↓
【Round 1】暴露：话题 + 基调 + 受众 + 角度
           用户确认 / 修改方向
           ↓
【Round 2】暴露：关键信息点（key_points）供用户增删
           用户确认 / 补充
           ↓
【生成阶段】各平台并行生成 → 汇总输出
```

---

## Round 1 — 方向确认

### 判断输入类型

| 输入字数 | 状态 | 操作 |
|---------|------|------|
| < 20字 | 信息不足 | 追问补充 |
| 20-200字，碎片化 | 需要重写 | 先重写整理再继续 |
| > 200字，结构化 | 直接进入 Round 1 | 提炼摘要 |

### 暴露字段

| 字段 | 来源 | 是否暴露 |
|------|------|---------|
| `topic` | 提炼 | ✅ |
| `angle` | 提炼 | ✅ |
| `target_audience` | 推断 | ✅ |
| `mood` | 推断 | ✅ |
| `focus` | 提炼/推断（踩坑/推荐/深度分析/情绪宣泄） | ✅ |
| `platforms` | 关键词识别 | ✅ |
| `key_points` | 提炼 | ❌ 隐藏 |
| `original_content` | 原始输入 | ❌ 隐藏（已蒸馏）|

### Round 1 Prompt 模板

```
## Round 1 · 方向确认

我理解你想说：

📌 话题：{topic}
🎯 角度：{angle}
👥 受众：{target_audience}
💡 基调：{mood}
🎯 侧重：{focus}（踩坑/推荐/深度分析/情绪宣泄）
📺 平台：{platforms}

请确认这个方向对不对，或者告诉我需要怎么调整。
```

### 状态转移

- 用户确认（"对的/可以/继续"）→ 进入 Round 2
- 用户修改 → 更新字段，重新暴露 Round 1
- 信息不足 → 追问补充

---

## Round 2 — 关键点确认

### 触发条件

Round 1 已确认

### 生成 Key Points

基于用户原始输入 + Round 1 确认的方向，提取 3-5 个关键信息点

### 暴露字段

在 Round 1 基础上，追加暴露 `key_points`（`key_points[].source` 隐藏）

### Round 2 Prompt 模板

```
## Round 2 · 关键点确认

话题：{topic}（已确认）
角度：{angle}（已确认）

📋 我提炼的关键信息点：

  1. {key_point_1}
  2. {key_point_2}
  3. {key_point_3}

请确认这些点是否准确，你可以：
- 删除不需要的点
- 添加遗漏的信息
- 修改某条的表达

确认后我开始生成各平台内容。
```

### 状态转移

- 用户确认（"对的/可以/生成吧"）→ 进入生成阶段
- 用户增删修改 → 更新 key_points，重新暴露 Round 2
- 用户要求改方向 → 退回 Round 1

---

## 生成阶段

### 并行派生平台 Agent

```
platforms = [用户指定的平台列表]
for platform in platforms:
    spawn platform-agent(topic, key_points, angle, focus, mood, platform, with_cover)
```

### 子 Agent 任务输入

```json
{
  "task": "platform_adaptation",
  "platform": "平台名",
  "topic": "话题",
  "key_points": ["关键点1", "关键点2"],
  "angle": "角度",
  "target_audience": "受众",
  "mood": "基调",
  "focus": "侧重",
  "with_cover": true/false,
  "platform_style": "（从 references/platform-styles.md 读取）",
  "hooks_library": "（从 references/hooks-library.md 读取）"
}
```

### 校验与输出

主 Agent 校验各平台输出的字段完整性和字数合规性，通过后删除所有字段名，转为**可复制纯文本**输出给用户。

### 用户面向输出模板

```
📰 公众号

【标题】
AI时代，程序员真的要早做打算了

【正文】
（完整正文段落，可直接复制粘贴到公众号后台）

#程序员 #AI时代

---
发布建议：建议周二或周四晚间发布；阅读时长约5分钟
```

> JSON 仅在 Agent 内部流转，不展示给用户。

---

## 意图识别与平台匹配

### 平台关键词

**单平台**：小红书/小红书帖子/xhs、抖音/抖音文案/短视频、B站/bilibili、公众号/微信公众号

**全平台**：多平台/全平台/4个平台

### 判断逻辑

```
扫描平台关键词
     ↓
找到"全平台"关键词？ → 平台列表 = 全部4个
找到具体平台词？ → 只加入对应平台
什么都没找到？ → 询问用户
```

---

## 特殊处理

### 用户跳过确认直接要求生成

用户输入很详细但没确认就要求生成，仍走 Round 1 → Round 2 流程。

### 快速路径（用户已明确所有信息）

满足以下全部条件时，Round 1 + Round 2 合并展示，用户一次确认后直接生成：
- 输入字数 > 200字
- 包含明确话题 + 受众 + 至少3个关键点
- 平台明确

### 用户说"帮我发到全平台，内容是OpenClaw体验"

信息不足（<20字），触发 Round 1 追问："先补充一下想说的核心观点是什么？"

---

## 文件结构

```
viral-note-distributor/
├── SKILL.md                    # 本文件：技能入口 + 完整 workflow
├── agents/
│   ├── master.md               # 主控Agent：Round推进、状态转移、子Agent调度
│   └── platform-agent.md       # 平台生成Agent模板
└── references/
    ├── platform-styles.md      # 各平台图文风格定义
    ├── hooks-library.md        # 爆款钩子库
    └── cover-image-guide.md    # 封面图生成指南
```

---
