---
name: "vibe-coding-learning"
description: |
  Generate structured learning notes from AI coding sessions. Invoke when user completes a coding task with AI and asks to summarize learning, explain code, extract knowledge points, review previous notes, or check learning progress.
  Also trigger on Chinese phrases: "总结今天学的", "帮我整理学习笔记", "帮我复习", "这段代码讲一下", "我学了多少了", "学习进度怎么样", "准备面试", "模拟面试", "帮我讲一下这段代码", "今天学了什么", "帮我记一下", "这段代码我不太懂"
license: MIT
metadata:
  author: lyqqqq66666
  version: "1.2.0"
  tags: [learning, education, cs-students, coding-notes, vibe-coding]
  compatible-tools: [workbuddy, claude-code, openclaw, codex, trae]
---

# Vibe Coding Learning

> **"You can outsource your thinking, but not your understanding."** — Andrej Karpathy
>
> 把 AI 生成的代码变回你真正理解的知识。详见 `references/vibe-coding-origin.md`。

Transform AI coding sessions into structured learning notes. Help CS students actually learn from vibe coding instead of just generating code.

## Use this skill when

- User just completed a coding task with AI and wants a learning summary
- User says "summarize today's learning", "explain this code", "extract knowledge points"
- User says "help me review", "what did I learn before", "review yesterday's notes"
- User says "learning progress", "what should I learn next", "learning calendar"
- User says "prepare for interview", "面试怎么讲", "帮我准备面试", "模拟面试"
- User references "vibe coding learning", "learning note", "knowledge card"

## Do NOT use this skill when

- User is still in the middle of coding and has NOT asked for a summary
  > 反例："帮我在这个函数里加个 try-catch"（用户还在写代码，不是在总结学习）
- User only wants code review, bug fixing, or refactoring without learning context
  > 反例："review 一下我的 PR"（纯代码审查，不涉及学习总结）
- User asks about non-programming topics
  > 反例："今天天气怎么样"（与编程学习无关）
- User only wants formatting / renaming without understanding intent
  > 反例："帮我把变量名改成驼峰命名"（纯格式化，无学习价值）
- The coding session is trivial (e.g., only changed a CSS color, single-line fix)
  > 反例：只改了一行颜色值，无需生成学习笔记

## 执行策略 (Execution Strategy)

Skill 启动后先判断执行模式，而非无差别全量执行。

### 双模式路由

根据用户意图和上下文充分度自动选择：

| 判断维度 | Auto 直出 | Collaborative 协作 |
|---------|----------|-------------------|
| 用户表达 | 明确具体（"总结今天 FastAPI 的登录代码"） | 模糊宽泛（"帮我整理学习笔记"） |
| 上下文 | 代码变更清晰，学习目标自明 | 多项目混杂，不确定聚焦哪个 |
| 行为 | 静默执行全流程，直接输出结果 | 关键节点确认，最多 3 个问题后执行 |
| 用户体验 | 快，一次性输出 | 节奏可控，可中途纠偏 |

### 意图识别 → 模式映射

详细路由规则见 `references/mode-routing.md`（包括意图标签定义、模式选择矩阵、最小提问规则）。

**快速参考**：

| 意图标签 | 触发示例 | 默认模式 |
|---------|---------|---------|
| `quick_summary` | "总结今天学的" | Mode 1 Auto |
| `guided_learning` | "这段代码讲一下" | Mode 1 Collaborative |
| `review_recall` | "复习昨天的" | Mode 2 Auto |
| `progress_check` | "我学了多少了" | Mode 3 Auto |
| `interview_prep` | "帮我准备面试" | Mode 4 Collaborative |
| `prompt_review` | "我的提示词怎么样" | Mode 5 Collaborative |
| `inbox_triage` | "有什么没整理的笔记吗" | Mode 6 Collaborative |
| `connection_review` | "今天学的和之前有什么关联" | Mode 7 Auto |
| `weekly_synthesis` | "周总结"、"生成本周学习报告" | Mode 8 Auto |
| `health_check` | "检查学习健康度"、"我有没有忘记复习的" | Mode 9 Auto |
| `ambiguous` | "学习笔记" | Collaborative，先澄清意图 |

### 最小提问规则

协作模式下有提问需求时，遵守以下纪律（详见 `references/mode-routing.md`）：

