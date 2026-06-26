---
name: techvideo-wizard-skill
description: Interactive video script wizard that guides users through a structured 6-step process to collect product video requirements and generate a professional video script in Markdown format. This skill should be used when users want to write a video script, need guidance on creating product demo or promotional videos, express intent like "help me write a XXX video script", "video script wizard", or when any task requires structured requirement gathering for video/multimedia content creation. Typical trigger examples include "帮我写个 SuperMap GIS 小视频的脚本", "帮我写个产品介绍视频的脚本", "视频脚本向导".
---

# TechVideo Wizard - Video Script Generator

## Overview

Guide users through a structured 6-step interactive process to collect product/feature video requirements, then automatically generate a professional video script. The output is a Markdown-formatted script file optimized for UI/design team collaboration.

**Core value**: Transform vague ideas into production-ready video scripts through progressive refinement.

## Workflow Protocol

```
Step 1: 一句话介绍 (必填) → [自动] 重复内容检查 → Step 2: 历史 vs 当前对比 (可选) → Step 3: 核心步骤 (必填) → Step 4: 变化/效果 (可选) → Step 5: 最终效果 (必填) → Step 6: 生成脚本 (自动) → [可选] Step 7: 自动优化
```

**Interaction rules**:
- Ask exactly **one question per step** using `ask_followup_question`
- Wait for user response before proceeding to the next step
- Store each answer as context for subsequent steps
- Step 2 and Step 4 are optional — accept skip keywords ("无", "跳过", "没有", "skip", "none") and proceed directly to the next step

---

## Step 1: One-Line Introduction (Guided + Strong Constraints)

Collect the user's core intent in a single, visualizable sentence.

**Use the following prompt verbatim:**

> 你是一个视频脚本助手，需要引导用户填写视频内容。
>
> 请用户输入"一句话介绍"。
>
> 【填写要求】
> 1. 使用"动词 + 对象 + 结果特征"
> 2. 必须具体、可视化（能让人脑海有画面）
> 3. 避免抽象表达（如：提升效率、优化体验）
> 4. 每句话不超过 15 字
>
> 【示例】
> - 构建高真实感铁路三维场景
> - 实现网络故障自动定位
> - 自动识别图像中的异常目标
> - 快速生成标准化运维报告
> - 实现跨系统统一调度
>
> 【错误示例】
> - 提升效率 ❌
> - 优化用户体验 ❌
>
> 请直接给出一句话介绍：

**Processing the answer:**
- Validate that the response follows "动词 + 对象 + 结果特征" pattern
- If too abstract (contains words like 提升、优化、增强 without specifics), prompt the user to refine with concrete imagery
- Verify each sentence ≤ 15 characters
- Save as `INTRODUCTION` context variable
- **IMMEDIATELY proceed to Duplicate Content Check (see below)**

---

### Duplicate Content Check (Auto-trigger after Step 1)

After collecting the one-line introduction, **automatically** check if similar video content already exists on WeChat Video Channels (微信视频号), Bilibili (B站), and Douyin (抖音).

**Execution logic**:

1. **Extract search keywords** from `INTRODUCTION`
2. **Use `web_search` tool** to search for existing content (execute multiple searches in parallel):

   **Search queries**:
   - `{关键词} 微信视频号` - 微信视频号搜索
   - `{关键词} 视频号` - 视频号通用搜索
   - `{关键词} site:bilibili.com` - B站官方域名搜索
   - `{关键词} B站 视频` - B站通用搜索
   - `{关键词} site:douyin.com` - 抖音官方域名搜索
   - `{关键词} 抖音 视频` - 抖音通用搜索

3. **Present search results** to user with clear formatting:

