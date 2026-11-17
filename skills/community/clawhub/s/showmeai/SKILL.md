---
name: showmeai
description: >
  Generate and edit images, create videos, convert images to 3D, synthesize speech or music,
  and process images through ShowMeAI. Use when a user asks an Agent to create media,
  configure ShowMeAI models, inspect token-group availability, or resume a generation task.
  Before creative intake, the Agent must check category onboarding and complete it when required.
version: "2.1.0"
template: multi-scene
author: ian
homepage: https://api.showmeai.art
license: MIT
compatibility: Python 3.10+; macOS, Linux, and Windows; Agent-platform independent
triggers:
  - generate or edit an image
  - generate a video or convert an image to 3D
  - synthesize speech or music
  - upscale an image or remove its background
  - configure ShowMeAI Key, models, or generation defaults
  - inspect token-group model availability
  - resume an unfinished generation task
token_budget:
  L0_trigger: 180
  L1_core: 1800
  L2_deep: 6000
  hard_cap: 8000
metadata:
  category: creative-media
  api: ShowMeAI
---

# ShowMeAI Universal Media Skill

## Purpose

Give Agents one safe, deterministic interface for ShowMeAI creative-media generation, configuration, result download, and long-task recovery.

## Context

The Agent interprets creative intent and chooses a workflow. The Python runtime owns secrets, parameter validation, API payloads, retries, state transitions, downloads, and persistence. Do not reimplement those deterministic operations in prose or ad-hoc shell calls.

Use `python3 {baseDir}/scripts/showmeai.py`. Every command returns JSON; generated files are also emitted as `MEDIA:<absolute-path>`.

## Instructions

The following order is mandatory. The readiness check is the first action for every new media request.

1. Before asking for prompt, style, dimensions, quality, or count, run `doctor --category <requested-category>`. Never begin creative intake first.
2. If it returns `SETUP_REQUIRED`, offer the one-time Key setup. Never ask for a Key that is already configured.
3. If it returns `ONBOARDING_REQUIRED`, run `onboarding models --category <category> --json`, show the current token group's relevant models with the recommended option first, and ask the user to explicitly choose a model and supported defaults. Then persist the choice with `onboarding apply`. Do not generate until it succeeds.
4. After category onboarding is complete, silently use the saved default unless the user requests an override. Do not ask for the model again on every generation.
5. Accept a Key only through hidden interactive input or `setup --key-stdin`; never put it in arguments, config JSON, logs, or replies.
6. Treat `models` as the current Key group's view. Different token groups can expose different models. If a requested model is absent, tell the user to switch the token group or enable automatic grouping, then refresh.
7. The initial image recommendation is `gemini-3.1-flash-image`; the user's confirmed choice always wins.
8. For video, 3D, music, and image-processing tasks, keep the command alive until terminal success or failure. Do not stop after a task ID. On interruption, preserve the journal and use `tasks resume`.
9. Return downloaded local files, not only remote URLs or task IDs.

## Configuration isolation

Never create, read, or modify OpenClaw, WorkBuddy, Hermes, Codex, Claude, or another host application's config or `.env` file for ShowMeAI setup. Use only this bundled runtime. Run `paths --json` when the exact ShowMeAI-owned config, credential, and state locations are needed. Do not invent a host-specific path.

## One-time setup

Local interactive setup:

```bash
python3 {baseDir}/scripts/showmeai.py setup
```

When the user sends a Key to a trusted Agent, start this command and write the Key to standard input without echoing it:

```bash
python3 {baseDir}/scripts/showmeai.py setup --key-stdin --json
```

The Key step validates and stores the credential, then reports `needs_defaults`. In a local TTY, the wizard can immediately collect category choices. In Agent-assisted mode, continue with `onboarding models` and `onboarding apply`; `--key-stdin` must never silently complete model onboarding. See [configuration.md](references/configuration.md).

## Route requests

| Intent | Command | Read when needed |
|---|---|---|
| Setup, diagnose, list/configure models | `setup`, `doctor`, `onboarding`, `models`, `paths`, `config` | [configuration.md](references/configuration.md) |
| Generate or edit an image | `image` | [image.md](references/image.md) |
| Generate video | `video` | [video.md](references/video.md) |
| Convert image to 3D | `3d` | [three-d.md](references/three-d.md) |
| Speech or music | `tts`, `music` | [audio.md](references/audio.md) |
| Upscale or remove background | `pic` | [image-tools.md](references/image-tools.md) |
| Long-running/recoverable task | `tasks list`, `tasks resume` | [polling.md](references/polling.md) |

Use `python3 {baseDir}/scripts/showmeai.py <command> --help` for exact flags. Legacy scripts remain compatibility wrappers.

## Output

```json
{"ok":true,"data":{"kind":"image","model":"gemini-3.1-flash-image","files":["/absolute/path/result.png"]}}
```

Failures use `{"ok":false,"error":{"code":"...","message":"...","retryable":false}}`. Relay the safe message and recovery action. For success, return all files and mention any fallback model actually used. Never expose secrets.

## Output file conventions

All media is downloaded below `output.directory` (default `./showmeai-output`) in a category subdirectory. Return every absolute path from `data.files` and every `MEDIA:` line. Never overwrite an existing file. Async state belongs in the OS-native state directory.

## Notes

- A task-ID response is not a completed media result.
- The saved user model overrides the initial recommendation.
- `verify_on_use` means cataloged but not discoverable through the current Key's `/v1/models` response.
- `verified_uncataloged` means a newly discovered creative model can be selected, but its special parameters must use API defaults until cataloged.
- Image `--count` is a 1–10 output contract. The runtime may use bounded parallel single-image calls, so report the physical request count and note that each request may be billed.
- A user-specified `--max-wait` is the only normal wall-clock cutoff; otherwise keep polling through nonterminal states.

## Files

See [README.md](README.md) for the annotated distribution tree covering entry points, shared modules, data, on-demand references, and tests.

Distribution inventory: `SKILL.md`, `README.md`, `README.zh-CN.md`, `DESIGN.md`, `CHANGELOG.md`, `LICENSE`, `data/model-catalog.json`, `references/audio.md`, `references/configuration.md`, `references/image-tools.md`, `references/image.md`, `references/polling.md`, `references/three-d.md`, `references/video.md`, `scripts/gen.py`, `scripts/image_to_3d.py`, `scripts/showmeai.py`, `scripts/video_gen.py`, `scripts/showmeai_core/__init__.py`, `scripts/showmeai_core/catalog.py`, `scripts/showmeai_core/config.py`, `scripts/showmeai_core/errors.py`, `scripts/showmeai_core/http.py`, `scripts/showmeai_core/outputs.py`, `scripts/showmeai_core/paths.py`, `scripts/showmeai_core/tasks.py`, and `tests/test.py`.

## Further Reading

- [README.md](README.md) — installation, Agent handoff prompt, examples, and file tree
- [DESIGN.md](DESIGN.md) — architecture, alternatives, limitations, and decisions
- [CHANGELOG.md](CHANGELOG.md) — release history
