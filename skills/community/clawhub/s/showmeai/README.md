# ShowMeAI Universal Skill

**English | [中文](README.zh-CN.md)**

## What this is

A platform-neutral Agent Skill for image generation/editing, video, image-to-3D, speech, music, upscaling, and background removal through the ShowMeAI API. It is intended for people using Codex, Hermes, WorkBuddy, OpenClaw, or another Python-capable Agent. It is not a replacement for a ShowMeAI account or API Key.

The current version is declared in [SKILL.md](SKILL.md). Version 2.1.0 adds runtime-enforced progressive onboarding: Key validation and default-model confirmation are separate steps, and generation cannot start until the requested media category is ready.

## Core capabilities

- Default image preference: `gemini-3.1-flash-image` (Nano Banana 2). The setup wizard can select another visible model.
- Guided defaults for image, video, 3D, TTS, and music, including model-specific quantity, size, aspect ratio, resolution, quality, duration, voice, and related parameters.
- The Key is requested once, validated against `/v1/models`, and stored with restricted permissions in the operating system's application config directory.
- Long-running jobs remain active until terminal success or failure. Submitted tasks are journaled and can be resumed after an Agent or terminal interruption.
- Every successful remote result is downloaded to a predictable local path and emitted as `MEDIA:<absolute-path>`.
- Image counts from 1 to 10 are fulfilled through native batching or bounded parallel completion requests, with aggregate usage and physical request-count reporting.
- Legacy commands remain available through thin wrappers.
- First-use readiness is enforced by the runtime, not just Agent instructions. Once a category default is confirmed, later requests use it without repeatedly asking for a model.

## Requirements

