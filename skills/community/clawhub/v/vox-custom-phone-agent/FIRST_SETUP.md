# First Setup

## Vox Platform Requirements

Before real calls can work, the Vox account behind `VOX_APP_ID` and `VOX_SECRET` must be enabled by TeddyMobile Vox.

Checklist:

- Enterprise account is registered and approved.
- Outbound API permission is enabled.
- `botType=custom` is enabled.
- Server egress IP is in the Vox IP whitelist.
- Account has available outbound quota and number resources.
- Server clock is accurate for GMT HMAC signing.

## Environment Variables

Minimum:

```text
VOX_APP_ID=...
VOX_SECRET=...
```

For local development, create `.env` from `.env.example` and keep it private. Do not publish `.env` or real credentials with the skill package.

Optional:

```text
VOX_BOT_ID=
VOX_OUTBOUND_BASE_URL=https://vox.teddymobile.cn
VOX_CREDENTIALS_FILE=/secure/path/credentials.json
SKILL_API_TOKEN=change-me
VOX_TRIAL_MODE=true
VOX_TRIAL_LIMIT=10
VOX_TRIAL_STATE_FILE=/secure/path/trial-state.json
```

## Credential File Alternative

Create a secure file outside the public skill package:

```json
{
  "appId": "your-vox-app-id",
  "secret": "your-vox-secret",
  "botId": "",
  "baseUrl": "https://vox.teddymobile.cn"
}
```

Then set:

```text
VOX_CREDENTIALS_FILE=/secure/path/credentials.json
```

## Production Recommendation

Use `resources/hosted_api_example.js` as a starting point, then replace it with a production backend that adds:

- User authentication.
- User-level call quotas.
- Content safety logging.
- Phone number masking in logs.
- Abuse prevention and audit trails.
- TLS termination with HTTPS.
