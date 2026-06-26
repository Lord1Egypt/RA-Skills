---
name: psd-automator
description: Automate PSD text replacement on Mac and Windows with Photoshop, dry-run safety, style-lock checks, rollback, and local PSD index cache. Use when requests include file/path hints, layer name, and replacement text from chat channels (including DingTalk) and require no popup dialogs.
metadata: { "openclaw": { "emoji": "🖼️", "skillKey": "psd-automator" } }
---

# PSD Automator

Cross-platform PSD text automation for teams using both macOS and Windows.

## Scope

- Phase 1 + 2 only.
- Screenshot understanding is intentionally out of scope.
- Uses one task protocol and two execution engines:
  - macOS: AppleScript (`osascript`)
  - Windows: Photoshop COM (PowerShell)

## Task Protocol

Read [references/task-schema.json](references/task-schema.json) before running.

Minimal required fields:

- `taskId`
- `input.edits[]` (`layerName` + `newText`)
- `input.exactPath` or `input.fileHint`

Key optional fields:

- `workflow.sourceMode`: `inplace` or `copy_then_edit`
- `output.exports[]`: PNG export (`mode=single` or `mode=layer_sets` for sliced/block assets)
- `output.bundle.zipName`: zip name for sliced assets bundle
- `options.pathBridgeMode`: `auto` / `always` / `off` (macOS Unicode path bridge)
- `options.bundleZip`: whether to bundle `layer_sets` PNGs into one zip
- `options.matchImagePath`: screenshot path for selecting most similar exported slice

## Build and Refresh PSD Index

Create or refresh local cache:

```bash
node skills/psd-automator/scripts/build-index.js \
  --root "/Projects/Design" \
  --root "/Users/me/Desktop/assets" \
  --index "~/.openclaw/psd-index.json"
```

Incremental refresh:

```bash
node skills/psd-automator/scripts/build-index.js --incremental
```

## Run a Task

Dry-run first (recommended):

```bash
node skills/psd-automator/scripts/run-task.js \
  --task "skills/psd-automator/examples/task.mac.json" \
  --dry-run
```

Execute:

```bash
node skills/psd-automator/scripts/run-task.js \
  --task "skills/psd-automator/examples/task.mac.json"
```

Natural-language dispatch (through OpenClaw chat command, supports `.psd` and `.psb`):

```text
/psd design-mac-01 帮我找到20260225工位名牌.psd或20260225工位名牌.psb，把姓名改成琳琳，座右铭改成步履不前，稳步前进，保存成png放置在桌面 --dry-run
```

## DingTalk image handoff (required)

When replying in DingTalk and task execution is successful with PNG output, the final response MUST include this marker with an absolute path:

```text
[DINGTALK_IMAGE]{"path":"<absolute_png_path>"}[/DINGTALK_IMAGE]
```

Rules:

- Use absolute path only (for example `/Users/name/Desktop/xxx.png`).
- Do not use filename-only values.
- If `pngOutputPath` (or first item in `pngOutputPaths`) is missing, clearly report failure and do not emit a fake marker.
- For `mode=layer_sets`, `pngOutputPaths` should contain all exported block images in the output folder.
- When available, use `selectedPngPath` as the single best-match image for screenshot workflows.
- When available, send `bundleZipPath` as file attachment: `[DINGTALK_FILE]{"path":"<absolute_zip_path>","fileName":"<name>.zip","fileType":"zip"}[/DINGTALK_FILE]`.
- Keep normal human-readable summary, then append marker on a new line at the end.

## OpenClaw Routing Pattern (Phase 2)

Use OpenClaw subagent routing guidance:

- [references/openclaw-subagent-routing.md](references/openclaw-subagent-routing.md)

Core idea:

1. Main agent parses request.
2. Resolve target machine + platform capabilities.
3. Spawn/dispatch to target subagent.
4. Subagent runs `run-task.js` locally.
5. Return normalized result + audit log.

## Safety Baseline

- Always support `dryRun`.
- Keep style lock (`font` and `size`) after text changes.
- Disable Photoshop dialogs.
- Create `.bak` backup before write.
- Stop on ambiguous file matches (`E_FILE_AMBIGUOUS`); never guess silently.
- On layer-not-found, return `availableLayers` + `suggestedLayers`.
- Emit standardized error codes from [references/error-codes.md](references/error-codes.md).
