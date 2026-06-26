# Strict Text/Image Turn Separation Policy

Version: 1.0.0

This policy is mandatory for this guide and for every generated specialized figure-making skill.

## Core rule

A single assistant response must be exactly one of:

- `TEXT_ONLY`: prose, planning, analysis, critique, prompt writing, state update, confirmation request.
- `IMAGE_ONLY`: ChatGPT web **Create image** through **ChatGPT Images 2.0**, or Codex `$imagegen` first, or ChatGPT Images 2.0 API / another approved image-generation API only when `$imagegen` is unavailable. No prose, no state footer, no caption, no explanation, and no SVG/Mermaid/TikZ/Graphviz/HTML-CSS/canvas/matplotlib/code-generated diagram substitute. Native image results may be returned/exported by the host as bitmap files such as PNG, JPEG, JPG, or WebP.

A response that first writes text and then generates an image is invalid. A response that generates an image and then adds explanatory text is invalid.

## First reply / startup gate

The first assistant reply after a skill is triggered must always be `STARTUP_PLAN_ONLY`, which is a strict `TEXT_ONLY` submode.

Even if the user's first message says “直接出图”, “生成 6 张图”, “继续生成候选图”, or provides enough material to make an image, the first assistant reply must not call image generation. It must only show the workflow/startup plan, record the received material as pending, and ask the user to continue or confirm.

For generated specialized skills, the first-trigger example, default prompt, and starter messages must preserve this boundary. They may mention that image generation is pending, but they must not include image markdown, an `$imagegen` call, an `IMAGE_ONLY` action, or any generated image artifact in the first assistant response.

## Text turn stop rule

If an assistant turn emits any visible prose, markdown, table, YAML state, caption, prompt, or next-step help, it must stop before image generation. It may propose the next image batch, but it must not invoke image generation in that same response.

Use wording such as:

> 我已经准备好生成 6 张候选图。请回复“生成 6 张候选图”，下一轮我将只出图，不夹杂文字。

At visual decision points, the text turn should recommend 4 / 5 / 6 generated candidate images, defaulting to 6, when image comparison would help. If the text reply presents multiple schemes, layouts, styles, or prompt options, the final next-step prompt must prefer asking the user to generate/display multiple candidate images or schematic boards instead of deciding from text alone. It must also state that ChatGPT web uses **Create image** through **ChatGPT Images 2.0**, Codex uses `$imagegen` first, and if `$imagegen` is unavailable Codex uses ChatGPT Images 2.0 API or another approved image-generation API. Native bitmap outputs such as PNG/JPEG/WebP are allowed, and SVG, Mermaid, or code-rendered diagrams/files are not.

## Image turn purity rule

If the user has explicitly requested image generation and the state is sufficient, the next assistant turn may be `IMAGE_ONLY`. That turn must contain only the native image generation action. It must not include a plan, status footer, caption, critique, or textual explanation.

If native image generation is unavailable, do not replace the `IMAGE_ONLY` turn with SVG, Mermaid, HTML/CSS, canvas, plotting-library, or code-drawn figures. Stop in a `TEXT_ONLY` turn and provide a copyable imagegen/API prompt handoff.

## Generated-skill requirements

Every generated specialized figure-making skill must include these rules in:

- `SKILL.md` operating contract;
- workflow/state contract;
- prompt/rendering policy;
- startup example;
- state footer template;
- release checklist.

A generated skill is not production-locked if its first-trigger path can produce an image, or if any template permits text and image generation in the same response.

Release validation must include an adversarial startup case where the user asks to generate images immediately. Passing output is startup text only. If the generated skill emits any image in that first response, lock validation fails.
