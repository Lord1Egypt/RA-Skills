# Zoho Projects scopes

The OAuth scopes Zoho Projects connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-projects#permissions.

```bash
maton connection create zoho-projects --scopes ZohoProjects.activities.READ
```

| Scope | Requested |
| --- | --- |
| `ZohoProjects.portals.ALL` | By default |
| `ZohoProjects.projects.ALL` | By default |
| `ZohoProjects.activities.READ` | By default |
| `ZohoProjects.milestones.ALL` | By default |
| `ZohoProjects.tasklists.ALL` | By default |
| `ZohoProjects.tasks.ALL` | By default |
| `ZohoProjects.timesheets.ALL` | By default |
| `ZohoProjects.bugs.ALL` | By default |
| `ZohoProjects.events.ALL` | By default |
| `ZohoProjects.forums.ALL` | By default |
| `ZohoProjects.users.ALL` | By default |
| `ZohoProjects.search.READ` | By default |
| `ZohoProjects.clients.ALL` | By default |
| `ZohoProjects.documents.ALL` | By default |
| `ZohoProjects.status.READ` | By default |
| `ZohoProjects.projects.READ` | Optional |
| `ZohoProjects.portals.READ` | Optional |
| `ZohoProjects.milestones.READ` | Optional |
| `ZohoProjects.tasklists.READ` | Optional |
| `ZohoProjects.tasks.READ` | Optional |
| `ZohoProjects.timesheets.READ` | Optional |
| `ZohoProjects.bugs.READ` | Optional |
| `ZohoProjects.events.READ` | Optional |
| `ZohoProjects.forums.READ` | Optional |
| `ZohoProjects.users.READ` | Optional |
| `ZohoProjects.clients.READ` | Optional |
| `ZohoProjects.documents.READ` | Optional |
| `AaaServer.profile.READ` | Always |