1. **容量上限**：每次交互最多 3 个关键问题
2. **可推断不提问**：能从上下文推断的信息，直接采纳
3. **给出默认值**：需要选择时先给推荐方案
4. **用户说"直接做"→ 切 Auto**
5. **默认方案兜底**：用户回复模糊时按推荐方案执行

## Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `coding_context` | string | Yes | What the user built with AI in this session |
| `changed_files` | list | Auto-detected | Files created or modified (scan project if not provided) |
| `preferred_format` | string | No | `md` (default) or `html` |
| `output_dir` | string | No | Directory to save notes (default: `learning-notes/`) |

## Output

| Artifact | Format | Description |
|----------|--------|-------------|
| Daily learning note | Markdown/HTML | Structured note with knowledge points, code explanation, pitfalls |
| Knowledge point cards | Markdown | Reusable cards for each extracted concept |
| Calendar entry | Markdown | Entry appended to monthly learning calendar |
| Progress update | Markdown | Updated progress overview |

## Workflow

### Mode 1: Generate Learning Note (after coding session)

**执行前 — 确定执行深度**

读取 `config.yaml` 中的 `learning.depth` 字段，确定本次执行深度：

| 深度 | 取值 | 执行范围 | 适用场景 | 预计 token |
|-------|------|---------|---------|------------|
| 轻量 | `light` | Phase 1-2（仅知识点+卡片） | 短会话、简单代码、快速记录 | ~2K |
| 标准 | `standard` | Phase 1-4（含笔记+陷阱，不含资源搜索） | 日常学习（默认） | ~5K |
| 深度 | `deep` | 全量 Phase 1-5 | 复杂项目、面试准备、复盘 | ~10K |

**自动判断逻辑**（当 `depth` 未设置或设为 `auto` 时）：
- 运行 `python3 scripts/analyze-session.py --quick` 分析本次会话复杂度
- 脚本输出 `light` / `standard` / `deep` 建议，按建议执行
- 脚本逻辑：代码变更 < 50 行 → light；50-200 行 → standard；> 200 行或跨多个文件 → deep

**深度覆盖**：用户可在对话中直接说"轻量模式"、"详细一点"来临时覆盖配置。

---

### Phase 1/5: 采集与识别 [所有深度均执行]

> 进度输出（仅 standard/deep 模式）: "正在分析你的代码结构..."

**Step 1 — Collect Context**
- Scan the project directory to identify files created or modified during this session
- If user provided `coding_context`, use it as the primary description
- Read the key source files to understand what was built
- **文件覆盖度硬性规则**：
  - 必须 Read ALL changed files（变更集中 ≥ 80% 的文件都要读）
  - 还必须 Read 被 changed files import/call 的关联文件（如 api.py import 了 state.py，则 state.py 也必须读）
  - import 链追踪：至少追踪一层（A import B → 必须读 B）
  - 覆盖度不达标时在自检清单中标注 `[自检：文件覆盖度不足，仅读了 X/Y 个文件]`

**Step 2 — Identify Technical Domain and Stack**
- Analyze the code to determine which domain(s) and tech stack(s) it belongs to:
  - **Domains**: backend, frontend, devops, ai-ml, mobile, data-engineering, security, testing, cloud
  - **Stacks** (examples): fastapi, django, express, react, vue, vanilla-js, docker, kubernetes, langchain, pytorch
- A session may span multiple domains and stacks

---

### Phase 2/5: 提炼与解读 [light 仅输出知识点列表；standard/deep 输出完整解读]

> 进度输出（仅 standard/deep 模式）: "已识别技术领域，正在提炼知识点..."

**Step 3 — Extract Knowledge Points** [所有深度均执行]
- From the code changes, identify 3-8 concrete knowledge points
- For each knowledge point, define:
  - Name (e.g., "JWT Authentication", "React useState Hook")
  - One-sentence definition
  - Core concept / how it works
  - Which file and line range implements it
  - Common mistakes / pitfalls
- Knowledge points should be things a CS student would encounter in coursework or interviews
- **light 模式**：到此为止，直接输出知识点列表 + 知识卡片，跳过 Step 4-8

**Step 4 — Write Code Explanation** [standard/deep 执行]
- Determine the recommended reading order (which file first, which function first)
- For each key file, write:
  - What this file does in plain language
  - Line-by-line or section-by-section explanation
  - Why it's designed this way (not just what it does). Answer: "为什么这里用这种结构而不是另一种？如果有替代方案，是什么？"
  - What design pattern it uses (if any). For each pattern found, also explain what the code would look like without it
  - **[deep 模式才输出]** **How to write it from scratch without AI**: step-by-step reconstruction guide

