# OpenClaw compatibility

Read this file only when installing or running the skill in OpenClaw. The core instructions in `SKILL.md` do not depend on OpenClaw.

The `metadata.openclaw` block in `SKILL.md` is a compatibility adapter. It declares:

- `python3` as the expected executable;
- `yandex_tracker_client` as an installable pip dependency;
- `TRACKER_TOKEN` and one of the supported organization ID variables.

Configure credentials through the `env` section of `openclaw.json`:

```json
{
  "env": {
    "TRACKER_TOKEN": "your_oauth_token",
    "TRACKER_ORG_ID": "12345678"
  }
}
```

For a Yandex Cloud organization, use `TRACKER_CLOUD_ORG_ID` instead of `TRACKER_ORG_ID`.

Keep the token out of prompts and repository files. If OpenClaw changes its metadata or secret-management format, update this reference and the `metadata.openclaw` block together.
