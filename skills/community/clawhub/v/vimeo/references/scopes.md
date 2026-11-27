# Vimeo scopes

The OAuth scopes Vimeo connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/vimeo#permissions.

```bash
maton connection create vimeo --scopes create
```

| Scope | Requested |
| --- | --- |
| `create` | By default |
| `edit` | By default |
| `delete` | By default |
| `interact` | By default |
| `stats` | By default |
| `public` | Always |
| `private` | Always |
