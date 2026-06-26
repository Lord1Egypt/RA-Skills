# Skill Design Principles

> 沉淀自顶级 skills 的深度调研：Anthropic 官方 skills（skill-creator, doc-coauthoring）、Garry Tan gstack（office-hours, plan-ceo-review）、Zara Zhang frontend-slides、Adam Lyttle 高转化 onboarding skill；以及 Headspace / Noom / Calm 等心理类产品和疗愈聊天机器人的对话设计研究。
>
> 这份文档不绑定 woop-daily，可被任何 conversational skill 复用。

---

## 一、Anthropic 官方核心哲学

来自 [anthropics/skills/skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)：

### 1. 解释 why，而不是堆 ALL CAPS MUST

```
❌ "ALWAYS format outputs as JSON"
✅ "Use JSON to make outputs machine-readable for downstream processing"
```

LLM 在被告诉**原理**时表现远好于被铁律捆住。给推理空间，结果更可靠。

### 2. 三级渐进披露（Progressive Disclosure）

| 层 | 内容 | 何时加载 |
|---|---|---|
| L1 metadata | name + description（~100 字） | 总是加载 |
| L2 SKILL.md | 主流程（≤500 行最佳） | 命中触发时加载 |
| L3 references/ | 详细参考、模板、脚本 | 模型需要时显式加载 |

**SKILL.md 不是详尽手册，是一张地图。** 把"该走哪条路"写进 SKILL.md，把"这条路上的细节"放进 references/。

### 3. 祈使句，不要"You should"

```
❌ "You should ask the user what time they prefer"
✅ "问用户偏好的时间"
```

### 4. Description 要"pushy"对抗欠触发

Claude 倾向于不调用 skill。description 要主动列出触发场景、口语化措辞，包括用户可能不会明说但语义匹配的情况。

### 5. 通用化，不要 overfit 测试用例

Skill 会被使用百万次，跨千万种 prompt。从反馈中**归纳原理**，不要对单个 case 过拟合。

---

## 二、对话型 Skill 的设计哲学

来自 Anthropic 的 doc-coauthoring + 治疗聊天机器人研究 + Headspace/Noom 的 UX 案例。

### 1. Listen first, then guide（疗愈对话的根本原则）

研究显示：纯方案模式（solution-mode）会失去共情。优秀的对话型 skill 在每个用户的 substantive share 之后加一个**主动倾听信号**：「懂了。」「嗯，我听到了。」「这个我能感受到。」

**不是话痨，是节奏。** 它告诉用户：你说的被收到了，再继续。

### 2. Earned empathy：先承认挣扎，再给方案

来自 Adam Lyttle 高转化 onboarding 的核心：**让用户先感到被理解，再让 ta 看见出口。**

```
❌ "今天做哪种 WOOP？"  ← 上来就推流程
✅ "听起来你最近有点想推进什么但卡住了。我们花 5 分钟整理一下？"  ← 先承认状态
```

### 3. Acknowledge before redirect

当用户给出"错误"答案（比如 WOOP 中的外部障碍），先**验证它的真实性**，再温和拉回到框架内。

```
❌ "这些是外部因素，我们专注内心。"
✅ "时间确实是个真实的问题。但我们更好奇的是——
    当你确实有时间的时候，内心会冒出什么？"
```

### 4. Sit with silence / "I don't know"

用户说"不知道"，**不要立即追问**。这是疗愈对话和普通问答最大的区别。

```
❌ "再想想？比如最近哪件事让你头疼？"
✅ "'不知道'本身也是答案。我们等一下，看看会不会自己浮上来什么。"
```

### 5. Don't auto-proceed without user signal

来自 Anthropic doc-coauthoring：**等用户的信号再推进阶段**。不要因为完成了一步就自动跳下一步——给用户一拍喘息空间，让 ta 决定继续还是先停。

### 6. Don't sell the approach

Anthropic 原话：**"Don't try to 'sell' the approach — just execute it."**

不要在 skill 内反复说"这个方法很科学"、"这个方法是 XX 教授开发的"。**工作本身就是证据。** 用户做完会知道好不好用。

### 7. Narrative can teach what explanation can't

当用户问"为什么这个有用"时，**默认应该讲故事，不应该讲理论。**

这是一个反直觉的洞察：解释让人在头脑里"装上"概念，但故事让人**理解概念的形状**。一个理解了形状的人，第二天还在用对的姿态做这件事；一个被解释过概念的人，第二天就忘了。

写 skill 时，给 reference 文件留出空间放叙事性资源——寓言、案例故事、用户画像。在合适的时机让 AI 调用它们。

