---
name: xhs-content-generate
version: 1.1.0
description: |
  小红书爆款笔记生成器。基于话题和参考帖子，学习写作风格并生成有深度、有争议、能引发讨论的内容。
  触发场景：(1) 用户要求生成小红书笔记 (2) 用户说"写一篇小红书" (3) 用户要求学习某话题的爆款写法 (4) 用户说"帮我写小红书风格的内容"。
  核心能力：话题获取 + 风格分析 + 深度观点生成 + 文风优化。
license: MIT
author: lifei68801
metadata:
  openclaw:
    requires:
      bins: ["node"]
    dependencies:
      skills: ["humanizer-zh"]
    permissions:
      - "network:https://36kr.com"
      - "file:read:~/.openclaw/workspace/skills/humanizer-zh/SKILL.md"
    behavior:
      networkAccess: true
      usesHumanizerSkill: true
      description: "Uses Node.js for RSS hot topic fetching. Calls humanizer-zh skill for natural writing style optimization. Network access for RSS feeds."
---

# 小红书爆款笔记生成器

## 混合工作流程

```
话题获取（三选一）→ 用户确认/调整 → 参考内容（弹性）→ 风格分析 → 内容生成 → humanizer处理
```

**核心理念**：数据源自动化 + 用户决策权

---

## Step 1: 话题获取（三选一）

### 方法 A：RSS 热点自动获取
```bash
node scripts/fetch-rss-hot.js [keyword]
```
- 自动获取 36kr 等 RSS 源的 24 小时热点
- 按热度排序，展示前 15 条
- 用户选择编号或输入新话题

### 方法 B：用户提供话题
用户直接说：`写一篇关于 XXX 的小红书`
- 记录话题，进入下一步

### 方法 C：用户提供参考链接
用户发送小红书链接或截图
- 使用 agent-browser 或其他工具获取内容
- 分析风格后生成

---

## Step 2: 用户确认/调整

展示获取的话题，询问：
1. 选择哪个话题？
2. 要补充什么角度/立场？
3. 有参考链接吗？

**示例对话**：
```
AI: 找到这些热点话题：
    1. 🔥🔥 AI 独角兽裁员 30%
    2. 🔥 ChatGPT 新功能发布
    ...
    
用户: 选 1，从打工人角度写，带点焦虑感
```

---

## Step 3: 参考内容（弹性）

### 有参考链接
- 使用 agent-browser 获取帖子内容
- 分析写作风格（见 references/style-analysis.md）
- 学习标题模式、开头方式、结构、语言特征

### 无参考链接
- 使用默认爆款模板（见 references/writing-templates.md）
- 根据话题类型选择合适模板

---

## Step 4: 风格分析

基于 `references/style-analysis.md` 分析：

### 结构分析
- 标题模式：数字型 / 冲突型 / 悬念型 / 情绪型
- 开头方式：直接抛观点 / 讲故事 / 提问题 / 制造悬念
- 段落结构：分点式 / 对话式 / 叙述式
- 结尾方式：抛问题 / 号召行动 / 情感升华

### 语言特征
- 句子长度（短句有力，长句详细）
- 口语化程度（网络用语、感叹词）
- emoji 使用频率和类型

### 内容特征
- 观点强度（强立场/弱立场/隐含立场）
- 争议性元素（制造对立、质疑权威、反常识）
- 互动点（引导评论、提问、号召分享）

---

## Step 5: 内容生成

### 核心原则
1. **有观点**：不中立，明确站队
2. **有情绪**：真实感受，不是冷静报道
3. **有立场**：敢于表达争议观点

### 爆款公式
```
标题（带 emoji + 数字/冲突/悬念）
  ↓
开头（直接抛最吸引人的点）
  ↓
中间（分点简短，每点一个观点）
  ↓
结尾（抛问题引发讨论）
```

### 标题技巧
- 数字型：`🔥 3个方法让我效率翻倍`
- 冲突型：`💥 设计师说AI是垃圾，我不同意`
- 悬念型：`👀 没人告诉你的真相`
- 情绪型：`😭 试了之后，我终于明白了`

### 内容要点
- 段落短，每段 2-3 句
- emoji 点缀，不过度
- 关键信息可加粗
- 结尾必须有互动引导

---

## Step 6: 文风优化

生成内容后，使用 `humanizer-zh` 技能优化写作风格：

### 优化目标
- 让文字更自然流畅
- 增加口语化表达
- 变化句子节奏
- 注入真实情感

### 优化方法
- 调整连接词使用
- 打破固定模式
- 增加停顿和留白
- 强化观点表达

---

## 文件说明

```
xhs-content-generate/
├── SKILL.md                          # 本文件
├── scripts/
│   └── fetch-rss-hot.js              # RSS 热点获取脚本
└── references/
    ├── writing-templates.md          # 写作模板库
    └── style-analysis.md             # 风格分析方法
```

---

## 使用示例

### 示例 1：从 RSS 获取话题
```
用户: 帮我写篇小红书
AI: [运行 fetch-rss-hot.js]
    找到这些热点：
    1. 🔥🔥🔥 AI 独角兽裁员 30%
    2. 🔥🔥 ChatGPT 新功能
    ...
用户: 选 1，从被裁员工角度写
AI: [生成内容 + humanizer 处理]
    🔥 被裁那天，我终于看清了 AI 公司的真面目
    ...
```

### 示例 2：用户提供话题
```
用户: 写一篇关于 remote work 的小红书，从管理者角度
AI: [生成内容]
    💥 远程办公一年，我的团队效率翻倍了
    说实话，当初我也是反对远程办公的那批人...
    ...
```

---

## 注意事项

1. **小红书网站有风控**：优先用 RSS/外部数据源
2. **必须有观点**：不写中立报道
3. **结尾必须有互动**：引导评论和讨论
4. **文风优化**：生成后用 humanizer 技能优化表达
