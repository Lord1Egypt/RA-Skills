# Zoho CRM scopes

The OAuth scopes Zoho CRM connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-crm#permissions.

```bash
maton connection create zoho-crm --scopes ZohoCRM.modules.READ
```

| Scope | Requested |
| --- | --- |
| `ZohoCRM.modules.contacts.ALL` | By default |
| `ZohoCRM.modules.leads.ALL` | By default |
| `ZohoCRM.modules.accounts.ALL` | By default |
| `ZohoCRM.modules.deals.ALL` | By default |
| `ZohoCRM.modules.campaigns.ALL` | By default |
| `ZohoCRM.modules.tasks.ALL` | By default |
| `ZohoCRM.settings.ALL` | By default |
| `ZohoCRM.org.ALL` | By default |
| `ZohoCRM.users.ALL` | By default |
| `ZohoCRM.modules.ALL` | By default |
| `ZohoCRM.modules.READ` | Optional |
| `ZohoCRM.modules.contacts.READ` | Optional |
| `ZohoCRM.modules.leads.READ` | Optional |
| `ZohoCRM.modules.accounts.READ` | Optional |
| `ZohoCRM.modules.deals.READ` | Optional |
| `ZohoCRM.modules.campaigns.READ` | Optional |
| `ZohoCRM.modules.tasks.READ` | Optional |
| `ZohoCRM.settings.READ` | Optional |
| `ZohoCRM.org.READ` | Optional |
| `ZohoCRM.users.READ` | Optional |
| `AaaServer.profile.READ` | Always |
