## Setup

Use the platform token issued by this platform.

Get the token from:
- `http://easyclaw.bar/shuziren/user/`

Preferred environment variables:

```json
{
  "EASYCLAW_PLATFORM_API_TOKEN": "your platform token"
}
```

Optional base URL override:

```json
{
  "EASYCLAW_PLATFORM_API_TOKEN": "your platform token",
  "EASYCLAW_PLATFORM_BASE_URL": "http://easyclaw.bar/shuzirenapi"
}
```

Compatible fallback names are also supported:
- `CHANJING_PLATFORM_API_TOKEN`
- `CHANJING_PLATFORM_BASE_URL`
- `EASYCLAW_PLATFORM_API_KEY`
- `EASYCLAW_PLATFORM_API_SECRET`
- `CHANJING_PLATFORM_API_KEY`
- `CHANJING_PLATFORM_API_SECRET`

Rules:
- Configure the token in the skill environment
- Do not modify OpenClaw core code or `openclaw.json` to inject this skill configuration
- The watcher command will carry the auth arguments it needs from the skill execution context
