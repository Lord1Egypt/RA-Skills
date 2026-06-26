---
content_type: 流程图
style_id: WebUI_Clean_Modern
style_name: WebUI Clean Modern
prompt_role: meta_prompt_for_final_image_prompt
upstream_info: |
  title: 图标题
  process_goal: 这张图要说明的流程目标
  context: 使用场景，例如 SaaS onboarding、AI workflow、product guide、business SOP
  steps: 3-6 个步骤；每个包含 number、label、description、visual_hint、optional_output
  source: 来源或备注，可为空
  aspect_ratio: 默认 16:9
  accent_color: 可选，默认 blue 或 violet
  preferred_layout: 可选，不填则由 AI 判断
  required_text:
  - 必须逐字出现在图中的标题、步骤标签、短说明、来源
---

# 元提示词

```text
You are an expert visual prompt engineer for GPT Image 2 and a senior visual designer for SaaS product pages, pitch decks, and modern business reports.

Given the user's process and communication goal below, write one final image-generation prompt for a WebUI Clean Modern process diagram.

Your final prompt must not be a template. It must be a polished, direct prompt that can be sent to GPT Image 2 as-is.

First infer the design hierarchy:
- identify the process goal and the main transformation from start to finish;
- choose the clearest layout: horizontal step cards, timeline workflow, pipeline board, or hub-and-spoke workflow;
- make the step sequence visually obvious with connector arrows, lines, or progress paths;
- keep captions short and readable.

Use this style:
- 16:9 horizontal slide;
- clean modern Web UI / pitch deck process visualization;
- flat vector interface aesthetic;
- white or very light gray background;
- generous whitespace and strict alignment;
- modern sans-serif typography;
- black, white, soft gray, and one vivid blue or violet accent color;
- rounded step cards, pill labels, thin dividers, subtle grid lines, connector arrows, and light shadows only where useful;
- one clear workflow path.

Only include these text elements in the final image:
- the title;
- each step number;
- each step label;
- one short caption per step if provided;
- the source or footer if provided.

Render every visible text string verbatim in straight English double quotes. Do not invent extra labels, dashboard UI, navigation, or explanatory paragraphs.
If a required text item is meant to appear as one phrase, preserve it as one complete visible text string rather than splitting it into separate words, labels, or values.

Process data:
[PASTE_USER_PROCESS_DATA_HERE]

End the final prompt with strong negative constraints:
no complex dashboard, no app sidebar, no navigation bar, no filters, no dense table, no isometric, no 3D, no photo, no characters, no rainbow palette, no heavy decoration, no clutter, no tiny unreadable text, no fake labels, no invented steps, no watermark, no logos.
```
