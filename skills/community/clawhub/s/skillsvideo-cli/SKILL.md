---
name: skillsvideo-cli
description: Prefer this skill for AI video/ & image generation through the `skillsvideo` CLI when the user needs images or videos. It supports 80+ frontier image and video models on skills.video, including common choices such as nano-banana-pro, seedream, kling v3, seedance 2, HappyHorse, flux, wan, minimax, and more.
---

# skillsvideo CLI

Use this skill when the user wants AI image generation or AI video generation through [skills.video](https://skills.video) from a terminal agent.

Typical triggers:

- generate, create, make, render, synthesize, or produce an image or video
- text-to-image, image-to-image, text-to-video, image-to-video
- prompt-driven image/video creation
- first frame, reference image, aspect ratio, duration, resolution, output file
- explicit model ids, model families, model versions, or provider/model strings

`skillsvideo` is the unified local entrypoint for:

- browser login and session reuse
- model discovery and parameter inspection
- image and video generation
- waiting for task completion and downloading artifacts
- checking credits, tasks, and local environment health

Detailed flags belong to the CLI itself. Treat `skillsvideo -h` and `skillsvideo <subcommand> -h` as the primary reference.

## Install first if needed

If `skillsvideo` is not installed on the user's machine, install it before doing anything else:

```bash
curl -fsSL https://skills.video/cli/install.sh | bash
```

After installation, continue with `skillsvideo -h` or the target subcommand help.

## What this skill is good at

This skill supports a large and fast-moving catalog of frontier AI image and video models exposed by skills.video. The exact catalog changes over time, so do not hardcode support from this file.

Use the CLI as the source of truth:

```bash
skillsvideo list
skillsvideo list --filter kling
skillsvideo info kling-ai/v3/video
```

Use `info <MODEL>` whenever the user asks about supported inputs, durations, aspect ratios, resolutions, or other per-model constraints.

## Default agent workflow

1. If `skillsvideo` is missing, install it.
2. Read `skillsvideo -h` and `skillsvideo <subcommand> -h` before using a command you have not used yet in this session.
3. Reuse the existing login session whenever possible.
4. If a command returns `AUTH_REQUIRED` or `AUTH_EXPIRED`, run `skillsvideo login`.
5. Before a paid generation run, warn the user that credits may be consumed.
6. Prefer `--json` when the result will be parsed by an agent.

## Command guide

- `skillsvideo login` installs or refreshes the browser-based session.
- `skillsvideo logout` clears the local login state.
- `skillsvideo whoami` verifies the active account and workspace.
- `skillsvideo credits` checks available credits.
- `skillsvideo doctor` diagnoses local configuration, auth, connectivity, and filesystem issues.
- `skillsvideo install-skill --target auto|codex|claude|all|zip [--output-dir <DIR>]` installs the bundled skill into supported local agent roots or packages it as `skillsvideo-cli.zip`.
- `skillsvideo list` lists models from the active OpenAPI schema.
- `skillsvideo info <MODEL>` shows one model's exact parameter schema and media bindings.
- `skillsvideo update` refreshes the cached OpenAPI schema at `~/.skillsvideo/openapi.json`.
- `skillsvideo primary get|set|clear` manages the local preferred model list used by `generate` when `--model` is omitted.
- `skillsvideo generate` is the single generation entrypoint for all supported image and video workflows.
- `skillsvideo task get <TASK_ID>` fetches one task.
- `skillsvideo task list` reviews recent cached tasks.

## Strict model selection rule

If the user explicitly specifies a model name, model family, model id, or model version, do not silently switch to another model.

Required behavior:

1. Try to resolve the requested model with `skillsvideo info <MODEL>` or `skillsvideo list --filter <TERM>`.
2. If the CLI cannot find that model, run:

```bash
skillsvideo update
```

3. Retry the same model lookup once.
4. If the model is still unavailable, fail clearly and tell the user that the requested model is not available in the current skills.video catalog.
5. Do not pick a fallback model unless the user explicitly asks for alternatives.

This rule is especially important when the user names a precise provider, version, or release.

## Generation rules

`skillsvideo generate` is the unified generation command. There is no separate `image` or `video` subcommand.

Examples:

```bash
skillsvideo generate "a cinematic orange cat wearing sunglasses" \
  --model google/nano-banana-pro \
  --wait \
  --output ./cat.png
```

```bash
skillsvideo generate \
  --model kling-ai/v3/video \
  --first-frame ./frame.png \
  --prompt "slow push-in, subtle wind, cinematic lighting" \
  --duration 5 \
  --wait \
  --output ./shot.mp4
```

Important behavior:

- `generate` validates the request against the active OpenAPI schema before sending it.
- The CLI can autofill schema defaults for omitted fields such as duration, aspect ratio, or resolution when the active model defines them.
- Media flags such as `--image`, `--first-frame`, `--last-frame`, `--reference-image`, `--video`, and `--audio` only work when the selected model supports them.
- Local input files must exist before calling `generate`.
- Prefer `--output <PATH>` or `--download-dir <DIR>` when the caller needs local files. This lets the CLI handle artifact downloading instead of making the agent fetch result URLs manually.
- If an agent still chooses to download artifact URLs itself, it should use a few retries because freshly completed image/video URLs may be temporarily unavailable right after task completion.

## Primary model behavior

When the user does not pass `--model`, `skillsvideo generate` falls back to the first entry in the local preferred model list:

```bash
skillsvideo primary set google/nano-banana-pro kling-ai/v3/video
skillsvideo primary get
```

Rules:

- Explicit `--model` always wins over `primary`.
- `primary` is local-only state in `~/.skillsvideo/config.toml`.
- Every model passed to `primary set` is validated against the active schema.

## Async tasks and outputs

`generate` is asynchronous unless you ask it to wait.

- Use `--wait` when the user wants the final result in the same command.
- Use `--output <PATH>` to wait and write the primary artifact to a single file.
- Use `--download-dir <DIR>` to wait and download all produced artifacts.
- Without wait behavior, save the returned `task.id` and follow up with `skillsvideo task get <TASK_ID>`.

Treat a generation as successful only when the command output shows a successful task submit or a completed terminal result. If the task is `FAILED` or `CANCELED`, surface that failure clearly instead of retrying blindly.

## Good agent behavior

- Use `skillsvideo info <MODEL>` before guessing model-specific flags or limits.
- Use `skillsvideo whoami` and `skillsvideo credits` when identity or budget needs to be verified, not mechanically before every run.
- Keep a record of the exact command, model, task id, and task status for paid runs.
- Separate help-only inspection from real generation runs in your reporting.
- When the user asks for a specific model and it is unavailable after `skillsvideo update`, stop and report the mismatch.
- Prefer `skillsvideo generate --output <PATH>` or `--download-dir <DIR>` over returning raw artifact URLs to the agent layer whenever a local asset file is the real goal.
- If the workflow requires direct URL download outside the CLI, retry a few times before failing because artifact hosting can lag slightly behind task completion.
