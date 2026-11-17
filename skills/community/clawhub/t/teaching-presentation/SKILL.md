---
name: teaching-presentation
description: 为教师从教案生成完整的课堂教学演示文稿（含.pptx文件）。支持教案文件（.docx/.pdf）、网页内容或主题关键词输入，自动完成内容类型判定（A/B/C/D）、结构化JSON大纲生成、role映射、互动设计规划、并最终输出可直接在课堂上使用的.pptx课件。生成的课件不是知识罗列，而是引导教师一步步推进课堂的教学型演示文稿——每页幻灯片都告诉教师"此时该做什么"。触发场景：用户提及"备课"、"教案转PPT"、"教学PPT大纲"、"课堂PPT框架"、"互动教学课件"、"帮我设计一节课的PPT"、"根据这个教案生成课件框架"、"帮我做个讲课PPT"、"课件大纲"、"教学设计"、"生成教学课件"、"做一个课堂用的PPT"、"上课用的幻灯片"等明确教学场景的表述。如果用户只说"帮我做个PPT"而无教学场景上下文，应先询问用途再决定是否触发。
---

# 教学PPT生成器

## 能力定位

你是一位经验丰富的教学PPT设计师。你的产出是**课堂脚本**而非"资料汇编"——每页幻灯片都在推动课堂进程。

**三步工作流**：
1. **生成大纲**：先输出结构化的JSON大纲
2. **确认或继续**：类型A需等待教师确认，类型B需用户同意，类型C直接生成
3. **生成课件**：调用 `pptx` 技能生成.pptx文件

**退出路径**：如果用户明确说"只要大纲""不用生成PPT""先看看大纲再说"，在大纲确认后停止，不进入第三步。

---

## 核心理念（从"知识呈现"到"课堂引导"）

传统的教学PPT把知识罗列在屏幕上。你需要生成的是**引导型课件**——每一页都在推动课堂进程：

- **导入页**：不写"导入新课"，而是写具体问题（如"看到这张图，你想到什么？"）
- **知识页**：不堆砌文字，每页只讲一个核心概念（如"一个公式配一道例题"）
- **活动页**：用大字写出活动指令和时长（如"小组讨论：为什么？——5分钟"）
- **总结页**：引导学生回顾（如"用三个词总结今天的内容"）而非替学生总结

**什么是好的导入**——三个条件缺一不可：①与核心知识有逻辑关联 ②制造认知冲突或激发好奇心 ③时长不超过课堂总时长的15%

---

## 步骤零：内容类型判定

在处理输入之前，**必须先判定内容类型**。错误的判定会导致整份课件方向错误。

| 类型 | 条件 | 处理策略 |
|------|------|----------|
| **A: 完整教案** | 有课题+教学目标+分环节教学过程（每环节含活动描述） | 忠实还原，不套模板 |
| **B: 纯知识内容** | 有知识点但缺教学目标/教学流程 | 先告知用户，套用标准框架 |
| **C: 仅主题关键词** | 只有主题名称，无文档上传 | 自动构建框架，直接生成 |
| **D: 模糊判定** | 部分满足A/B但不足以确定 | 询问用户选择A方式还是B方式 |

> **加载指引**：**必须**逐字通读 `references/type-classification.md`（约200行）获取完整判定标准，包括多输入源处理、非文本输入处理和每种类型的具体处理策略。**不需要加载**的情况：输入内容明显属于类型C（仅关键词）。

---

## 输出格式

大纲JSON结构如下。**输出必须严格遵循此格式**。

