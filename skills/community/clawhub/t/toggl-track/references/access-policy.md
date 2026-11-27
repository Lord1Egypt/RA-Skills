# Toggl Track access policy

An access policy limits which endpoints Toggl Track connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/toggl-track#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Toggl Track: its 169 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create toggl-track --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/v9/workspaces/{id}/alerts"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/alerts/{id}/deliveries"},
    {"method": "GET", "path": "api/v9/audit_logs/{id}/{id}/{id}"},
    {"method": "GET", "path": "api/v9/auth/saml2/login"},
    {"method": "GET", "path": "api/v9/me/clients"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/clients"},
    {"method": "POST", "path": "api/v9/workspaces/{id}/clients/data"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/clients/{id}"},
    {"method": "GET", "path": "api/v9/countries"},
    {"method": "GET", "path": "api/v9/countries/{id}/subdivisions"},
    {"method": "GET", "path": "api/v9/currencies"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/currencies"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/dashboard/all_activity"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/dashboard/most_active"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/dashboard/top_activity"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/expenses"},
    {"method": "GET", "path": "api/v9/me/export/data/{id}"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/exports/data/{id}"},
    {"method": "GET", "path": "api/v9/me/favorites"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/favorites"},
    {"method": "GET", "path": "api/v9/me/features"},
    {"method": "GET", "path": "api/v9/me/flags"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/goals"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/goals/{id}"},
    {"method": "GET", "path": "api/v9/organizations/{id}/groups"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/groups"},
    {"method": "GET", "path": "api/v9/ical/workspace_user/{id}"},
    {"method": "GET", "path": "api/v9/me/id"},
    {"method": "POST", "path": "insights/api/v1/workspace/{id}/data_trends/projects"},
    {"method": "POST", "path": "insights/api/v1/workspace/{id}/profitability/employees.csv"},
    {"method": "POST", "path": "insights/api/v1/workspace/{id}/profitability/employees.xlsx"},
    {"method": "POST", "path": "insights/api/v1/workspace/{id}/profitability/projects.csv"},
    {"method": "POST", "path": "insights/api/v1/workspace/{id}/profitability/projects.xlsx"},
    {"method": "POST", "path": "insights/api/v1/workspace/{id}/trends/projects.csv"},
    {"method": "POST", "path": "insights/api/v1/workspace/{id}/trends/projects.xlsx"},
    {"method": "GET", "path": "api/v9/integrations/calendar"},
    {"method": "GET", "path": "api/v9/integrations/calendar/calendars"},
    {"method": "GET", "path": "api/v9/integrations/calendar/calendars/selected"},
    {"method": "GET", "path": "api/v9/integrations/calendar/events"},
    {"method": "POST", "path": "api/v9/integrations/calendar/events/details-suggestion"},
    {"method": "GET", "path": "api/v9/integrations/calendar/events/{id}/details-suggestion"},
    {"method": "GET", "path": "api/v9/integrations/calendar/setup"},
    {"method": "GET", "path": "api/v9/integrations/calendar/{id}/calendars"},
    {"method": "GET", "path": "api/v9/integrations/calendar/{id}/calendars/{id}/events"},
    {"method": "GET", "path": "api/v9/integrations/calendar/{id}/calendars/{id}/events/{id}/attendees"},
    {"method": "GET", "path": "api/v9/organizations/{id}/invoices/{id}"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/invoices"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/invoices/{id}"},
    {"method": "GET", "path": "api/v9/keys"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/linked_sso_profiles"},
    {"method": "GET", "path": "api/v9/me/location"},
    {"method": "GET", "path": "api/v9/me/logged"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/logo"},
    {"method": "GET", "path": "api/v9/me/organizations"},
    {"method": "GET", "path": "api/v9/organizations/{id}"},
    {"method": "GET", "path": "api/v9/organizations/{id}/owner"},
    {"method": "GET", "path": "api/v9/organizations/{id}/owner/transfer"},
    {"method": "GET", "path": "api/v9/organizations/{id}/owner/transfer/{id}"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/payment_receipts/{id}"},
    {"method": "GET", "path": "api/v9/organizations/{id}/payment_records"},
    {"method": "GET", "path": "api/v9/organizations/{id}/plans"},
    {"method": "GET", "path": "api/v9/organizations/{id}/plans/{id}"},
    {"method": "GET", "path": "api/v9/me/preferences"},
    {"method": "GET", "path": "api/v9/me/preferences/{id}"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/preferences"},
    {"method": "GET", "path": "api/v9/me/projects"},
    {"method": "GET", "path": "api/v9/me/projects/paginated"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/project_groups"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/project_users"},
    {"method": "POST", "path": "api/v9/workspaces/{id}/project_users/paginated"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/projects"},
    {"method": "POST", "path": "api/v9/workspaces/{id}/projects/billable-amounts"},
    {"method": "POST", "path": "api/v9/workspaces/{id}/projects/task_count"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/projects/templates"},
    {"method": "POST", "path": "api/v9/workspaces/{id}/projects/user_count"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/projects/{id}"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/projects/{id}/periods"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/projects/{id}/statistics"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/projects/{id}/tasks"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/projects/{id}/tasks/{id}"},
    {"method": "GET", "path": "api/v9/me/push_services"},
    {"method": "GET", "path": "api/v9/me/quota"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/rates/{id}/{id}"},
    {"method": "POST", "path": "reports/api/v3/shared/{id}"},
    {"method": "POST", "path": "reports/api/v3/shared/{id}/csv"},
    {"method": "POST", "path": "reports/api/v3/shared/{id}/pdf"},
    {"method": "POST", "path": "reports/api/v3/shared/{id}/xlsx"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/comparative"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/data_trends/clients"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/data_trends/projects"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/data_trends/users"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/filters/clients"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/filters/project_groups"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/filters/project_users"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/filters/projects"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/filters/projects/status"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/filters/tasks"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/filters/tasks/status"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/filters/users"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/profitability/projects"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/projects/summary"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/projects/{id}/summary"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/search/clients"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/search/projects"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/search/tasks"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/search/time_entries"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/search/time_entries.csv"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/search/time_entries.pdf"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/search/time_entries.xlsx"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/search/time_entries/totals"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/search/users"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/summary/time_entries"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/summary/time_entries.csv"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/summary/time_entries.pdf"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/summary/time_entries.xlsx"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/weekly/time_entries"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/weekly/time_entries.csv"},
    {"method": "POST", "path": "reports/api/v3/workspace/{id}/weekly/time_entries.pdf"},
    {"method": "GET", "path": "api/v9/organizations/{id}/roles"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/scheduled_reports"},
    {"method": "GET", "path": "api/v9/organizations/{id}/segmentation"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/statistics"},
    {"method": "GET", "path": "api/v9/status"},
    {"method": "GET", "path": "api/v9/organizations/{id}/subscription"},
    {"method": "GET", "path": "api/v9/organizations/{id}/subscription/customer"},
    {"method": "GET", "path": "api/v9/organizations/{id}/subscription/invoice_summary"},
    {"method": "GET", "path": "api/v9/organizations/{id}/subscription/payment_failed"},
    {"method": "GET", "path": "api/v9/organizations/{id}/subscription/trial/opt-in"},
    {"method": "GET", "path": "api/v9/subscriptions/plans"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/subscription"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/subscription/purchase_orders/{id}"},
    {"method": "GET", "path": "api/v9/sync-server/me/goals"},
    {"method": "GET", "path": "api/v9/me/tags"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/tags"},
    {"method": "GET", "path": "api/v9/me/tasks"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/tasks"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/tasks/basic"},
    {"method": "POST", "path": "api/v9/workspaces/{id}/tasks/data"},
    {"method": "GET", "path": "api/v9/me/time_entries"},
    {"method": "GET", "path": "api/v9/me/time_entries/checklist"},
    {"method": "GET", "path": "api/v9/me/time_entries/current"},
    {"method": "GET", "path": "api/v9/me/time_entries/{id}"},
    {"method": "POST", "path": "api/v9/me/time_entries_shared_with"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/time_entry_constraints"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/time_entry_invitations"},
    {"method": "GET", "path": "api/v9/timeline"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/timesheet_setups"},
    {"method": "GET", "path": "api/v9/me/timesheets"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/timesheets"},
    {"method": "POST", "path": "api/v9/workspaces/{id}/timesheets/hours"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/timesheets/{id}/{id}/history"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/timesheets/{id}/{id}/time_entries"},
    {"method": "GET", "path": "api/v9/timezones"},
    {"method": "GET", "path": "api/v9/timezones/offsets"},
    {"method": "GET", "path": "api/v9/me/track_reminders"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/track_reminders"},
    {"method": "GET", "path": "api/v9/organizations/{id}/users"},
    {"method": "GET", "path": "api/v9/organizations/{id}/users/detailed"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/users"},
    {"method": "POST", "path": "api/v9/workspaces/{id}/users/data"},
    {"method": "GET", "path": "api/v9/workspaces/{id}/workspace_users"},
    {"method": "GET", "path": "api/v9/me/web-timer"},
    {"method": "GET", "path": "webhooks/api/v1/event_filters"},
    {"method": "GET", "path": "webhooks/api/v1/limits/{id}"},
    {"method": "GET", "path": "webhooks/api/v1/status"},
    {"method": "GET", "path": "api/v9/organizations/{id}/workspaces/statistics"},
    {"method": "GET", "path": "api/v9/organizations/{id}/workspaces/{id}/groups"},
    {"method": "GET", "path": "api/v9/organizations/{id}/workspaces/{id}/workspace_users"},
    {"method": "GET", "path": "api/v9/workspaces/plans"}
  ],
  "deny": []
}
```

## Endpoints

The Toggl Track endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | api/v9/me/accept_tos | write | accept_tos | Accepts the last version of the Terms of Service for the current user. |
| GET | api/v9/workspaces/{id}/alerts | read | alerts | Returns a list of existing alerts. |
| POST | api/v9/workspaces/{id}/alerts | write | alerts | Handles POST alert requests. |
| PUT | api/v9/workspaces/{id}/alerts/{id} | write | alerts | Handles PUT alert requests. |
| DELETE | api/v9/workspaces/{id}/alerts/{id} | write | alerts | Handles DELETE alert requests. |
| GET | api/v9/workspaces/{id}/alerts/{id}/deliveries | read | alerts | Returns up to 151 active delivery records ordered by ID. |
| GET | api/v9/audit_logs/{id}/{id}/{id} | read | audit_logs | Returns a list of audit log events for the specified organization and time range. |
| GET | api/v9/auth/saml2/login | read | auth | Returns the SSO URL given an email address for authenticating in an Identity Provider. |
| POST | api/v9/auth/saml2/login/{id} | write | auth | Receives the IdP Callback containing the SAML2 assertion with response of user authentication in the IdP. |
| POST | api/v9/avatars | write | avatars | Handles POST avatar requests. |
| DELETE | api/v9/avatars | write | avatars | Handles DELETE avatar requests. |
| POST | api/v9/avatars/use_gravatar | write | avatars | Change user avatar to gravatar. |
| GET | api/v9/me/clients | read | clients | Get Clients. |
| GET | api/v9/workspaces/{id}/clients | read | clients | List clients from workspace. |
| POST | api/v9/workspaces/{id}/clients | write | clients | Create workspace client. |
| POST | api/v9/workspaces/{id}/clients/archive | write | clients | Archives workspace clients and related projects. |
| POST | api/v9/workspaces/{id}/clients/data | read | clients | List clients from workspace by client_ids. |
| POST | api/v9/workspaces/{id}/clients/delete | write | clients | Delete one or more workspace clients. |
| GET | api/v9/workspaces/{id}/clients/{id} | read | clients | Load client from workspace. |
| PUT | api/v9/workspaces/{id}/clients/{id} | write | clients | Update workspace client. |
| DELETE | api/v9/workspaces/{id}/clients/{id} | write | clients | Delete workspace client. |
| POST | api/v9/workspaces/{id}/clients/{id}/archive | write | clients | Archives a workspace client and related projects. |
| POST | api/v9/workspaces/{id}/clients/{id}/restore | write | clients | Restores client and all related or specified projects from the given workspace. |
| POST | api/v9/me/close_account | write | close_account | Close Account. |
| GET | api/v9/countries | read | countries | Returns a list of existing countries. |
| GET | api/v9/countries/{id}/subdivisions | read | countries | Returns a list of subdivisions for a specific country. |
| GET | api/v9/currencies | read | currencies | Returns a list of available currencies. |
| GET | api/v9/workspaces/{id}/currencies | read | currencies | Get the currencies for a given workspace. |
| GET | api/v9/workspaces/{id}/dashboard/all_activity | read | dashboard | Dashboard's main purpose is to give an overview of what users in the workspace are doing and have been doing. |
| GET | api/v9/workspaces/{id}/dashboard/most_active | read | dashboard | Dashboard's main purpose is to give an overview of what users in the workspace are doing and have been doing. |
| GET | api/v9/workspaces/{id}/dashboard/top_activity | read | dashboard | Dashboard's main purpose is to give an overview of what users in the workspace are doing and have been doing. |
| GET | api/v9/desktop_login | write | desktop_login | Store new desktop login token. Kept out of read: it stores and returns a desktop login token. |
| POST | api/v9/desktop_login_tokens | write | desktop_login_tokens | Store new desktop login token. |
| POST | api/v9/me/disable_product_emails/{id} | write | disable_product_emails | Disable product emails. |
| POST | api/v9/me/disable_weekly_report/{id} | write | disable_weekly_report | Disable weekly report. |
| POST | api/v9/me/enable_sso | write | enable_sso | Confirm SSO enabling in existing Toggl account after successful SSO. |
| GET | api/v9/workspaces/{id}/expenses | read | expenses | Get work expenses. |
| POST | api/v9/workspaces/{id}/expenses/upload | write | expenses | Upload a work expense. |
| GET | api/v9/me/export | write | export | List of objects to be downloaded for an user. Kept out of read: it returns a data export token. |
| POST | api/v9/me/export | write | export | An object which data to be downloaded for an user. |
| GET | api/v9/me/export/data/{id} | read | export | Get a zip file List of download requests from an user. |
| GET | api/v9/workspaces/{id}/exports | write | exports | List of workspace download requests from a given workspace. Kept out of read: it returns data export tokens. |
| POST | api/v9/workspaces/{id}/exports | write | exports | List of workspaces downloaded from a given workspace. |
| GET | api/v9/workspaces/{id}/exports/data/{id} | read | exports | Send a zip file List of workspace download requests from a given workspace. |
| GET | api/v9/me/favorites | read | favorites | Gets all favorites for the requesting user. |
| POST | api/v9/me/favorites | write | favorites | This endpoint allows the creation of a favorite given some parameters. |
| PUT | api/v9/me/favorites | write | favorites | This endpoint allows updating an array of favorites. |
| POST | api/v9/me/favorites/suggestions | write | favorites | It will create 3 favorites based on past user's TE activity and return them. |
| DELETE | api/v9/me/favorites/{id} | write | favorites | Deletes a given favorite logically from database, as well as its tags. |
| GET | api/v9/workspaces/{id}/favorites | read | favorites | Gets all favorites for the requesting user. |
| POST | api/v9/workspaces/{id}/favorites | write | favorites | This endpoint allows the creation of a favorite. |
| PUT | api/v9/workspaces/{id}/favorites | write | favorites | This endpoint allows updating an array of favorites. |
| POST | api/v9/workspaces/{id}/favorites/suggestions | write | favorites | It will create 3 favorites based on past user's TE activity and return them. |
| DELETE | api/v9/workspaces/{id}/favorites/{id} | write | favorites | Deletes a given favorite logically from database, as well as its tags. |
| GET | api/v9/me/features | read | features | Get features. |
| POST | api/v9/feedback | write | feedback | Send Feedback. |
| GET | api/v9/me/flags | read | flags | Returns flags for the current user. |
| POST | api/v9/me/flags | write | flags | Add flags for the current user. |
| GET | api/v9/workspaces/{id}/goals | read | goals | Gets all goals for the requesting user in the workspace. |
| POST | api/v9/workspaces/{id}/goals | write | goals | Create a Goal object with its parameters. |
| GET | api/v9/workspaces/{id}/goals/{id} | read | goals | Gets a goal that relates to the calling user in the specified workspace. |
| PUT | api/v9/workspaces/{id}/goals/{id} | write | goals | Update a goal with the updatable parameters given by UpdatePayload. |
| DELETE | api/v9/workspaces/{id}/goals/{id} | write | goals | Delete a goal that was created by the calling user. |
| GET | api/v9/organizations/{id}/groups | read | groups | Returns list of groups in organization based on set of url parameters. |
| POST | api/v9/organizations/{id}/groups | write | groups | Creates a group in the specified organization. |
| PUT | api/v9/organizations/{id}/groups/{id} | write | groups | Edits a group in the specified organization. |
| PATCH | api/v9/organizations/{id}/groups/{id} | write | groups | Patches a group in the specified organization. |
| DELETE | api/v9/organizations/{id}/groups/{id} | write | groups | Deletes a group from the specified organization. |
| GET | api/v9/workspaces/{id}/groups | read | groups | Returns a list of groups for the specified workspace. |
| POST | api/v9/workspaces/{id}/groups | write | groups | Creates a group in the specified workspace. |
| PUT | api/v9/workspaces/{id}/groups/{id} | write | groups | Updates the group. |
| DELETE | api/v9/workspaces/{id}/groups/{id} | write | groups | Deletes the group. |
| GET | api/v9/ical/workspace_user/{id} | read | ical | Returns ical file with TEs from last 14 days. |
| POST | api/v9/workspaces/{id}/ical/reset | write | ical | Reset the iCal token for a given workspace. |
| POST | api/v9/workspaces/{id}/ical/toggle | write | ical | Toggle the iCal token on/off for a given workspace. |
| GET | api/v9/me/id | read | id | Returns the local Track user ID for the authenticated user. |
| POST | api/v9/workspaces/{id}/import-preview-counts | write | import-preview-counts | Returns optimized count-only import preview counts for Track entities. |
| POST | insights/api/v1/workspace/{id}/data_trends/projects | read | insights | Returns the projects' data trends projects from a workspace. |
| POST | insights/api/v1/workspace/{id}/profitability/employees.csv | read | insights | Downloads employee profitability insights in the specified format: csv or xlsx. |
| POST | insights/api/v1/workspace/{id}/profitability/employees.xlsx | read | insights | Downloads employee profitability insights in the specified format: csv or xlsx. |
| POST | insights/api/v1/workspace/{id}/profitability/projects.csv | read | insights | Downloads profitability project insights in the specified format: csv or xlsx. |
| POST | insights/api/v1/workspace/{id}/profitability/projects.xlsx | read | insights | Downloads profitability project insights in the specified format: csv or xlsx. |
| POST | insights/api/v1/workspace/{id}/trends/projects.csv | read | insights | Downloads projects data trends in the specified format: csv or xlsx. |
| POST | insights/api/v1/workspace/{id}/trends/projects.xlsx | read | insights | Downloads projects data trends in the specified format: csv or xlsx. |
| GET | api/v9/integrations/calendar | read | integrations | Get all integrations a user has. |
| GET | api/v9/integrations/calendar/calendars | read | integrations | Get all calendars for a given user that was previously saved in the database. |
| GET | api/v9/integrations/calendar/calendars/selected | read | integrations | Get all selected calendars for a given user that was previously saved in the database. |
| GET | api/v9/integrations/calendar/events | read | integrations | Get all events from selected calendars for the caller user. |
| POST | api/v9/integrations/calendar/events/details-suggestion | read | integrations | Given one or more event IDs, this endpoint responds with the most probable event details. |
| POST | api/v9/integrations/calendar/events/update | write | integrations | Fetch all events from a user's selected calendars and save in database. |
| GET | api/v9/integrations/calendar/events/{id}/details-suggestion | read | integrations | Given an event ID, this endpoint responds with the most probable event details (and the accuracy) to. |
| GET | api/v9/integrations/calendar/setup | read | integrations | Set up an integration with a given provider, returning a URL to the said provider in order to. |
| PUT | api/v9/integrations/calendar/{id} | write | integrations | Updates an integration properties. |
| DELETE | api/v9/integrations/calendar/{id} | write | integrations | Executes logic deletion of an integration. |
| GET | api/v9/integrations/calendar/{id}/calendars | read | integrations | Get all calendars for a given integration that was previously saved in the database. |
| POST | api/v9/integrations/calendar/{id}/calendars/update | write | integrations | This endpoint uses the passed integration to get a provider and update all the calendars from that. |
| PATCH | api/v9/integrations/calendar/{id}/calendars/{id} | write | integrations | This endpoint is used to set updatable fields of a calendar like selected field. |
| GET | api/v9/integrations/calendar/{id}/calendars/{id}/events | read | integrations | Get all events for a given calendar in a given integration. |
| GET | api/v9/integrations/calendar/{id}/calendars/{id}/events/{id}/attendees | read | integrations | Get all attendees associated with a given calendar event. |
| POST | api/v9/organizations/{id}/integrations/slack/request | write | integrations | Endpoint for requesting Slack integration. |
| GET | api/v9/invitations/{id} | write | invitations | Returns an invitation data by code. Kept out of read: it returns the invitation token. |
| POST | api/v9/organizations/{id}/invitations | write | invitations | Creates a new invitation for the user. |
| PUT | api/v9/organizations/{id}/invitations/{id}/resend | write | invitations | Resend invitation email to user. |
| GET | api/v9/organizations/{id}/invoices/{id} | read | invoices | Returns a Invoice document in PDF form. |
| GET | api/v9/workspaces/{id}/invoices | read | invoices | Get invoices for given workspace with pagination. |
| POST | api/v9/workspaces/{id}/invoices | write | invoices | Creates new user invoice. |
| GET | api/v9/workspaces/{id}/invoices/{id} | read | invoices | Returns an Invoice document in PDF form. |
| DELETE | api/v9/workspaces/{id}/invoices/{id} | write | invoices | Deletes user invoice by ID if exists. |
| GET | api/v9/keys | read | keys | Returns the current JWKS keyset used to sign JWT tokens. |
| GET | api/v9/workspaces/{id}/linked_sso_profiles | read | linked_sso_profiles | Returns a list of SSO profiles that are linked to the given workspace. |
| PUT | api/v9/workspaces/{id}/linked_sso_profiles/{id} | write | linked_sso_profiles | Link the workspace with the given ID to an SSO profile with the given ID. |
| DELETE | api/v9/workspaces/{id}/linked_sso_profiles/{id} | write | linked_sso_profiles | Unlink the workspace from an SSO profile. |
| GET | api/v9/me/location | read | location | Returns the client's IP-based location. |
| GET | api/v9/me/logged | read | logged | Used to check if authentication works. |
| GET | api/v9/workspaces/{id}/logo | read | logo | Get the logo for a given workspace. |
| POST | api/v9/workspaces/{id}/logo | write | logo | Post the logo for a given workspace. |
| DELETE | api/v9/workspaces/{id}/logo | write | logo | Delete the logo for a given workspace. |
| GET | api/v9/me | write | me | Returns details for the current user. Kept out of read: it returns the API token. |
| PUT | api/v9/me | write | me | Updates details for the current user. |
| GET | api/v9/me/organizations | read | organizations | Get all organizations a given user is part of. |
| POST | api/v9/organizations | write | organizations | Creates a new organization with a single workspace and assigns current user as the organization owner. |
| GET | api/v9/organizations/{id} | read | organizations | Returns organization name and current pricing plan. |
| PUT | api/v9/organizations/{id} | write | organizations | Updates an existing organization. |
| GET | api/v9/organizations/{id}/owner | read | owner | Returns organization owner data. |
| GET | api/v9/organizations/{id}/owner/transfer | read | owner | Returns list of organization transfers made in the organization. |
| POST | api/v9/organizations/{id}/owner/transfer | write | owner | Return the ownership transfer for a given organization. |
| GET | api/v9/organizations/{id}/owner/transfer/{id} | read | owner | Returns single organization transfer in the organization. |
| POST | api/v9/organizations/{id}/owner/transfer/{id}/{id} | write | owner | Return the ownership transfer for a given organization and emails stakeholders. |
| GET | api/v9/workspaces/{id}/payment_receipts/{id} | read | payment_receipts | Returns payment receipt pdf file. |
| GET | api/v9/organizations/{id}/payment_records | read | payment_records | Returns paid invoices. |
| GET | api/v9/organizations/{id}/plans | read | plans | Returns pricing plans for an organization. |
| GET | api/v9/organizations/{id}/plans/{id} | read | plans | Returns pricing plan for an organization identified by plan_id. |
| GET | api/v9/me/preferences | read | preferences | Returns user preferences and alpha features. |
| POST | api/v9/me/preferences | write | preferences | With this endpoint, preferences can be modified and alpha features can be enabled or disabled. |
| GET | api/v9/me/preferences/{id} | read | preferences | Returns user preferences and alpha features. |
| POST | api/v9/me/preferences/{id} | write | preferences | With this endpoint, preferences can be modified and alpha features can be enabled or disabled. |
| GET | api/v9/workspaces/{id}/preferences | read | preferences | Get the preferences for a given workspace. |
| POST | api/v9/workspaces/{id}/preferences | write | preferences | Update the preferences for a given workspace. |
| POST | api/v9/organizations/{id}/premium-upgrade-discount-email | write | premium-upgrade-discount-email | Sends a one-off promotional email to every admin of the organization, offering a 30% discount on Premium annual. |
| GET | api/v9/me/projects | read | projects | Get projects. |
| GET | api/v9/me/projects/paginated | read | projects | Get paginated projects. |
| GET | api/v9/workspaces/{id}/project_groups | read | projects | Get project groups for given workspace. |
| POST | api/v9/workspaces/{id}/project_groups | write | projects | Adds group to project for given workspace. |
| DELETE | api/v9/workspaces/{id}/project_groups/{id} | write | projects | Remove project group for a given workspace. |
| GET | api/v9/workspaces/{id}/project_users | read | projects | List all projects users for a given workspace. |
| POST | api/v9/workspaces/{id}/project_users | write | projects | Include a project user for a given workspace. |
| POST | api/v9/workspaces/{id}/project_users/paginated | read | projects | List projects users for a given workspace and set of project IDs paginated. |
| PUT | api/v9/workspaces/{id}/project_users/{id} | write | projects | Update the data for a project user for a given workspace. |
| PATCH | api/v9/workspaces/{id}/project_users/{id} | write | projects | Patch a list of project users for a given workspace. |
| DELETE | api/v9/workspaces/{id}/project_users/{id} | write | projects | Delete a project user for a given workspace. |
| GET | api/v9/workspaces/{id}/projects | read | projects | Get projects for given workspace. |
| POST | api/v9/workspaces/{id}/projects | write | projects | Create project for given workspace. |
| POST | api/v9/workspaces/{id}/projects/billable-amounts | read | projects | Get projects billable amounts. |
| POST | api/v9/workspaces/{id}/projects/task_count | read | projects | Retrieves the task count for the specified projects. |
| GET | api/v9/workspaces/{id}/projects/templates | read | projects | Get projects templates for given workspace. |
| POST | api/v9/workspaces/{id}/projects/user_count | read | projects | Retrieves the user count for the specified projects. |
| GET | api/v9/workspaces/{id}/projects/{id} | read | projects | Get project for given workspace. |
| PUT | api/v9/workspaces/{id}/projects/{id} | write | projects | Update project for given workspace. |
| PATCH | api/v9/workspaces/{id}/projects/{id} | write | projects | Bulk editing workspace projects. |
| DELETE | api/v9/workspaces/{id}/projects/{id} | write | projects | Delete project for given workspace. |
| GET | api/v9/workspaces/{id}/projects/{id}/periods | read | projects | Get recurring project periods for given workspace. |
| POST | api/v9/workspaces/{id}/projects/{id}/pin | write | projects | Pin or unpin a project to top of user's project list. |
| GET | api/v9/workspaces/{id}/projects/{id}/statistics | read | projects | Get statistics for given workspace and project. |
| GET | api/v9/workspaces/{id}/projects/{id}/tasks | read | projects | Get project tasks for given workspace. |
| POST | api/v9/workspaces/{id}/projects/{id}/tasks | write | projects | Post project tasks for given workspace. |
| GET | api/v9/workspaces/{id}/projects/{id}/tasks/{id} | read | projects | Get project task for given task id. |
| PUT | api/v9/workspaces/{id}/projects/{id}/tasks/{id} | write | projects | Put project task for given workspace. |
| PATCH | api/v9/workspaces/{id}/projects/{id}/tasks/{id} | write | projects | Patch project tasks for given workspace. |
| DELETE | api/v9/workspaces/{id}/projects/{id}/tasks/{id} | write | projects | Delete projects task for given workspace. |
| GET | api/v9/me/push_services | read | push_services | Get list of firebase tokens registered for current user. |
| POST | api/v9/me/push_services | write | push_services | Register Firebase token for current user. |
| DELETE | api/v9/me/push_services | write | push_services | Unregister Firebase token for current user. |
| GET | api/v9/me/quota | read | quota | Returns the API quota for the current user for all the organizations they are part of. |
| POST | api/v9/workspaces/{id}/rates | write | rates | Creates a new rate. |
| GET | api/v9/workspaces/{id}/rates/{id}/{id} | read | rates | Get rates by level(workspace\|project\|task\|user). |
| GET | api/v9/workspaces/{id}/reports/shared | write | reports | Get shared report. Kept out of read: it returns shared report tokens. |
| POST | api/v9/workspaces/{id}/reports/shared | write | reports | Add shared report. |
| PUT | api/v9/workspaces/{id}/reports/shared | write | reports | Change shared report. |
| PATCH | api/v9/workspaces/{id}/reports/shared/bulk_delete | write | reports | Bulk delete saved reports. |
| GET | api/v9/workspaces/{id}/reports/shared/{id} | write | reports | Get a saved report. Kept out of read: it returns the shared report token. |
| PUT | api/v9/workspaces/{id}/reports/shared/{id} | write | reports | Change saved report. |
| DELETE | api/v9/workspaces/{id}/reports/shared/{id} | write | reports | Delete saved report. |
| POST | reports/api/v3/shared/{id} | read | reports | Returns the previously saved report. |
| POST | reports/api/v3/shared/{id}/csv | read | reports | Downloads a previously saved report in csv. |
| POST | reports/api/v3/shared/{id}/pdf | read | reports | AuthenticationA public report is accessible by anyone, a private one is only accessible by the report's owner or workspace admin. |
| POST | reports/api/v3/shared/{id}/xlsx | read | reports | Downloads a previously saved report in xlsx. |
| POST | reports/api/v3/workspace/{id}/comparative | read | reports | Returns comparative report. |
| POST | reports/api/v3/workspace/{id}/data_trends/clients | read | reports | Returns the clients' data trends. |
| POST | reports/api/v3/workspace/{id}/data_trends/projects | read | reports | Returns projects' data trends. |
| POST | reports/api/v3/workspace/{id}/data_trends/users | read | reports | Returns users' data trends. |
| POST | reports/api/v3/workspace/{id}/filters/clients | read | reports | Returns filtered clients from a workspace (only ID and name). |
| POST | reports/api/v3/workspace/{id}/filters/project_groups | read | reports | Returns the project groups from a workspace. |
| POST | reports/api/v3/workspace/{id}/filters/project_users | read | reports | Returns filtered user projects. |
| POST | reports/api/v3/workspace/{id}/filters/projects | read | reports | Returns filtered projects from a workspace. |
| POST | reports/api/v3/workspace/{id}/filters/projects/status | read | reports | Returns	filtered projects statuses from a workspace. |
| POST | reports/api/v3/workspace/{id}/filters/tasks | read | reports | Returns filtered tasks from workspace. |
| POST | reports/api/v3/workspace/{id}/filters/tasks/status | read | reports | Filter tasks statuses from a workspace. |
| POST | reports/api/v3/workspace/{id}/filters/users | read | reports | Returns filtered users from a workspace. |
| POST | reports/api/v3/workspace/{id}/profitability/projects | read | reports | Returns profitability projects report. |
| POST | reports/api/v3/workspace/{id}/projects/summary | read | reports | Returns summary user projects. |
| POST | reports/api/v3/workspace/{id}/projects/{id}/summary | read | reports | Returns project's summary. |
| POST | reports/api/v3/workspace/{id}/search/clients | read | reports | Returns filtered clients from a workspace (whole client object). |
| POST | reports/api/v3/workspace/{id}/search/projects | read | reports | Returns filtered projects from a workspace (whole project object). |
| POST | reports/api/v3/workspace/{id}/search/tasks | read | reports | Returns filtered tasks from workspace. |
| POST | reports/api/v3/workspace/{id}/search/time_entries | read | reports | Returns time entries for detailed report according to the given filters. |
| POST | reports/api/v3/workspace/{id}/search/time_entries.csv | read | reports | Downloads detailed report in the specified format: csv or xlsx. |
| POST | reports/api/v3/workspace/{id}/search/time_entries.pdf | read | reports | Downloads detailed report in pdf format. |
| POST | reports/api/v3/workspace/{id}/search/time_entries.xlsx | read | reports | Downloads detailed report in the specified format: csv or xlsx. |
| POST | reports/api/v3/workspace/{id}/search/time_entries/totals | read | reports | Returns totals sums for detailed report. |
| POST | reports/api/v3/workspace/{id}/search/users | read | reports | Returns filtered users from a workspace. |
| POST | reports/api/v3/workspace/{id}/summary/time_entries | read | reports | Returns time entries for summary report according to the given filters. |
| POST | reports/api/v3/workspace/{id}/summary/time_entries.csv | read | reports | Downloads summary report in the specified in the specified format: csv or xlsx. |
| POST | reports/api/v3/workspace/{id}/summary/time_entries.pdf | read | reports | Downloads summary report in pdf format. |
| POST | reports/api/v3/workspace/{id}/summary/time_entries.xlsx | read | reports | Downloads summary report in the specified in the specified format: csv or xlsx. |
| POST | reports/api/v3/workspace/{id}/weekly/time_entries | read | reports | Returns time entries for weekly report according to the given filters. |
| POST | reports/api/v3/workspace/{id}/weekly/time_entries.csv | read | reports | Downloads weekly report in csv format. |
| POST | reports/api/v3/workspace/{id}/weekly/time_entries.pdf | read | reports | Downloads weekly report in pdf format. |
| POST | api/v9/me/reset_token | write | reset_token | Resets API token for the current user. |
| GET | api/v9/organizations/{id}/roles | read | roles | Returns a list of organization specific and global roles. |
| GET | api/v9/workspaces/{id}/scheduled_reports | read | scheduled_reports | Lists scheduled reports. |
| POST | api/v9/workspaces/{id}/scheduled_reports | write | scheduled_reports | Endpoint for setting up a scheduled report. |
| DELETE | api/v9/workspaces/{id}/scheduled_reports/{id} | write | scheduled_reports | Endpoint for delete a scheduled report. |
| GET | api/v9/organizations/{id}/segmentation | read | segmentation | Returns organization segmentation information. |
| PUT | api/v9/organizations/{id}/segmentation | write | segmentation | Save organization segmentation information. |
| POST | api/v9/smail/contact | write | smail | Send an email to a contact. |
| POST | api/v9/smail/demo | write | smail | Send an email for a demo. |
| POST | api/v9/smail/meet | write | smail | Send an email for meet with message and location. |
| GET | api/v9/workspaces/{id}/statistics | read | statistics | Returns workspace admins list, members count and groups count. |
| GET | api/v9/status | read | status | Returns API status. |
| GET | api/v9/organizations/{id}/subscription | read | subscription | Returns subscription data. |
| POST | api/v9/organizations/{id}/subscription | write | subscription | Allows to create a new unified subscription for an organization. |
| PUT | api/v9/organizations/{id}/subscription | write | subscription | Allows to update existing unified subscription for an organization. |
| DELETE | api/v9/organizations/{id}/subscription | write | subscription | Cancels an existing subscription. |
| POST | api/v9/organizations/{id}/subscription/cancellation_feedback | write | subscription | Allows to create a cancellation feedback for an organization subscription. |
| GET | api/v9/organizations/{id}/subscription/customer | read | subscription | Retrieve unified customer belonging to the organization. |
| POST | api/v9/organizations/{id}/subscription/customer | write | subscription | Creates unified customer for organization. |
| PUT | api/v9/organizations/{id}/subscription/customer | write | subscription | Allows to update unified customer data. |
| POST | api/v9/organizations/{id}/subscription/discount_request | write | subscription | Endpoint for client's feedback when canceling plan. |
| POST | api/v9/organizations/{id}/subscription/feature_upsell_multi | write | subscription | Gets feature upsell information for all organizations the user has access to. |
| GET | api/v9/organizations/{id}/subscription/invoice_summary | read | subscription | Returns a summary of the next invoice for an Organization. |
| POST | api/v9/organizations/{id}/subscription/payment/confirm | write | subscription | Re-reads and saves the subscription after the customer completed a payment challenge, and reports whether it is. |
| GET | api/v9/organizations/{id}/subscription/payment_failed | read | subscription | Returns subscription payment failed details. |
| POST | api/v9/organizations/{id}/subscription/promocode | write | subscription | Applies the given promotion code to organization's customer. |
| DELETE | api/v9/organizations/{id}/subscription/promocode | write | subscription | Removes any discount (promotion code) applied to the organization's customer. |
| POST | api/v9/organizations/{id}/subscription/setup_intent | write | subscription | Create a setup intent for collecting customer's payment method for future payments. |
| POST | api/v9/organizations/{id}/subscription/trial | write | subscription | Allows to create a new unified subscription on initial 30-day trial for an organization. |
| DELETE | api/v9/organizations/{id}/subscription/trial | write | subscription | Cancels an active trial. |
| GET | api/v9/organizations/{id}/subscription/trial/opt-in | read | subscription | Returns whether the organization is eligible for an opt-in trial. |
| POST | api/v9/organizations/{id}/subscription/trial/opt-in | write | subscription | Starts a new opt-in trial for the organization if eligible. |
| POST | api/v9/organizations/{id}/subscription/upgrade_request/{id} | write | subscription | Endpoint for triggering a call to action on admins for upgrading their subscription. |
| POST | api/v9/organizations/{id}/subscription/usage_based_discount | write | subscription | Endpoint for applying a usage based discount given a variant of the discount. |
| DELETE | api/v9/organizations/{id}/subscription/usage_based_discount | write | subscription | Endpoint for removing a usage based discount given to organization. |
| POST | api/v9/organizations/{id}/subscriptions/item/discount | write | subscription | Body: { "coupon_id"?: "...", "promotion_code"?: "..." }. |
| GET | api/v9/subscriptions/plans | read | subscription | Get all available plans along with all features available per plan. |
| GET | api/v9/workspaces/{id}/subscription | read | subscription | Returns subscription data. |
| GET | api/v9/workspaces/{id}/subscription/purchase_orders/{id} | read | subscription | Returns a Purchase Order document in PDF form. |
| GET | api/v9/sync-server/me/goals | read | sync-server | Gets all goals for the requesting user. |
| GET | api/v9/me/tags | read | tags | Returns tags for the current user. |
| GET | api/v9/workspaces/{id}/tags | read | tags | List Workspace tags. |
| POST | api/v9/workspaces/{id}/tags | write | tags | Create workspace tags. |
| PATCH | api/v9/workspaces/{id}/tags | write | tags | Patch will not be executed if there are errors with some records. |
| PUT | api/v9/workspaces/{id}/tags/{id} | write | tags | Update workspace tags. |
| DELETE | api/v9/workspaces/{id}/tags/{id} | write | tags | Delete workspace tags. |
| GET | api/v9/me/tasks | read | tasks | Returns tasks from projects in which the user is participating. |
| GET | api/v9/workspaces/{id}/tasks | read | tasks | List Workspace tasks. |
| GET | api/v9/workspaces/{id}/tasks/basic | read | tasks | List Workspace tasks. |
| POST | api/v9/workspaces/{id}/tasks/data | read | tasks | List tasks from workspace by project_ids. |
| GET | api/v9/me/time_entries | read | time_entries | Lists latest time entries. |
| GET | api/v9/me/time_entries/checklist | read | time_entries | Check the needed time entries requirement to offer coupon to user. |
| GET | api/v9/me/time_entries/current | read | time_entries | Load running time entry for user ID. |
| GET | api/v9/me/time_entries/{id} | read | time_entries | Load time entry by ID that is accessible by the current user. |
| POST | api/v9/workspaces/{id}/time_entries | write | time_entries | Creates a new workspace TimeEntry. |
| PUT | api/v9/workspaces/{id}/time_entries/{id} | write | time_entries | Updates a workspace time entry. |
| PATCH | api/v9/workspaces/{id}/time_entries/{id} | write | time_entries | In short: http://tools.ietf.org/html/rfc6902 and http://tools.ietf.org/html/rfc6901 with some additions. |
| DELETE | api/v9/workspaces/{id}/time_entries/{id} | write | time_entries | Deletes a workspace time entry. |
| PATCH | api/v9/workspaces/{id}/time_entries/{id}/stop | write | time_entries | Stops a workspace time entry. |
| POST | api/v9/me/time_entries_shared_with | read | time_entries_shared_with | Get the sharing details of the specified time entries in bulk. |
| GET | api/v9/workspaces/{id}/time_entry_constraints | read | time_entry_constraints | Get the time entry constraints for a given workspace. |
| POST | api/v9/workspaces/{id}/time_entry_constraints | write | time_entry_constraints | Post the time entry constraints for a given workspace. |
| GET | api/v9/workspaces/{id}/time_entry_invitations | read | time_entry_invitations | Get invitations for time entries. |
| POST | api/v9/workspaces/{id}/time_entry_invitations/{id}/{id} | write | time_entry_invitations | Accept or reject an invitation for a time entry. |
| GET | api/v9/timeline | read | timeline | Get timeline events. |
| POST | api/v9/timeline | write | timeline | Save timeline events and returns timeline settings. |
| DELETE | api/v9/timeline | write | timeline | Delete all timeline data for the current user. |
| GET | api/v9/workspaces/{id}/timesheet_setups | read | timesheet_setups | Get timesheet setups for a given workspace. |
| POST | api/v9/workspaces/{id}/timesheet_setups | write | timesheet_setups | Create timesheet setups. |
| POST | api/v9/workspaces/{id}/timesheet_setups/{id} | write | timesheet_setups | Updates a timesheet setups. |
| DELETE | api/v9/workspaces/{id}/timesheet_setups/{id} | write | timesheet_setups | Delete a timesheet setup for a given workspace. |
| GET | api/v9/me/timesheets | read | timesheets | Returns the timehseets for the current user. |
| GET | api/v9/workspaces/{id}/timesheets | read | timesheets | Get timesheets applying various filters. |
| PUT | api/v9/workspaces/{id}/timesheets | write | timesheets | Updates a batch of timesheets. |
| POST | api/v9/workspaces/{id}/timesheets/hours | read | timesheets | Get timesheet working hours and total tracked seconds. |
| PUT | api/v9/workspaces/{id}/timesheets/{id}/{id} | write | timesheets | Updates a timesheet. |
| GET | api/v9/workspaces/{id}/timesheets/{id}/{id}/history | read | timesheets | Get the timesheet history from the event stream. |
| GET | api/v9/workspaces/{id}/timesheets/{id}/{id}/time_entries | read | timesheets | Get the time entries from within a timesheet timeframe. |
| GET | api/v9/timezones | read | timezones | Returns known timezones. |
| GET | api/v9/timezones/offsets | read | timezones | Returns known timezones with their offsets. |
| GET | api/v9/me/track_reminders | read | track_reminders | Returns a list of track reminders. |
| GET | api/v9/workspaces/{id}/track_reminders | read | track_reminders | Returns a list of track reminders. |
| POST | api/v9/workspaces/{id}/track_reminders | write | track_reminders | Creates a workspace tracking reminder. |
| PUT | api/v9/workspaces/{id}/track_reminders/{id} | write | track_reminders | Updates a workspace tracking reminder. |
| DELETE | api/v9/workspaces/{id}/track_reminders/{id} | write | track_reminders | Deletes a workspace tracking reminder. |
| GET | api/v9/organizations/{id}/users | read | users | Returns list of users in organization based on set of url parameters. |
| PATCH | api/v9/organizations/{id}/users | write | users | Apply changes in bulk to users in an organization (currently deletion only). |
| GET | api/v9/organizations/{id}/users/detailed | read | users | Returns list of users in organization based on set of url parameters. |
| DELETE | api/v9/organizations/{id}/users/leave | write | users | Leaves organization, effectively delete user account in org and delete organization if it is last user. |
| PUT | api/v9/organizations/{id}/users/{id} | write | users | Changes a single organization-user. |
| GET | api/v9/workspaces/{id}/users | read | users | List all users for a given workspace. |
| POST | api/v9/workspaces/{id}/users/data | read | users | List of the specified workspace users basic data for a given workspace. |
| PUT | api/v9/workspaces/{id}/users/{id} | write | users | Update the data for a user in a given workspace. |
| GET | api/v9/workspaces/{id}/workspace_users | read | users | List all workspace_users for a given workspace. |
| PUT | api/v9/workspaces/{id}/workspace_users/{id} | write | users | Update the data for a workspace_user in a given workspace. |
| DELETE | api/v9/workspaces/{id}/workspace_users/{id} | write | users | Removes user from workspace. |
| GET | api/v9/me/web-timer | read | web-timer | Get web timer. |
| GET | webhooks/api/v1/event_filters | read | webhooks | Returns the list of supported event filters to be used when creating or updating a subscription. |
| GET | webhooks/api/v1/limits/{id} | read | webhooks | Returns the webhook limits (amount and event filters) for the given workspace ID. |
| POST | webhooks/api/v1/ping/{id}/{id} | write | webhooks | Sends a dummy payload to subscription's callback URL to check it's accessible and returns the correct status. |
| GET | webhooks/api/v1/status | read | webhooks | Retrieve the Webhooks server status. |
| GET | webhooks/api/v1/subscriptions/{id} | write | webhooks | Retrieves existing subscriptions for the requested workspace ID. Kept out of read: it returns webhook signing secrets. |
| POST | webhooks/api/v1/subscriptions/{id} | write | webhooks | Creates a subscription for the requested workspace ID. |
| PUT | webhooks/api/v1/subscriptions/{id}/{id} | write | webhooks | Updates existing subscription given its ID and workspace ID. |
| PATCH | webhooks/api/v1/subscriptions/{id}/{id} | write | webhooks | Updates existing subscription enabled status. |
| DELETE | webhooks/api/v1/subscriptions/{id}/{id} | write | webhooks | Remove existing subscription given its ID and workspace ID. |
| GET | webhooks/api/v1/validate/{id}/{id}/{id} | write | webhooks | Sets the subscription as validated if the received {validation_code} matches the ones stored for {subscription_id}. Kept out of read: it marks the subscription as validated. |
| GET | api/v9/me/workspaces | write | workspaces | Lists workspaces for given user. Kept out of read: it returns workspace API tokens. |
| POST | api/v9/organizations/{id}/workspaces | write | workspaces | Create a workspace within an existing organization. |
| GET | api/v9/organizations/{id}/workspaces/statistics | read | workspaces | Returns map indexed by workspace ID where each map element contains workspace admins list. |
| GET | api/v9/organizations/{id}/workspaces/{id}/groups | read | workspaces | Returns list of groups in a workspace based on set of url parameters. |
| GET | api/v9/organizations/{id}/workspaces/{id}/workspace_users | read | workspaces | Returns any users who belong to the workspace directly or through at least one group. |
| PATCH | api/v9/organizations/{id}/workspaces/{id}/workspace_users | write | workspaces | Changes the users in a workspace (currently deletion only). |
| GET | api/v9/workspaces/plans | read | workspaces | Lists Public subscription plans. |
| GET | api/v9/workspaces/{id} | write | workspaces | Get information of single workspace. Kept out of read: it returns the workspace API token. |
| PUT | api/v9/workspaces/{id} | write | workspaces | Update a specific workspace. |
| POST | api/v9/organizations/invitations/{id}/accept | write | {invitation_code} | User connected with invitation is marked as joined, email is sent to the inviter. |
| POST | api/v9/organizations/invitations/{id}/reject | write | {invitation_code} | User connected with invitation is marked as deleted. |
