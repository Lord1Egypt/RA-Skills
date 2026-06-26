# Security And External Access

Language switch: English | [中文说明](./security.md)

This document is a quick audit guide for users, reviewers, and programmatic callers who want to know what `audiobook` reads, what it sends out, and which actions may incur billing.

## Runtime Requirements

`audiobook` currently declares and actually depends on the following runtime requirements by default:

- environment variable: `STEP_API_KEY`
- system binary: `ffmpeg`
- system binary: `ffprobe`

These requirements are now also declared in the `SKILL.md` frontmatter under `metadata.openclaw.requires` so the ClawHub / OpenClaw registry metadata stays aligned with the human-readable docs.

## Default External Endpoints

If you do not manually override any `base_url`, the default external targets are Step endpoints only:

- `scripts/sync_voice_library.py`
  - `https://api.stepfun.com/v1/audio/system_voices`
  - `https://api.stepfun.com/v1/chat/completions`
- `scripts/step_tts_client.py` / `scripts/synthesize_tts_requests.py`
  - `https://api.stepfun.com/v1/audio/speech`
- `scripts/clone_selected_voices.py`
  - `https://api.stepfun.com/v1/files`
  - `https://api.stepfun.com/v1/audio/voices`
- `scripts/llm_json.py` for structured-script generation, casting, and other reasoning steps
  - default: `https://api.stepfun.com/step_plan/v1/chat/completions`

## When A Non-default Endpoint Can Be Used

The following cases are explicit user-directed overrides, not default skill behavior:

- you change `llm.*.base_url` inside `voice-library.yaml`
- you pass `--base-url` to scripts that expose it
- you pass `--api-key-env` to the synthesis path so a different environment variable name is used

In other words: the default configuration points to Step endpoints; only your own config or CLI overrides can redirect traffic to another compatible service.

## Environment Variables Read By Default

By default, the skill only requires and reads:

- `STEP_API_KEY`

Additional notes:

- `scripts/run_audiobook.py` and `scripts/synthesize_tts_requests.py` support `--api-key-env`, which lets you explicitly choose a different environment variable name.
- That does not mean the skill automatically enumerates many secrets from the environment; it reads only the key name you specify.
- The current templates, docs, and default configuration all assume `STEP_API_KEY`.

## File Read / Upload Scope

`audiobook` does not automatically crawl the whole disk and does not bundle arbitrary workspace files for upload.

It mainly works with explicitly provided inputs such as:

- the story text file you point it at
- reference audio files you place into `audiobook-library/voices/inbox/`
- clone reference audio paths registered in `voice-library.yaml`
- intermediate and final outputs under the current story run directory

The only file that gets uploaded to Step is the specific reference audio chosen for a real paid clone. That upload happens inside `scripts/clone_selected_voices.py` and only for the selected `asset_id`.

## Paid-action Boundary

The only action that may incur billing is the real Step voice cloning step:

- `scripts/run_audiobook.py` performs clone preview only and does not automatically trigger a real paid clone
- `scripts/clone_selected_voices.py --dry-run` is preview-only and does not call the real paid cloning path
- a real clone requires all of the following:
  - `voice-library.yaml -> clones.<asset_id>.selected_for_clone = true`
  - no `--dry-run`
  - an explicit `--confirm-paid-action`

If the last confirmation flag is missing, the script exits with an error before the paid API call is made.

## Recommended Safe Validation Flow

Before first use or before publishing, it is safer to validate the skill like this:

1. use a test key, limited-scope key, or a key you are ready to rotate
2. run it in an isolated environment, container, or separate workspace first
3. run `clone_selected_voices.py --dry-run` before any real clone
4. inspect `voice-library.yaml` and make sure nothing unexpected is marked for upload or cloning
5. rotate the key after testing if the environment was not fully trusted

## Reviewer Quick Checklist

If you are doing a fast audit, focus on these files first:

- `scripts/common.py` for API key loading and source reporting
- `scripts/sync_voice_library.py` for official voice sync and `step-audio-r1.1` analysis targets
- `scripts/clone_selected_voices.py` to confirm `--confirm-paid-action` is still required
- `scripts/step_tts_client.py` to confirm TTS requests still target the expected TTS endpoint
- `scripts/run_audiobook.py` to confirm it still performs clone dry-run preview only