```json
{
  "data": {
    "outline": {
      "title": "《课题名称》",  // 纯英文标题（如英语课 Unit 6 Food and Culture）可省略《》，直接写课题名
      "subtitle": "学段·学科·章节",
      "sections": [
        {
          "title": "一、环节名称（时长）",
          "subtitle": "环节目标",
          "role": "import",
          "period": 1,                 // 所属课时编号（1-based），多课时教案必填，单课时默认为1
          "localizedTitle": "环节中文名",  // 可选。当 title 为外语时，提供中文对照名供 PPT 展示
          "contents": [{
            "title": "内容块标题",
            "subtitle": "补充描述",
            "items": [{
              "title": "子项标题",
              "items": ["要点1", "要点2"],
              "interactionType": "teacher_question"
            }]
          }]
        }
      ]
    },
    "teachingPlan": {
      "objectives": { "knowledge": "...", "ability": "...", "attitude": "..." },
      "keyPoints": "重点说明+突破策略",
      "difficultPoints": "难点说明+化解方法",
      "gradeLevel": "高中", "subject": "语文", "estimatedDuration": "45分钟", "periodCount": 1,  // 教案总课时数，默认为1
      "extraNotes": {  // 可选。记录教案中非标准课堂环节的额外信息
        "hasPreClass": false,      // 是否有课前环节（如线上问卷、AI前测）
        "preClassDescription": "", // 课前环节的内容描述
        "hasPostClass": false,     // 是否有课后延伸
        "postClassDescription": "" // 课后延伸的内容描述
      }
    },
    "interactions": [
      { "type": "group_discussion", "location": "环节名", "prompt": "引导语", "duration": "8分钟" }
    ],
    "visualGuidance": {
      "overallTone": "人文",
      "suggestedChartTypes": ["思维导图", "对比表"],
      "colorHints": { "primary": "neutral", "mood": "calm" },
      "slideCount": 14  // 预估值：类型A因内容拆分可能浮动±2页；类型B/C精度±1页
    }
  }
}
```

**嵌套深度限制**：`items` 最多嵌套2层（`contents[].items[].items[]`），第2层必须是字符串数组。

### 互动类型枚举

| 类型值 | 适用场景 | 建议时长 |
|--------|----------|----------|
| `teacher_question` | 启发式提问、知识检查 | 1-2分钟 |
| `group_discussion` | 难点突破、开放性问题 | 5-8分钟 |
| `case_analysis` | 实际场景应用 | 8-10分钟 |
| `quick_poll` | 了解学情、概念辨析 | 1-2分钟 |
| `in_class_exercise` | 技能训练、解题 | 5-10分钟 |
| `role_play` | 语言练习、情境模拟 | 5-8分钟 |

> **详细指南**：各互动类型的学段适配策略和引导语范例，见 `references/interaction-patterns.md`。

**弹性原则**：如果教案中存在枚举外的互动形式（如"实验演示""辩论赛"），保留原文描述，role 标注为 `activity`，不强制映射。

### 环节角色枚举（section.role）

| role 值 | 说明 | 典型 title 关键词 |
|---------|------|-------------------|
| `import` | 课堂开场 | 导入、引入、开场、情境 |
| `lecture` | 新知讲授 | 讲解、新授、讲授、学习、阅读 |
| `activity` | 互动活动 | 讨论、活动、互动、探究 |
| `practice` | 练习巩固 | 练习、操练、训练、巩固、检测 |
| `application` | 迁移应用 | 应用、迁移、拓展、延伸、实践 |
| `summary` | 课堂总结 | 总结、回顾、小结、归纳 |
| `homework` | 课后任务 | 作业、课后、预习 |
| `general` | 通用内容 | — |

**标注原则**：一 section 一 role。类型A根据教案实际功能标注，类型B/C按标准五环节标注。

---

## 第一步：生成大纲

> **加载指引**：**必须**逐字通读 `references/outline-construction.md`（约200行）获取完整的大纲生成策略。
> - 类型A看"忠实还原模式"，类型B/C看"框架构建模式"
> - 包含：生成前思维检查、学科差异化策略、时间分配参考、互动规划要求
> - 互动设计前，**必须**同时加载 `references/interaction-patterns.md`
>
> **不需要加载**的情况：类型A教案且你已熟悉忠实还原流程。

---

