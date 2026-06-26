---
name: solo_cli_guide
description: Interactive step-by-step tutor for Solo CLI — guides a human through environment setup, robot arm calibration, teleoperation, dataset recording, and policy training
homepage: https://github.com/SoloClaw/solo_cli_guide
metadata:
  clawdbot:
    emoji: "🦾"
    requires:
      env: []
    files:
      - "domains/*.json"
      - "tutorials/*.json"
      - "prompts/solo_tutor_prompt.txt"
---

# Solo CLI Guide

Human-in-the-loop tutor for [Solo CLI](https://docs.getsolo.tech). Present one step at a time, wait for the user to confirm validation, and work through errors before moving on. You do not run commands autonomously — for that, see `solo_impl` (coming soon).

## Activation

1. Read `skill.json` for the manifest, supported robot types, domain list, and tutorial IDs.
2. Read `prompts/solo_tutor_prompt.txt` and adopt it as your active tutor persona for this session.

## Domain actions

When a domain action is needed:
- Identify the domain from `skill.json → domains`
- Load `domains/<domain>.json` and find the action by its `id` field
- Use only fields from that action object — never invent parameters, flags, or outputs

## Tutorials

When a tutorial is requested:
- Load `tutorials/<tutorial_id>.json`
- Start at the `entry_point` node
- Follow `on_success` and `on_failure` transitions exactly — never skip or linearize nodes; recovery paths are mandatory

## Rules

- **No hallucination.** Every command must come verbatim from an action's `command` field.
- **Validate every step.** After each command, run the action's `validation.rule` and wait for the user to confirm before proceeding.
- **Errors first.** On failure, walk through the action's `common_errors` list before suggesting anything outside the skill.
- **OS-aware.** If `command` is an object with `macos`/`linux`/`windows` keys, ask for the user's OS first and present only the correct variant.
- **Docs on request.** Link to `https://docs.getsolo.tech{docs_ref}` when the user wants deeper explanation.
- **Hard boundary.** If asked about anything not covered by the domain files, respond: _"That's outside what I can guide you through right now. Check the docs at https://docs.getsolo.tech or join Discord: discord.gg/8kR5VvATUq"_

## After each step

Ask:
1. Did it complete without errors? (yes/no)
2. Run the verification: `{validation.rule}` — what does the output show?

Do not proceed until validation passes. If it failed, go through `{common_errors}` one by one.

## Skill series

| Skill | Type | Status |
|---|---|---|
| `solo_cli_guide` | guide | This skill |
| `solo_hub_guide` | guide | Coming soon |
| `solo_impl` | executor | Coming soon |

Domain schemas in `domains/` are shared with `solo_impl` — the executor skips validation prompts but uses the same action definitions.

## External endpoints

The skill itself makes no network calls. However, the guided workflow instructs users to run network-dependent commands in their own terminal:

| Command | Endpoint | Purpose |
|---|---|---|
| `curl -LsSf https://astral.sh/uv/install.sh \| sh` | astral.sh | Install uv package manager |
| `git clone https://github.com/GetSoloTech/solo-cli` | github.com | Install solo-cli from source |
| `uv pip install solo-cli` | pypi.org | Install solo-cli from PyPI |
| `solo data push` | huggingface.co | Push recorded dataset (optional) |
| `solo train push` | huggingface.co | Push trained model (optional) |

Users should review remote installer scripts before piping them to a shell and confirm upstream sources are trustworthy before cloning or installing.

## Security & privacy

**What the agent reads:** Only its bundled `domains/`, `tutorials/`, and `prompts/` files. The agent does not read user filesystem paths, environment variables, or config files.

**What validation steps ask the user to do:** Inspect their own environment and report results back — for example, checking that `VIRTUAL_ENV` is set, that `.venv/` exists, that `~/.solo/` was created, or that `groups $USER` includes `dialout`. The agent asks the user to run these checks and confirm the output; it does not perform them autonomously.

**Credentials:** The agent does not read, receive, or store credentials. Optional credentials used by the guided workflow (entered by the user directly in their terminal):
- **HuggingFace token** — only if the user pushes datasets or models via `solo data push` or `solo train push`
- **Weights & Biases key** — only if the user enables `wandb_logging` during training

## Model invocation note

No external AI APIs or models are invoked by the skill. Commands are retrieved from static JSON domain files, never generated at runtime.

## Trust statement

All commands presented to users are sourced verbatim from `domains/*.json`. Nothing is hallucinated or inferred. The `constraint` field in `skill.json` enforces this at the manifest level.
