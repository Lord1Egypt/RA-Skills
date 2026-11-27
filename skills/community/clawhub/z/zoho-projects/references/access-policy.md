# Zoho Projects access policy

An access policy limits which endpoints Zoho Projects connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-projects#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Zoho Projects: its 244 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create zoho-projects --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/timelogs/approver"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/attachments"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/attachments/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/baselinedetails"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/baselines"},
    {"method": "GET", "path": "api/v3/portal/{id}/automation/blueprint/next-transitions"},
    {"method": "GET", "path": "api/v3/portal/{id}/automation/blueprint/{id}/transition/{id}/during-actions"},
    {"method": "GET", "path": "api/v3/portal/{id}/automation/blueprints"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/budget"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/currency"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasks/{id}/associated-bugs"},
    {"method": "GET", "path": "api/v3/portal/{id}/bulk/export/fields"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/timelogs"},
    {"method": "GET", "path": "api/v3/portal/{id}/timelogs"},
    {"method": "GET", "path": "api/v3/portal/{id}/business-hours"},
    {"method": "GET", "path": "api/v3/portal/{id}/business-hours/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/business-hours/{id}/users"},
    {"method": "GET", "path": "api/v3/portal/{id}/time-zones"},
    {"method": "GET", "path": "api/v3/portal/{id}/clients"},
    {"method": "GET", "path": "api/v3/portal/{id}/clients/users"},
    {"method": "GET", "path": "api/v3/portal/{id}/clients/{id}/projects"},
    {"method": "GET", "path": "api/v3/portal/{id}/customers"},
    {"method": "GET", "path": "api/v3/portal/{id}/client/{id}/contacts"},
    {"method": "GET", "path": "api/v3/portal/{id}/contacts/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/custom-domain"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entities"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entities/count"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entities/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/portal_export/history"},
    {"method": "GET", "path": "api/v3/portal/{id}/portal_export/{id}/status"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/documents"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/folders"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/eventcomments/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/events/{id}/comments"},
    {"method": "GET", "path": "api/v3/portal/{id}/events/{id}/participants"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/events"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/events/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/extensions/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/status"},
    {"method": "GET", "path": "api/v3/portal/{id}/folder"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/documents/folders/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasks/{id}/forums"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/categories"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/forumcomments/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/forums/{id}/comments"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/forums/{id}/comments/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/forums/{id}/followers"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/forums"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/forums/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/forums/{id}/tasks"},
    {"method": "GET", "path": "api/v3/portal/{id}/holiday-list"},
    {"method": "GET", "path": "api/v3/portal/{id}/holiday-list/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/holiday-list/{id}/associated-business-hours"},
    {"method": "GET", "path": "api/v3/portal/{id}/holiday-list/{id}/holidays"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/{id}/attachments"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/{id}/attachments/comments"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/{id}/comments"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/{id}/comments/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/issues/customviews"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/customviews"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/customviews/{id}"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/projects/{id}/issues/{id}/followers"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/{id}/followers"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/projects/{id}/issues/settings/link-types"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/projects/{id}/issues/{id}/linked-issues"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/{id}/linkedissues"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/projects/{id}/issues/{id}/resolution"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/{id}/resolution"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/projects/{id}/issues/{id}/associated-tasks"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/projects/{id}/tasks/{id}/associated-issues"},
    {"method": "GET", "path": "api/v3/portal/{id}/issues/associated-tasks"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/{id}/associated-tasks"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/projects/{id}/issues/{id}/status-timeline"},
    {"method": "GET", "path": "api/v3/portal/{id}/issues"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/{id}/activities"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/{id}/description"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issues/{id}/statustransition"},
    {"method": "GET", "path": "api/v3/portal/{id}/leave"},
    {"method": "GET", "path": "api/v3/portal/{id}/leave/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/extensions/{id}/config"},
    {"method": "GET", "path": "api/v3/portal/{id}/extensions/{id}/storage"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasks/{id}/blocking-waiting-tasks"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/fields"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/fields/{id}/associated-layouts"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/fields/{id}/associated-projects"},
    {"method": "GET", "path": "api/v3/portal/{id}/entity/integrations"},
    {"method": "GET", "path": "api/v3/portal/{id}/integration-field/service"},
    {"method": "GET", "path": "api/v3/portal/{id}/integration-field/service/{id}/module/{id}/fields"},
    {"method": "GET", "path": "api/v3/portal/{id}/integration-field/service/{id}/modules"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/layouts"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/layouts/default-layout"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/layouts/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/layouts/{id}/associated-entities"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/fields"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/options"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/fields-configuration"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/global-statuses"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/modules"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/modules/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/users/me/{id}/permissions"},
    {"method": "GET", "path": "api/v3/portal/{id}/users/me/{id}/permissions"},
    {"method": "GET", "path": "api/v3/portal/{id}/license"},
    {"method": "GET", "path": "api/v3/portal/{id}/profiles/cm/{id}/permissions"},
    {"method": "GET", "path": "api/v3/portal/{id}/profiles/{id}/permissions"},
    {"method": "GET", "path": "api/v3/portal/{id}/profiles/{id}/{id}/permissions"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/phases/{id}/comments"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/phases/{id}/followers"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/phases"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/projects/{id}/phases"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/projects/{id}/phases/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/phases"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/phases"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/phases/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/phases/{id}/activities"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/phases/{id}/status-timeline"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/timelogs/pin"},
    {"method": "GET", "path": "api/v3/portal/{id}/timelogs/pin"},
    {"method": "GET", "path": "api/v3.1/portals"},
    {"method": "GET", "path": "api/v3/portal/{id}"},
    {"method": "GET", "path": "api/v3/portals"},
    {"method": "GET", "path": "api/v3/portal/{id}/profiles"},
    {"method": "GET", "path": "api/v3/portal/{id}/profiles/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/comments"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/comments/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/client/{id}/contacts"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/customview"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/customview/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/clients"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/clients/users"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/crm/accounts"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/crm/contacts"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/crm/deals"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/customers"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/export"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/export-form"},
    {"method": "GET", "path": "api/v3/portal/{id}/my-project-groups"},
    {"method": "GET", "path": "api/v3/portal/{id}/project-groups"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tags"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/teams"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/projects/{id}/users"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/projects/{id}/users/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/users"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/users/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/modules"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entity/{id}/attachmentcount"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entity/{id}/attachments"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entity/{id}/edits"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entity/{id}/edits/count"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entity/{id}/edits/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entity/{id}/status-timeline"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entity/{id}/comments"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entity/{id}/comments/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entity/{id}/count"},
    {"method": "GET", "path": "api/v3/portal/{id}/views/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/export"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/export/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entity/{id}/followers"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/entity/{id}/isuser"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/import/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/import/{id}/error-details"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/import/{id}/file-details"},
    {"method": "GET", "path": "api/v3/portal/{id}/module/{id}/my-imports"},
    {"method": "GET", "path": "api/v3/portal/{id}/resources/{id}/skills"},
    {"method": "GET", "path": "api/v3/portal/{id}/roles"},
    {"method": "GET", "path": "api/v3/portal/{id}/roles/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/search"},
    {"method": "GET", "path": "api/v3/portal/{id}/search"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/timelog"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/timelog/meta-data"},
    {"method": "GET", "path": "api/v3/portal/{id}/settings/date-time"},
    {"method": "GET", "path": "api/v3/portal/{id}/skills/{id}/history"},
    {"method": "GET", "path": "api/v3/portal/{id}/skills/{id}/resources"},
    {"method": "GET", "path": "api/v3/portal/{id}/skills/{id}/users"},
    {"method": "GET", "path": "api/v3/portal/{id}/skills"},
    {"method": "GET", "path": "api/v3/portal/{id}/skills/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasks/{id}/status-timeline"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/taskstatushistory"},
    {"method": "GET", "path": "api/v3/portal/{id}/taskstatushistory"},
    {"method": "GET", "path": "api/v3/portal/{id}/tags"},
    {"method": "GET", "path": "api/v3/portal/{id}/tags/projects"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasks/{id}/attachments"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasks/{id}/comments"},
    {"method": "GET", "path": "api/v3/portal/{id}/customviews/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasks/customviews"},
    {"method": "GET", "path": "api/v3/portal/{id}/tasks/customviews/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasks/{id}/followers"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasklists/{id}/comments"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasklists/{id}/comments/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasklists/{id}/followers"},
    {"method": "GET", "path": "api/v3/portal/{id}/templates/tasklists"},
    {"method": "GET", "path": "api/v3/portal/{id}/templates/tasklists/{id}/tasks"},
    {"method": "GET", "path": "api/v3/portal/{id}/all-tasklists"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasklists"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasklists/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasks"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasks/count"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/tasks/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/tasks"},
    {"method": "GET", "path": "api/v3/portal/{id}/tasks/attachments"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/documents/teamfolder/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/teams"},
    {"method": "GET", "path": "api/v3/portal/{id}/teams/projects"},
    {"method": "GET", "path": "api/v3/portal/{id}/teams/users"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/logs/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/logs/new/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/issue/timelogs/{id}/timers"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/task/timelogs/{id}/timers"},
    {"method": "GET", "path": "api/v3/portal/{id}/timelogs/timers"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/timelogs/report"},
    {"method": "GET", "path": "api/v3/portal/{id}/timelogs/clientreport"},
    {"method": "GET", "path": "api/v3/portal/{id}/timelogs/projectreport"},
    {"method": "GET", "path": "api/v3/portal/{id}/timelogs/report"},
    {"method": "GET", "path": "api/v3/portal/{id}/timelogs/reports/count"},
    {"method": "GET", "path": "api/v3/portal/{id}/bin"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/users/export"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/users/export/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/users/export"},
    {"method": "GET", "path": "api/v3/portal/{id}/users/export/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/user/{id}/descendants"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/users/{id}/permissions"},
    {"method": "GET", "path": "api/v3/portal/{id}/projects/{id}/users/{id}/{id}/permissions"},
    {"method": "GET", "path": "api/v3/portal/{id}/users/{id}/skills"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/users"},
    {"method": "GET", "path": "api/v3.1/portal/{id}/users/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/users"},
    {"method": "GET", "path": "api/v3/portal/{id}/users/license-details"},
    {"method": "GET", "path": "api/v3/portal/{id}/users/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/users/{id}/audit-logs"},
    {"method": "GET", "path": "api/v3/portal/{id}/users/{id}/projects"},
    {"method": "GET", "path": "api/v3/portal/{id}/users/{id}/teams"},
    {"method": "GET", "path": "api/v3/portal/{id}/users/email-templates"},
    {"method": "GET", "path": "api/v3/portal/{id}/users/email-templates/{id}"},
    {"method": "GET", "path": "api/v3/portal/{id}/reports/workload"},
    {"method": "GET", "path": "api/v3/portal/{id}/reports/workload/details"},
    {"method": "GET", "path": "api/v3/portal/{id}/reports/workload/entity/{id}/details"},
    {"method": "GET", "path": "api/v3/portal/{id}/reports/workload/groups"},
    {"method": "GET", "path": "api/v3/portal/{id}/reports/workload/groups/owners"},
    {"method": "GET", "path": "api/v3/portal/{id}/reports/workload/groups/{id}/owners"},
    {"method": "GET", "path": "api/v3/portal/{id}/reports/workload/meta"},
    {"method": "GET", "path": "api/v3/portal/{id}/reports/workload/owner/{id}/details"}
  ],
  "deny": []
}
```

## Endpoints

The Zoho Projects endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/v3/portal/{id}/projects/{id}/timelogs/approver | read | approvers | Retrieve the default approver of the user in a project. |
| PATCH | api/v3/portal/{id}/projects/{id}/timelogs/approver | write | approvers | Modify the default time log approver of the user in a project. |
| POST | api/v3/portal/{id}/associate-attachments | write | attachments | Upload one or more files and associate them with a record (entity) in the Zoho Projects portal. |
| POST | api/v3/portal/{id}/attachments | write | attachments | Upload one or more files to the Zoho Projects portal. |
| POST | api/v3/portal/{id}/attachments/associate | write | attachments | Associate Multiple attachments for all entities. |
| DELETE | api/v3/portal/{id}/attachments/disassociate | write | attachments | Disassociate Multiple attachments for all entities. |
| POST | api/v3/portal/{id}/entity-attachments | write | attachments | Associate an uploaded file with a specific module's entity in Zoho Projects. |
| POST | api/v3/portal/{id}/inline-attachments | write | attachments | Upload files within a comment. |
| GET | api/v3/portal/{id}/projects/{id}/attachments | read | attachments | Get attachments details by Entity id. |
| GET | api/v3/portal/{id}/projects/{id}/attachments/{id} | read | attachments | Get attachments details by attachment id. |
| POST | api/v3/portal/{id}/projects/{id}/attachments/{id} | write | attachments | Associate attachments for all entities. |
| DELETE | api/v3/portal/{id}/projects/{id}/attachments/{id} | write | attachments | Disassociate for all entities. |
| POST | api/v3/portal/{id}/upload-attachments | write | attachments | Upload files to Zoho WorkDrive from Zoho Projects using Base64 encoded content. |
| POST | api/v3/portal/{id}/projects/{id}/baseline | write | baseline | Create a baseline based on the current schedules in a project. |
| GET | api/v3/portal/{id}/projects/{id}/baselinedetails | read | baseline | Retrieve task details captured under a specific baseline. |
| GET | api/v3/portal/{id}/projects/{id}/baselines | read | baseline | Retrieve all baselines from a project. |
| GET | api/v3/portal/{id}/automation/blueprint/next-transitions | read | blueprints | Retrieve actions that are set to execute after transition. |
| GET | api/v3/portal/{id}/automation/blueprint/{id}/transition/{id}/during-actions | read | blueprints | Retrieve data of the action that is set to execute during the transition. |
| POST | api/v3/portal/{id}/automation/blueprint/{id}/transition/{id}/execute | write | blueprints | Execute transition in a blueprint. |
| GET | api/v3/portal/{id}/automation/blueprints | read | blueprints | Retrieve details of all blueprints from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/currency | write | budget | Add a new currency to the organisation. |
| PATCH | api/v3/portal/{id}/currency/{id} | write | budget | Update an existing currency configured for the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/currency/{id} | write | budget | Remove a currency configured for the Zoho Projects portal. |
| GET | api/v3/portal/{id}/settings/budget | read | budget | Retrieve the budget settings configured for the Zoho Projects portal. |
| POST | api/v3/portal/{id}/settings/budget | write | budget | Update the budget settings configured for the Zoho Projects portal. |
| GET | api/v3/portal/{id}/settings/currency | read | budget | Retrieve the currency settings configured for the Zoho Projects portal. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/associate-bugs | write | bug_association | Associate bugs to a task. |
| GET | api/v3/portal/{id}/projects/{id}/tasks/{id}/associated-bugs | read | bug_association | Get Associated Bugs from a task. |
| DELETE | api/v3/portal/{id}/projects/{id}/tasks/{id}/bug/{id} | write | bug_association | Disassociate bug from a task. |
| POST | api/v3/portal/{id}/bulk/export | write | bulk_read | Create a bulk read job to export records of a module from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/bulk/export/fields | read | bulk_read | Retrieve the field metadata for the specified modules from the Zoho Projects portal. |
| PATCH | api/v3.1/portal/{id}/timelogs | write | bulk_time_logs | Update multiple time log entries in the Zoho Projects portal. |
| DELETE | api/v3.1/portal/{id}/timelogs | write | bulk_time_logs | Remove multiple time log entries from a specific portal. |
| POST | api/v3/portal/{id}/addbulktimelogs | write | bulk_time_logs | Add multiple time log entries to a specific portal. |
| PATCH | api/v3/portal/{id}/logs | write | bulk_time_logs | Bulk Update Time Logs. |
| GET | api/v3/portal/{id}/projects/{id}/timelogs | read | bulk_time_logs | Retrieve all time logs from a project. |
| GET | api/v3/portal/{id}/timelogs | read | bulk_time_logs | Retrieve all time logs from the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/timelogs/bulkdelete | write | bulk_time_logs | Bulk Delete Time Logs. |
| GET | api/v3/portal/{id}/business-hours | read | business_hours | Retrieve the list of business hours from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/business-hours | write | business_hours | Create a business calendar in the Zoho Projects portal. |
| PUT | api/v3/portal/{id}/business-hours | write | business_hours | Modify the work hours by archiving the business hours and creating a new one in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/business-hours/{id} | read | business_hours | Retrieve details of the business hours using its ID. |
| DELETE | api/v3/portal/{id}/business-hours/{id} | write | business_hours | Remove a business calendar from the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/business-hours/{id}/mark-as-default | write | business_hours | Set default business hours in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/business-hours/{id}/users | read | business_hours | Retrieve the list of users associated to the business hours from the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/business-hours/{id}/users | write | business_hours | Associate/disassociate user from the business hours. |
| GET | api/v3/portal/{id}/time-zones | read | business_hours | Retrieve the list of IANA timezones from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/clients | read | clients_and_customers | Get Customers. |
| POST | api/v3/portal/{id}/clients | write | clients_and_customers | Add customers to the Zoho Projects portal. |
| GET | api/v3/portal/{id}/clients/users | read | clients_and_customers | Retrieve customers and client users from the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/clients/users/{id} | write | clients_and_customers | Remove a client user from the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/clients/{id} | write | clients_and_customers | Modify customer details in the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/clients/{id} | write | clients_and_customers | Remove the client company from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/clients/{id}/projects | read | clients_and_customers | Retrieve all projects associated with a customer from the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/clients/{id}/projects | write | clients_and_customers | Modify the projects associated with customer in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/customers | read | clients_and_customers | Retrieve customer details from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/client/{id}/contacts | read | contacts | Retrieve all contacts from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/contacts | write | contacts | Create new contacts in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/contacts/{id} | read | contacts | Retrieve details of a contact from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/contacts/{id} | write | contacts | Convert contact to a client user in the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/contacts/{id} | write | contacts | Update a contact in the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/contacts/{id} | write | contacts | Remove a contact from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/custom-domain | read | custom_domain | Retrieve custom domain details for the portal. |
| POST | api/v3/portal/{id}/custom-domain | write | custom_domain | Add a custom domain for the portal. |
| DELETE | api/v3/portal/{id}/custom-domain | write | custom_domain | Remove the custom domain configuration from the Zoho Projects portal. |
| PUT | api/v3/portal/{id}/custom-domain/status | write | custom_domain | Update the custom domain status. |
| GET | api/v3/portal/{id}/custom-domain/validate | write | custom_domain | Validate custom domain configuration. Kept out of read: triggers a domain validation check. |
| POST | api/v3/portal/{id}/automation/customfunction/{id}/execute | write | custom_functions | Execute a custom function in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/module/{id}/entities | read | custom_module_records | Retrieve the list of records from a module. |
| POST | api/v3/portal/{id}/module/{id}/entities | write | custom_module_records | Create a record in a custom module. |
| GET | api/v3/portal/{id}/module/{id}/entities/count | read | custom_module_records | Retrieve the count of records from a module. |
| GET | api/v3/portal/{id}/module/{id}/entities/{id} | read | custom_module_records | Retrieve details of a specific record. |
| PATCH | api/v3/portal/{id}/module/{id}/entities/{id} | write | custom_module_records | Modify details of an existing record. |
| DELETE | api/v3/portal/{id}/module/{id}/entities/{id} | write | custom_module_records | Remove a record permanently from the recycle bin. |
| POST | api/v3/portal/{id}/module/{id}/entities/{id}/restore | write | custom_module_records | Restore the trashed record from recycle bin. |
| DELETE | api/v3/portal/{id}/module/{id}/entities/{id}/trash | write | custom_module_records | Move a record to recycle bin within Zoho Projects portal. |
| POST | api/v3/portal/{id}/projects/{id}/timesheet/customviews/{id}/mark-favourite | write | custom_views | Mark a time log custom view as favourite in a project. |
| POST | api/v3/portal/{id}/projects/{id}/timesheet/customviews/{id}/set-default-view | write | custom_views | Set a time log custom view as the default view in a project. |
| POST | api/v3/portal/{id}/projects/{id}/timesheet/customviews/{id}/unmark-favourite | write | custom_views | Unmark a time log custom view as favourite in a project. |
| POST | api/v3/portal/{id}/timesheet/customviews/{id}/mark-favourite | write | custom_views | Mark a time log custom view as favourite across portal. |
| POST | api/v3/portal/{id}/timesheet/customviews/{id}/set-default-view | write | custom_views | Set a time log custom view as the default view across the portal. |
| POST | api/v3/portal/{id}/timesheet/customviews/{id}/unmark-favourite | write | custom_views | Unmark a time log custom view as favourite across portal. |
| POST | api/v3/portal/{id}/portal_export | write | data_backup | Schedule a data backup for the portal. |
| GET | api/v3/portal/{id}/portal_export/history | read | data_backup | Retrieve the history of portal data backups. |
| GET | api/v3/portal/{id}/portal_export/{id}/status | read | data_backup | Retrieve the status of a portal data backup. |
| GET | api/v3/portal/{id}/projects/{id}/documents | read | documents | Retrieve the team folder or folder settings from a project. |
| GET | api/v3/portal/{id}/projects/{id}/folders | read | documents | Get a Team Folder associated to a Project. |
| GET | api/v3/portal/{id}/projects/{id}/eventcomments/{id} | read | event_comments | Retrieve the details of a specific event comment using its comment ID. Use this API to access an event comment without requiring the event ID. |
| GET | api/v3/portal/{id}/projects/{id}/events/{id}/comments | read | event_comments | Retrieve all comments on a specific event in a project. |
| POST | api/v3/portal/{id}/projects/{id}/events/{id}/comments | write | event_comments | Add a comment to a specific event in a project. |
| PATCH | api/v3/portal/{id}/projects/{id}/events/{id}/comments/{id} | write | event_comments | Update an existing comment associated with an event in a project within the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/projects/{id}/events/{id}/comments/{id} | write | event_comments | Delete a comment associated with an event in a project within the Zoho Projects portal. |
| GET | api/v3/portal/{id}/events/{id}/participants | read | events | Retrieve all participants of a specific event in a portal. |
| GET | api/v3/portal/{id}/projects/{id}/events | read | events | Retrieve all events associated with a specific project. |
| POST | api/v3/portal/{id}/projects/{id}/events | write | events | Add a new event to a specific project. |
| GET | api/v3/portal/{id}/projects/{id}/events/{id} | read | events | Retrieve the details of a specific event in a project. |
| PATCH | api/v3/portal/{id}/projects/{id}/events/{id} | write | events | Update details of an event in the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/projects/{id}/events/{id} | write | events | Remove a specific event from a project. |
| POST | api/v3/portal/{id}/extensions/install | write | extensions | Install an extension in the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/extensions/widget/{id} | write | extensions | Update the details of an extension widget such as name, visibility, modules, projects, profiles, and users. |
| GET | api/v3/portal/{id}/extensions/{id} | read | extensions | Retrieve the details of a specific extension by its ID. |
| DELETE | api/v3/portal/{id}/extensions/{id} | write | extensions | Uninstall an extension from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/extensions/{id}/version-update | write | extensions | Update the extension to the latest available version. |
| GET | api/v3/portal/{id}/projects/{id}/status | read | feed_status | Retrieve the status from a project. |
| POST | api/v3/portal/{id}/projects/{id}/status | write | feed_status | Create a new status in a project. |
| GET | api/v3/portal/{id}/folder | read | folder | Get Folders Details. |
| POST | api/v3/portal/{id}/projects/{id}/documents/folders | write | folder | Create a folder in a project. |
| POST | api/v3/portal/{id}/projects/{id}/documents/folders/associate | write | folder | Associate folder(s) to a project. |
| GET | api/v3/portal/{id}/projects/{id}/documents/folders/{id} | read | folder | Retrieve details of the folder settings from a project. |
| PATCH | api/v3/portal/{id}/projects/{id}/documents/folders/{id} | write | folder | Modify folder settings in a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/documents/folders/{id} | write | folder | Delete a Folder. |
| DELETE | api/v3/portal/{id}/projects/{id}/documents/folders/{id}/disassociate | write | folder | Disassociate folder(s) from a project. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/associate-forums | write | forum_association | Link one or more forums to a task. |
| DELETE | api/v3/portal/{id}/projects/{id}/tasks/{id}/associate-forums | write | forum_association | Disassociate multiple forums from a task. |
| GET | api/v3/portal/{id}/projects/{id}/tasks/{id}/forums | read | forum_association | Retrieve multiple forums from a task. |
| GET | api/v3/portal/{id}/projects/{id}/categories | read | forum_categories | Retrieve all forum categories in a specific project. |
| POST | api/v3/portal/{id}/projects/{id}/categories | write | forum_categories | Add a new category for forums in a specific project. |
| PATCH | api/v3/portal/{id}/projects/{id}/categories/{id} | write | forum_categories | Update a forum category in a specific project. |
| DELETE | api/v3/portal/{id}/projects/{id}/categories/{id} | write | forum_categories | Delete a forum category from a specific project. |
| GET | api/v3/portal/{id}/projects/{id}/forumcomments/{id} | read | forum_comments | Retrieve the details of a specific forum comment using its comment ID. Use this API to access a forum comment without requiring the forum ID. |
| GET | api/v3/portal/{id}/projects/{id}/forums/{id}/comments | read | forum_comments | Retrieve all comments from a specific forum in a project. |
| POST | api/v3/portal/{id}/projects/{id}/forums/{id}/comments | write | forum_comments | Add a comment to a specific forum in a project. |
| GET | api/v3/portal/{id}/projects/{id}/forums/{id}/comments/{id} | read | forum_comments | Retrieve a specific comment from a forum in a project. |
| PATCH | api/v3/portal/{id}/projects/{id}/forums/{id}/comments/{id} | write | forum_comments | Update a comment in a specific forum in a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/forums/{id}/comments/{id} | write | forum_comments | Delete a comment from a specific forum in a project. |
| POST | api/v3/portal/{id}/projects/{id}/forums/{id}/comments/{id}/markbestanswer | write | forum_comments | Mark a specific comment as the best answer in a forum. |
| DELETE | api/v3/portal/{id}/projects/{id}/forums/{id}/comments/{id}/markbestanswer | write | forum_comments | Remove the best answer designation from a specific comment in a forum. |
| POST | api/v3/portal/{id}/projects/{id}/forums/{id}/follow | write | forum_followers | Follow a specific forum in a project to receive notifications. |
| GET | api/v3/portal/{id}/projects/{id}/forums/{id}/followers | read | forum_followers | Retrieve all followers of a specific forum in a project. |
| POST | api/v3/portal/{id}/projects/{id}/forums/{id}/unfollow | write | forum_followers | Unfollow a specific forum in a project to stop receiving notifications. |
| GET | api/v3/portal/{id}/projects/{id}/forums | read | forums | Retrieve all forums in a specific project. |
| POST | api/v3/portal/{id}/projects/{id}/forums | write | forums | Add a new forum to a specific project. |
| GET | api/v3/portal/{id}/projects/{id}/forums/{id} | read | forums | Retrieve the details of a specific forum in a project. |
| PATCH | api/v3/portal/{id}/projects/{id}/forums/{id} | write | forums | Update a forum in a specific project. |
| DELETE | api/v3/portal/{id}/projects/{id}/forums/{id} | write | forums | Delete a forum from a specific project. |
| GET | api/v3/portal/{id}/projects/{id}/forums/{id}/tasks | read | forums | Retrieve all tasks associated with a specific forum in a project. |
| GET | api/v3/portal/{id}/holiday-list | read | holidays | Retrieve holiday lists from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/holiday-list | write | holidays | Create a holiday list in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/holiday-list/{id} | read | holidays | Retrieve holiday list details using its ID. |
| PATCH | api/v3/portal/{id}/holiday-list/{id} | write | holidays | Modify the details of an holiday list in the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/holiday-list/{id} | write | holidays | Remove a holiday list from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/holiday-list/{id}/associated-business-hours | read | holidays | Retrieve business hours associated with the holiday list. |
| GET | api/v3/portal/{id}/holiday-list/{id}/holidays | read | holidays | Retrieve holidays for the specified year from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/projects/{id}/issues/{id}/attachments | read | issue_attachment | Retrieve all attachments of an issue. |
| POST | api/v3/portal/{id}/projects/{id}/issues/{id}/attachments | write | issue_attachment | Associate attachments with an issue. |
| DELETE | api/v3/portal/{id}/projects/{id}/issues/{id}/attachments/{id} | write | issue_attachment | Dissociate an attachment from an issue. |
| GET | api/v3/portal/{id}/projects/{id}/issues/{id}/attachments/comments | read | issue_comments | Retrieve attachments of a comment. |
| GET | api/v3/portal/{id}/projects/{id}/issues/{id}/comments | read | issue_comments | Retrieve all comments of an issue. |
| POST | api/v3/portal/{id}/projects/{id}/issues/{id}/comments | write | issue_comments | Add a comment to an issue. |
| GET | api/v3/portal/{id}/projects/{id}/issues/{id}/comments/{id} | read | issue_comments | Retrieve a specific comment on an issue. |
| PATCH | api/v3/portal/{id}/projects/{id}/issues/{id}/comments/{id} | write | issue_comments | Update a comment on an issue. |
| DELETE | api/v3/portal/{id}/projects/{id}/issues/{id}/comments/{id} | write | issue_comments | Remove a comment from an issue. |
| GET | api/v3/portal/{id}/issues/customviews | read | issue_custom_views | Retrieve custom views of the portal. |
| GET | api/v3/portal/{id}/projects/{id}/issues/customviews | read | issue_custom_views | Retrieve custom views of a project. |
| GET | api/v3/portal/{id}/projects/{id}/issues/customviews/{id} | read | issue_custom_views | Retrieve the details of a custom view along with its fields. |
| POST | api/v3.1/portal/{id}/projects/{id}/issues/{id}/follow | write | issue_followers | Add or update followers to an issue in a project. |
| GET | api/v3.1/portal/{id}/projects/{id}/issues/{id}/followers | read | issue_followers | Retrieve followers of an issue in a project. |
| POST | api/v3.1/portal/{id}/projects/{id}/issues/{id}/unfollow | write | issue_followers | Remove followers from an issue in a project. |
| GET | api/v3/portal/{id}/projects/{id}/issues/{id}/followers | read | issue_followers | Retrieve the followers of an issue in a project. |
| POST | api/v3/portal/{id}/projects/{id}/issues/{id}/followers | write | issue_followers | Receive updates or notifications about the issue in a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/issues/{id}/followers | write | issue_followers | Remove followers from an issue in a project. |
| GET | api/v3.1/portal/{id}/projects/{id}/issues/settings/link-types | read | issue_link_types | Get all link types for a project. |
| PUT | api/v3.1/portal/{id}/projects/{id}/issues/settings/link-types | write | issue_link_types | Create or update a link type in a project. |
| DELETE | api/v3.1/portal/{id}/projects/{id}/issues/settings/link-types/{id} | write | issue_link_types | Delete a link type in a project. |
| POST | api/v3.1/portal/{id}/projects/{id}/issue-links | write | issue_linking | Link multiple issues at once in a project. |
| DELETE | api/v3.1/portal/{id}/projects/{id}/issue-links | write | issue_linking | Unlink multiple issues at once in a project. |
| PATCH | api/v3.1/portal/{id}/projects/{id}/issues-links/{id} | write | issue_linking | Change the link type between two issues. |
| GET | api/v3.1/portal/{id}/projects/{id}/issues/{id}/linked-issues | read | issue_linking | Retrieve all the linked issues to a specific issue. |
| POST | api/v3/portal/{id}/projects/{id}/issues/bulk-link-bugs | write | issue_linking | Link multiple issues at once in a project. |
| POST | api/v3/portal/{id}/projects/{id}/issues/{id}/link | write | issue_linking | Establish a link between multiple issues. |
| POST | api/v3/portal/{id}/projects/{id}/issues/{id}/link/{id} | write | issue_linking | Modify the link type between two linked issues. |
| DELETE | api/v3/portal/{id}/projects/{id}/issues/{id}/link/{id} | write | issue_linking | Remove the link between issues in a project. |
| GET | api/v3/portal/{id}/projects/{id}/issues/{id}/linkedissues | read | issue_linking | Retrieve all linked issues of an issue. |
| GET | api/v3.1/portal/{id}/projects/{id}/issues/{id}/resolution | read | issue_resolution | Get resolution of an issue. |
| POST | api/v3.1/portal/{id}/projects/{id}/issues/{id}/resolution | write | issue_resolution | Add resolution of an issue. |
| PATCH | api/v3.1/portal/{id}/projects/{id}/issues/{id}/resolution | write | issue_resolution | Update resolution of an issue. |
| DELETE | api/v3.1/portal/{id}/projects/{id}/issues/{id}/resolution | write | issue_resolution | Remove the resolution of an issue. |
| GET | api/v3/portal/{id}/projects/{id}/issues/{id}/resolution | read | issue_resolution | Retrieve the resolution of an issue. |
| POST | api/v3/portal/{id}/projects/{id}/issues/{id}/resolution | write | issue_resolution | Add the resolution to an issue. |
| PUT | api/v3/portal/{id}/projects/{id}/issues/{id}/resolution | write | issue_resolution | Modify the resolution of an issue. |
| DELETE | api/v3/portal/{id}/projects/{id}/issues/{id}/resolution | write | issue_resolution | Remove the resolution of an issue. |
| GET | api/v3.1/portal/{id}/projects/{id}/issues/{id}/associated-tasks | read | issue_task_mapping | Retrieve tasks associated to a specific issue. |
| POST | api/v3.1/portal/{id}/projects/{id}/task-issue-mapping | write | issue_task_mapping | Link multiple tasks to multiple issues in a project. |
| DELETE | api/v3.1/portal/{id}/projects/{id}/task-issue-mapping | write | issue_task_mapping | Unlink multiple tasks from multiple issues in a project. |
| GET | api/v3.1/portal/{id}/projects/{id}/tasks/{id}/associated-issues | read | issue_task_mapping | Retrieve issues associated to a specific task. |
| GET | api/v3/portal/{id}/issues/associated-tasks | read | issue_task_mapping | Retrieve the tasks associated with issues. |
| POST | api/v3/portal/{id}/projects/{id}/issues/bulk-associate-tasks | write | issue_task_mapping | Associate multiple tasks with multiple issues in a project. |
| POST | api/v3/portal/{id}/projects/{id}/issues/{id}/associate-tasks | write | issue_task_mapping | Associate tasks with a specific issue. |
| GET | api/v3/portal/{id}/projects/{id}/issues/{id}/associated-tasks | read | issue_task_mapping | Retrieve the tasks associated with an issue. |
| DELETE | api/v3/portal/{id}/projects/{id}/issues/{id}/task/{id} | write | issue_task_mapping | Remove task association from an issue. |
| GET | api/v3.1/portal/{id}/projects/{id}/issues/{id}/status-timeline | read | issues | Retrieve the status transitions history of an issue. |
| GET | api/v3/portal/{id}/issues | read | issues | Retrieve all issues from the portal. |
| GET | api/v3/portal/{id}/projects/{id}/issues | read | issues | Retrieve all issues from a project. |
| POST | api/v3/portal/{id}/projects/{id}/issues | write | issues | Create an issue in a project. |
| GET | api/v3/portal/{id}/projects/{id}/issues/{id} | read | issues | Retrieve details of an issue in a project. |
| PATCH | api/v3/portal/{id}/projects/{id}/issues/{id} | write | issues | Modify an issue in a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/issues/{id} | write | issues | Remove an issue from a project. |
| GET | api/v3/portal/{id}/projects/{id}/issues/{id}/activities | read | issues | Retrieve activities performed on issues in a project. |
| POST | api/v3/portal/{id}/projects/{id}/issues/{id}/clone | write | issues | Clone an issue in a project. |
| GET | api/v3/portal/{id}/projects/{id}/issues/{id}/description | read | issues | Retrieve the description of the issue in a project. |
| POST | api/v3/portal/{id}/projects/{id}/issues/{id}/move | write | issues | Move an issue to another project. |
| GET | api/v3/portal/{id}/projects/{id}/issues/{id}/statustransition | read | issues | Retrieve the status transitions history of an issue. |
| GET | api/v3/portal/{id}/leave | read | leaves | Retrieve all the leaves from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/leave | write | leaves | Create a leave in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/leave/{id} | read | leaves | Retrieve specific leave details from the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/leave/{id} | write | leaves | Update the leave details in the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/leave/{id} | write | leaves | Remove a leave from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/extensions/{id}/config | read | marketplace | Retrieve the configuration of the extension. |
| GET | api/v3/portal/{id}/extensions/{id}/storage | read | marketplace | Retrieve all entity or app properties from an extension. |
| POST | api/v3/portal/{id}/extensions/{id}/storage | write | marketplace | Store all the entity or app properties of the extension. |
| PATCH | api/v3/portal/{id}/extensions/{id}/storage | write | marketplace | Modify the entity or app property in an extension. |
| DELETE | api/v3/portal/{id}/extensions/{id}/storage | write | marketplace | Remove the entity or app property from the extension. |
| GET | api/v3/portal/{id}/projects/{id}/tasks/{id}/blocking-waiting-tasks | read | meta | Retrieve details of a blocking waiting tasks for a given task. |
| GET | api/v3/portal/{id}/settings/fields | read | module_fields | Retrieve the list of fields available in a module along with their metadata such as API name, display name, and field type. |
| PUT | api/v3/portal/{id}/settings/fields | write | module_fields | Create a new field or update an existing field in a module layout. |
| DELETE | api/v3/portal/{id}/settings/fields/{id} | write | module_fields | Remove a field from the custom module. |
| GET | api/v3/portal/{id}/settings/fields/{id}/associated-layouts | read | module_fields | Retrieve the associated layouts of a field. |
| GET | api/v3/portal/{id}/settings/fields/{id}/associated-projects | read | module_fields | Retrieve the associated projects of a field. |
| GET | api/v3/portal/{id}/entity/integrations | read | module_integration | Retrieve the integration details of a module from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/integration-field/service | read | module_integration_field | Retrieve external services available for integration fields. |
| GET | api/v3/portal/{id}/integration-field/service/{id}/module/{id}/fields | read | module_integration_field | Retrieve fields from an external service module. |
| GET | api/v3/portal/{id}/integration-field/service/{id}/modules | read | module_integration_field | Retrieve modules available within an external service. |
| GET | api/v3/portal/{id}/settings/layouts | read | module_layouts | Retrieve the list of layouts available in a module. |
| POST | api/v3/portal/{id}/settings/layouts | write | module_layouts | Create a new layout in a module. |
| GET | api/v3/portal/{id}/settings/layouts/default-layout | read | module_layouts | Retrieve the default layout configured for a module. |
| GET | api/v3/portal/{id}/settings/layouts/{id} | read | module_layouts | Retrieve the complete details of a layout including sections and associated fields. |
| PATCH | api/v3/portal/{id}/settings/layouts/{id} | write | module_layouts | Modify the details of an existing layout. |
| DELETE | api/v3/portal/{id}/settings/layouts/{id} | write | module_layouts | Remove a layout from the module. |
| GET | api/v3/portal/{id}/settings/layouts/{id}/associated-entities | read | module_layouts | Retrieve the entities associated with a layout. |
| DELETE | api/v3/portal/{id}/settings/layouts/{id}/fields/{id} | write | module_layouts | Remove a specific field from a layout. |
| GET | api/v3/portal/{id}/module/{id}/fields | read | module_meta | Retrieve the list of fields available in a module along with their metadata such as API name, display name, and field type. |
| GET | api/v3/portal/{id}/settings/options | read | module_options | Retrieve available options for a field. |
| POST | api/v3/portal/{id}/settings/options | write | module_options | Create bulk options for a field in a custom module. |
| PATCH | api/v3/portal/{id}/settings/options | write | module_options | Update existing options for a field. |
| DELETE | api/v3/portal/{id}/settings/options | write | module_options | Remove or disassociate bulk options for a field. |
| PUT | api/v3/portal/{id}/settings/layouts/{id}/sections | write | module_sections | Add or update a section in the layout. |
| DELETE | api/v3/portal/{id}/settings/layouts/{id}/sections/{id} | write | module_sections | Remove a section from a layout. |
| GET | api/v3/portal/{id}/settings/fields-configuration | read | modules | Retrieve field configuration details for a module, including supported field types and field limits. |
| GET | api/v3/portal/{id}/settings/global-statuses | read | modules | Retrieve the list of global statuses configured for a module along with their metadata such as status ID, name, color, type, and sequence order. |
| GET | api/v3/portal/{id}/settings/modules | read | modules | Retrieve a list of modules available in the portal along with their configuration details. |
| POST | api/v3/portal/{id}/settings/modules | write | modules | Create a new custom module in the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/settings/modules/bin/{id} | write | modules | Remove a module from the trash permanently. |
| POST | api/v3/portal/{id}/settings/modules/bin/{id}/recover | write | modules | Restore a module from the trash. |
| GET | api/v3/portal/{id}/settings/modules/{id} | read | modules | Retrieve the details of a specific module using its ID or API name. |
| PATCH | api/v3/portal/{id}/settings/modules/{id} | write | modules | Modify the configuration of an existing module. |
| DELETE | api/v3/portal/{id}/settings/modules/{id} | write | modules | Move a module to Trash. |
| PATCH | api/v3/portal/{id}/settings/modules/{id}/{id} | write | modules | Activate or deactivate a module. |
| GET | api/v3/portal/{id}/projects/{id}/users/me/{id}/permissions | read | my_permissions | Retrieve project permission details of the current user. |
| GET | api/v3/portal/{id}/users/me/{id}/permissions | read | my_permissions | Retrieve field permission details of the current user. |
| GET | api/v3/portal/{id}/license | read | payments | Retrieve the license details for the current portal. |
| GET | api/v3/portal/{id}/profiles/cm/{id}/permissions | read | permissions | Get permissions on a module for many Profile. |
| GET | api/v3/portal/{id}/profiles/{id}/permissions | read | permissions | Retrieve module permission details of multiple profiles. |
| GET | api/v3/portal/{id}/profiles/{id}/{id}/permissions | read | permissions | Retrieve module permission details of a profile. |
| PATCH | api/v3/portal/{id}/profiles/{id}/{id}/permissions/grant | write | permissions | Grant module permission for a profile. |
| PATCH | api/v3/portal/{id}/profiles/{id}/{id}/permissions/revoke | write | permissions | Remove module permissions for a profile. |
| GET | api/v3/portal/{id}/projects/{id}/phases/{id}/comments | read | phase_comments | Get all the comments on a phase. |
| POST | api/v3/portal/{id}/projects/{id}/phases/{id}/comments | write | phase_comments | Add a comment to a phase. |
| PATCH | api/v3/portal/{id}/projects/{id}/phases/{id}/comments/{id} | write | phase_comments | Update a comment on a phase. |
| DELETE | api/v3/portal/{id}/projects/{id}/phases/{id}/comments/{id} | write | phase_comments | Remove a comment on a phase. |
| POST | api/v3/portal/{id}/projects/{id}/phases/{id}/follow | write | phase_followers | Add followers to update about the phase. |
| GET | api/v3/portal/{id}/projects/{id}/phases/{id}/followers | read | phase_followers | Retrieve followers of a phase. |
| DELETE | api/v3/portal/{id}/projects/{id}/phases/{id}/unfollow | write | phase_followers | Remove followers from a phase. |
| GET | api/v3.1/portal/{id}/phases | read | phases | Retrieve all phases from the portal. |
| GET | api/v3.1/portal/{id}/projects/{id}/phases | read | phases | Retrieve phases from a project. |
| POST | api/v3.1/portal/{id}/projects/{id}/phases | write | phases | Create a phase in a project. |
| GET | api/v3.1/portal/{id}/projects/{id}/phases/{id} | read | phases | Retrieve details of a phase. |
| PATCH | api/v3.1/portal/{id}/projects/{id}/phases/{id} | write | phases | Update a phase in a project. |
| DELETE | api/v3.1/portal/{id}/projects/{id}/phases/{id} | write | phases | Trash a phase from a project. |
| GET | api/v3/portal/{id}/phases | read | phases | Get Phases. |
| GET | api/v3/portal/{id}/projects/{id}/phases | read | phases | Get Project Phases. |
| POST | api/v3/portal/{id}/projects/{id}/phases | write | phases | Create Phase. |
| GET | api/v3/portal/{id}/projects/{id}/phases/{id} | read | phases | Get Phase Details. |
| POST | api/v3/portal/{id}/projects/{id}/phases/{id} | write | phases | Update Phase. |
| DELETE | api/v3/portal/{id}/projects/{id}/phases/{id} | write | phases | Delete Phase. |
| GET | api/v3/portal/{id}/projects/{id}/phases/{id}/activities | read | phases | Get activities performed on a phase. |
| POST | api/v3/portal/{id}/projects/{id}/phases/{id}/clone | write | phases | Clone a phase within a project. |
| PATCH | api/v3/portal/{id}/projects/{id}/phases/{id}/move | write | phases | Move a phase to another project. |
| GET | api/v3/portal/{id}/projects/{id}/phases/{id}/status-timeline | read | phases | Retrieve the status transition history of a phase. |
| GET | api/v3/portal/{id}/projects/{id}/timelogs/pin | read | pins | Retrieve all pinned entries from the time logs weekly form for a specific project. |
| GET | api/v3/portal/{id}/timelogs/pin | read | pins | Retrieve all pinned entries from the time logs weekly form for a specific portal. |
| POST | api/v3/portal/{id}/timelogs/pin | write | pins | Pin a time log in the Zoho Projects Portal. |
| PATCH | api/v3/portal/{id}/timelogs/pin/{id} | write | pins | Update an existing pinned entry in the time logs for a portal. |
| DELETE | api/v3/portal/{id}/timelogs/pin/{id} | write | pins | Remove a pinned time log from the Zoho Projects portal. |
| GET | api/v3.1/portals | read | portals | Retrieve all portals accessible to the current user, along with their details.This is an enhanced version of the Get All Portals API. Portal metadata such as company. |
| GET | api/v3/portal/{id} | read | portals | Retrieve a specific detail of the Zoho Projects portal. |
| GET | api/v3/portals | read | portals | Get All Portals. |
| GET | api/v3/portal/{id}/profiles | read | profiles | Retrieve all profiles in a specific portal. |
| POST | api/v3/portal/{id}/profiles | write | profiles | Create a new profile in a specific portal. |
| GET | api/v3/portal/{id}/profiles/{id} | read | profiles | Retrieve the details of a specific profile in a portal. |
| PATCH | api/v3/portal/{id}/profiles/{id} | write | profiles | Modify the details of a specific profile in a portal. |
| DELETE | api/v3/portal/{id}/profiles/{id} | write | profiles | Remove a specific profile from a portal. |
| POST | api/v3/portal/{id}/profiles/{id}/setprimary | write | profiles | Set a specific profile as the default profile in a portal. |
| GET | api/v3/portal/{id}/projects/{id}/comments | read | project_comments | Retrieve comments from a project. |
| POST | api/v3/portal/{id}/projects/{id}/comments | write | project_comments | Add a comment to a project. |
| GET | api/v3/portal/{id}/projects/{id}/comments/{id} | read | project_comments | Fetch Single Comment Detail. |
| PATCH | api/v3/portal/{id}/projects/{id}/comments/{id} | write | project_comments | Modify an existing comment. |
| DELETE | api/v3/portal/{id}/projects/{id}/comments/{id} | write | project_comments | Delete Comment in a Project. |
| GET | api/v3/portal/{id}/projects/{id}/client/{id}/contacts | read | project_contacts | Retrieve all customer contacts associated with a project. |
| POST | api/v3/portal/{id}/projects/{id}/contacts | write | project_contacts | Associate existing contacts with a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/contacts | write | project_contacts | Remove contacts from a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/contacts/{id} | write | project_contacts | Disassociate a contact from a project. |
| GET | api/v3/portal/{id}/projects/customview | read | project_custom_view | Retrieve the custom views available for a specific project. |
| GET | api/v3/portal/{id}/projects/customview/{id} | read | project_custom_view | Retrieve the details of a project custom view, along with its associated fields. |
| POST | api/v3/portal/{id}/projects/customview/{id}/markanchored | write | project_custom_view | Mark a custom view as the default view for a project. |
| POST | api/v3/portal/{id}/projects/customview/{id}/markfavourite | write | project_custom_view | Mark a custom view as a favorite view for a project. |
| POST | api/v3/portal/{id}/projects/{id}/associate-client | write | project_customers | Associate customers to a project. |
| GET | api/v3/portal/{id}/projects/{id}/clients | read | project_customers | Get Project Customer. |
| POST | api/v3/portal/{id}/projects/{id}/clients | write | project_customers | Create new customer within a project in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/projects/{id}/clients/users | read | project_customers | Retrieve customers and client users associated with a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/clients/users/{id} | write | project_customers | Remove a client user from the project. |
| DELETE | api/v3/portal/{id}/projects/{id}/clients/{id} | write | project_customers | Remove a customer from the project. |
| GET | api/v3/portal/{id}/projects/{id}/crm/accounts | read | project_customers | Retrieve CRM accounts associated with a project. |
| GET | api/v3/portal/{id}/projects/{id}/crm/contacts | read | project_customers | Retrieve CRM contacts associated with a project. |
| GET | api/v3/portal/{id}/projects/{id}/crm/deals | read | project_customers | Retrieve CRM deals associated with a project in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/projects/{id}/customers | read | project_customers | Retrieve details of customers associated with a project. |
| POST | api/v3/portal/{id}/projects/{id}/primary-client/{id} | write | project_customers | Modify the primary customer for a project. |
| GET | api/v3/portal/{id}/projects/export | read | project_export | Retrieve the details of project exports from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/projects/export | write | project_export | Create a project export in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/projects/export-form | read | project_export | Retrieve the Project export form from the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/projects/export/{id} | write | project_export | Modify the details of an existing project export in the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/projects/export/{id} | write | project_export | Remove a project export from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/my-project-groups | read | project_group | Retrieve project groups associated with a user. |
| GET | api/v3/portal/{id}/project-groups | read | project_group | Retrieve all project groups from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/project-groups | write | project_group | Add a new project group in the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/project-groups/{id} | write | project_group | Update details of a project group. |
| DELETE | api/v3/portal/{id}/project-groups/{id} | write | project_group | Remove a project group from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/projects/{id}/tags | read | project_tags | Retrieve tags from a project. |
| POST | api/v3/portal/{id}/projects/{id}/tags/associate | write | project_tags | Associate tags with a module in a project. |
| POST | api/v3/portal/{id}/projects/{id}/tags/dissociate | write | project_tags | Remove associated tags from a module in a project. |
| POST | api/v3/portal/{id}/projects/{id}/associate-teams | write | project_teams | Add an existing team to a specific project. |
| DELETE | api/v3/portal/{id}/projects/{id}/dissociate-teams/{id} | write | project_teams | Remove a specific team from a project. |
| GET | api/v3/portal/{id}/projects/{id}/teams | read | project_teams | Retrieve all teams associated with a specific project. |
| GET | api/v3.1/portal/{id}/projects/{id}/users | read | project_users | Retrieve all users from a project. |
| GET | api/v3.1/portal/{id}/projects/{id}/users/{id} | read | project_users | Retrieve details of a project user from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/projects/{id}/clientuser | write | project_users | Add a client user to a specific project. |
| POST | api/v3/portal/{id}/projects/{id}/projectusers | write | project_users | Add a user to a specific project. |
| GET | api/v3/portal/{id}/projects/{id}/users | read | project_users | Get Project Users. |
| GET | api/v3/portal/{id}/projects/{id}/users/{id} | read | project_users | Get Project User Details. |
| POST | api/v3/portal/{id}/projects/{id}/users/{id} | write | project_users | Modify the details of a specific user in a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/users/{id} | write | project_users | Remove a specific user from a project. |
| GET | api/v3/portal/{id}/projects | read | projects | Retrieve a list of all projects from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/projects | write | projects | Create a new project in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/projects/{id} | read | projects | Retrieve details of a project. |
| PATCH | api/v3/portal/{id}/projects/{id} | write | projects | Modify details of an existing project. |
| DELETE | api/v3/portal/{id}/projects/{id} | write | projects | Remove a project from the trash permanently. |
| GET | api/v3/portal/{id}/projects/{id}/modules | read | projects | Get Project Associated Modules Details. |
| POST | api/v3/portal/{id}/projects/{id}/restore | write | projects | Restore a project from the trash. |
| POST | api/v3/portal/{id}/projects/{id}/trash | write | projects | Move a project to the trash. |
| GET | api/v3/portal/{id}/module/{id}/entity/{id}/attachmentcount | read | record_attachments | Retrieve the count of attachments from a record. |
| GET | api/v3/portal/{id}/module/{id}/entity/{id}/attachments | read | record_attachments | Retrieve all attachments of a record. |
| GET | api/v3/portal/{id}/module/{id}/entity/{id}/edits | read | record_audit | Retrieve all changes made to a record. |
| GET | api/v3/portal/{id}/module/{id}/entity/{id}/edits/count | read | record_audit | Retrieve the total number of edits made to a record within a module. |
| GET | api/v3/portal/{id}/module/{id}/entity/{id}/edits/{id} | read | record_audit | Retrieve edits made to a record using a specific audit ID. |
| POST | api/v3/portal/{id}/module/{id}/entity/{id}/export-status-timeline | write | record_audit | Exports status timeline of a record. |
| GET | api/v3/portal/{id}/module/{id}/entity/{id}/status-timeline | read | record_audit | Retrieve the status timeline of a record. |
| GET | api/v3/portal/{id}/module/{id}/entity/{id}/comments | read | record_comments | Retrieve all comments for a record. |
| POST | api/v3/portal/{id}/module/{id}/entity/{id}/comments | write | record_comments | Add a comment to a record. |
| GET | api/v3/portal/{id}/module/{id}/entity/{id}/comments/{id} | read | record_comments | Retrieve the details of a specific comment from a record. |
| PATCH | api/v3/portal/{id}/module/{id}/entity/{id}/comments/{id} | write | record_comments | Modify details of an existing comment in a record. |
| DELETE | api/v3/portal/{id}/module/{id}/entity/{id}/comments/{id} | write | record_comments | Remove a comment from a record. |
| GET | api/v3/portal/{id}/module/{id}/entity/{id}/count | read | record_comments | Retrieve the total number of comments for a record. |
| GET | api/v3/portal/{id}/views/{id} | read | record_custom_view | Get detail of the custom view. |
| GET | api/v3/portal/{id}/module/{id}/export | read | record_export | Retrieve scheduled and completed exports for a portal-level Custom Module. |
| POST | api/v3/portal/{id}/module/{id}/export | write | record_export | Create a Custom Module export in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/module/{id}/export/{id} | read | record_export | Retrieve the details of a specific portal-level Custom Module export, including its file format, selected fields, filter criteria, schedule and notified users. |
| PATCH | api/v3/portal/{id}/module/{id}/export/{id} | write | record_export | Modify a portal-level Custom Module export. |
| DELETE | api/v3/portal/{id}/module/{id}/export/{id} | write | record_export | Remove a portal-level Custom Module export. |
| PATCH | api/v3/portal/{id}/module/{id}/export/{id}/status | write | record_export | Toggle a portal-level Custom Module scheduled export on or off. |
| POST | api/v3/portal/{id}/module/{id}/entity/{id}/follow | write | record_followers | Add a follower to the record. |
| GET | api/v3/portal/{id}/module/{id}/entity/{id}/followers | read | record_followers | Retrieve the list of followers from the record. |
| POST | api/v3/portal/{id}/module/{id}/entity/{id}/followers | write | record_followers | Add or remove multiple followers for a record. |
| GET | api/v3/portal/{id}/module/{id}/entity/{id}/isuser | read | record_followers | Verify whether the user is a follower. |
| DELETE | api/v3/portal/{id}/module/{id}/entity/{id}/unfollow | write | record_followers | Remove a follower from the record. |
| POST | api/v3/portal/{id}/module/{id}/import | write | record_import | Initiate an import operation for a module by uploading a file. |
| GET | api/v3/portal/{id}/module/{id}/import/{id} | read | record_import | Retrieve the details of an import operation. |
| PATCH | api/v3/portal/{id}/module/{id}/import/{id} | write | record_import | Modify the details of an import operation. |
| DELETE | api/v3/portal/{id}/module/{id}/import/{id} | write | record_import | Remove an import entry from the table. |
| GET | api/v3/portal/{id}/module/{id}/import/{id}/error-details | read | record_import | Retrieve the error details of the import operation. |
| GET | api/v3/portal/{id}/module/{id}/import/{id}/file-details | read | record_import | Retrieve the details of the uploaded files for mapping in import operation. |
| GET | api/v3/portal/{id}/module/{id}/my-imports | read | record_import | Retrieve the list of import operations. |
| GET | api/v3/portal/{id}/resources/{id}/skills | read | resource_skills | Retrieve all skills associated with a specific resource along with their proficiency levels. |
| POST | api/v3/portal/{id}/resources/{id}/skills | write | resource_skills | Associate or disassociate skills for a specific resource in a single request. |
| GET | api/v3/portal/{id}/roles | read | roles | Retrieves all roles from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/roles | write | roles | Create a new role in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/roles/{id} | read | roles | Retrieve the details of a role from the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/roles/{id} | write | roles | Modify the existing role in the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/roles/{id} | write | roles | Remove a role from a Zoho Projects portal. |
| POST | api/v3/portal/{id}/roles/{id}/setprimary | write | roles | Set the default role in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/projects/{id}/search | read | search | Retrieve search results from a project. |
| GET | api/v3/portal/{id}/search | read | search | Retrieve search results from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/settings/timelog | read | settings | Retrieve the time log settings for a specific portal. |
| PATCH | api/v3/portal/{id}/settings/timelog | write | settings | Modify the time log settings of a project. |
| GET | api/v3/portal/{id}/settings/timelog/meta-data | read | settings | Retrieve the metadata for time log settings in a specific portal. |
| GET | api/v3/portal/{id}/settings/date-time | read | setup | Get the date and time settings of the portal. |
| PATCH | api/v3/portal/{id}/settings/date-time | write | setup | Update date and time settings for the portal. |
| GET | api/v3/portal/{id}/skills/{id}/history | read | skill_history | Retrieve the audit history for a specific skill, including user associations, level updates, and field edits. |
| GET | api/v3/portal/{id}/skills/{id}/resources | read | skill_resources | Retrieve all resources associated with a specific skill along with their proficiency levels. |
| POST | api/v3/portal/{id}/skills/{id}/resources | write | skill_resources | Add or remove resources from a specific skill in a single request. |
| POST | api/v3/portal/{id}/skills/{id}/resources/bulk-update | write | skill_resources | Update the proficiency level of multiple resources for a skill in a single request. |
| POST | api/v3/portal/{id}/skills/{id}/resources/{id} | write | skill_resources | Update the proficiency level of a specific resource for a skill. |
| POST | api/v3/portal/{id}/settings/skills | write | skill_settings | Enable or disable the Skill feature for the portal. |
| GET | api/v3/portal/{id}/skills/{id}/users | read | skill_users | Retrieve all portal users associated with a specific skill along with their proficiency levels. |
| POST | api/v3/portal/{id}/skills/{id}/users | write | skill_users | Add or remove portal users from a specific skill in a single request. |
| POST | api/v3/portal/{id}/skills/{id}/users/bulk-update | write | skill_users | Update the proficiency level of multiple portal users for a skill in a single request. |
| POST | api/v3/portal/{id}/skills/{id}/users/{id} | write | skill_users | Update the proficiency level of a specific portal user for a skill. |
| GET | api/v3/portal/{id}/skills | read | skills | Retrieve all skills in a portal along with their associated users, resources, and proficiency levels. |
| POST | api/v3/portal/{id}/skills | write | skills | Create a new skill in the portal that can be associated with users and resources. |
| GET | api/v3/portal/{id}/skills/{id} | read | skills | Retrieve the details of a specific skill, including its associated users and resources. |
| PATCH | api/v3/portal/{id}/skills/{id} | write | skills | Update the name or description of an existing skill. |
| DELETE | api/v3/portal/{id}/skills/{id} | write | skills | Permanently delete a skill from the portal. |
| POST | api/v3/portal/{id}/exportstatustimeline | write | status_timeline | Export Task Status Timeline. |
| GET | api/v3/portal/{id}/projects/{id}/tasks/{id}/status-timeline | read | status_timeline | Retrieve the status change timeline for a task. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/status-timeline/export | write | status_timeline | Export the status timeline of tasks from a portal. |
| GET | api/v3/portal/{id}/projects/{id}/taskstatushistory | read | status_timeline | Retrieve the status history of all tasks in a project. |
| GET | api/v3/portal/{id}/taskstatushistory | read | status_timeline | Retrieve the status history of all tasks across a portal. |
| GET | api/v3/portal/{id}/tags | read | tags | Retrieve all tags from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/tags | write | tags | Create new tags in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/tags/projects | read | tags | Get associated projects for tags. |
| PATCH | api/v3/portal/{id}/tags/{id} | write | tags | Update a tag in the Zoho Projects portal. |
| DELETE | api/v3/portal/{id}/tags/{id} | write | tags | Remove a tag from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/projects/{id}/tasks/{id}/attachments | read | task_attachment | Get all attachments of a Task. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/attachments | write | task_attachment | Associate attachments to a task. |
| GET | api/v3/portal/{id}/projects/{id}/tasks/{id}/comments | read | task_comments | Retrieve all comments from a task. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/comments | write | task_comments | Add a new comment to a task. |
| PATCH | api/v3/portal/{id}/projects/{id}/tasks/{id}/comments/{id} | write | task_comments | Modify a comment in a task. |
| DELETE | api/v3/portal/{id}/projects/{id}/tasks/{id}/comments/{id} | write | task_comments | Remove a comment from a task. |
| GET | api/v3/portal/{id}/customviews/{id} | read | task_custom_view | Get portal Custom View Details. |
| GET | api/v3/portal/{id}/projects/{id}/tasks/customviews | read | task_custom_view | Retrieve all task custom views available in a project. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/customviews/{id}/markfavourite | write | task_custom_view | Set a custom view as a favourite for a project. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/customviews/{id}/setdefaultview | write | task_custom_view | Set a custom task view as the default view for a project. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/customviews/{id}/unmarkfavourite | write | task_custom_view | Remove a custom view from the favorite views for a project. |
| GET | api/v3/portal/{id}/tasks/customviews/{id} | read | task_custom_view | Retrieve the details of a custom task view. |
| DELETE | api/v3/portal/{id}/tasks/customviews/{id} | write | task_custom_view | Remove a task custom view from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/tasks/customviews/{id}/markfavourite | write | task_custom_view | Set a custom view as a favourite at the portal level. |
| POST | api/v3/portal/{id}/tasks/customviews/{id}/setdefaultview | write | task_custom_view | Set a custom view as the default view at the portal level. |
| POST | api/v3/portal/{id}/tasks/customviews/{id}/unmarkfavourite | write | task_custom_view | Remove a custom view from favorites at the portal level. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/dependency | write | task_dependency | Create a dependency between two tasks in a project. |
| PATCH | api/v3/portal/{id}/projects/{id}/tasks/dependency | write | task_dependency | Modify the dependency between tasks in a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/tasks/dependency | write | task_dependency | Remove a task dependency between tasks in a project. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/follow | write | task_followers | Follow a task in a project. |
| GET | api/v3/portal/{id}/projects/{id}/tasks/{id}/followers | read | task_followers | Retrieve followers for a task. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/followers | write | task_followers | Add followers to a task. |
| PATCH | api/v3/portal/{id}/projects/{id}/tasks/{id}/followers | write | task_followers | API to add or update followers to a given task. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/unfollow | write | task_followers | API to unfollow a given task. |
| GET | api/v3/portal/{id}/projects/{id}/tasklists/{id}/comments | read | task_list_comments | Retrieve multiple comments from a task list. |
| POST | api/v3/portal/{id}/projects/{id}/tasklists/{id}/comments | write | task_list_comments | Add a comment to a task list. |
| GET | api/v3/portal/{id}/projects/{id}/tasklists/{id}/comments/{id} | read | task_list_comments | Retrieve a specific comment from a task list. |
| PATCH | api/v3/portal/{id}/projects/{id}/tasklists/{id}/comments/{id} | write | task_list_comments | Modify a comment in a task list. |
| DELETE | api/v3/portal/{id}/projects/{id}/tasklists/{id}/comments/{id} | write | task_list_comments | Remove a comment from a task list. |
| POST | api/v3/portal/{id}/projects/{id}/tasklists/{id}/follow | write | task_list_followers | Follow a task list to receive updates and notifications. |
| GET | api/v3/portal/{id}/projects/{id}/tasklists/{id}/followers | read | task_list_followers | Retrieve the list of followers for a specific task list. |
| POST | api/v3/portal/{id}/projects/{id}/tasklists/{id}/unfollow | write | task_list_followers | Unfollow a task list to stop receiving its notifications. |
| POST | api/v3/portal/{id}/projects/{id}/tasklists/{id}/make-as-template | write | task_list_templates | Convert a task list into a template in a project. |
| GET | api/v3/portal/{id}/templates/tasklists | read | task_list_templates | Retrieves task lists that are associated with a template in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/templates/tasklists/{id}/tasks | read | task_list_templates | Retrieve tasks from a task list template. |
| GET | api/v3/portal/{id}/all-tasklists | read | task_lists | Retrieve task lists from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/projects/{id}/default-tasklists | write | task_lists | Create Default tasklist for a Project. |
| GET | api/v3/portal/{id}/projects/{id}/tasklists | read | task_lists | Retrieve task lists associated with a specific project. |
| POST | api/v3/portal/{id}/projects/{id}/tasklists | write | task_lists | Add a Task list to the project. |
| POST | api/v3/portal/{id}/projects/{id}/tasklists/clone | write | task_lists | Create a task list in the specified project by cloning an existing task list from a project, project template, or task template. |
| GET | api/v3/portal/{id}/projects/{id}/tasklists/{id} | read | task_lists | Retrieve the details of a specific task list. |
| PATCH | api/v3/portal/{id}/projects/{id}/tasklists/{id} | write | task_lists | Modify details of the task list in a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/tasklists/{id} | write | task_lists | Remove a task list from the project. |
| POST | api/v3/portal/{id}/projects/{id}/tasklists/{id}/mark-as-closed | write | task_lists | Modify status of the task list as closed in a project. |
| PATCH | api/v3/portal/{id}/bulk-tasks | write | tasks | Modify multiple tasks at once in the Zoho Projects portal.Note: A maximum of 100 tasks across 5 unique projects can be updated per request. |
| POST | api/v3/portal/{id}/projects/{id}/bulk-tasks | write | tasks | Add a task to the project. |
| GET | api/v3/portal/{id}/projects/{id}/tasks | read | tasks | Retrieve all tasks from a specific project. |
| POST | api/v3/portal/{id}/projects/{id}/tasks | write | tasks | Add a task to the project. |
| GET | api/v3/portal/{id}/projects/{id}/tasks/count | read | tasks | Displays the total number of tasks associated with each project. |
| GET | api/v3/portal/{id}/projects/{id}/tasks/{id} | read | tasks | Retrieve the details of a specific task in a project. |
| PATCH | api/v3/portal/{id}/projects/{id}/tasks/{id} | write | tasks | Modify details of the task in a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/tasks/{id} | write | tasks | Remove a task from the project. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/bugs | write | tasks | Associate bugs to a task. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/clone | write | tasks | Clone a task to create multiple instances within the project. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/make-as-subtask | write | tasks | Convert a task into a subtask under a specified parent task in the project.Note: Parent task : The task directly above a subtask in the hierarchy. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/make-as-task | write | tasks | Convert a subtask into a root task in the project.Note: Parent task : The task directly above a subtask in the hierarchy. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/make-as-tasklist | write | tasks | to make the parent task as Tasklist. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/move | write | tasks | Move a task to a different task list or milestone within a project. |
| POST | api/v3/portal/{id}/projects/{id}/tasks/{id}/reorder | write | tasks | Update the order of tasks within a task list. |
| GET | api/v3/portal/{id}/tasks | read | tasks | Retrieve all tasks across the Zoho Projects portal. |
| GET | api/v3/portal/{id}/tasks/attachments | read | tasks | Get Tasks Attachments. |
| POST | api/v3/portal/{id}/tasks/gantt/logo | write | tasks | Upload PDF Logo. |
| POST | api/v3/portal/{id}/projects/{id}/documents/teamfolder | write | team_folder | Create a team folder in a project. |
| PUT | api/v3/portal/{id}/projects/{id}/documents/teamfolder/associate | write | team_folder | Associate an existing team folder to a project. |
| GET | api/v3/portal/{id}/projects/{id}/documents/teamfolder/{id} | read | team_folder | Retrieve the team folder settings of a project. |
| PUT | api/v3/portal/{id}/projects/{id}/documents/teamfolder/{id} | write | team_folder | Modify the settings of a team folder in a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/documents/teamfolder/{id} | write | team_folder | Remove a team folder from a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/documents/teamfolder/{id}/disassociate | write | team_folder | Disassociate team folder(s) from a project. |
| GET | api/v3/portal/{id}/teams | read | teams | Retrieve all teams in a specific portal. |
| POST | api/v3/portal/{id}/teams | write | teams | Create a new team in a specific portal. |
| GET | api/v3/portal/{id}/teams/projects | read | teams | Retrieve all projects associated with teams in a specific portal. |
| GET | api/v3/portal/{id}/teams/users | read | teams | Retrieve all users across teams in a specific portal. |
| PATCH | api/v3/portal/{id}/teams/{id} | write | teams | Modify the details of a specific team in a portal. |
| DELETE | api/v3/portal/{id}/teams/{id} | write | teams | Remove a specific team from a portal. |
| DELETE | api/v3.1/portal/{id}/projects/{id}/timelogs/{id} | write | time_log_operations | Remove the time log from a project. |
| POST | api/v3/portal/{id}/projects/{id}/log | write | time_log_operations | Add a time log to a project. |
| GET | api/v3/portal/{id}/projects/{id}/logs/{id} | read | time_log_operations | Retrieve time log details from a project. |
| PATCH | api/v3/portal/{id}/projects/{id}/logs/{id} | write | time_log_operations | Modify the time log in a project. |
| DELETE | api/v3/portal/{id}/projects/{id}/logs/{id} | write | time_log_operations | Delete Time Log. |
| GET | api/v3/portal/{id}/projects/{id}/logs/new/{id} | read | time_logs | Retrieve time log details from a project. |
| GET | api/v3/portal/{id}/projects/{id}/issue/timelogs/{id}/timers | read | timers | Retrieve timer details for a specific time log entry in a project. |
| POST | api/v3/portal/{id}/projects/{id}/issue/timelogs/{id}/timers | write | timers | Modify the notes for a timer associated with a specific time log entry in a project. |
| GET | api/v3/portal/{id}/projects/{id}/task/timelogs/{id}/timers | read | timers | Retrieve timer details for a specific time log entry in a project. |
| POST | api/v3/portal/{id}/projects/{id}/task/timelogs/{id}/timers | write | timers | Modify the notes for a timer associated with a specific time log entry in a project. |
| GET | api/v3/portal/{id}/timelogs/timers | read | timers | Retrieve all running timers from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/timelogs/timers | write | timers | Start a new timer for a module. |
| POST | api/v3/portal/{id}/timelogs/timers/pushnotification | write | timers | Push generic timers notification. |
| DELETE | api/v3/portal/{id}/timelogs/timers/{id} | write | timers | Remove a timer entry from the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/timelogs/timers/{id}/pause | write | timers | Pause a running timer in the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/timelogs/timers/{id}/resume | write | timers | Resume a paused timer in the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/timelogs/timers/{id}/stop | write | timers | Stop a running timer in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/projects/{id}/timelogs/report | read | timesheet_reports | Retrieve time log reports from a project. |
| GET | api/v3/portal/{id}/timelogs/clientreport | read | timesheet_reports | Get time log client report. |
| GET | api/v3/portal/{id}/timelogs/projectreport | read | timesheet_reports | Get time log project report. |
| GET | api/v3/portal/{id}/timelogs/report | read | timesheet_reports | Retrieve time log reports from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/timelogs/reports/count | read | timesheet_reports | Retrieve time log report count. |
| GET | api/v3/portal/{id}/bin | read | trash | Retrieve records that have been moved to the recycle bin. |
| DELETE | api/v3/portal/{id}/bin | write | trash | Remove records from the recycle bin permanently. |
| POST | api/v3/portal/{id}/bin/restore | write | trash | Restore records from the recycle bin. |
| DELETE | api/v3/portal/{id}/empty-bin | write | trash | Delete all records from the recycle bin permanently. |
| POST | api/v3/portal/{id}/trash | write | trash | Move records to the recycle bin. |
| GET | api/v3/portal/{id}/projects/{id}/users/export | read | user_exports | Retrieve the export history of project users from the past 15 days. |
| POST | api/v3/portal/{id}/projects/{id}/users/export | write | user_exports | Export all users in a specific project. |
| GET | api/v3/portal/{id}/projects/{id}/users/export/{id} | read | user_exports | Retrieve the details of a specific project user export using its export ID. Use this API to access the status and download link of a previously initiated export. |
| GET | api/v3/portal/{id}/users/export | read | user_exports | Retrieve the export history of portal users from the past 15 days. |
| POST | api/v3/portal/{id}/users/export | write | user_exports | Export the portal users from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/users/export/{id} | read | user_exports | Retrieve the details of a specific portal user export using its export ID. Use this API to access the status and download link of a previously initiated export. |
| GET | api/v3/portal/{id}/user/{id}/descendants | read | user_hierarchy | Retrieve all subordinates of a specific user in a portal. |
| GET | api/v3/portal/{id}/projects/{id}/users/{id}/permissions | read | user_permissions | Retrieve module permission details of a user in a project. |
| PATCH | api/v3/portal/{id}/projects/{id}/users/{id}/permissions | write | user_permissions | Modify project permissions for a user. |
| GET | api/v3/portal/{id}/projects/{id}/users/{id}/{id}/permissions | read | user_permissions | Retrieve project permission details of the user. |
| GET | api/v3/portal/{id}/users/{id}/skills | read | user_skills | Retrieve all skills associated with a specific portal user along with their proficiency levels. |
| POST | api/v3/portal/{id}/users/{id}/skills | write | user_skills | Associate or dissociate skills for a specific portal user in a single request. |
| GET | api/v3.1/portal/{id}/users | read | users | Retrieve all users, client users, and contacts from the Zoho Projects portal. |
| POST | api/v3.1/portal/{id}/users | write | users | Modify the details of existing users in the Zoho Projects portal. |
| GET | api/v3.1/portal/{id}/users/{id} | read | users | Retrieve details of a user from the Zoho Projects portal. |
| PATCH | api/v3.1/portal/{id}/users/{id} | write | users | Modify the details of an existing user in the Zoho Projects portal. |
| POST | api/v3/portal/{id}/client-users/{id}/activate | write | users | Activate a specific client user in a portal. |
| POST | api/v3/portal/{id}/client-users/{id}/deactivate | write | users | Deactivate a specific client user in a portal. |
| POST | api/v3/portal/{id}/clientuser | write | users | Add a new client user to the Zoho Projects portal. |
| GET | api/v3/portal/{id}/users | read | users | Get Users. |
| POST | api/v3/portal/{id}/users | write | users | Add a new user to the Zoho Projects portal. |
| GET | api/v3/portal/{id}/users/license-details | read | users | Retrieve the license details of portal and client users in a specific portal. |
| GET | api/v3/portal/{id}/users/{id} | read | users | Get User Details. |
| POST | api/v3/portal/{id}/users/{id} | write | users | Update User. |
| DELETE | api/v3/portal/{id}/users/{id} | write | users | Remove a specific user from a portal. |
| POST | api/v3/portal/{id}/users/{id}/activate | write | users | Activate a specific user in a portal. |
| GET | api/v3/portal/{id}/users/{id}/audit-logs | read | users | Retrieve audit details of a user from the Zoho Projects portal. |
| POST | api/v3/portal/{id}/users/{id}/deactivate | write | users | Deactivate a specific user in a portal. |
| GET | api/v3/portal/{id}/users/{id}/projects | read | users | Retrieve all projects associated with a specific user in a portal. |
| GET | api/v3/portal/{id}/users/{id}/teams | read | users | Retrieve the details of the teams associated with a user. |
| GET | api/v3/portal/{id}/users/email-templates | read | users_invitation_templates | Retrieve all invitation templates from a portal. |
| POST | api/v3/portal/{id}/users/email-templates | write | users_invitation_templates | Create a new invitation template in the Zoho Projects portal. |
| GET | api/v3/portal/{id}/users/email-templates/{id} | read | users_invitation_templates | Retrieve the details of a specific invitation template in a portal. |
| PATCH | api/v3/portal/{id}/users/email-templates/{id} | write | users_invitation_templates | Update a specific invitation template in a portal. |
| DELETE | api/v3/portal/{id}/users/email-templates/{id} | write | users_invitation_templates | Remove a specific invitation template from the Zoho Projects portal. |
| PATCH | api/v3/portal/{id}/users/email-templates/{id}/make-default | write | users_invitation_templates | Set the invitation template as the default one. |
| DELETE | api/v3/portal/{id}/users/email-templates/{id}/make-default | write | users_invitation_templates | Remove the invitation template as the default. |
| PUT | api/v3/portal/{id}/reports/custom-workload | write | workload | Create or Update a custom workload report in the Zoho projects portal. |
| GET | api/v3/portal/{id}/reports/workload | read | workload | Retrieve workload report details from the Zoho projects portal. |
| GET | api/v3/portal/{id}/reports/workload/details | read | workload | Retrieve allocated work details of multiple users or resources from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/reports/workload/entity/{id}/details | read | workload | Retrieve the workload details of a task from the Zoho Projects portal. |
| GET | api/v3/portal/{id}/reports/workload/groups | read | workload | Retrieve the groups from the workload report. |
| GET | api/v3/portal/{id}/reports/workload/groups/owners | read | workload | Retrieve the list of records across multiple groups in the workload report. |
| GET | api/v3/portal/{id}/reports/workload/groups/{id}/owners | read | workload | Retrieve the list of records that belong to a specific group in the workload report. |
| GET | api/v3/portal/{id}/reports/workload/meta | read | workload | Retrieve workload report meta details from the Zoho projects portal. |
| GET | api/v3/portal/{id}/reports/workload/owner/{id}/details | read | workload | Retrieve allocated work details of an existing user or resource from the Zoho Projects portal. |