---

### Phase 3/5: 陷阱与资源 [仅 standard/deep 执行；资源搜索仅 deep]

> 进度输出（仅 deep 模式）: "知识点已提取，正在整理常见陷阱..."

**Step 5 — Compile Pitfalls** [standard/deep 执行]
- List 3-5 common mistakes for this domain
- Format: table with columns [Pitfall, Correct Approach, Common Mistake]
- Base this on both the code analysis and general domain knowledge

**Step 6 — Recommend Learning Resources** [仅 deep 执行]
- **Attempt WebSearch first** to find relevant tutorials for each knowledge point
- Search queries: "[knowledge point] tutorial bilibili", "[knowledge point] official documentation"
- Prioritize: Bilibili video tutorials, official docs, well-known tech blogs
- Provide 1-3 resources per knowledge point with title and URL
- **If WebSearch is unavailable or fails**: mark the section explicitly as `（基于通用知识推荐，非实时搜索结果）` and skip URL links — never fabricate search results

---

### Phase 4/5: 更新与归档 [standard/deep 执行]

> 进度输出（仅 deep 模式）: "正在更新学习日历和目录结构..."

**Step 7 — Update Learning Calendar and Progress** [standard/deep 执行]
- Check if `learning-notes/calendar/YYYY-MM.md` exists. If not, create it.
- Append today's entry to the calendar:
  ```
  | YYYY-MM-DD | [domain] | [keywords] | [link to note] |
  ```
- Check if `learning-notes/progress.md` exists. If not, create it.
- Update domain progress bars and statistics. Use four mastery levels: 🟢🟢 teachable / 🟢 mastered / 🟡 understood / 🔴 exposed
- After updating, the progress.md should show per-domain breakdown with mastery ratios

**Step 8 — Save to Three-Layer Structure** [standard/deep 执行]

Save outputs to the appropriate locations in the three-layer directory structure.

**每个笔记文件必须包含 YAML frontmatter**（M1 Step 2 已识别 domain/stack，保存时自动设 `status: processed`）：

```markdown
---
title: "[笔记标题]"
date: YYYY-MM-DD
domain: [backend/frontend/...]
stack: [fastapi/react/...]
status: processed          # 自动设置，无需用户确认
last_review_date: null
review_count: 0
mastery_level: "🔴 exposed"   # 初次创建默认 exposed；四级体系：🔴 exposed / 🟡 understood / 🟢 mastered / 🟢🟢 teachable
tags: [tag1, tag2]
---
```

