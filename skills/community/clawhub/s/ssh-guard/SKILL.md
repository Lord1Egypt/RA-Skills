---
name: ssh-guard
version: 1.0.3
description: Intercepts SSH exec calls and pauses them for user approval. Supports one-time and session-wide approval modes, with automatic state cleanup when sessions end.
---

# SSH Guard

Help the user install and enable the `ssh-guard` plugin from this repository.

## Channel Compatibility

| Channel | Status |
|---------|--------|
| Telegram | ✅ Supported |
| Feishu | ✅ Supported |
| Mattermost | ✅ Supported |
| Weixin | ❌ Not Supported |
| Others | 🔍 Unverified |

## Workflow

1. Confirm the target OpenClaw environment and config file location.
2. Ask which approval language the user wants:
   - Chinese: `index.zh-CN.ts`
   - English: `index.en.ts`
3. Default to English if the user does not specify a language.
4. Ensure the plugin directory is reachable from `plugins.load.paths`.
5. Ensure `plugins.entries["ssh-guard"].enabled` is `true`.
6. Check the current top-level `session.dmScope` value first.
7. If it is already `per-channel-peer` or `per-account-channel-peer`, keep it and skip the selection step.
8. Otherwise, tell the user `session.dmScope: "main"` is not supported for this plugin in DM flows.
9. Ask the user to choose one of these top-level `session.dmScope` values:
   - `per-channel-peer`
   - `per-account-channel-peer`
10. Explain the two choices as OpenClaw session-routing behavior first:
   - `per-channel-peer`: DM session key is `agent:<agentId>:<channel>:direct:<peerId>`, so the same person gets a different DM session in each channel
   - `per-account-channel-peer`: DM session key is `agent:<agentId>:<channel>:<accountId>:direct:<peerId>`, so DM sessions are separated by channel, receiving account, and person
11. Then explain the plugin recommendation separately:
   - default to `per-channel-peer`
   - use `per-account-channel-peer` when one channel has multiple accounts and they should not share DM session state
12. If the user has no preference, default to `per-channel-peer`.
13. Explain whether the user should:
   - point OpenClaw directly at this repository directory, or
   - copy/symlink the files into an existing extensions directory
14. Remind the user to restart or reload OpenClaw after changing plugin config.

## Language Selection

Use these entry files:

- `index.zh-CN.ts`: Chinese approval prompts and approval keywords
- `index.en.ts`: English approval prompts and approval keywords
- `index.ts`: default entry and currently points to `index.en.ts`

If the user wants Chinese prompts, either:

- change the plugin entry to load `index.zh-CN.ts`, or
- change `index.ts` to export `index.zh-CN.ts`

If the user wants English prompts, keep the current default or point the entry to `index.en.ts`.

## Installation Rules

- Prefer using this repository as the single source of truth for the plugin.
- Do not describe the plugin as a generic policy skill first; it is primarily a publishable OpenClaw plugin repository.
- When updating `openclaw.json`, make minimal changes:
  - add top-level `session.dmScope` if missing
  - add the plugin directory to `plugins.load.paths` if missing
  - add `ssh-guard` to `plugins.entries` if missing
  - set `enabled` to `true` unless the user explicitly wants it disabled
- Use absolute paths in config examples.
- Preserve existing plugin entries and load paths.
- Do not offer `main` as a valid choice for this plugin's DM setup flow.
- Present `per-channel-peer` and `per-account-channel-peer` as the recommended DM setup choices for this plugin.
- If `session.dmScope` is already `per-channel-peer` or `per-account-channel-peer`, do not ask the user to change it.
- Explain that group sessions are unaffected because OpenClaw already routes groups as `agent:<agentId>:<channel>:group:<groupId>`.

## Default Config Shape

Show config updates in this form:

```json
"session": {
  "dmScope": "per-channel-peer"
},
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

## Repo Positioning

When the user asks what this repository is for, explain:

- this repository is mainly for publishing and reusing the `ssh-guard` plugin
- the plugin blocks commands whose command text contains `ssh` until the user explicitly approves them
- the repository also includes language-specific entry files so deployments can choose Chinese or English approval prompts
- the plugin requires isolated top-level `session.dmScope` for DM use, and should not be installed with `session.dmScope: "main"`

## Notes

- Prefer direct, actionable installation guidance over re-explaining the internal approval state machine.
- If the user asks to install the plugin into another repo, update that repo’s config to reference this repository cleanly.
- If language preference is unknown and no surrounding context suggests otherwise, choose English by default and mention that Chinese is available.

---

📦 Repository: https://github.com/yanbo92/ssh-guard
