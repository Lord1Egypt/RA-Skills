# Wrike access policy

An access policy limits which endpoints Wrike connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/wrike#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Wrike: its 103 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create wrike --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/v4/access_roles"},
    {"method": "GET", "path": "api/v4/account"},
    {"method": "GET", "path": "api/v4/approvals"},
    {"method": "GET", "path": "api/v4/approvals/{id}"},
    {"method": "GET", "path": "api/v4/folders/{id}/approvals"},
    {"method": "GET", "path": "api/v4/tasks/{id}/approvals"},
    {"method": "GET", "path": "api/v4/async_job/{id}"},
    {"method": "GET", "path": "api/v4/attachments"},
    {"method": "GET", "path": "api/v4/attachments/{id}"},
    {"method": "GET", "path": "api/v4/attachments/{id}/download"},
    {"method": "GET", "path": "api/v4/attachments/{id}/preview"},
    {"method": "GET", "path": "api/v4/folders/{id}/attachments"},
    {"method": "GET", "path": "api/v4/tasks/{id}/attachments"},
    {"method": "GET", "path": "api/v4/audit_log"},
    {"method": "GET", "path": "api/v4/bookings"},
    {"method": "GET", "path": "api/v4/bookings/{id}"},
    {"method": "GET", "path": "api/v4/folders/{id}/bookings"},
    {"method": "GET", "path": "api/v4/colors"},
    {"method": "GET", "path": "api/v4/comments"},
    {"method": "GET", "path": "api/v4/comments/{id}"},
    {"method": "GET", "path": "api/v4/comments/{id}/comments"},
    {"method": "GET", "path": "api/v4/folders/{id}/comments"},
    {"method": "GET", "path": "api/v4/tasks/{id}/comments"},
    {"method": "GET", "path": "api/v4/contacts"},
    {"method": "GET", "path": "api/v4/contacts/{id}"},
    {"method": "GET", "path": "api/v4/contacts/{id}/contacts_history"},
    {"method": "GET", "path": "api/v4/customfields"},
    {"method": "GET", "path": "api/v4/customfields/{id}"},
    {"method": "GET", "path": "api/v4/spaces/{id}/customfields"},
    {"method": "GET", "path": "api/v4/custom_item_types"},
    {"method": "GET", "path": "api/v4/custom_item_types/{id}"},
    {"method": "GET", "path": "api/v4/spaces/{id}/custom_item_types"},
    {"method": "GET", "path": "api/v4/data_export"},
    {"method": "GET", "path": "api/v4/data_export/{id}"},
    {"method": "GET", "path": "api/v4/data_export_schema"},
    {"method": "GET", "path": "api/v4/dependencies/{id}"},
    {"method": "GET", "path": "api/v4/folders/{id}/dependencies"},
    {"method": "GET", "path": "api/v4/tasks/{id}/dependencies"},
    {"method": "POST", "path": "api/v4/ediscovery_search"},
    {"method": "GET", "path": "api/v4/folder_blueprints"},
    {"method": "GET", "path": "api/v4/spaces/{id}/folder_blueprints"},
    {"method": "GET", "path": "api/v4/folders"},
    {"method": "GET", "path": "api/v4/folders/{id}"},
    {"method": "GET", "path": "api/v4/folders/{id}/folders"},
    {"method": "GET", "path": "api/v4/folders/{id}/folders_history"},
    {"method": "GET", "path": "api/v4/spaces/{id}/folders"},
    {"method": "GET", "path": "api/v4/groups"},
    {"method": "GET", "path": "api/v4/groups/{id}"},
    {"method": "GET", "path": "api/v4/contacts/{id}/hourly_rates"},
    {"method": "GET", "path": "api/v4/folders/{id}/hourly_rates"},
    {"method": "GET", "path": "api/v4/placeholders/{id}/hourly_rates"},
    {"method": "GET", "path": "api/v4/ids"},
    {"method": "GET", "path": "api/v4/invitations"},
    {"method": "GET", "path": "api/v4/jobroles"},
    {"method": "GET", "path": "api/v4/jobroles/{id}"},
    {"method": "GET", "path": "api/v4/placeholders"},
    {"method": "GET", "path": "api/v4/placeholders/{id}"},
    {"method": "GET", "path": "api/v4/request_forms"},
    {"method": "GET", "path": "api/v4/request_forms/{id}"},
    {"method": "GET", "path": "api/v4/spaces/{id}/request_forms"},
    {"method": "POST", "path": "api/v4/request_forms/{id}/prefill_url"},
    {"method": "GET", "path": "api/v4/folders/{id}/rollups"},
    {"method": "GET", "path": "api/v4/tasks/{id}/rollups"},
    {"method": "GET", "path": "api/v4/spaces"},
    {"method": "GET", "path": "api/v4/spaces/{id}"},
    {"method": "GET", "path": "api/v4/spaces/{id}/task_blueprints"},
    {"method": "GET", "path": "api/v4/task_blueprints"},
    {"method": "GET", "path": "api/v4/folders/{id}/tasks"},
    {"method": "GET", "path": "api/v4/spaces/{id}/tasks"},
    {"method": "GET", "path": "api/v4/tasks"},
    {"method": "GET", "path": "api/v4/tasks/{id}"},
    {"method": "GET", "path": "api/v4/tasks/{id}/tasks_history"},
    {"method": "GET", "path": "api/v4/timelog_categories"},
    {"method": "GET", "path": "api/v4/folders/{id}/timelog_lock_periods"},
    {"method": "GET", "path": "api/v4/spaces/{id}/timelog_lock_periods"},
    {"method": "GET", "path": "api/v4/tasks/{id}/timelog_lock_periods"},
    {"method": "GET", "path": "api/v4/contacts/{id}/timelogs"},
    {"method": "GET", "path": "api/v4/folders/{id}/timelogs"},
    {"method": "GET", "path": "api/v4/tasks/{id}/timelogs"},
    {"method": "GET", "path": "api/v4/timelog_categories/{id}/timelogs"},
    {"method": "GET", "path": "api/v4/timelogs"},
    {"method": "GET", "path": "api/v4/timelogs/{id}"},
    {"method": "GET", "path": "api/v4/timesheet_submission_rules"},
    {"method": "GET", "path": "api/v4/workschedules/{id}/timesheet_submission_rules"},
    {"method": "GET", "path": "api/v4/timesheets"},
    {"method": "GET", "path": "api/v4/user_schedule_capacity_change"},
    {"method": "GET", "path": "api/v4/user_schedule_capacity_change/{id}"},
    {"method": "GET", "path": "api/v4/user_schedule_exclusions"},
    {"method": "GET", "path": "api/v4/user_schedule_exclusions/{id}"},
    {"method": "GET", "path": "api/v4/user_schedule_partial_exclusion"},
    {"method": "GET", "path": "api/v4/user_schedule_partial_exclusion/{id}"},
    {"method": "GET", "path": "api/v4/user_types"},
    {"method": "GET", "path": "api/v4/users/{id}"},
    {"method": "GET", "path": "api/v4/version"},
    {"method": "GET", "path": "api/v4/whiteboard_ids"},
    {"method": "GET", "path": "api/v4/workschedule_capacity_change/{id}"},
    {"method": "GET", "path": "api/v4/workschedules/{id}/workschedule_capacity_change"},
    {"method": "GET", "path": "api/v4/workschedule_exclusions/{id}"},
    {"method": "GET", "path": "api/v4/workschedules/{id}/workschedule_exclusions"},
    {"method": "GET", "path": "api/v4/workschedules"},
    {"method": "GET", "path": "api/v4/workschedules/{id}"},
    {"method": "GET", "path": "api/v4/spaces/{id}/workflows"},
    {"method": "GET", "path": "api/v4/workflows"}
  ],
  "deny": []
}
```

## Endpoints

The Wrike endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/v4/access_roles | read | access-roles | Get Access Roles. |
| GET | api/v4/account | read | account | Query Accounts. |
| PUT | api/v4/account | write | account | Modify Account. |
| GET | api/v4/approvals | read | approvals | Get Approvals (Account). |
| GET | api/v4/approvals/{id} | read | approvals | Get Approvals By ID. |
| PUT | api/v4/approvals/{id} | write | approvals | Update approval. |
| DELETE | api/v4/approvals/{id} | write | approvals | Cancel approval. |
| GET | api/v4/folders/{id}/approvals | read | approvals | Get Approvals (Folder). |
| POST | api/v4/folders/{id}/approvals | write | approvals | Create Approvals (Folder). |
| GET | api/v4/tasks/{id}/approvals | read | approvals | Get Approvals (Task). |
| POST | api/v4/tasks/{id}/approvals | write | approvals | Create Approvals (Task). |
| POST | api/v4/assets | write | assets | Create Equipment. |
| PUT | api/v4/assets/{id} | write | assets | Update Equipment. |
| DELETE | api/v4/assets/{id} | write | assets | Delete Equipment. |
| GET | api/v4/async_job/{id} | read | async-job | Get async job. |
| GET | api/v4/attachments | read | attachments | Get Attachments (Account). |
| GET | api/v4/attachments/{id} | read | attachments | Get Attachments By ID. |
| PUT | api/v4/attachments/{id} | write | attachments | Update Attachment. |
| DELETE | api/v4/attachments/{id} | write | attachments | Delete Attachment. |
| GET | api/v4/attachments/{id}/download | read | attachments | Download Attachment. |
| GET | api/v4/attachments/{id}/preview | read | attachments | Preview Attachment. |
| GET | api/v4/attachments/{id}/url | write | attachments | Get Attachment URL. Kept out of read: returns a time-limited public link to the file. |
| GET | api/v4/folders/{id}/attachments | read | attachments | Get Attachments (Folder). |
| POST | api/v4/folders/{id}/attachments | write | attachments | Create Attachment (Folder). |
| GET | api/v4/tasks/{id}/attachments | read | attachments | Get Attachments (Task). |
| POST | api/v4/tasks/{id}/attachments | write | attachments | Create Attachment (Task). |
| GET | api/v4/audit_log | read | audit-log | Get Audit Log. |
| POST | api/v4/batch | write | batch-operations | Create Batch Operation. |
| GET | api/v4/bookings | read | bookings | Get Bookings (Account). |
| GET | api/v4/bookings/{id} | read | bookings | Get Bookings By ID. |
| PUT | api/v4/bookings/{id} | write | bookings | Update Booking. |
| DELETE | api/v4/bookings/{id} | write | bookings | Delete Booking. |
| GET | api/v4/folders/{id}/bookings | read | bookings | Get Bookings (Folder). |
| POST | api/v4/folders/{id}/bookings | write | bookings | Create Booking. |
| POST | api/v4/folders/{id}/cascading_field_settings | write | cascading-field-settings | Trigger field cascading. |
| DELETE | api/v4/folders/{id}/cascading_field_settings | write | cascading-field-settings | Delete active cascading field settings. |
| POST | api/v4/tasks/{id}/cascading_field_settings | write | cascading-field-settings | Trigger field cascading. |
| DELETE | api/v4/tasks/{id}/cascading_field_settings | write | cascading-field-settings | Delete active cascading field settings. |
| GET | api/v4/colors | read | colors | Query Colors. |
| GET | api/v4/comments | read | comments | Get Comments (Account). |
| GET | api/v4/comments/{id} | read | comments | Get Comments By ID. |
| PUT | api/v4/comments/{id} | write | comments | Update Comment. |
| DELETE | api/v4/comments/{id} | write | comments | Delete Comment. |
| GET | api/v4/comments/{id}/comments | read | comments | Get Comment Replies. |
| POST | api/v4/comments/{id}/comments | write | comments | Create Comment Reply. |
| GET | api/v4/folders/{id}/comments | read | comments | Get Comments (Folder). |
| POST | api/v4/folders/{id}/comments | write | comments | Create Comment (Folder). |
| GET | api/v4/tasks/{id}/comments | read | comments | Get Comments (Task). |
| POST | api/v4/tasks/{id}/comments | write | comments | Create Comment (Task). |
| GET | api/v4/contacts | read | contacts | Query Contacts. |
| GET | api/v4/contacts/{id} | read | contacts | Query Contacts. |
| PUT | api/v4/contacts/{id} | write | contacts | Modify Contact. |
| GET | api/v4/contacts/{id}/contacts_history | read | contacts | Query Contacts fields history. |
| POST | api/v4/workschedules/{id}/duplicate | write | copy-work-schedule | Copy Work Schedule. |
| GET | api/v4/customfields | read | custom-fields | Get Custom Fields (Account). |
| POST | api/v4/customfields | write | custom-fields | Create Custom Field (Account). |
| GET | api/v4/customfields/{id} | read | custom-fields | Get Custom Fields By ID. |
| PUT | api/v4/customfields/{id} | write | custom-fields | Modify Custom Field. |
| GET | api/v4/spaces/{id}/customfields | read | custom-fields | Get Custom Fields (Space). |
| GET | api/v4/custom_item_types | read | custom-item-types | Query All Custom Item Types. |
| GET | api/v4/custom_item_types/{id} | read | custom-item-types | Query Specific Custom Item Type by ID. |
| POST | api/v4/custom_item_types/{id}/instantiate | write | custom-item-types | Create Work from Custom Item Type. |
| GET | api/v4/spaces/{id}/custom_item_types | read | custom-item-types | Query All Custom Item Types. |
| GET | api/v4/data_export | read | data-export | Get Data Export. |
| POST | api/v4/data_export | write | data-export | Refresh Data Export. |
| GET | api/v4/data_export/{id} | read | data-export | Get Data Export. |
| GET | api/v4/data_export_schema | read | data-export-schema | Get Data Export Schema. |
| GET | api/v4/dependencies/{id} | read | dependencies | Get Dependencies By ID. |
| PUT | api/v4/dependencies/{id} | write | dependencies | Modify Dependency. |
| DELETE | api/v4/dependencies/{id} | write | dependencies | Delete Dependency. |
| GET | api/v4/folders/{id}/dependencies | read | dependencies | Get Dependencies (Project). |
| POST | api/v4/folders/{id}/dependencies | write | dependencies | Create Dependency (Project). |
| GET | api/v4/tasks/{id}/dependencies | read | dependencies | Get Dependencies (Task). |
| POST | api/v4/tasks/{id}/dependencies | write | dependencies | Create Dependency (Task). |
| POST | api/v4/ediscovery_search | read | ediscovery | eDiscovery Search. |
| GET | api/v4/folder_blueprints | read | folder-blueprints | Get Folder Blueprints (Account). |
| POST | api/v4/folder_blueprints/{id}/launch_async | write | folder-blueprints | Async Work Creation. |
| GET | api/v4/spaces/{id}/folder_blueprints | read | folder-blueprints | Get Folder Blueprints (Space). |
| POST | api/v4/copy_folder/{id} | write | folders-projects | Copy Folder. |
| POST | api/v4/copy_folder_async/{id} | write | folders-projects | Copy Folder async. |
| GET | api/v4/folders | read | folders-projects | Get Folders (Account). |
| GET | api/v4/folders/{id} | read | folders-projects | Get Folder By ID. |
| PUT | api/v4/folders/{id} | write | folders-projects | Update Folders (Bulk). |
| DELETE | api/v4/folders/{id} | write | folders-projects | Delete Folder. |
| GET | api/v4/folders/{id}/folders | read | folders-projects | Get Folders (Folder). |
| POST | api/v4/folders/{id}/folders | write | folders-projects | Create Folder. |
| GET | api/v4/folders/{id}/folders_history | read | folders-projects | Query Folders fields history. |
| GET | api/v4/spaces/{id}/folders | read | folders-projects | Get Folders (Space). |
| GET | api/v4/groups | read | groups | Query Groups. |
| POST | api/v4/groups | write | groups | Create Groups. |
| GET | api/v4/groups/{id} | read | groups | Query Groups. |
| PUT | api/v4/groups/{id} | write | groups | Modify Groups. |
| DELETE | api/v4/groups/{id} | write | groups | Delete Groups. |
| PUT | api/v4/groups_bulk | write | groups | Bulk modify groups. |
| GET | api/v4/contacts/{id}/hourly_rates | read | hourly-rates | Get Budget Rates (Contacts). |
| GET | api/v4/folders/{id}/hourly_rates | read | hourly-rates | Get Budget Rates (Folder). |
| PUT | api/v4/folders/{id}/hourly_rates | write | hourly-rates | Update Budget Rates (Folder). |
| DELETE | api/v4/folders/{id}/project_team_members | write | hourly-rates | Exclude team members. |
| PUT | api/v4/hourly_rates | write | hourly-rates | Update Budget Rates (Account). |
| GET | api/v4/placeholders/{id}/hourly_rates | read | hourly-rates | Get Budget Rates (Placeholders). |
| PUT | api/v4/contacts/{id}/hourly_rates_provision | write | hourly-rates-provision | Provision. |
| GET | api/v4/ids | read | ids | Legacy API v2 IDs converter. |
| GET | api/v4/invitations | read | invitations | Query Invitations. |
| POST | api/v4/invitations | write | invitations | Create Invitation. |
| PUT | api/v4/invitations/{id} | write | invitations | Update Invitation. |
| DELETE | api/v4/invitations/{id} | write | invitations | Delete Invitation. |
| GET | api/v4/jobroles | read | job-roles | Get Job Roles (Account). |
| POST | api/v4/jobroles | write | job-roles | Create Job Role. |
| GET | api/v4/jobroles/{id} | read | job-roles | Get Job Roles By ID. |
| PUT | api/v4/jobroles/{id} | write | job-roles | Update Job Role. |
| DELETE | api/v4/jobroles/{id} | write | job-roles | Delete Job Role. |
| GET | api/v4/placeholders | read | placeholders | Get Placeholders (Account). |
| GET | api/v4/placeholders/{id} | read | placeholders | Get Placeholders By ID. |
| GET | api/v4/request_forms | read | request-forms | Query Request Forms. |
| GET | api/v4/request_forms/{id} | read | request-forms | Get Request Form by ID. |
| GET | api/v4/spaces/{id}/request_forms | read | request-forms | Query Request Forms. |
| POST | api/v4/request_forms/{id}/prefill_url | read | request-forms-prefill | Generate prefilled Request Form URL. |
| POST | api/v4/request_forms/{id}/submit | write | request-forms-submit | Submit Request Form. |
| GET | api/v4/folders/{id}/rollups | read | rollups | Get Rollup Settings (Folder). |
| PUT | api/v4/folders/{id}/rollups | write | rollups | Update Rollup Settings (Folder). |
| GET | api/v4/tasks/{id}/rollups | read | rollups | Get Rollup Settings (Task). |
| PUT | api/v4/tasks/{id}/rollups | write | rollups | Update Rollup Settings (Task). |
| GET | api/v4/spaces | read | spaces | Get Spaces (Account). |
| POST | api/v4/spaces | write | spaces | Create Space. |
| GET | api/v4/spaces/{id} | read | spaces | Get Space By ID. |
| PUT | api/v4/spaces/{id} | write | spaces | Update Space. |
| DELETE | api/v4/spaces/{id} | write | spaces | Delete Space. |
| GET | api/v4/spaces/{id}/task_blueprints | read | task-blueprints | Get Task Blueprints (Space). |
| GET | api/v4/task_blueprints | read | task-blueprints | Get Task Blueprints (Account). |
| POST | api/v4/task_blueprints/{id}/launch_async | write | task-blueprints | Async Work Creation. |
| GET | api/v4/folders/{id}/tasks | read | tasks | Get Tasks (Folder). |
| POST | api/v4/folders/{id}/tasks | write | tasks | Create Task (Folder). |
| GET | api/v4/spaces/{id}/tasks | read | tasks | Get Tasks (Space). |
| GET | api/v4/tasks | read | tasks | Get Tasks (Account). |
| GET | api/v4/tasks/{id} | read | tasks | Get Tasks By IDs. |
| PUT | api/v4/tasks/{id} | write | tasks | Update Tasks (Bulk). |
| DELETE | api/v4/tasks/{id} | write | tasks | Delete Tasks By ID. |
| GET | api/v4/tasks/{id}/tasks_history | read | tasks | Query Tasks fields history. |
| GET | api/v4/timelog_categories | read | timelog-categories | Query Timelog categories. |
| GET | api/v4/folders/{id}/timelog_lock_periods | read | timelog-lock-periods | Get Timelog Locks (Folder). |
| POST | api/v4/folders/{id}/timelog_lock_periods | write | timelog-lock-periods | Create Timelog Lock (Folder). |
| DELETE | api/v4/folders/{id}/timelog_lock_periods | write | timelog-lock-periods | Delete Timelog Lock (Folder). |
| GET | api/v4/spaces/{id}/timelog_lock_periods | read | timelog-lock-periods | Get Timelog Locks (Space). |
| POST | api/v4/spaces/{id}/timelog_lock_periods | write | timelog-lock-periods | Create Timelog Lock (Space). |
| DELETE | api/v4/spaces/{id}/timelog_lock_periods | write | timelog-lock-periods | Delete Timelog Lock (Space). |
| GET | api/v4/tasks/{id}/timelog_lock_periods | read | timelog-lock-periods | Get Timelog Locks (Task). |
| GET | api/v4/contacts/{id}/timelogs | read | timelogs | Get Timelogs (User). |
| GET | api/v4/folders/{id}/timelogs | read | timelogs | Get Timelogs (Folder). |
| GET | api/v4/tasks/{id}/timelogs | read | timelogs | Get Timelogs (Task). |
| POST | api/v4/tasks/{id}/timelogs | write | timelogs | Create Timelog. |
| GET | api/v4/timelog_categories/{id}/timelogs | read | timelogs | Get Timelogs (Category). |
| GET | api/v4/timelogs | read | timelogs | Get Timelogs (Account). |
| GET | api/v4/timelogs/{id} | read | timelogs | Get Timelogs By ID. |
| PUT | api/v4/timelogs/{id} | write | timelogs | Modify Timelog. |
| DELETE | api/v4/timelogs/{id} | write | timelogs | Delete Timelog. |
| PUT | api/v4/timesheet_rows/{id} | write | timesheet-rows | Update Timesheet Row. |
| GET | api/v4/timesheet_submission_rules | read | timesheet-submission-rules | Get Timesheet Submission Rules (Account). |
| GET | api/v4/workschedules/{id}/timesheet_submission_rules | read | timesheet-submission-rules | Get Timesheet Submission Rules (Work Schedule). |
| PUT | api/v4/workschedules/{id}/timesheet_submission_rules | write | timesheet-submission-rules | Update Timesheet Submission Rules. |
| GET | api/v4/timesheets | read | timesheets | Query Timesheets. |
| POST | api/v4/timesheets | write | timesheets | Create Timesheet. |
| PUT | api/v4/timesheets/{id} | write | timesheets | Update Timesheet. |
| GET | api/v4/user_schedule_capacity_change | read | user-schedule-capacity-changes | Get Work Schedule Capacity Changes (User). |
| GET | api/v4/user_schedule_capacity_change/{id} | read | user-schedule-capacity-changes | Get User Work Schedule Capacity Change by ID. |
| PUT | api/v4/user_schedule_capacity_change/{id} | write | user-schedule-capacity-changes | Update User Schedule Capacity change. |
| DELETE | api/v4/user_schedule_capacity_change/{id} | write | user-schedule-capacity-changes | Delete User Schedule Capacity change. |
| POST | api/v4/users/{id}/user_schedule_capacity_change | write | user-schedule-capacity-changes | Create User Schedule Capacity change. |
| GET | api/v4/user_schedule_exclusions | read | user-schedule-exceptions | Query User Schedule exception. |
| POST | api/v4/user_schedule_exclusions | write | user-schedule-exceptions | Create User Schedule exception. |
| GET | api/v4/user_schedule_exclusions/{id} | read | user-schedule-exceptions | Query User Schedule exception. |
| PUT | api/v4/user_schedule_exclusions/{id} | write | user-schedule-exceptions | Update User Schedule exception. |
| DELETE | api/v4/user_schedule_exclusions/{id} | write | user-schedule-exceptions | Delete User Schedule exception. |
| GET | api/v4/user_schedule_partial_exclusion | read | user-schedule-partial-exclusions | Query User Schedule partial exceptions. |
| POST | api/v4/user_schedule_partial_exclusion | write | user-schedule-partial-exclusions | Create User Schedule partial exception. |
| GET | api/v4/user_schedule_partial_exclusion/{id} | read | user-schedule-partial-exclusions | Query User Schedule partial exceptions. |
| PUT | api/v4/user_schedule_partial_exclusion/{id} | write | user-schedule-partial-exclusions | Update User Schedule partial exception. |
| DELETE | api/v4/user_schedule_partial_exclusion/{id} | write | user-schedule-partial-exclusions | Delete User Schedule partial exception. |
| GET | api/v4/user_types | read | user-types | Get User Types. |
| GET | api/v4/users/{id} | read | users | Query User. |
| PUT | api/v4/users/{id} | write | users | Modify User. |
| GET | api/v4/version | read | version | API Version. |
| GET | api/v4/whiteboard_ids | read | whiteboard-ids-converter | Convert whiteboard ID formats. |
| GET | api/v4/workschedule_capacity_change/{id} | read | work-schedule-capacity-changes | Get Work Schedule Capacity Changes by Change ID. |
| PUT | api/v4/workschedule_capacity_change/{id} | write | work-schedule-capacity-changes | Update Work Schedule capacity change. |
| DELETE | api/v4/workschedule_capacity_change/{id} | write | work-schedule-capacity-changes | Delete Work Schedule capacity change. |
| GET | api/v4/workschedules/{id}/workschedule_capacity_change | read | work-schedule-capacity-changes | Get Work Schedule Capacity Changes (Work Schedule). |
| POST | api/v4/workschedules/{id}/workschedule_capacity_change | write | work-schedule-capacity-changes | Create Work Schedule capacity change. |
| GET | api/v4/workschedule_exclusions/{id} | read | work-schedule-exceptions | Get Work Schedule Exception by ID. |
| PUT | api/v4/workschedule_exclusions/{id} | write | work-schedule-exceptions | Update Work Schedule exception. |
| DELETE | api/v4/workschedule_exclusions/{id} | write | work-schedule-exceptions | Delete Work Schedule exception. |
| GET | api/v4/workschedules/{id}/workschedule_exclusions | read | work-schedule-exceptions | Get Work Schedule Exceptions (Work Schedule). |
| POST | api/v4/workschedules/{id}/workschedule_exclusions | write | work-schedule-exceptions | Create Work Schedule exception. |
| GET | api/v4/workschedules | read | work-schedules | Query Work Schedules. |
| POST | api/v4/workschedules | write | work-schedules | Create Work Schedule. |
| GET | api/v4/workschedules/{id} | read | work-schedules | Query Work Schedules. |
| PUT | api/v4/workschedules/{id} | write | work-schedules | Update Work Schedule. |
| DELETE | api/v4/workschedules/{id} | write | work-schedules | Delete Work Schedule. |
| GET | api/v4/spaces/{id}/workflows | read | workflows | Query Workflows. |
| GET | api/v4/workflows | read | workflows | Query Workflows. |
| POST | api/v4/workflows | write | workflows | Create Workflow. |
| PUT | api/v4/workflows/{id} | write | workflows | Modify Workflow. |
