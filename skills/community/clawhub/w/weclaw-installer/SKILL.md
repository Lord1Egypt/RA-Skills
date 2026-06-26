---
name: weclaw-installer
description: Automate installing and configuring the WeClaw WeChat bot environment on macOS. Use when the user asks to download/install WeClaw, set up a local Python environment with uv, or gets blocked on macOS Accessibility permissions / API key setup.
metadata:
  openclaw:
    os: ["darwin"]
    requires:
      bins: ["git", "uv", "python3"]
---

## Source repository

The installer clones this repo into a local folder named `weclaw-package-upload-test`:

- https://github.com/Popilopi168/weclaw-package-upload-test

## ClawHub

- **Slug:** `weclaw-installer`

**Why `Path must be a folder`:** The ClawHub CLI resolves paths as `resolve(workdir, <path>)`. If your current directory has **no** `.clawhub` marker, `workdir` defaults to your OpenClaw workspace (not this repo), so `skills/weclaw-installer` points nowhere.

This repo includes a `.clawhub/` folder so that when your shell `cd` is the repo root, `workdir` stays the repo.

**Publish (from repo root, recommended):**

```bash
clawhub publish skills/weclaw-installer --version 1.0.0 --slug weclaw-installer
```

**If you still see the error** (e.g. `CLAWHUB_WORKDIR` overrides), use an explicit workdir or an absolute path:

```bash
clawhub --workdir "$(pwd)" publish skills/weclaw-installer --version 1.0.0 --slug weclaw-installer
# or
clawhub publish /absolute/path/to/weclaw-installer-plugin/skills/weclaw-installer --version 1.0.0 --slug weclaw-installer
```

## When to use

Use this skill when the user wants to:
- Install / download / bootstrap the WeClaw project locally
- Set up Python dependencies with `uv`
- Configure an API key / `.env`
- Fix common macOS setup blockers (especially Accessibility permission)

## Workflow

1. Ensure prerequisites are available: `git`, `uv`, `python3`.
2. If macOS Accessibility permission is not enabled, open the System Settings page and instruct the user to enable it for the terminal/app running the automation.
3. Ask the user for the required API key if it is not already provided.
4. Run the setup entrypoint to perform the automated steps.

## Entrypoint (wrapper script)

Run:

- `python3 scripts/run_setup.py`

To pass the API key non-interactively:

- `python3 scripts/run_setup.py --api-key "<KEY>"`

After the user has enabled macOS Accessibility permission:

- `python3 scripts/run_setup.py --api-key "<KEY>" --mac-permission-confirmed`

## Safety / guardrails

- Do not request or store unrelated secrets.
- Only write `.env` / config values that are explicitly required for WeClaw setup.
- If a step fails, surface the exact error output and suggest the smallest next fix.