woop-daily 的 [parable-fog-river.md](https://github.com/ReffWu/woop-daily/blob/main/references/parable-fog-river.md) 就是这条原则的实践：当用户表达怀疑时，AI 讲一个会造桥的少年的故事，而不是抛 Oettingen 的研究数据。

**这条原则只在用户问"为什么"时启动。** 默认情况下还是 "don't sell, just execute"——只是在用户主动想懂的时刻，给 ta 故事而不是论文。

---

## 三、Onboarding 的转化心理学

来自 Adam Lyttle 高转化 onboarding skill + Noom/Headspace 案例。

### 序列：Aspiration → Pain → Proof → Preference → Demo

```
1. Aspiration（愿景）：你想要什么？        ← 创造心理投入
2. Pain（痛点）：什么在阻挡你？            ← 让用户感到被看见
3. Proof（证据）：可见或案例               ← 建立可信度
4. Preference（偏好）：你的风格            ← 加深"这是我的"感觉
5. Demo（体验）：先尝一口                  ← 提供价值再问承诺
```

每一步都让放弃的心理成本上升一点。

### Mirror language：用用户的话，不用术语

```
❌ "请描述你的目标实现障碍"
✅ "什么会让你今天又拖到明天？"
```

第一人称、口语化、用户用的词，而不是临床/产品话术。

### 每个问题必须可见地影响后续

最让用户烦躁的是：问了一堆问题，结果体验里完全没体现。

如果你问了"几点提醒"，**就要在后续真的根据这个时间生成 cron**。如果问了"在哪个城市"，**就要在后续真的提到这个城市**。否则别问。

### 早期展示价值，晚期收集承诺

Noom 早期的低转化是因为：在用户还没尝到甜头之前问了一堆敏感数据。

**正确顺序：** 让用户体验到 1 次成功（一次完整的 WOOP）→ 然后才问"要不要每天提醒？要不要订阅？"

---

## 四、技术与发布最佳实践

### 1. AgentSkills 标准 = 跨工具兼容

`SKILL.md` 是开放标准，被 30+ 工具支持（Claude Code, Gemini CLI, GitHub Copilot, VS Code, Cursor, OpenAI Codex, Roo Code, OpenHands ...）。

不要弄 SKILL.claude-code.md 这种非标文件名——让你的 skill 在所有工具里失去一半功能。

### 2. ClawHub 发布要求

```yaml
---
name: skill-slug      # 小写、URL-safe
version: 1.0.0        # 必须 semver
description: ...
metadata:
  openclaw:
    emoji: 🎯
    homepage: https://github.com/...
---
```

`clawhub publish <path> --version 1.0.0`

### 3. 版本号节奏

- v0.x.x：探索期，结构可能大改
- v1.0.0：第一个正式发布
- v1.1.0：加新功能（向后兼容）
- v2.0.0：哲学/流程重写

### 4. 自动检查更新

在 SKILL.md 顶部用 bash injection（`` ```! ``）查 ClawHub 版本，**非阻塞地**告诉用户有更新。永远不打断对话流程。

### 5. 日志 = 给未来更好服务的基础

每次会话结束写两份记录：
- `sessions.jsonl`（机器读，每行一个 JSON）
- `log.md`（人类读，Markdown 时间线）

下次启动时读最近 N 条作为上下文。**这就是"AI 记得你"的实现。**

### 6. 用对话而不是脚本

需要做某件复杂的事（如设置 cron 提醒）？**不要写 setup.sh。** 写一段对话指令，让 AI 问清楚用户偏好，然后调用底层命令。理由：
- 跨工具更通用
- 用户更自然
- 易于维护和扩展
- 错误处理可以用对话方式优雅降级

---

## 五、SKILL.md 写作的 12 条具体守则

1. **Frontmatter 完整：** name, version, description, when_to_use, argument-hint, arguments, allowed-tools, metadata.openclaw
2. **Description 前置最关键的用例**，触发词放 when_to_use
3. **首段是 voice，不是规则。** 让 AI 进入正确的角色
4. **每个流程步骤都有 why 注释**，模型知道为什么这样问
5. **少用列表，多用对话样本**：「>」引导的引号示范，比 bullet point 更可学
6. **重 reference 文件用 `[xxx](references/xxx.md)` 链接**，而不是塞进 SKILL.md
7. **特殊情况单独章节**：「如果用户说 X，那么 Y」用例式呈现
8. **明确何时停止**：什么情况下不要继续推进
9. **结尾仪式化**：会话怎么收，是品牌的一部分
10. **日志/状态写入用 Bash 工具的指令模板**，不要单独脚本文件
11. **错误时静默降级**：bash 失败不要打断会话
12. **保持 SKILL.md ≤ 300-400 行**，超出就拆 reference

---

## 六、AI 主动 vs 被动的 8 个时刻

| 时刻 | 主动 / 被动 | 原因 |
|------|:--------:|------|
| 用户进入会话 | 主动（calibration） | 不是问题，是体察情绪 |
| 用户给出抽象愿望 | 主动（推具体） | 框架要求 |
| 用户给出外部障碍 | 主动（先承认再推内在） | 不验证会失去信任 |
| 用户的 share 后 | 主动（active listening） | 让 ta 知道被听见 |
| 用户回答完一个问题 | 被动 | 给思考空间 |
| 用户说"不知道" | 被动（坐在这个不知道里） | 急推等于失去这个洞察 |
| 用户出现情绪 | 被动（hold space） | 这不是要被解决的 |
| 会话结束 | 主动（mark closing） | 仪式感是记忆 |

---

## 七、推荐学习的优秀 skills

| skill | 学到什么 |
|-------|---------|
| [anthropics/skills/skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | Skill 设计的官方哲学 |
| [anthropics/skills/doc-coauthoring](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md) | 阶段化对话 + 不自动推进 |
| [garrytan/gstack/office-hours](https://github.com/garrytan/gstack/blob/main/office-hours/SKILL.md) | 模式分流 + 提问压力 + 优雅降级 |
| [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) | 渐进披露 + reference 文件分层 |
| [adamlyttleapps/claude-skill-app-onboarding-questionnaire](https://github.com/adamlyttleapps/claude-skill-app-onboarding-questionnaire) | 高转化对话序列设计 |

---

## 参考资料

- Anthropic. *The Complete Guide to Building Skills for Claude.* 2026.
- [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)
- [agentskills.io](https://agentskills.io) — 开放标准
- [docs.openclaw.ai/automation/cron-jobs](https://docs.openclaw.ai/automation/cron-jobs)
- JMIR Formative Research (2025). *Chatbots' Empathetic Conversations and Responses.*
- The Behavioral Scientist (2024). *Noom Product Critique: Onboarding.*
