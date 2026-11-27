# Trello scopes

The OAuth scopes Trello connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/trello#permissions.

```bash
maton connection create trello --scopes read:board:trello
```

| Scope | Requested |
| --- | --- |
| `read:board:trello` | By default |
| `write:board:trello` | By default |
| `write:board:membership:trello` | By default |
| `read:organization:trello` | By default |
| `write:organization:trello` | By default |
| `write:organization:membership:trello` | By default |
| `write:member:trello` | By default |
| `read:enterprise:trello` | By default |
| `write:enterprise:trello` | By default |
| `offline_access` | Always |
| `read:member:trello` | Always |
