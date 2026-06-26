# Setup

Configure OpenClaw so this skill can control the logged-in browser session. Answer generation uses `curl` to call the zhihuiapi inference endpoint directly — no llm-task plugin required.

## Required OpenClaw Settings

Put the skill folder under `<workspace>/skills/zhihu-draft-writer` or point `skills.load.extraDirs` at this repository's `skills` directory.

Add a config block similar to this in `~/.openclaw/openclaw.json`:

```json5
{
  browser: {
    enabled: true,
  },
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
  skills: {
    entries: {
      "zhihu-draft-writer": {
        enabled: true,
      },
    },
  },
}
```

## Environment Variable

The skill reads the API key from the `ZHIHUIAPI_KEY` environment variable at runtime.

Set it in your shell profile (e.g., `~/.bashrc`, `~/.zshrc`, or Windows user environment variables):

```bash
export ZHIHUIAPI_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxx"
```

Keep the real key out of the repository. Never commit it to version control.

## API Endpoint

| Item | Value |
|------|-------|
| Base URL | `https://cc.zhihuiapi.top/v1` |
| Endpoint | `/chat/completions` |
| Model | `claude-sonnet-4-6` |
| Auth | `Authorization: Bearer ${ZHIHUIAPI_KEY}` |
| Format | OpenAI-compatible chat completions |

## Prerequisites

- `curl` must be available in the shell environment where OpenClaw runs.
  - macOS / Linux: pre-installed
  - Windows: available in Git Bash, WSL, or Windows 11 built-in curl

## Notes

- Log into Zhihu manually in the Chrome session that OpenClaw is allowed to control **before** using the skill. The skill will stop immediately if Zhihu shows a login wall.
- This skill does not use llm-task. Do not configure a llm-task plugin entry for this skill.
- This skill does not support automated Zhihu login and will never store or transmit your Zhihu credentials.

## Quick Verification

Run these checks before testing the full workflow:

```bash
# Confirm browser control is available
openclaw browser status --json

# Confirm curl is available and the API key is set
curl https://cc.zhihuiapi.top/v1/models \
  -s \
  -H "Authorization: Bearer ${ZHIHUIAPI_KEY}" | head -c 200
```

Confirm:
1. `browser.status` is `connected` and `hostControl` is `true`.
2. The curl command returns a JSON response without an auth error.

Then start a fresh OpenClaw session and ask it to use the `zhihu-draft-writer` skill.
