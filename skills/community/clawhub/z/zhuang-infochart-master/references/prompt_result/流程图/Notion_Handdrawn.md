---
content_type: 流程图
style_id: Notion_Handdrawn
style_name: Notion Handdrawn
prompt_role: meta_prompt_for_final_image_prompt
upstream_info: |
  title: 图标题
  process_goal: 这张图要说明的流程目标
  context: 使用场景，例如 Notion guide、SaaS onboarding、service explainer、lifestyle how-to、website section
  steps: 3-5 个步骤；每个包含 number、label、description、visual_action
  source: 来源或备注，可为空
  aspect_ratio: 默认 16:9
  preferred_layout: 可选；不填则由 AI 判断
  caption_mode: exact_text 或 blank_caption_space，默认 exact_text
  required_text:
  - 必须逐字出现在图中的标题、步骤标签、短说明、来源
  optional_cta: 可选；只适合网页 section 或服务介绍
---

# 元提示词

```text
You are an expert GPT Image 2 prompt engineer. Read the process data and internally choose the most suitable Notion hand-drawn layout before writing the final image prompt.

Available layouts:
1. "2x2 Instructional Panels" for a four-step sequential workflow with one action per step.
2. "Airy How-To Sheet" for lifestyle, craft, coaching, care, or warm human-centered instructions.
3. "Horizontal Process Row" for 3-5 step SaaS, Notion, AI, or tool workflows.
4. "Website Section / Multi-Card Row" for parallel service categories, roles, capabilities, or module options.

After choosing internally, write one direct GPT Image 2 prompt. Do not mention your reasoning.

The prompt must:
- state the chosen layout explicitly;
- describe the title position, step placement, and spacing;
- create one distinct simple black line-art illustration for each step;
- preserve every required title, label, value, caption, CTA, and source exactly in quotation marks;
- keep text short, readable, and in clean sans-serif type;
- use minimal black-and-white Notion-style hand-drawn illustration;
- use thin black outlines, simple vector-like hand drawing, generous white space, and a white or very light gray background;
- include simple human figures and objects when useful, based on each step's visual_action;
- include strong negative constraints against colorful infographic, dashboard, technical architecture diagram, 3D, isometric, photorealism, clutter, and unreadable tiny text.

Process data:
[PASTE_USER_PROCESS_DATA_HERE]

Write only the final GPT Image 2 prompt.
```
