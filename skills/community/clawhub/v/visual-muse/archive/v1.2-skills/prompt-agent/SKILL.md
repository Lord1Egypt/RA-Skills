---
name: prompt-agent
description: "将中文创意需求转换为 SDXL 或 Flux 可用的高质量英文图像提示词。当用户要求生成图片、画一张图、出图、AI绘画时触发。"
metadata: { "openclaw": { "emoji": "🎨" } }
---

# Prompt Agent

将用户的中文需求转成可执行的英文 prompt。

## 第一步：读取风格模板库

```bash
cat /home/node/.openclaw/workspace/prompt-templates.json
```

根据用户需求匹配最合适的风格模板。匹配规则：
- 用户说"电影感/电影风" → cinematic
- 用户说"动漫/二次元/卡通" → anime
- 用户说"写实/照片/真实" → photorealistic
- 用户说"概念艺术/概念图" → concept_art
- 用户说"水彩" → watercolor
- 用户说"油画" → oil_painting
- 用户说"赛博朋克" → cyberpunk
- 用户说"奇幻/魔幻" → fantasy
- 用户说"复古/昭和/怀旧" → vintage
- 用户没指定风格 → cinematic（默认）

## 第二步：结构化拆解（6维）

收到需求后，先拆解为以下 6 个维度，并分别产出英文关键词：
- `subject`：画面中心主体（人物/动物/物体）
- `environment`：场景地点（街道、森林、室内等）
- `style`：画风、年代感、材质质感
- `lighting`：时间与光线（晨光、霓虹夜景、逆光等）
- `camera`：景别、角度、镜头（close-up, wide shot, low angle, 35mm）
- `mood`：氛围与情绪（nostalgic, tense, dreamy, warm）

组合顺序：`subject -> environment -> style -> lighting -> camera -> mood`。

## 第三步：权重控制规范

- 用户强调元素（如“重点是XXX”）必须加权：`(keyword:1.4)` 到 `(keyword:1.5)`
- 重要但非核心元素：`(keyword:1.2)` 到 `(keyword:1.3)`
- 需要弱化元素：`(keyword:0.7)` 到 `(keyword:0.9)`
- SDXL 使用关键词+权重格式；Flux 使用自然语言段落，但仍可对核心词做轻量加权。

## 第四步：负向 prompt 模板库

先写通用排除，再拼接风格专用排除。

- 通用排除（必须包含）：
  `bad anatomy, bad hands, blurry, watermark, text, logo, deformed`
- 写实风格额外排除：
  `cartoon, anime, illustration, painting`
- 动漫风格额外排除：
  `photorealistic, photo, 3d render`
- 复古风格额外排除：
  `modern, digital, clean, sharp`

## 第五步：用户意图确认机制

当需求模糊时先确认，再出最终 prompt。

- 触发“模糊需求”条件：
  - 用户输入少于 10 个字，且
  - 未明确风格词（如动漫、写实、赛博朋克、复古等）
- 模糊需求处理：
  1. 先输出 6 维拆解草案
  2. 询问：`这样理解对吗？`
  3. 用户确认后再输出最终 JSON
- 明确需求处理：
  - 输入超过 10 个字，或已指定风格，直接输出 JSON

## 第六步：输出 JSON

只输出 JSON，不附加解释。

```json
{
  "positive": "结构化组合后的英文 prompt",
  "negative": "通用负向 + 风格负向",
  "model": "sdxl",
  "style": "匹配到的风格名",
  "recommended_checkpoint": "模板推荐的checkpoint",
  "style_tags": ["标签1", "标签2"],
  "decomposition": {
    "subject": "...",
    "environment": "...",
    "style": "...",
    "lighting": "...",
    "camera": "...",
    "mood": "..."
  }
}
```

## 禁止事项

- 不输出 markdown 代码块
- 不输出解释或前言
- 不使用空泛词
- 不给出互相冲突的风格指令（如同时强调 realistic 与 anime）
