# Standard Page Skeleton

Use this reference when creating the final HTML deliverable for video comment analysis.

## Goal

Create a page that feels like a **commercial proposal / editorial business report**, not a dark dashboard or generic AI report.

## Default page module order

1. 封面 / 项目概览
2. 核心结论摘要
3. 评论主题分布
4. 用户关注点分析
5. 购买意向分析
6. 成交驱动因素
7. 影响转化因素
8. 优化建议
9. 代表性评论证据
10. 统计口径 / 方法说明

## Layout guidance

### Hero section
Include:
- report title
- target video / platform / link
- one-line business conclusion
- sample statement

### Summary cards
Use 3–4 cards for:
- purchase intent level
- biggest selling point
- biggest blocker
- overall seller judgment

### Analysis sections
Each section should include:
- a clear section title
- one primary visual or structured block
- 1–3 short interpretation paragraphs

### Evidence section
Show 4–8 representative comments.
Each comment should support a conclusion already made above.

### Method section
Always state:
- main-comment sample size
- reply-thread count
- whether replies were excluded from chart-level statistics
- effective-comment definition
- which modules use counted metrics vs analyst judgment

## Style guidance

Prefer:
- warm white / cream / sand backgrounds
- brown-gray text
- 1 main accent + 1 support accent
- large spacing and obvious hierarchy
- restrained charts

Avoid:
- dashboard-heavy card walls
- harsh black or neon UI by default
- too many badges
- fake precision score displays

## Template usage guidance

If speed matters, start from `assets/html-report-template/index.html` and replace:
- title
- meta chips
- section text
- charts / bars / labels
- evidence comments
- method note

Keep the module order unless the user explicitly asks for a different structure.
