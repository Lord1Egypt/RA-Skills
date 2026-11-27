# Zoho Recruit scopes

The OAuth scopes Zoho Recruit connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-recruit#permissions.

```bash
maton connection create zoho-recruit --scopes ZohoRecruit.modules.READ
```

| Scope | Requested |
| --- | --- |
| `ZohoRecruit.users.ALL` | By default |
| `ZohoRecruit.settings.ALL` | By default |
| `ZohoRecruit.modules.ALL` | By default |
| `ZohoRecruit.modules.READ` | Optional |
| `ZohoRecruit.users.READ` | Optional |
| `ZohoRecruit.settings.READ` | Optional |
| `AaaServer.profile.READ` | Always |
