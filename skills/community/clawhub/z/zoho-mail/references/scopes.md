# Zoho Mail scopes

The OAuth scopes Zoho Mail connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-mail#permissions.

```bash
maton connection create zoho-mail --scopes ZohoMail.accounts.READ
```

| Scope | Requested |
| --- | --- |
| `ZohoMail.messages.ALL` | By default |
| `ZohoMail.accounts.READ` | By default |
| `ZohoMail.folders.READ` | By default |
| `ZohoMail.contacts.READ` | By default |
| `ZohoMail.folders.ALL` | By default |
| `ZohoMail.tags.ALL` | By default |
| `ZohoMail.messages.READ` | Optional |
| `AaaServer.profile.READ` | Always |
