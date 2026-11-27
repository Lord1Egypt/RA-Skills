# Zoho Calendar scopes

The OAuth scopes Zoho Calendar connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-calendar#permissions.

```bash
maton connection create zoho-calendar --scopes ZohoCalendar.calendar.READ
```

| Scope | Requested |
| --- | --- |
| `ZohoCalendar.calendar.ALL` | By default |
| `ZohoCalendar.event.ALL` | By default |
| `ZohoCalendar.settings.ALL` | By default |
| `ZohoCalendar.calendar.READ` | Optional |
| `ZohoCalendar.event.READ` | Optional |
| `ZohoCalendar.settings.READ` | Optional |
| `AaaServer.profile.READ` | Always |
