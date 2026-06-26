# Prompt Engineering Skills - 场景路由指南

本指南用于10个AI提示词工程场景的智能路由。

---

## 快速决策树

```
用户请求
    ↓
【判断场景类型】
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 视频生成？ → video-prompt-generator                            │
│ (Sora, Sora 2, Veo, Veo 3.1, Runway, Pika, 视频生成, 运镜)      │
├─────────────────────────────────────────────────────────────────┤
│ 图像生成？ → image-prompt-generator                            │
│ (Flux, Midjourney, MJ, Stable Diffusion, Nano Banana, 生图)    │
├─────────────────────────────────────────────────────────────────┤
│ AI编程？ → coding-prompt-assistant                              │
│ (Cursor, VS Code, Copilot, .cursorrules, TDD, 代码生成)         │
├─────────────────────────────────────────────────────────────────┤
│ 结构化提示词？ → json-prompt-architect                          │
│ (JSON, Schema, API对接, 批量生成, 结构化输出)                   │
├─────────────────────────────────────────────────────────────────┤
│ 数据分析？ → data-analyst-prompter                              │
│ (Python, Pandas, EDA, CSV, Excel, 代码执行, 数据可视化)         │
├─────────────────────────────────────────────────────────────────┤
│ 去AI味？ → humanizing-expert                                    │
│ (去AI味, 人性化, 避免AI腔, 风格克隆, 自然化重写)                 │
├─────────────────────────────────────────────────────────────────┤
│ 创意写作/角色扮演？ → creative-writing-coach                    │
│ (创意写作, 角色扮演, 模仿风格, 小说, 剧本, 文案)                 │
├─────────────────────────────────────────────────────────────────┤
│ 深度调研？ → research-agent                                     │
│ (调研, 深度研究, 行业分析, 竞品分析, 信源验证)                   │
├─────────────────────────────────────────────────────────────────┤
│ 实时语音/对话？ → voice-conversation-coach                      │
│ (语音对话, 实时语音, 雅思口语, 面试模拟, 辩论)                   │
├─────────────────────────────────────────────────────────────────┤
│ 长期运行/Agent？ → long-running-orchestrator                    │
│ (Agent, 智能体, 长期运行, 自动化, 工作流, LangGraph, n8n)        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 场景识别关键词

### 场景1：视频生成 (video-prompt-generator)

**触发关键词**：
- 英文：Sora, Sora 2, Veo, Veo 3.1, Runway, Pika, video generation, text-to-video, camera movement, motion, dynamics, timeline, time-lapse, slow motion
- 中文：视频生成, 文生视频, 运镜, 镜头运动, 动作描述, 动态场景, 延时, 慢动作

**示例请求**：
- "帮我写一个Sora 2的视频提示词"
- "生成赛博朋克武士拔刀的视频提示词"
- "怎么写Veo的视频prompt？"
- "Write a video prompt for Sora"

---

### 场景2：图像生成 (image-prompt-generator)

**触发关键词**：
- 英文：Flux, Midjourney, MJ, Stable Diffusion, SD, Nano Banana, image generation, text-to-image, inpainting, image editing, ID photo, product photo, style transfer
- 中文：图像生成, 文生图, 生图, 提示词抽卡, 图像编辑, 证件照, 白底图, 风格克隆

**示例请求**：
- "生成Flux的提示词"
- "帮我把这张图换成雪景背景"
- "写一个证件照的提示词"
- "Create an image prompt for Midjourney"

---

### 场景3：AI编程 (coding-prompt-assistant)

**触发关键词**：
- 英文：Cursor, VS Code, Copilot, AI coding, code generation, .cursorrules, system prompt, TDD, test-driven development, refactor, bug fix, code review, Plan-Review-Execute
- 中文：AI编程, 代码生成, 测试驱动, 重构, bug修复, 代码审查, 计划审查执行

**示例请求**：
- "帮我写.cursorrules"
- "生成登录页面的测试用例"
- "重构这个组件用Context API"
- "Write a .cursorrules file for my project"

---

### 场景4：结构化提示词 (json-prompt-architect)

**触发关键词**：
- 英文：JSON, structured output, Schema, API integration, workflow automation, batch generation, templated, structured prompt, JSON format
- 中文：结构化输出, API对接, 工作流自动化, 批量生成, 模板化, 结构化提示词

**示例请求**：
- "设计一个JSON提示词Schema"
- "帮我写结构化的视频提示词"
- "创建批量生成的JSON模板"
- "Design a JSON schema for structured prompts"

---

### 场景5：数据分析 (data-analyst-prompter)

**触发关键词**：
- 英文：data analysis, Python, Pandas, code execution, EDA, exploratory data analysis, data visualization, CSV, Excel, data cleaning, statistical analysis, trend analysis, code interpreter, data interpreter
- 中文：数据分析, 代码执行, 探索性数据分析, 数据可视化, 数据清洗, 统计分析, 趋势分析

**示例请求**：
- "分析这个CSV文件的销售数据"
- "用Python做EDA分析"
- "为什么销售额下降了？"
- "Analyze this CSV file's sales data"

---

### 场景6：去AI味 (humanizing-expert)

**触发关键词**：
- 英文：humanizing, naturalize, avoid AI tone, make text more natural, AI detection, remove AI traces, style cloning, human-like writing, natural rewrite
- 中文：去AI味, 人性化, 避免AI腔, 让文字更自然, 去除AI痕迹, 风格克隆, 像人写的

**示例请求**：
- "把这段AI文字改成更自然"
- "去除文章的AI味"
- "写一篇不像AI写的文章"
- "Make this text sound less AI-generated"

---

### 场景7：创意写作/角色扮演 (creative-writing-coach)

**触发关键词**：
- 英文：creative writing, roleplay, persona, imitate style, parody, style clone, fiction, script, copywriting, character, tone of voice, corpus samples
- 中文：创意写作, 角色扮演, 扮演, 模仿风格, 仿写, 风格克隆, 小说, 剧本, 文案, 人设, 口吻

**示例请求**：
- "模仿乔布斯的口吻写产品介绍"
- "扮演马斯克回答问题"
- "写一个悬疑小说开头"
- "Write in the style of Steve Jobs"

---

### 场景8：深度调研 (research-agent)

**触发关键词**：
- 英文：research, in-depth research, information gathering, industry analysis, competitive analysis, market research, source verification, traceability, critical analysis, academic research, paper analysis
- 中文：调研, 深度研究, 信息搜集, 行业分析, 竞品分析, 市场调研, 信源验证, 溯源, 批判性分析, 学术研究

**示例请求**：
- "调研2026年AI视频市场"
- "分析竞品的优缺点"
- "找关于这个主题的学术资料"
- "Research the AI video market in 2026"

---

### 场景9：实时语音/对话 (voice-conversation-coach)

**触发关键词**：
- 英文：voice conversation, real-time voice, Voice Mode, IELTS speaking, English practice, speaking practice, mock interview, debate, debate practice, conversation flow, turn-taking
- 中文：语音对话, 实时语音, 雅思口语, 英语练习, 口语陪练, 面试模拟, 模拟面试, 辩论, 辩论练习, 对话流

**示例请求**：
- "帮我练习英语口语"
- "模拟Google产品经理面试"
- "和我辩论AI是否取代程序员"
- "Help me practice English speaking"

---

### 场景10：长期运行/Agent (long-running-orchestrator)

**触发关键词**：
- 英文：Agent, autonomous agent, long-running, continuous task, automation, task monitoring, sentiment monitoring, automated operations, state persistence, resume, checkpoint, LangGraph, n8n, workflow
- 中文：智能体, 长期运行, 持续任务, 自动化, 任务监控, 舆情监控, 自动运营, 状态持久化, 断点续传, 工作流

**示例请求**：
- "设计一个长期运行的监控Agent"
- "创建自动化内容发布系统"
- "写一个能运行数天的任务脚本"
- "Design a long-running monitoring agent"

---

## 边界场景处理

### 跨场景请求

当用户请求涉及多个场景时：

**示例1**："调研AI视频市场并写报告"
- 主场景：research-agent（调研）
- 次场景：creative-writing-coach（写报告）
- 处理：先调用调研，结果传递给写作

**示例2**："用JSON格式写视频生成提示词"
- 主场景：json-prompt-architect（JSON格式）
- 次场景：video-prompt-generator（视频内容）
- 处理：以JSON架构为主，整合视频生成知识

### 不明确场景

当无法判断场景时：
```
您的请求涉及多个可能的场景：
A. [场景1描述]
B. [场景2描述]

请选择您需要的主要场景？
```

---

## Skill调用格式

Claude Code 会根据用户请求中的关键词自动识别并调用对应的 Skill。

**自动触发示例**：
- 用户说 "写 Sora 2 的提示词" → 自动调用 `video-prompt-generator`
- 用户说 "生成 Flux 的 prompt" → 自动调用 `image-prompt-generator`
- 用户说 "帮我写 .cursorrules" → 自动调用 `coding-prompt-assistant`

---

## 技能优化记录

### 2024-01-15: Description 优化
- 为所有 10 个 skills 的 description 添加了英文和中文触发关键词
- 提高了自动路由的准确性
- 添加了具体的工具名称和场景关键词
