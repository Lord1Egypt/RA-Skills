---
name: zhuang-infochart-master
description: 为知识型配图、文章配图、概念解释图、流程图、数据图表和信息图创作高质量生图 Prompt，并可在用户确认后生成图片。适用于用户想把文字、数据、流程、方法论或概念做成 GPT Image 2 配图，或需要在 Web UI、2.5D isometric、墨水简约、Notion 手绘、概念卡片等风格中选择并作图的场景。
---

# Zhuang Infochart Master

## Core Workflow

Use this skill to turn a user request into a polished image-generation prompt for an information visual, then render the image if the user approves.

1. Identify the content type from the user's input.
2. If the content type is unclear, ask the user to choose from the closest options.
3. Read `references/style_catalog.md`, then show the available style schools for that content type using only the compact description and suitable use cases. Recommend one style.
4. After the user confirms the style, load the matching lean prompt file from `references/prompt_result/<content_type>/<style>.md`.
5. Use the loaded YAML frontmatter upstream-info contract and `元提示词` plus the user's material to write one final English image-generation prompt.
6. Also give the user a Chinese translation or explanation of that final prompt.
7. Ask whether to proceed with image generation.
8. After approval, create a run folder under `runs/YYYYMMDD_short-task/`, save the final prompts, and generate the image.

Never put intermediate research notes into the run folder. The run folder is for the user's concrete task: request notes, chosen route, final prompt, Chinese translation, image output, and generation metadata.

## Content Type Routing

- `数据图表`: Use when the request contains numbers, KPIs, percentages, ranking, comparison, trend, allocation, progress, survey results, or a data-backed conclusion.
- `流程图`: Use when the request describes steps, workflow, SOP, user journey, pipeline, agent chain, onboarding, review flow, or a sequence from start to finish.
- `概念解释`: Use when the request explains a concept, term, framework, model, method, argument, feature, or a set of related ideas.

If a request can fit more than one content type, explain the difference in one sentence and ask the user to confirm. Example: "这既可以做成概念解释图，也可以做成流程图；如果重点是定义和组成，选概念解释；如果重点是执行顺序，选流程图。"

## Style Selection

Read `references/style_catalog.md` before presenting style options. It contains compact content-type routing and one short entry per style. Keep the user-facing style descriptions short and practical:

- summarize the visual character;
- summarize best-fit content;
- then give your recommendation.

Do not overwhelm the user with every prompt rule. Only load the corresponding lean prompt file after the style is confirmed.

## Lean Prompt File Contract

Each file under `references/prompt_result/<content_type>/<style>.md` should contain only:

- YAML frontmatter: content type, `style_id`, display style name, and upstream information expected from the user or caller.
- Body: the actual meta-prompt used to transform the user's material into one final image-generation prompt.

Do not expect usage notes, scope notes, test conclusions, or research history in these files. Compact style-selection information belongs in `references/style_catalog.md`; research history stays in the original research workspace.

## Prompt Writing Rules

When generating the final image prompt:

- Use English for the final image-generation prompt by default.
- Preserve user-specified visible text exactly. Quote every visible text string in straight double quotes.
- Keep each `required_text` item as a complete visible text unit when the user expects the phrase to appear together.
- Keep visible text sparse and readable.
- Do not invent data, labels, steps, sources, legends, navigation, UI copy, or explanatory paragraphs.
- If the user provides Chinese visible text, keep it in Chinese inside the English prompt.
- Include the aspect ratio, composition, content hierarchy, visual style, exact visible text, and negative constraints.
- Output one final prompt, not several alternatives, unless the user explicitly asks for variations.

When reporting back to the user, include:

- `英文作图 Prompt`: the exact prompt that can be sent to the image model.
- `中文理解版`: a faithful Chinese translation or explanation for review.
- A short question asking whether to start image generation.

## Run Folder Rules

After the user approves image generation:

1. Create `runs/YYYYMMDD_short-task/` inside this skill folder.
2. Save:
   - `request.md`
   - `route.json`
   - `final_prompt_en.txt`
   - `final_prompt_zh.md`
3. Save generated images as `output.png`, `output_01.png`, etc.
4. If a script renders the image, also save `generation_request.json` and `generation_result.json`. Treat these as debug metadata; do not share them publicly because they can contain provider URLs.

Use concise lowercase English for `short-task`, for example `20260523_agent-memory-map`.

## Image Generation Order

Prefer the current AI agent's built-in image generation tool when available. Use the final English prompt exactly.

If the built-in tool returns an image file outside the run folder, copy or move the final image into the run folder before finishing.

If the current AI agent cannot generate images directly, use the bundled fallback script:

```bash
python3 scripts/render_image.py \
  --mode create \
  --prompt-file runs/YYYYMMDD_short-task/final_prompt_en.txt \
  --run-dir runs/YYYYMMDD_short-task \
  --channel fal \
  --image-size landscape_16_9
```

For image editing through the same unified command:

```bash
python3 scripts/render_image.py \
  --mode edit \
  --prompt-file runs/YYYYMMDD_short-task/final_prompt_en.txt \
  --image-url https://example.com/source.png \
  --run-dir runs/YYYYMMDD_short-task \
  --channel fal
```

The fallback script reads `config.json`. The user must fill the channel `api_key` before using that channel. All channels should expose the same command shape: mode, prompt input, channel, output run directory, image size, quality, number of images, output format, and edit reference images when needed.

## Bundled Resources

- `references/style_catalog.md`: content-type and style routing table.
- `references/prompt_result/`: final tested meta-prompts, organized by content type and style.
- `config.json`: generation channel configuration. API keys are blank by default and can be filled by the user.
- `scripts/render_image.py`: fallback renderer for fal.ai-compatible image channels.
