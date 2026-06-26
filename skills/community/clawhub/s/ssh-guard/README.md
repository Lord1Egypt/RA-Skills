# ssh-guard

[中文](./README.zh-CN.md)

`ssh-guard` is a standalone repository that contains both:

- the original OpenClaw plugin source: `index.ts` + `openclaw.plugin.json`
- localized plugin implementations: `index.zh-CN.ts` and `index.en.ts`
- a matching skill definition: `SKILL.md`

Its purpose is simple: require explicit approval before any command containing `ssh` is executed.

## Channel Compatibility

| Channel | Status |
|---------|--------|
| Telegram | ✅ Supported |
| Feishu | ✅ Supported |
| Mattermost | ✅ Supported |
| Weixin | ❌ Not Supported |
| Others | 🔍 Unverified |

## Example Flow

When a user asks OpenClaw to run an SSH command, `ssh-guard` blocks it first and forces an explicit approval step.

Blocked command:

```text
I need to run an SSH command to inspect the remote machine's resource usage. Please confirm before I continue.
```

```bash
sshpass -p '<REDACTED_PASSWORD>' ssh -o StrictHostKeyChecking=no <REDACTED_USER>@<REDACTED_HOST> "uptime && echo '---' && free -h && echo '---' && df -h"
```

```
Reply with one of: allow / approve / proceed / yes
For session-wide approval, reply: I understand the risk. Allow all SSH commands for this session.
```

## Why

Running `ssh` from an agent is higher risk than ordinary local operations. A single command can modify a remote machine, exfiltrate data, or lock a user out of a host.

`ssh-guard` adds an explicit approval checkpoint before those commands run, so SSH access is never treated as a casual default.

## Features

- Block commands containing `ssh` before execution until the user explicitly approves them
- Support one-time approval and session-wide approval flows
- Keep approval state scoped to the current session and inherited sub-agents
- Clear approval state automatically when a session or sub-agent ends
- Provide localized approval prompts through `index.zh-CN.ts` and `index.en.ts`
- Work as a publishable OpenClaw plugin repository and as an install/configuration skill source

## How It Works

1. The plugin listens to OpenClaw tool-call hooks.
2. When it detects an execution request whose command contains `ssh`, it blocks the call.
3. It asks the user for explicit approval using the configured language variant.
4. After approval, it allows either:
   - a single SSH execution, or
   - all SSH executions for the current session
5. It clears approval state when the session or sub-agent ends.

## Quick Start

1. Choose the language variant:
   - Chinese: keep `index.ts` as-is or point to `index.zh-CN.ts`
   - English: point the plugin entry to `index.en.ts`, or change `index.ts` to export it
2. Set top-level `session.dmScope` in `openclaw.json`.
   - Do not use `main` for `ssh-guard`
   - Choose one of: `per-channel-peer`, `per-account-channel-peer`
   - Recommended default: `per-channel-peer`
3. Add this repository path to `plugins.load.paths` in `openclaw.json`.
4. Enable `ssh-guard` in `plugins.entries`.
5. Restart or reload OpenClaw.

## Repository Layout

```text
ssh-guard/
├── index.ts
├── index.en.ts
├── index.zh-CN.ts
├── openclaw.plugin.json
├── SKILL.md
├── README.md
└── README.zh-CN.md
```

## Use As An OpenClaw Plugin

Add this directory to `plugins.load.paths` in `openclaw.json`, then enable `ssh-guard` in `plugins.entries`:

```json
"plugins": {
  "load": {
    "paths": [
      "/absolute/path/to/ssh-guard"
    ]
  },
  "entries": {
    "ssh-guard": {
      "enabled": true
    }
  }
}
```

`ssh-guard` depends on isolated DM session routing. Do not use top-level `session.dmScope: "main"` with this plugin.

Choose one of these two values instead:

- `per-channel-peer`
  OpenClaw builds direct-message session keys as `agent:<agentId>:<channel>:direct:<peerId>`.
  This means one person gets a separate direct-message session in each channel. The same user talking over Telegram and another channel will not share the same DM session.
- `per-account-channel-peer`
  OpenClaw builds direct-message session keys as `agent:<agentId>:<channel>:<accountId>:direct:<peerId>`.
  This means OpenClaw separates DM sessions not only by channel and person, but also by the receiving account. Use this when one channel has multiple bot/accounts and each account should keep its own DM session history.

For `ssh-guard`, `per-channel-peer` is the usual default, and `per-account-channel-peer` is the safer choice when multiple accounts exist on the same channel.

Why `main` is not supported:

- with `main`, OpenClaw may route direct-message tool calls to `agent:main:main`
- `ssh-guard` approval replies are keyed from the inbound conversation id
- those two keys do not match in DM flows, so approval can fail to bind to the blocked command

This limitation applies to direct messages. Group sessions already route as `agent:<agentId>:<channel>:group:<groupId>`, so group approval stays keyed by the group id.

`index.ts` currently re-exports the English implementation from `index.en.ts`.
If you want the Chinese approval prompts instead, point the plugin entry to `index.zh-CN.ts` or swap the root export before loading it.

## Use As A Skill

Load `SKILL.md` through your skill directory or package this repository as a skill source. Once triggered, the agent should help the user install and configure this plugin, including the language variant.
