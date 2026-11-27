# Zoho Bigin scopes

The OAuth scopes Zoho Bigin connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-bigin#permissions.

```bash
maton connection create zoho-bigin --scopes ZohoBigin.users.READ
```

| Scope | Requested |
| --- | --- |
| `ZohoBigin.users.ALL` | By default |
| `ZohoBigin.org.ALL` | By default |
| `ZohoBigin.settings.ALL` | By default |
| `ZohoBigin.modules.contacts.ALL` | By default |
| `ZohoBigin.modules.accounts.ALL` | By default |
| `ZohoBigin.modules.products.ALL` | By default |
| `ZohoBigin.modules.pipelines.ALL` | By default |
| `ZohoBigin.modules.ALL` | By default |
| `ZohoBigin.users.READ` | Optional |
| `ZohoBigin.org.READ` | Optional |
| `ZohoBigin.modules.contacts.READ` | Optional |
| `ZohoBigin.modules.accounts.READ` | Optional |
| `ZohoBigin.modules.products.READ` | Optional |
| `ZohoBigin.modules.pipelines.READ` | Optional |
| `AaaServer.profile.READ` | Always |
