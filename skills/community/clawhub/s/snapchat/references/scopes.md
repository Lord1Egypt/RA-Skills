# Snapchat scopes

The OAuth scopes Snapchat connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/snapchat#permissions.

```bash
maton connection create snapchat --scopes snapchat-offline-conversions-api
```

| Scope | Requested |
| --- | --- |
| `snapchat-offline-conversions-api` | By default |
| `snapchat-profile-api` | By default |
| `snapchat-marketing-api` | Always |
