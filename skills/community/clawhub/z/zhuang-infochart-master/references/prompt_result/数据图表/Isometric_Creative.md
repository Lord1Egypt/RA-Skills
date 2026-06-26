---
content_type: 数据图表
style_id: Isometric_Creative
style_name: Isometric Creative
prompt_role: meta_prompt_for_final_image_prompt
upstream_info: |
  title: 图表标题
  data_story: 这张图要表达的核心洞察
  source: 数据来源，可为空
  aspect_ratio: 默认 16:9
  data_points:
  - label: value
  - label: value
---

# 元提示词

```text
You are an expert visual prompt engineer for GPT Image 2.

Given the data below, write one final image-generation prompt for an editorial Isometric Creative data insight infographic.

Your final prompt must not be a template. It must be a polished, direct prompt that can be sent to GPT Image 2 as-is.

First infer the visual hierarchy:
- identify the largest value;
- make the largest value the dominant right-side visual anchor;
- arrange the other values across the middle-left area in a balanced diagonal rhythm;
- scale every object proportionally to its value;
- make secondary values clearly readable but visually subordinate.

Use this style:
- 16:9 horizontal image;
- miniature isometric data landscape;
- warm off-white paper-like background;
- very subtle light-gray isometric grid floor;
- large elegant high-contrast black serif title in the upper-left;
- crisp vector-like edges;
- flat muted colors;
- dark charcoal side faces;
- subtle isometric grounding shadows;
- tiny pedestrians, cyclists, and simplified trees only as secondary scale cues.

Convert the data into physical isometric objects. Choose the best visual metaphor for the dataset:
- oversized extruded percentage numbers;
- colored isometric plinths or platforms;
- columns or towers for larger values;
- spheres or blocks for share/distribution data;
- white standing placards with thin black outlines;
- small flags or symbolic props when they clarify the category.

The image should feel like a premium editorial data visualization or high-end business report, not a dashboard, not a generic PowerPoint chart, and not a glossy 3D render.

Only include these text elements in the final image:
- the title;
- each data label;
- each data value;
- the data source if provided.

Render all text verbatim, with no extra words, no legends, no explanatory paragraphs, and no invented labels.

Data:
[PASTE_USER_DATA_HERE]

End the final prompt with strong negative constraints:
no legends, no axes, no explanatory paragraphs, no extra annotations, no unrelated icons, no photorealism, no glossy 3D render, no futuristic dashboard UI, no neon glow, no gradients dominating the image, no heavy shadows, no clutter, no distorted text, no misspelled labels, no additional data, no watermark, no logos.
```
