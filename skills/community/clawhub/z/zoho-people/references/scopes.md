# Zoho People scopes

The OAuth scopes Zoho People connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-people#permissions.

```bash
maton connection create zoho-people --scopes ZohoPeople.organization.READ
```

| Scope | Requested |
| --- | --- |
| `ZohoPeople.employee.ALL` | By default |
| `ZohoPeople.forms.ALL` | By default |
| `ZohoPeople.leave.ALL` | By default |
| `ZohoPeople.organization.READ` | By default |
| `ZohoPeople.forms.READ` | Optional |
| `ZohoPeople.leave.READ` | Optional |
| `AaaServer.profile.READ` | Always |
