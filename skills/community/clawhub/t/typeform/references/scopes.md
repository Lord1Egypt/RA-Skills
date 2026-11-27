# Typeform scopes

The OAuth scopes Typeform connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/typeform#permissions.

```bash
maton connection create typeform --scopes forms:read
```

| Scope | Requested |
| --- | --- |
| `forms:read` | By default |
| `forms:write` | By default |
| `responses:read` | By default |
| `responses:write` | By default |
| `offline` | Always |
| `accounts:read` | Always |