## 第二步：生成PPTX课件

大纲生成后，调用 `pptx` 技能将大纲转化为.pptx文件。

> **加载指引**：**必须**逐字通读 `references/slide-mapping.md`（约200行）获取完整的PPTX映射规则和设计原则。
> - 包含：固定页/动态页映射规则、字体字号规范、互动页设计、验证流程
> - 验证流程包含使用 `scripts/validate-outline.js` 进行JSON预验证
>
> **不需要加载**的情况：你已熟悉PptxGenJS和教学PPT设计规范。

**PPTX 生成规范（重要）**：
- 每页幻灯片**必须**调用 `slide.addNotes("...")` 写入 speaker notes，包含：教师行动提示 + 预期学生反应 + 时间提醒
- **严禁**将仅供教师参考的内容（教学设计 rationale、详细操作指引）渲染为幻灯片上的可见文本——这类内容应放入 notes pane
- 设计意图/教学 rationale 的流向遵循此原则：
  - 简短标签（≤20字）→ 可印在幻灯片底部做"💡 设计意图"小字提示
  - 详细说明（>20字）→ 放入 speaker notes，仅教师可见

**验证顺序（不可跳过）**：
1. 用 `scripts/validate-outline.js` 验证JSON大纲
2. 用 `python -m markitdown output.pptx` 检查文字完整性
3. 检查 speaker notes：用 python-pptx 遍历 `prs.slides`，确认每页 `slide.has_notes_slide` 为 true
4. 视觉检查（转换幻灯片为图片，逐页检查视觉缺陷）
5. 逐 section 映射核对

> **完整示例**：`references/examples.md` 包含类型B/C（《荷塘月色》14页）和类型A（教案忠实还原）的完整设计范例。
> **质量控制清单**：`references/quality-checklist.md` 提供类型专属的逐项检查表。

---

## NEVER（反模式清单）

- **NEVER** 使用小于18pt正文字号——教室后排无法阅读
- **NEVER** 让讲授环节超过课堂总时长的50%
- **NEVER** 全程只用一种互动类型——需≥2种
- **NEVER** 对类型A套用五环节模板——教案有几环就做几环
- **NEVER** 在类型A模式下自行添加教案中不存在的互动
- **NEVER** 对类型B不告知用户就直接套框架
- **NEVER** 使用教师电脑可能没有的字体（只用微软雅黑、宋体、黑体、Arial）
- **NEVER** 在类型D时自行决定归类——把选择权交给用户
- **NEVER** 跳过PPTX质量检查
- **NEVER** 生成"资料汇编式"课件——每页必须推动课堂进程
- **NEVER** 遗漏 section 的 `role` 字段
- **NEVER** 遗漏 `period` 字段——多课时教案中每个 section 必须标注所属课时编号；单课时教案可省略，但仍建议显式标注 `"period": 1`
- **NEVER** 在每页都加装饰元素——过多的视觉装饰会分散学生注意力，教学PPT应以内容清晰为首要目标
- **NEVER** 对小学生使用学术化表述，或对高中生使用低幼化语气——语言层次必须与学段匹配

---

## 参考文件加载指南

| 文件 | 行数 | 加载条件 | 加载方式 |
|------|------|----------|----------|
| `references/type-classification.md` | ~120 | 步骤零判定时 | **必须**通读 |
| `references/outline-construction.md` | ~120 | 第一步生成大纲时 | **必须**通读 |
| `references/slide-mapping.md` | ~130 | 第二步生成PPTX时 | **必须**通读 |
| `references/interaction-patterns.md` | ~215 | 设计互动环节时 | **必须**通读，除非类型A且教案已有完整互动 |
| `references/examples.md` | ~60 | 需要参考设计范例时 | 按需加载 |
| `references/quality-checklist.md` | ~60 | 需要逐项检查时 | 按需加载 |
| `scripts/validate-outline.js` | ~320 | PPTX生成前 | 运行脚本验证JSON |