1. **topics/** — Save the daily learning note
   - Create a project-specific folder: `topics/[project-name]/`
   - Save note as: `topics/[project-name]/YYYY-MM-DD-[title].md`
   - Example: `topics/fastapi-login-register/2026-06-11-fastapi-login-register.md`
   - **必须包含上方 frontmatter**

2. **domains/** — Update the domain and stack indexes (MANDATORY — do NOT skip)
   - Determine the domain (e.g., `backend`) and stack (e.g., `fastapi`)
   - Create or update `domains/[domain]/_index.md` with knowledge checklist
   - Create or update `domains/[domain]/[stack]/_index.md` with stack-specific notes
   - Link back to the topic note from the domain index
   - After writing, verify: check that the domain index file exists and contains today's knowledge points

3. **cards/** — Save extracted knowledge point cards
   - Determine the card category (e.g., `auth`, `css`, `js`, `python`)
   - Create the category folder if it doesn't exist: `cards/[category]/`
   - Save each card as: `cards/[category]/[kebab-case-name].md`
   - Example: `cards/auth/jwt.md`, `cards/css/flexbox.md`
   - Cards should be self-contained and reusable across any project
   - Cards should also include frontmatter with `status: processed`

### Phase 5/5: 最终产出

> 进度输出: "正在生成学习笔记，马上就好..."

**Step 9 — Generate Output Files**
- Generate the daily learning note following the template at `templates/daily-learning-note.md`
- Save to the appropriate topic folder
- If `preferred_format` is `html`, generate an HTML version using the html-report skill

**Step 10 — 费曼自评** [仅 standard/deep 模式，当 `config.yaml` 的 `feynman_enabled: true` 时]

> 形成"提取 → 整理 → 自评 → 调整"闭环。详见 `references/feynman-assessment.md`。

1. 列出刚才提取的所有知识点，问用户："哪个知识点你最不熟悉？"
2. 根据回答调整 mastery_level：
   - 用户说"第 X 个最陌生" → 降级为 `🔴 exposed`
   - 用户说"第 X 个我能给别人讲" → 升级为 `🟢🟢 teachable`
   - 用户说"全部熟悉" → 保持原 mastery_level，跳过
3. 根据自评结果给出后续分流建议（如"建议对 🔴 知识点做 Mode 2 互动复习"）

**deep 模式两步流** [仅 deep 模式执行]

- **Step 10A** — 先生成简版 session log（当日学习日志）：
  ```markdown
  ## Session Log — YYYY-MM-DD
  - 会话时长：~X 分钟
  - 变更文件：[文件列表]
  - 关键操作：[操作摘要]
  - 初步感知：[用户直觉理解]
  ```
- **Step 10B** — 再提炼为完整主题笔记（即 Step 9 的输出）
  > light/standard 直接一步到位，不生成 session log

### Mode 2: Review Previous Learning (on user request)

When user asks to review or recall previous learning:

1. Read `learning-notes/progress.md` to get the full learning overview
2. If user specifies a date/topic: read the corresponding note file from `topics/`
3. If user says "yesterday" or "recent": find the most recent calendar entry
4. Present a quiz-style review:
   - First, list the knowledge points WITHOUT code (test recall)
   - Ask the user to explain the core logic in their own words
   - Then reveal the code explanation for comparison
   - Mark knowledge points the user struggled with as 🔴 exposed in the mastery tracker (降级规则：🟢🟢 → 🟢 → 🟡 → 🔴，根据复习表现逐级降级), so Mode 3 reflects the true mastery level

### Mode 3: Learning Progress Check (on user request)

When user asks about overall progress:

1. Read `learning-notes/progress.md`
2. Scan `learning-notes/domains/` for domain-level status
3. Present:
   - Total learning days, domains covered, knowledge points count
   - **Per-domain progress with four mastery levels**:
     - 🟢🟢 **可教学**：能给别人讲清楚，举出类比和例子 → 对应 `teachable`
     - 🟢 **已掌握**：能不看代码讲清楚原理 → 对应 domain index 中标记为 `mastered` 的知识点
     - 🟡 **理解了**：知道怎么用但还不能脱离代码 → 对应 `understood`
     - 🔴 **接触过**：见过但还不会用 → 对应 `exposed`
   - **Mastery ratio** calculation: `可教学+已掌握 / (全部四级) × 100%`
   - Recent learning calendar (last 7 days)
   - Suggested next topics based on gaps: prioritize 🔴 items with highest interview relevance

### Mode 4: Interview Preparation (on user request)

**IMPORTANT**: Only trigger this mode when user explicitly mentions interview/job preparation. Do NOT include interview content in daily learning notes by default.

When user asks for interview preparation:

1. **Gather context** — Read `learning-notes/progress.md` and `learning-notes/domains/` to understand what the user has learned
2. **Identify relevant knowledge** — Scan knowledge point cards in `learning-notes/cards/` and recent topic notes for content that matches the user's target role
3. **Generate interview output**:
   - **30-second summary** for each major project/domain: concise enough for a quick self-introduction
   - **90-second deep-dive** for key technical choices: explain WHY you chose certain technologies
   - **Common interview questions** for the learned tech stack with suggested answers based on actual experience
   - **Weakness analysis**: identify gaps between what was learned and common interview expectations for the target role
4. **If user says "模拟面试" (mock interview)**:
   - Randomly pick 3-5 knowledge points from their cards
   - Ask each as an interview question, wait for the user's response
   - Provide feedback: what was good, what was missing, how to improve

**Interview question generation rules**:
- Draw questions from the user's actual learned content, not generic lists
- For backend roles: focus on auth flows, database design, API design, error handling
- For frontend roles: focus on component design, state management, performance, responsive design
- For full-stack roles: ask about integration decisions, data flow, debugging approaches
- Always reference the user's specific project experience when formulating questions

**Target role mapping** (use when user specifies a target role):

| Target Role | Priority Domains | Interview Focus |
|-------------|-----------------|-----------------|
| 后端开发(实习) | backend, database, security | API design, auth, database optimization |
| 前端开发(实习) | frontend, css, js | Component design, responsive, performance |
| 全栈开发(实习) | backend, frontend, devops | Integration, data flow, deployment |
| AI 应用(实习) | ai-ml, python | RAG, prompt engineering, LLM integration |
| 测试开发(实习) | testing, devops | Test design, CI integration, automation |

---

### Mode 5: 对话分析与提示词优化（新增 · v1.1.0）

**IMPORTANT**: 当用户说"分析一下我的对话记录"、"我的提示词写得怎么样"、"怎么问才能得到更好的回答"、"prompt 优化"时触发。可独立触发，也可在 Mode 1-4 执行后作为延伸功能触发。

#### 执行步骤

**Step 1 — 读取对话历史**
- 从 `learning-notes/` 或网页端导入的对话数据中读取最近 N 次对话（默认 N=10，用户可指定）
- 提取：用户的提示词模式、AI 的回答质量、反复追问的知识点

**Step 2 — 分析提示词模式**
- 分类统计以下维度（每项 1-10 分）：
  - **具体程度**：是否明确了技术栈、约束条件、预期输出格式
  - **上下文完整性**：是否提供了足够的背景信息
  - **任务分解能力**：复杂任务是否拆分成多步
  - **迭代次数**：平均几次交互达到目标
- 识别低效模式：
  - 过于模糊（"帮我写个登录"→ 缺少技术栈和约束）
  - 一次性抛多个问题（AI 难以逐一回答）
  - 缺少输出格式指定（导致需要多轮澄清）

**Step 3 — 生成优化建议**
- 针对具体对话给出"改前 vs 改后"对比
- 引用公开 Prompt Engineering 资料作为依据：
  - Anthropic Prompt Library: https://docs.anthropic.com/en/prompt-library
  - OpenAI Prompt Engineering Guide: https://platform.openai.com/docs/guides/prompt-engineering
  - Google Prompt Engineering Guide: https://ai.google.dev/docs/prompt_engineering
- 给出 1-3 条可操作的改进建议

**Step 4 — 输出学习洞察**（可选，用户主动询问时触发）
- 识别用户反复追问的知识点（= 未完全掌握）
- 推导技术栈掌握程度矩阵（基于对话内容，不依赖手动记录）
- 建议下一步学习重点（优先补强弱项）

#### 输出格式

```markdown
## 提示词优化分析报告

### 📊 你的提示词风格
| 维度 | 评分 | 说明 |
|------|------|------|
| 具体程度 | X/10 | ... |
| 上下文完整性 | X/10 | ... |
| 任务分解 | X/10 | ... |

### 💡 针对本次对话的优化建议

**原提示词**：
> "..."

**优化后**：
> "..."

**为什么更好**：
- ...

### 📚 参考资料
- [Anthropic Prompt Library](https://...)
- [OpenAI Prompt Engineering Guide](https://...)
```

#### 与网页端（Web Hub）的集成

当 Skill 在网页端环境中运行时，Mode 5 的输出可额外包含：
- 可点击的"应用此优化"按钮（自动生成优化后的提示词供复制）
- 提示词历史对比视图
- 与 Obsidian 笔记联动（将优化建议保存为 `cards/prompt-optimization/` 下的可复用卡片）

---

### Mode 6: inbox-triage — 知识生命周期管理（新增 · v1.1.0）

**IMPORTANT**: 当用户说"有什么没整理的笔记吗"、"整理一下 inbox"、"批处理今天的会话"时触发。

#### 执行步骤

**Step 1 — 扫描待处理笔记**
- 扫描 `learning-notes/` 目录，找出：
  - 文件名含 `temp_` 或 `session_` 的未整理笔记
  - 最近 3 天内创建但未移动的笔记
  - `inbox/` 子目录下的所有笔记

**Step 2 — 批处理分类**
- 列出所有待处理笔记，建议归档路径
- 等待用户确认或修改分类

**Step 3 — 关联检测**
- 对刚分类的笔记，搜索同领域其他笔记
- 建议关联（详见 `references/connection-review.md`）

**Step 4 — 晋升检查**
- 检测已复习多次的笔记，提示标记为「已掌握」

#### 输出格式

详见 `references/inbox-triage.md`。

---

### Mode 7: connection-review — 知识关联（新增 · v1.1.0）

**IMPORTANT**: 当用户说"今天学的和之前有什么关联"、"帮我建立知识关联"时触发。也可在 Mode 1 写入新笔记后自动触发。

#### 执行步骤

**Step 1 — 关键词重叠检测**
- 提取新笔记的 `tags` 和标题关键词
- 与已有笔记匹配，找出重叠度 ≥ 2 的主题

**Step 2 — 时间邻近检测**
- 同一天或连续几天内学习的主题，建议关联

**Step 3 — 生成关联建议**
- 强关联：建议立即建立双向链接
- 弱关联：可选建立链接
- 对比关联：建议生成对比笔记

**Step 4 — 写入双向链接**
- 经用户确认后，在笔记中插入 `[[双向链接]]`

#### 输出格式

详见 `references/connection-review.md`。

---

### Mode 8: weekly-synthesis — 深度周总结（新增 · v1.1.0）

**IMPORTANT**: 当用户说"周总结"、"生成本周学习报告"、"这周学了什么"时触发。替代 Mode 3 的浅层统计，生成深度报告。

#### 执行步骤

**Step 1 — 收集本周数据**
- 读取 `learning-notes/calendar/YYYY-MM.md`
- 统计学习天数、笔记数、主要领域

**Step 2 — 构建知识图谱**
- 分析本周笔记的关联关系
- 生成 Mermaid 知识图谱（如配置了图表输出）

**Step 3 — 掌握度评估**
- 基于复习次数和笔记质量，评估每个主题的掌握度
- 输出掌握度雷达图数据（供网页端可视化）

**Step 4 — 知识盲区检测**
- 基于本周学习的主题，反向查找缺失的前置知识
- 给出补强建议

**Step 5 — 下周学习计划**
- 基于掌握度和盲区，生成下周学习重点
- 包含复习计划和实践项目建议

#### 输出格式

详见 `references/weekly-synthesis.md`。

---

### Mode 9: health-check — 知识健康诊断（新增 · v1.1.0）

**IMPORTANT**: 当用户说"检查学习健康度"、"我有没有忘记复习的"、"知识诊断"时触发。也可配置为每周自动运行。

#### 执行步骤

**Step 1 — 遗忘检测**
- 扫描笔记的 `last_review_date`
- 超过 `config.yaml` 中设置的天数（默认 30 天）未复习的主题 → 提醒

**Step 2 — 关联建议**
- 检测同一时间窗口内学习但未建立关联的主题 → 建议链接

**Step 3 — 学习盲区检测**
- 基于本周学习的主题，反向查找缺失的前置知识

**Step 4 — 学习疲劳检测**
- 同一领域连续学习超过 7 天 → 建议切换

**Step 5 — 笔记质量检查**
- 检测内容过短或格式不规范的笔记 → 提示补充

#### 输出格式

详见 `references/health-check.md`。

#### 配置项

在 `config.yaml` 中：

```yaml
health:
  auto_run: true
  auto_run_day: monday
  notification_method: chat
```

---

## Writing Rules

- Write in plain Chinese. Explain technical terms the first time they appear.
- Target audience: CS undergraduate students who use AI coding tools
- Always include concrete file paths and line references from the actual project
- Include reading guidance: "read this function first, then see where it's called"
- Be honest about uncertainty — if something is ambiguous, say so
- Keep each daily note focused on ONE session, not a general overview
- **卡片层次规则**：知识卡片分"主卡片"和"引用卡片"两个层次：
  - **主卡片**：首次完整解释某个概念的卡片，包含完整的"是什么 / 核心原理 / 怎么用"
  - **引用卡片**：后续卡片遇到同一概念时，用 `> 详见 [[cards/category/primary-card-name]]` 引用，不再重述
  - 自检规则：如果两张卡片有 > 3 行内容重复，说明需要改为引用关系
- **行号引用规则**：所有代码行号引用（如 `state.py:15`）必须在写入前通过 Read 工具实时验证，确保行号准确。不要靠记忆猜测行号——用户点击 IDE 跳转如果对不上，会很失望
- Knowledge point cards should be self-contained and reusable across sessions

## Note Template

Follow the template structure defined in `templates/daily-learning-note.md`.

## Directory Structure for Learning Notes

The learning notes use a **three-layer architecture** for scalability:

```
learning-notes/
├── README.md                    # Overview dashboard & usage guide
├── progress.md                  # Progress tracking across all domains
├── calendar/
│   └── YYYY-MM.md              # Monthly learning calendar
│
├── topics/                      # Layer 1: Project/session-based notes
│   └── [project-name]/          # One folder per coding project/session
│       └── YYYY-MM-DD-[title].md
│
├── domains/                     # Layer 2: Domain & stack indexes
│   └── [domain]/                # e.g., backend, frontend, devops, ai-ml
│       ├── _index.md            # Domain-level knowledge checklist
│       └── [stack]/             # e.g., fastapi, react, docker
│           └── _index.md        # Stack-specific notes & progress
│
└── cards/                       # Layer 3: Reusable knowledge cards
    └── [category]/              # e.g., auth, css, js, python, database
        └── [card-name].md       # Self-contained, cross-topic reusable
```

### Three-Layer Design Rationale

| Layer | Purpose | When to Create | Example |
|-------|---------|---------------|---------|
| **topics/** | Raw session notes tied to a specific project | Every new coding session | `topics/fastapi-login-register/` |
| **domains/** | Curated indexes organized by tech domain/stack | When a new domain or stack is encountered | `domains/backend/fastapi/` |
| **cards/** | Atomic, reusable knowledge nuggets | When extracting a reusable concept | `cards/auth/jwt.md` |

This structure ensures:
- **Scalability**: Adding a new tech stack only requires creating a new `domains/[domain]/[stack]/` folder
- **Reusability**: Knowledge cards in `cards/` can be referenced by any future project
- **Discoverability**: Domain indexes provide a curated view of what you've learned per tech area
- **No flat-folder bloat**: Cards are categorized so no single folder grows too large

## Card Category Guidelines

When saving knowledge point cards, use these standard categories (create new ones as needed):

| Category | For |
|----------|-----|
| `auth/` | Authentication, authorization, JWT, OAuth, bcrypt, session management |
| `css/` | CSS properties, layout, animation, responsive design |
| `js/` | JavaScript language features, DOM, events, async |
| `ts/` | TypeScript types, generics, decorators |
| `python/` | Python language, FastAPI, Django, SQLAlchemy |
| `database/` | SQL, ORM, indexing, transactions |
| `devops/` | Docker, K8s, CI/CD, Terraform |
| `ai-ml/` | LLM, RAG, LangChain, PyTorch |
| `security/` | OWASP, XSS, CSRF, encryption |
| `testing/` | Unit test, integration test, E2E |

## 输出后续分流

每次产出后，根据内容类型建议一步行动（详见 `references/output-routing.md`）。

**快速参考**：

| 输出内容 | 建议下一步 |
|---------|-----------|
| 每日学习笔记 | "需要我把核心知识点生成卡片保存吗？" |
| 知识卡片 | "想用这几个知识点做一次模拟面试自测吗？" |
| 进度报告 | "看到你在 [domain] 上已有积累，需要我针对弱项推荐学习路径吗？" |
| 代码详解 | "要不要自己不看代码复述一遍逻辑？我可以帮你检查" |
| 连续 3 天同领域 | "这个领域已经连续 3 天了，要换一个拓展一下吗？" |
| 长时间未复习 | "上一次复习 [topic] 是 [N] 天前，需要温习一下吗？" |

> **注意**：分流建议只输出一次，用户忽略则不重复。不支持的分流路径直接跳过。

## On Failure

- If no code files can be found: ask the user to specify which files were created/modified
- If WebSearch returns no results: skip tutorial recommendations, use general knowledge instead
- If output directory is not writable: inform the user and suggest an alternative path
- If the session is too trivial (e.g., only changed a CSS color): suggest skipping note generation

---

## 输出自检清单

> 每次 Mode 执行完毕后，AI 应自行检查以下项目。如有未达标项，在输出末尾标注 `[自检：X/Y 通过]` 并说明未通过项。

### Mode 1 输出自检

- [ ] 是否提取了 3-8 个知识点（不多不少）
- [ ] 每个知识点是否有"为什么这样设计"的解释
- [ ] 是否有"如何从头写"的逐步重构指南
- [ ] 代码讲解是否按推荐阅读顺序组织
- [ ] 是否更新了 `learning-notes/progress.md`（如已存在）
- [ ] 是否保存了知识卡片到 `cards/`（如用户确认）
- [ ] 教程推荐是否优先 Bilibili 和官方文档（如启用了 WebSearch）
- [ ] **文件覆盖度**：是否读了 ≥ 80% 变更集中的文件 + 一层 import 链
- [ ] **行号验证**：代码行号引用（如 `state.py:15`）是否通过 Read 工具实时验证，而非靠记忆猜测
- [ ] **费曼自评**（standard/deep）：是否在 Step 10 询问了用户对知识点的不熟悉程度

### Mode 2 输出自检

- [ ] 是否先让用户回忆，再揭晓答案（非直接给答案）
- [ ] 是否标记了用户卡壳的知识点（mastery 降级）
- [ ] 是否给出了具体的复习建议（非泛泛而谈）

### Mode 3 输出自检

- [ ] 是否展示了四个掌握度层级（🟢🟢🟢🟡🔴）
- [ ] 是否计算了 mastery ratio（可教学+已掌握 / 全部四级）
- [ ] 是否给出了针对弱项的下一步建议

### Mode 4 输出自检

- [ ] 面试话术是否基于用户的真实项目（非通用模板）
- [ ] 模拟面试问题是否从用户的 cards/ 中抽取（非网上抄的题）
- [ ] 是否标注了回答中的知识盲区

### Mode 5 输出自检（新增）

- [ ] 提示词评分是否有具体维度（非只给总分）
- [ ] 优化建议是否有"改前 vs 改后"对比
- [ ] 参考资料链接是否真实可访问（非捏造）

### Mode 6 输出自检（新增）

- [ ] 是否扫描了所有待处理笔记（inbox/、temp_、session_）
- [ ] 是否给出了明确的归档建议（含目标路径）
- [ ] 是否检测了新笔记与已有笔记的关联

### Mode 7 输出自检（新增）

- [ ] 是否基于关键词重叠和时间邻近双重检测
- [ ] 关联建议是否区分了强/弱/对比三种类型
- [ ] 是否经用户确认后再写入双向链接

### Mode 8 输出自检（新增）

- [ ] 是否包含知识图谱（Mermaid 或文字描述）
- [ ] 是否评估了每个主题的掌握度
- [ ] 是否检测了知识盲区（缺失的前置知识）
- [ ] 是否给出了下周学习计划（含复习和实践）

### Mode 9 输出自检（新增）

- [ ] 是否检测了遗忘风险（超过 N 天未复习）
- [ ] 是否检测了未建立关联的笔记对
- [ ] 是否检测了学习盲区
- [ ] 是否给出了健康评分和优先处理建议

---

## Troubleshooting

### 问题 1：Skill 触发了但输出质量差

**可能原因**：
- `coding_context` 未提供，AI 没有足够上下文
- 项目目录结构复杂，AI 无法正确识别变更文件

**修复**：
```
用户：帮我总结今天学的
AI：我看到你修改了多个文件，能告诉我你主要做了什么功能吗？
```

### 问题 2：知识卡片重复生成

**可能原因**：同一知识点在多个 session 中被重复提取。

**修复**：写入 `cards/` 前，先搜索是否已存在同类卡片（按标题关键词匹配）。

### 问题 3：`progress.md` 数据不准确

**可能原因**：手动编辑 `progress.md` 时格式出错，或 Skill 写入时覆盖了他内容。

**修复**：运行 `python3 scripts/validate-structure.py` 检查目录结构一致性。

### 问题 4：WebSearch 失败导致无教程推荐

**现象**：输出中教程推荐部分为空或只有文字说明。

**修复**：Skill 已在 Step 6 中内置了 fallback（标注"基于通用知识推荐，非实时搜索结果"），不会捏造链接。如 WebSearch 持续失败，检查网络或使用 `find-skills` 安装替代搜索 Skill。

### 问题 5：Mode 5 提示词分析不准确

**可能原因**：对话历史读取不完整（只读了最近几条）。

**修复**：在触发 Mode 5 时明确指定范围，如"分析我最近 10 次与 AI 的对话"。

### 问题 6：Mode 6 inbox-triage 检测不到未整理笔记

**可能原因**：笔记已手动移动，或文件名不符合检测规则。

**修复**：检查 `learning-notes/` 目录下是否还有 `temp_` 或 `session_` 前缀的文件；如无，说明已整理完毕。

### 问题 7：Mode 7 connection-review 关联建议不准确

**可能原因**：关键词提取不完整，或时间窗口设置过宽/过窄。

**修复**：手动指定关联检测范围，如"帮我检查 `fastapi-login.md` 与 `jwt-auth.md` 的关联"。

### 问题 8：Mode 8 weekly-synthesis 报告过于简单

**可能原因**：本周学习笔记过少，或笔记内容质量低（仅代码片段，无知识点提炼）。

**修复**：确保 Mode 1 执行时完整提取知识点；如笔记质量低，先重新执行 Mode 1。

### 问题 9：Mode 9 health-check 遗忘提醒不准确

**可能原因**：`last_review_date` 未正确更新，或 `config.yaml` 中 `review_reminder_days` 设置不合理。

**修复**：手动更新笔记的 `last_review_date` 字段；或在 `config.yaml` 中调整提醒天数。