- Python 3.10+
- A [ShowMeAI API Key](https://api.showmeai.art)
- No third-party Python package is required

## Quick start

1. Copy or install the repository as an Agent Skill.
2. Ask the Agent to read [SKILL.md](SKILL.md).
3. Run `python3 scripts/showmeai.py setup` once.
4. Confirm the default model and supported parameters for the first media category you use.
5. Ask for a media task or use one of the commands below.

## Trigger examples

- “Generate a 16:9 product hero image and save it locally.”
- “Animate this image into a five-second 720p video with audio.”
- “Use ShowMeAI to turn this transparent PNG into a GLB model.”
- “Configure my default image model and 2K resolution.”

## Who is this for

Use this Skill when an individual or team wants the same ShowMeAI workflow across different Agent hosts, wants a Key configured only once, or needs asynchronous media jobs to finish reliably. For direct HTTP integration inside an application server, use the ShowMeAI API documentation and a normal application client instead.

## Installation

Install or copy this Skill into any Agent's Skill directory, then ask the Agent to read `SKILL.md`. The runtime itself uses OS-native paths rather than Codex-, Hermes-, WorkBuddy-, or OpenClaw-specific paths.

Run the local wizard:

```bash
python3 scripts/showmeai.py setup
```

The local TTY wizard validates the Key, fetches models visible to its token group, and lets you choose models and supported parameters. Agent-assisted setup validates the Key first, then deliberately waits for the Agent to present model choices and save the user's explicit selection.

### Copy this setup guide to your Agent

Send the following message to a trusted Agent, followed by the Key only when it is ready to write standard input:

> Read this Skill's `SKILL.md`. Before asking about my creative prompt, run `doctor --category <requested-category> --json`. If the Key is missing, run `setup --key-stdin --json`, pass my ShowMeAI Key through standard input without echoing it or placing it in command arguments, and wait for validation. If onboarding is required, run `onboarding models --category <requested-category> --json`, show me the recommended model first plus the alternatives and supported parameters available to this Key's token group, and ask me to choose. Save my choice with `onboarding apply`. Remind me that different token groups expose different models. Do not generate before onboarding succeeds, and do not ask for the Key or model again after the category is configured unless I request a change. Never create or edit an OpenClaw, WorkBuddy, Hermes, Codex, or other host config file for ShowMeAI.

If the Agent cannot safely write to a process's standard input, run the interactive wizard yourself. Do not paste a Key into a shell command, URL, checked-in file, or public conversation.

## Token groups matter

`/v1/models` returns the models available to the current API Key's token group—not the whole ShowMeAI catalog. Different groups may expose different models. If the desired model is missing, change the token group or enable automatic grouping in the ShowMeAI console, then rerun:

```bash
python3 scripts/showmeai.py models
python3 scripts/showmeai.py doctor
```

Task-style capabilities can appear as `verify_on_use` when they are known to the local catalog but cannot be confirmed by `/v1/models`; the runtime verifies them when called.

A newly released creative ID can appear as `verified_uncataloged`: it is visible to the Key and can be selected, but its model-specific parameter schema is not bundled yet, so use API defaults until the catalog is updated.

## Configuration locations

| System | Default configuration directory |
|---|---|
| macOS | `~/Library/Application Support/ShowMeAI Skill/` |
| Linux | `${XDG_CONFIG_HOME:-~/.config}/showmeai-skill/` |
| Windows | `%APPDATA%\ShowMeAI Skill\` |

The Key is saved separately in `credentials` with owner-only permissions where supported. Non-secret preferences live in `config.json`. Override locations with `SHOWMEAI_CONFIG_DIR`, `SHOWMEAI_CONFIG_FILE`, and `SHOWMEAI_STATE_DIR`. `SHOWMEAI_API_KEY` remains the highest-priority Key source; legacy `Showmeai_API_KEY` is read for migration.

ShowMeAI never needs a host application's configuration directory. Run `python3 scripts/showmeai.py paths --json` to inspect the exact ShowMeAI-owned paths. Do not store the Key in `.openclaw`, `.workbuddy`, `.hermes`, `.codex`, or a host `.env` file.

Useful commands:

```bash
python3 scripts/showmeai.py config show
python3 scripts/showmeai.py onboarding status --category image
python3 scripts/showmeai.py onboarding models --category image
python3 scripts/showmeai.py onboarding apply --category image --model gemini-3.1-flash-image --params-json '{"n":1,"image_size":"1K","aspect_ratio":"1:1"}'
python3 scripts/showmeai.py config set defaults.image.model gpt-image-2
python3 scripts/showmeai.py config set defaults.image.params '{"n":1,"size":"auto","quality":"high","output_format":"png"}'
python3 scripts/showmeai.py setup --replace-key
```

`config set` is a low-level compatibility command. Editing a category default with it intentionally resets that category to `needs_defaults`; use `onboarding apply` to validate and confirm the new model and parameters.

## Generation examples

```bash
# Image generation; defaults to gemini-3.1-flash-image after a fresh setup
python3 scripts/showmeai.py image --prompt "A luminous city floating above clouds" --image-size 2K --aspect-ratio 16:9

# Edit one or more images
python3 scripts/showmeai.py image --prompt "Turn this into a watercolor poster" --input source.png

# Video; the process polls and downloads the completed file
python3 scripts/showmeai.py video --prompt "A paper boat crosses a moonlit lake" --resolution 720p --duration 5 --audio

# Image to 3D; transparent PNGs generally work best
python3 scripts/showmeai.py 3d --image character.png --format glb --steps 10

# Text to speech
python3 scripts/showmeai.py tts --text "Welcome to ShowMeAI" --voice alloy

# Music
python3 scripts/showmeai.py music --mode inspiration --description "Warm cinematic ambient music"

# Image tools
python3 scripts/showmeai.py pic upscale --image portrait.png --type face --scale-factor 2
python3 scripts/showmeai.py pic remove-bg --image product.png --type object
```

Add `--json` anywhere in a command for compact machine-readable output. Use `<command> --help` for the full parameter list.

The runtime treats `--count` (1–10) as an output contract for every image model. It uses a model's native count parameter when available; otherwise, or when an upstream response is incomplete, it makes bounded parallel one-image completion requests. `--concurrency` controls that cap and defaults to 4. The result reports the physical request count, and every physical request may be billed separately. The upstream service may normalize exact pixel dimensions while preserving the requested aspect ratio.

## Durable polling and recovery

Video, 3D, music, and image-tool commands do not exit merely because an API returned a task ID. They poll with a bounded backoff, print periodic heartbeats to standard error, stop only at terminal success/failure or an explicit user `--max-wait`, and download all result URLs.

Task state is persisted before polling and after every response. If the process is interrupted, resume it with:

```bash
python3 scripts/showmeai.py tasks list
python3 scripts/showmeai.py tasks resume
```

The default output root is `./showmeai-output/`, organized by media category. Existing filenames are never overwritten.

## Documentation

- [Configuration and credentials](references/configuration.md)
- [Image models and parameters](references/image.md)
- [Video workflow](references/video.md)
- [3D workflow](references/three-d.md)
- [Speech and music](references/audio.md)
- [Polling and recovery](references/polling.md)
- [ShowMeAI API documentation](https://showmeai.apifox.cn)
- [Agent instructions](SKILL.md)
- [Architecture](DESIGN.md)
- [Release history](CHANGELOG.md)

## Limitations and caveats

- Model visibility and invocation rights depend on the API Key's token group.
- Model parameters are not interchangeable; unsupported fields are filtered or rejected.
- Multi-image completion can require more than one billed API request, and an accepted custom image size may be normalized to another resolution with the same aspect ratio.
- A local runtime cannot keep polling after the host forcibly kills it, but the persisted task can be resumed.
- The Skill downloads remote media; ensure the output directory has enough storage and is appropriate for the content.

## File structure

This annotated tree is the canonical distribution-file inventory referenced by `SKILL.md`.

```text
showmeai-skill/
├── SKILL.md                 # Agent routing and mandatory behavior
├── README.md                # English user guide
├── README.zh-CN.md          # Chinese user guide
├── DESIGN.md                # Architecture and security boundaries
├── CHANGELOG.md             # Release history
├── data/
│   └── model-catalog.json   # Creative model and parameter catalog
├── references/
│   ├── configuration.md     # Setup, Key, group, and default rules
│   ├── image.md             # Image models and parameters
│   ├── video.md             # Seedance video workflow
│   ├── three-d.md           # Image-to-3D workflow
│   ├── audio.md             # TTS and music workflows
│   ├── image-tools.md       # Upscale and background removal
│   └── polling.md           # Terminal-state and recovery rules
├── scripts/
│   ├── showmeai.py          # Unified command-line entry point
│   ├── showmeai_core/       # Config, catalog, HTTP, output, task modules
│   ├── gen.py               # Legacy image compatibility entry point
│   ├── video_gen.py         # Legacy video compatibility entry point
│   └── image_to_3d.py       # Legacy 3D compatibility entry point
└── tests/
    └── test.py              # Offline contract and runtime tests
```

## Compatibility

The old `gen.py`, `video_gen.py`, and `image_to_3d.py` commands forward to the unified runtime. New projects should use `showmeai.py`.

Licensed under the MIT License.
