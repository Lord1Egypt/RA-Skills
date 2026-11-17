# Configuration and credentials

Read this reference for setup, Key errors, model visibility, or default changes. Routing rules remain in `SKILL.md`.

## Setup contract

`setup` must validate the Key with `GET /v1/models` before saving it. Interactive setup uses hidden input. Agent-assisted setup uses `--key-stdin`; the Agent writes the secret to the child process and must not echo it, put it in an argument, or retain it in a reply.

After validation, setup returns `needs_defaults` until the user explicitly confirms category defaults. A local TTY wizard can collect those choices immediately. Agent-assisted `--key-stdin` setup intentionally stops after Key validation and model discovery so the Agent can present the choices to the user instead of silently accepting defaults.

## Mandatory first-use sequence

Before creative intake, the Agent must run:

```bash
python3 scripts/showmeai.py doctor --category image --json
```

Replace `image` with `video`, `3d`, `tts`, or `music` for the requested capability. `SETUP_REQUIRED` means the Key is missing. `ONBOARDING_REQUIRED` means the Key exists but the user has not confirmed that category's model and parameters.

For Agent-guided configuration:

```bash
python3 scripts/showmeai.py onboarding status --category image --json
python3 scripts/showmeai.py onboarding models --category image --json
python3 scripts/showmeai.py onboarding apply --category image --model gemini-3.1-flash-image --params-json '{"n":1,"image_size":"1K","aspect_ratio":"1:1"}' --json
```

The model list places the recommendation first and includes each model's supported parameter schema. Ask for an explicit choice, validate only supported values, and save it with `onboarding apply`. Once complete, use the saved default without asking again unless the user requests an override.

Onboarding is progressive: an image request only requires image defaults. A later first video request configures video without asking for the Key again. Existing version-2 configurations migrate to `needs_defaults` once so their inherited defaults can be reviewed.

## Group-aware discovery

The API model list is scoped to the Key's token group. A missing model is not evidence that ShowMeAI does not support it. Tell the user to switch token groups or enable automatic grouping in the ShowMeAI console, then rerun `models` or `setup`.

Entries marked `verified` were returned by `/v1/models`. Cataloged task APIs that cannot be discovered there may be shown as `verify_on_use`.

New creative model IDs recognized from the live response but absent from the bundled parameter catalog are shown as `verified_uncataloged`. They can be selected, but the Agent must not invent model-specific parameters; use API defaults until the catalog is updated.

## Resolution order and paths

Key resolution order:

1. `SHOWMEAI_API_KEY`
2. legacy `Showmeai_API_KEY`
3. OS-native `credentials` file

The non-secret `config.json` and secret `credentials` file live under:

- macOS: `~/Library/Application Support/ShowMeAI Skill/`
- Linux: `${XDG_CONFIG_HOME:-~/.config}/showmeai-skill/`
- Windows: `%APPDATA%\ShowMeAI Skill\`

The task journal uses the corresponding state directory. `SHOWMEAI_CONFIG_DIR`, `SHOWMEAI_CONFIG_FILE`, and `SHOWMEAI_STATE_DIR` are portable overrides.

These are ShowMeAI-owned paths. Never write the Key or preferences to `.openclaw`, `.workbuddy`, `.hermes`, `.codex`, another host application's configuration, or a host `.env` file. Inspect the exact resolved paths with:

```bash
python3 scripts/showmeai.py paths --json
```

## Commands

```bash
python3 scripts/showmeai.py setup
python3 scripts/showmeai.py setup --key-stdin --json
python3 scripts/showmeai.py setup --replace-key
python3 scripts/showmeai.py doctor
python3 scripts/showmeai.py doctor --category image
python3 scripts/showmeai.py models
python3 scripts/showmeai.py onboarding status --category image
python3 scripts/showmeai.py onboarding models --category image
python3 scripts/showmeai.py onboarding apply --category image --model gemini-3.1-flash-image --params-json '{"n":1,"image_size":"1K","aspect_ratio":"1:1"}'
python3 scripts/showmeai.py paths
python3 scripts/showmeai.py config show
python3 scripts/showmeai.py config set defaults.image.model gemini-3.1-flash-image
```

`config show` exposes only a Key fingerprint. Never print the credentials file.
