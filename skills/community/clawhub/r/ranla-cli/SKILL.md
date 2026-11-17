---
name: ranla-cli
description: >-
  Drive Ranla from the terminal with ranla-cli — sign in through the browser
  (no API key to paste), run Ranla's own commands (campaign, segment, page,
  ads, reddit, …) and handle approval cards. Use when the user wants an agent
  to work their Ranla account: list or draft campaigns, build segments, check
  approvals, or anything Ranla does in chat.
license: MIT
metadata:
  author: ranla
  homepage: https://docs.ranla.ai/guides/agent-cli
  source: https://github.com/Super-Send/ranla-skills
  documentation: https://docs.ranla.ai/guides/agent-cli
---

# Ranla CLI

Run it as `npx -y ranla-cli@latest <command>` (always `@latest`), or `ranla <command>` if the user installed it globally.

## Sign in — never ask for a key

1. Run `npx -y ranla-cli@latest login`. It exits at once with JSON: `status: "pending"`, `verification_url`, `user_code`.
2. Give the user the link and the code. Ask them to open it, sign up or sign in, check the code matches, pick the workspace and approve.
3. When they say they approved, run `login` again. It finishes with `status: "signed_in"` and the workspace. The key is saved for the CLI; you never see or handle it.
4. `npx -y ranla-cli@latest whoami` confirms the person and workspace.

Never ask the user for a password or an API key, and never print, log or commit one. If `RANLA_API_KEY` is already set, the CLI uses it.

Several workspaces: each sign-in is one workspace. `workspaces list` shows them; if none is picked the CLI says so — ask the user which, then `workspaces use "<name>"`. Never pick for them. `--workspace "<name>"` uses one for a single call.

## Commands

```bash
npx -y ranla-cli@latest run help                 # every noun, its verbs, and the fields a write takes
npx -y ranla-cli@latest run help <noun>          # each verb's full input schema
npx -y ranla-cli@latest run <noun> <verb> --input '<json object>'
```

- Input is one JSON object: `--input '{…}'`, `--file input.json`, or `--input -` for stdin.
- Output is JSON when piped. Exit `0` ok, `1` failed (message on stderr), `2` wrong command line — the message lists the valid nouns, verbs or fields. Fix the call from it; don't guess.
- Read before you write. Prefer drafts and proposals.

## Approvals — the user decides

Anything that sends, publishes, posts or spends comes back as `status: "pending_approval"` with `pendingApproval.messageId`, a `summary`, and a `url` in the app. Nothing has changed yet.

- Show the user the summary and ask. Only on a clear yes: `npx -y ranla-cli@latest approvals approve <messageId>`; on a no, `approvals reject <messageId>`.
- `approvals list` shows everything waiting; `approvals get <id>` one card.
- Some cards (payout runs) can only be decided in the app; the CLI prints the link.

Ask the user before anything that costs money or sends or publishes — even when the command itself would not wait.

## Ranla's brain (model keys)

`npx -y ranla-cli@latest brain` shows whether Ranla thinks with Included or the workspace's own OpenRouter, Anthropic, OpenAI or Google key. Adding a key is the user's job: they run `ranla brain key <provider>` themselves, piping the key in. Never ask for a key in chat, never put one in a command line, and never read one out of a file to pass along.

## Sign out

`npx -y ranla-cli@latest logout` revokes the CLI's key and removes it from this computer.

Guide: https://docs.ranla.ai/guides/agent-cli