> 🔍 **重复内容检查完成**
>
> **微信视频号搜索结果**:
> - ✅ [视频标题](链接)
>   - 平台：微信视频号 | 发布时间：YYYY-MM-DD
> - （无结果）
>
> **B站搜索结果**:
> - ✅ [视频标题](链接)
>   - 平台：B站 | 时长：XX:XX | 发布时间：YYYY-MM-DD
> - （无结果）
>
> **抖音搜索结果**:
> - ✅ [视频标题](链接)
>   - 平台：抖音 | 发布时间：YYYY-MM-DD
> - （无结果）
>
> **补充检查**：如需进一步确认，请在以下文档中使用关键词搜索是否存在相似视频：
> [视频列表文档](https://doc.weixin.qq.com/sheet/e3_AbEABwZhAOEELyAyNqUQ4urnvazrm?scode=AEwAawe0AAgC6L3AHYADQA7AahAB0&tab=BB08J2)
>
> **是否继续制作？**
> - 回复「继续」→ 进入 Step 2
> - 回复「调整主题」→ 重新思考视频角度

**Processing rules**:
- If user chooses "调整主题", restart from Step 1
- If user chooses "继续", proceed to Step 2

**Search optimization tips**:
- Use specific product/feature names for better results
- If no results found on first try, use alternative keywords
- Prioritize recent content (within 1 year) for relevance

---

## Step 2: Before vs After Comparison (Optional)

Collect optional historical vs current state comparison to highlight the transformation value.

**Use the following prompt verbatim:**

> 请描述：有了这个功能后，效果有哪些变化？
>
> 【填写要求】
> 1. 用"原来... → 现在..."的对比方式
> 2. 量化或具体描述变化
> 3. 突出价值感
>
> 【示例】
> - 原来人工建模需要 2 天 → 现在 10 分钟完成
> - 原来客户看不到三维效果 → 现在实时在线浏览
> - 原来报告生成依赖手工汇总 → 现在一键自动导出
>
> 请填写（可选）：
>

**Processing the answer:**
- Accept skip keywords: "无", "跳过", "没有", "skip", "none", "—", empty response
- If skipped, set `BEFORE_AFTER` to empty and proceed to Step 3
- Otherwise save the response as `BEFORE_AFTER` context variable

---

## Step 3: Core Steps (Key Section)

Break down the requirement into 3-8 actionable steps. This section is the core content of the video.

**Use the following prompt verbatim:**

> 【填写要求】
> 1. 支持 3-8 步（推荐 4-6 步）
> 2. 每一步包含**核心说明**和**旁白补充**（可选）
>
> 【格式】
> 步骤编号：核心说明（≤15字，动词开头）
> 旁白：讲解内容第一句（≤15字）
> 旁白：讲解内容第二句（≤15字）
> （可选）截图：[截图描述或文件名]
>
> 【示例】
> 第一步：导入三维数据
> 旁白：支持多种格式一键导入
> 旁白：智能识别坐标自动配准
> 截图：[数据导入界面]
>
> 第二步：配置发布参数
> 旁白：根据规模智能推荐配置
> 旁白：拖拽调整实时预览
> 截图：[参数配置界面]
>
> 第三步：一键发布服务
>
> 第四步：前端参数调整
>
> 【说明】
> - 如果只填写"核心说明"，AI 会自动生成旁白补充
> - 如果填写完整内容，AI 会保持原样
>
> 【错误示例】
> - 提升分析能力 ❌
> - 更高效处理 ❌
>
> 【易懂性审核示例】
>
> 输入："处理数据"
> 审核：⚠️ 过于笼统，无法形成画面
> 建议："读取 Excel 表格数据"
>
> 输入："完成任务"
> 审核：⚠️ 缺少宾语，什么任务？
> 建议："生成数据汇总报告"
>
> 输入："查看结果"
> 审核：⚠️ 歧义：是图表、报告还是列表？
> 建议："查看预测准确率图表"
>
> 请按"每行一步"填写：

**Processing the answer:**
- Parse steps with structure: `步骤编号`, `旁白:`, `截图:`
- **Step-by-step review**: After user submits each step, apply the "User Comprehension Review"

### User Comprehension Review (Each Step)

After user inputs each step, evaluate from the target audience's perspective:

**Review criteria:**
1. **具体性**: 是否具体可感知？还是有歧义？
2. **画面感**: 用户脑海里能否形成画面？
3. **易懂性**: 是否有过多专业术语？普通用户能理解吗？
4. **动词明确性**: 动词是否清晰表达动作？

**If issues found**, show:

> 📝 **文字优化建议**
>
> 【原文】xxx
> 【问题】xxx（如：专业术语过多、不够具体、可能有歧义）
> 【建议修改】xxx
>
> 是否接受修改？
> - 回复「接受」→ 使用优化后的文字
> - 回复「保持」→ 保留原样
> - 回复「其他建议」→ 提供你自己的想法

**Narration Design Principle (CRITICAL):**

When generating or optimizing narration, follow this logic pattern:

1. **先确定目标** - 要操作什么、在哪里操作
2. **再指定来源** - 数据从哪来、选什么
3. **最后执行** - 确认后执行操作

**Example:**
- User input: "导入符号库"
- Narration: 先打开符号库管理界面 → 再导出待合并工作空间中的符号库 → 最后统一导入目标工作空间

**Apply this logic to ALL steps.**

**If text is clear**, acknowledge and continue:

> ✅ 收到，继续下一步（或请填写下一步）

- If step has no narration, generate 2-3 sentences based on core description (after user confirms)
- Each generated narration ≤ 15 characters
- Save as `CORE_STEPS` context variable (preserve structure for script generation)

### Step Review & Modification (After All Steps Collected)

After all steps are collected (用户完成所有步骤填写后), display a summary and ask for modification preference:

> ✅ 所有步骤已收集完成！
>
> **当前步骤概览：**
> 1. 第一步：导入三维数据
> 2. 第二步：配置发布参数
> 3. 第三步：一键发布服务
> ...
>
> **【过渡提示 - 随机选择以下示例之一】**
> - "好了，以上就是XX的配置方法"
> - "这样，XX就安装完成了"
> - "按照这三步，XX就能正常跑起来了"
> - "完成这些操作，XX就设置好了"
> - "通过以上步骤，XX已经准备就绪"
>
> **是否需要修改？**
> - 回复「修改第X步」→ 重新编辑指定步骤（如：修改第2步）
> - 回复「修改全部」→ 重新编辑所有步骤
> - 回复「继续」→ 进入下一步骤，描述最终效果

**Modification handling:**
- **修改第X步**: Show the selected step content and ask for new input, then return to summary
- **修改全部**: Clear `CORE_STEPS` and restart Step 3 from beginning
- **继续**: Proceed to Step 4

---

## Step 4: Change/Effect (Optional Guidance)

Collect optional before/after comparison information.

**Use the following prompt verbatim:**

> 请描述这个功能带来的变化或效果（可选）。
>
> 【建议】
> 用"原来 vs 现在"的方式表达，更容易理解
>
> 【示例】
> - 原来人工逐点排查 → 现在系统自动定位
> - 原来耗时数小时 → 现在分钟级完成
> - 无需人工建模 → 自动生成结果
>
> 【说明】
> 如果这个功能本身已经很直观，可以简单描述或跳过
>
> 请填写（可选）：

**Processing the answer:**
- Accept skip keywords: "无", "跳过", "没有", "skip", "none", "—", empty response
- If skipped, set `CHANGE_EFFECT` to empty and proceed to Step 5
- Otherwise save the response as `CHANGE_EFFECT` context variable

---

## Step 5: Final Effect (Strong Constraint)

Collect quantifiable, perceivable outcome metrics.

**Use the following prompt verbatim:**

> 请描述最终带来的效果。
>
> 【填写要求】
> 1. 必须具体、可感知
> 2. 尽量量化或对比
> 3. 禁止使用空话（如提升效率、优化体验）
>
> 【示例】
> - 故障定位时间缩短80%
> - 建模时间从2小时降至10分钟
> - 操作步骤由5步减少至1步
> - 人工成本降低50%
>
> 【错误示例】
> - 提升效率 ❌
> - 优化体验 ❌
>
> 请填写：

**Processing the answer:**
- Enforce specificity — reject abstract responses
- Look for numbers, percentages, time comparisons, or concrete metrics
- Save as `FINAL_EFFECT` context variable

---

## Step 6: Generate Video Script (Auto Output)

Automatically generate the final video script based on all collected context.

**Do NOT ask the user anything in this step.** Execute the following generation logic:

### Terminology Constraints (CRITICAL)

Before generating, read and apply constraints from `TERM_CONSTRAINTS.md`:

1. **Load constraints**: Read the terminology constraint table
2. **Preserve terms**: All terms listed in the constraint table must be preserved exactly as written
3. **Priority rule**: Terminology constraints override general optimization rules
4. **User-defined terms**: If user explicitly states "请保留XX术语", add to temporary constraint list

**Constraint categories**:
- Product Names (e.g., SuperMap GIS, SuperMap iDesktop)
- Technical Terms (e.g., 三维场景, 倾斜摄影, BIM模型)
- Feature Modules (e.g., 数据导入, 服务发布)
- Industry Applications (e.g., 智慧轨交, 数字孪生)
- Action Commands (e.g., 一键导入, 实时预览)
- Effect Descriptions (e.g., 纤毫毕现, 身临其境)

### Generation Template

Use this structure to generate the script:

```markdown
# {基于 INTRODUCTION 的视频标题} - 视频脚本

> **生成时间**: {当前日期}
> **风格**: 科技感、简洁、有节奏

---

## 脚本正文

### 🎬 开头

{基于 INTRODUCTION 生成 1-2 句开场文案，每句 ≤ 15 字}
{**要求**：必须包含问句或痛点场景，吸引注意力}
{**示例**："还在为数据导入报错发愁吗？" 而非 "这是 GIS 数据导入功能"}

### 🔧 方案

{基于 CORE_STEPS 生成详细分镜文案，每个步骤包含：}
{1. 步骤标题（≤15字）}
{2. 旁白内容（2-3句，每句 ≤ 15 字）}
{3. 截图位置标注（如果有）}

{如果用户填写了旁白，保持原样；如果未填写，AI 根据核心说明拓展生成}

{如果 BEFORE_AFTER 非空，插入对比说明：}

**前后对比（可选）**
{基于 BEFORE_AFTER 生成 1-2 句对比文案}

### 📈 结果

{基于 FINAL_EFFECT 生成 1-2 句结果文案，每句 ≤ 15 字，量化价值}

{**过渡提示**：随机选择以下示例之一}
{"好了，以上就是XX的配置方法" / "这样，XX就安装完成了" / "按照这三步，XX就能正常跑起来了" / "完成这些操作，XX就设置好了" / "通过以上步骤，XX已经准备就绪"}

### 🎯 收尾（包含行动号召 CTA）

{1-2 句收尾文案，每句 ≤ 15 字}
{**要求**：必须包含明确的行动号召 (CTA)，引导用户互动}
{**CTA 示例**：}
{- "想亲自试试？评论区领安装包。"}
{- "觉得好用，点个赞支持一下。"}
{- "你的 GIS 项目还在手工建模吗？"}
{- "遇到问题？评论区告诉我。"}
{- "想看更多技巧？关注不迷路。"}

---

## 原始输入记录

| 项目 | 内容 |
|------|------|
| 一句话介绍 | {INTRODUCTION} |
| 历史 vs 当前对比 | {BEFORE_AFTER 或 "（已跳过）"} |
| 核心步骤 | {CORE_STEPS} |
| 变化/效果 | {CHANGE_EFFECT 或 "（已跳过）"} |
| 最终效果 | {FINAL_EFFECT} |
```

### Output Rules

1. **Structure**: 开头（含问句/痛点） → 方案 → 结果（含过渡提示） → 收尾（含 CTA）
2. **Line length**: Each sentence MUST be ≤ 15 Chinese characters
3. **Narration generation**: If user provided narration, keep it; otherwise generate 2-3 sentences per step
4. **Style**: Tech-forward, concise, rhythmic — prioritize "value perception"
5. **No repetition**: Avoid repeating the same concept across sections
6. **Value-first**: Every line should convey tangible benefit or capability
7. **Terminology preservation**: Strictly follow `TERM_CONSTRAINTS.md` — preserve all fixed terms exactly as specified
8. **Opening requirement**: 开头 MUST contain a question or pain point scenario (e.g., "还在为数据导入报错发愁吗？")
9. **CTA requirement**: 收尾 MUST include clear Call-to-Action to guide user interaction (e.g., "想亲自试试？评论区领安装包。")

### File Output

After generating the script content:
- Write the complete Markdown content to `{视频标题}-视频脚本.md` in the current working directory using `write_to_file`
- Display a summary showing: file path, total lines
- Ask if user wants **Step 7 optimization**

---

## Step 7: Auto-Optimize Input (Optional Enhancement)

Offer to optimize/refine the raw inputs for better video expression.

**Only execute if user agrees after Step 6.**

**Use the following prompt:**

> 是否需要对原始输入内容进行自动优化？
>
> 优化将使表达更清晰、更具体、更适合视频旁白表达。

If user confirms, apply this transformation to each of the 4 input fields:

**Optimization template:**

> 请将以下内容优化为更具体、可用于视频表达的句子：
>
> 要求：
> 1. 更清晰
> 2. 更具体
> 3. 避免抽象词（如提升、优化）
>
> 【输入】
> {{用户填写的原始内容}}

Apply optimization to `INTRODUCTION`, `BEFORE_AFTER`, `CORE_STEPS`, `CHANGE_EFFECT`, and `FINAL_EFFECT` respectively, then regenerate the script with optimized content. Save as `{视频标题}-视频脚本-优化版.md`.

**Optimization Constraints**:
- All terms from `TERM_CONSTRAINTS.md` must be preserved exactly
- Optimization should improve clarity and flow without changing fixed terminology
- When terminology conflicts with length constraints, preserve the term and adjust surrounding text

---

## Anti-Patterns

**DO NOT:**
- Ask multiple questions in a single step
- Skip Step 1, Step 3, or Step 5 (these are mandatory)
- Use sentences exceeding 15 characters in the output script
- Include abstract terms like "提升效率", "优化体验" in the generated script
- Proceed to Step 6 without collecting answers from all mandatory steps

**DO:**
- Validate each answer against the constraints before proceeding
- Gently guide users to rephrase if their input violates the format rules
- Maintain a helpful, guiding tone throughout
- Preserve exact prompt wording from Steps 1-5 as specified above
- **Automatically trigger duplicate content check after Step 1**

## Quality Checklist

Before delivering the final script, verify:
- [ ] All 3 mandatory fields collected (Step 1: INTRODUCTION, Step 3: CORE_STEPS, Step 5: FINAL_EFFECT; Step 2 and Step 4 may be skipped)
- [ ] Each output sentence ≤ 15 characters
- [ ] Script follows 开头→方案→结果→收尾 structure
- [ ] Each step has core description + narration (user-provided or AI-generated)
- [ ] No abstract/empty phrases in output
- [ ] All terms from `TERM_CONSTRAINTS.md` preserved exactly
- [ ] Markdown file written to working directory
- [ ] File name follows `{title}-视频脚本.md` format
- [ ] Duplicate content check performed after Step 1
