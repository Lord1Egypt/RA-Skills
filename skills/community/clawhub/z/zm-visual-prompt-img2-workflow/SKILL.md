---
name: zm-visual-prompt-img2-workflow
version: 1.0.0
description: ZM IMG2 视觉提示词编排。用于把漫画页、PPT 主视觉、封面/配图等结构化视觉需求，编译为可执行的 happy/gpt-image-2 提示词，并检查参考图、主角图、风格、禁止项和 IMG2 生产证据。
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      bins:
        - python3
      skills:
        - zm-img2-generation-direct
---

# Visual Prompt Compiler IMG2

This skill is a thin compiler and evidence wrapper for comic image generation. It does **not** call Responses/Codex image tools. Actual image creation is delegated to:

```bash
python3 skills/zm-img2-generation-direct/scripts/run.py
```

With reference images present, that direct skill routes to `/images/edits` on the configured Happy OpenAI-compatible image provider (`https://sub2api.happyhourse.cn/v1`, model `gpt-image-2`).

## Purpose

Use this when a comic page has a long editorial brief but the image API needs a short, hard, clear prompt.

The compiler accepts structured JSON/YAML or CLI fields:

- `page_id`
- `title`
- `scene`
- `dialogues` / `dialogue`
- `screen_text`
- `reminder`
- `characters`
- `forbidden`
- `style_ref_text`
- `reference_images`

It produces a concise prompt, normally about 200-500 Chinese/English characters for simple comic pages, and avoids embedding long review standards.

## Reference image policy

Default behavior is minimal:

- use only explicit character reference images from `reference_images`;
- do **not** add a style page image by default;
- optional `--style-image <path>` can add one style reference, for example P1;
- reject any input image whose path/name matches a forbidden term, such as `P2`;
- require non-empty `input_images` by default (`--require-character-refs`, default true);
- cap input images with `--max-input-images`, default `2`.

## Artifacts

Each compiler run creates a directory under:

```text
<openclaw-home>/generated-images/zm-visual-prompt-img2-workflow/_compiler_runs/<task>-<timestamp>/
```

Artifacts:

- `compiled_prompt.txt`
- `request.json`
- `result.json`
- `run_command.md`
- `stdout.txt`
- `stderr.txt`
- `summary.json`

For actual runs, `summary.json` also points to the underlying `zm-img2-generation-direct` run directory and output image.

## Dry-run

Compile and validate only:

```bash
python3 skills/zm-visual-prompt-img2-workflow/scripts/compile_and_run.py \
  skills/zm-visual-prompt-img2-workflow/examples/ai_hallucination_p03.json \
  --task-name ai-hallucination-p03-compiler-test \
  --dry-run
```

Check:

```bash
cat <openclaw-home>/generated-images/zm-visual-prompt-img2-workflow/_compiler_runs/<run>/compiled_prompt.txt
cat <openclaw-home>/generated-images/zm-visual-prompt-img2-workflow/_compiler_runs/<run>/summary.json
```

## Actual img2img run

Single attempt, 600000ms timeout:

```bash
python3 skills/zm-visual-prompt-img2-workflow/scripts/compile_and_run.py \
  skills/zm-visual-prompt-img2-workflow/examples/ai_hallucination_p03.json \
  --task-name ai-hallucination-p03-compiler-test \
  --run \
  --timeout-ms 600000 \
  --max-attempts 1
```

Expected proof for acceptance:

- `summary.json.ok: true`
- `summary.json.used_direct_endpoint_actual: /images/edits`
- `summary.json.actual_mode: edit`
- `summary.json.input_images` contains only the cat and husky references;
- no `P2`, no logo/QR/lobster/OpenClaw input image;
- underlying `result.json` has `provider: happy`, `model: gpt-image-2`, `mode: edit`, `input_images` populated.

## Lightweight checks

```bash
python3 -m py_compile skills/zm-visual-prompt-img2-workflow/scripts/compile_and_run.py
python3 skills/zm-visual-prompt-img2-workflow/scripts/compile_and_run.py --help
python3 skills/zm-visual-prompt-img2-workflow/scripts/compile_and_run.py \
  skills/zm-visual-prompt-img2-workflow/examples/ai_hallucination_p03.json --dry-run
```

## Notes

- This skill has no delivery/upload behavior.
- It does not mutate `zm-img2-generation-direct`.
- It intentionally favors short prompts and minimal references to reduce slow or interrupted upstream requests.
