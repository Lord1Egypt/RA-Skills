# Todoist access policy

An access policy limits which endpoints Todoist connections may call through Maton. Todoist doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/todoist#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Todoist: its 47 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create todoist --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/v1/tasks"},
    {"method": "GET", "path": "api/v1/tasks/completed/by_completion_date"},
    {"method": "GET", "path": "api/v1/tasks/completed/by_due_date"},
    {"method": "GET", "path": "api/v1/tasks/filter"},
    {"method": "GET", "path": "api/v1/tasks/{id}"},
    {"method": "GET", "path": "api/v1/projects"},
    {"method": "GET", "path": "api/v1/projects/archived"},
    {"method": "GET", "path": "api/v1/projects/permissions"},
    {"method": "GET", "path": "api/v1/projects/search"},
    {"method": "GET", "path": "api/v1/projects/{id}"},
    {"method": "GET", "path": "api/v1/projects/{id}/collaborators"},
    {"method": "GET", "path": "api/v1/projects/{id}/full"},
    {"method": "GET", "path": "api/v1/sections"},
    {"method": "GET", "path": "api/v1/sections/search"},
    {"method": "GET", "path": "api/v1/sections/{id}"},
    {"method": "GET", "path": "api/v1/labels"},
    {"method": "GET", "path": "api/v1/labels/search"},
    {"method": "GET", "path": "api/v1/labels/shared"},
    {"method": "GET", "path": "api/v1/labels/{id}"},
    {"method": "GET", "path": "api/v1/comments"},
    {"method": "GET", "path": "api/v1/comments/{id}"},
    {"method": "GET", "path": "api/v1/reminders"},
    {"method": "GET", "path": "api/v1/reminders/{id}"},
    {"method": "GET", "path": "api/v1/location_reminders"},
    {"method": "GET", "path": "api/v1/location_reminders/{id}"},
    {"method": "GET", "path": "api/v1/folders"},
    {"method": "GET", "path": "api/v1/folders/{id}"},
    {"method": "GET", "path": "api/v1/workspaces/invitations"},
    {"method": "GET", "path": "api/v1/workspaces/invitations/all"},
    {"method": "GET", "path": "api/v1/workspaces/joinable"},
    {"method": "GET", "path": "api/v1/workspaces/plan_details"},
    {"method": "GET", "path": "api/v1/workspaces/users"},
    {"method": "GET", "path": "api/v1/workspaces/{id}/projects/active"},
    {"method": "GET", "path": "api/v1/workspaces/{id}/projects/archived"},
    {"method": "GET", "path": "api/v1/tasks/completed/stats"},
    {"method": "GET", "path": "api/v1/activities"},
    {"method": "GET", "path": "api/v1/templates"},
    {"method": "GET", "path": "api/v1/templates/categories"},
    {"method": "GET", "path": "api/v1/templates/file"},
    {"method": "GET", "path": "api/v1/templates/preview"},
    {"method": "GET", "path": "api/v1/templates/{id}/preview"},
    {"method": "GET", "path": "api/v1/backups"},
    {"method": "GET", "path": "api/v1/id_mappings/{id}/{id}"},
    {"method": "POST", "path": "api/v1/payments/get_subscription_info"},
    {"method": "GET", "path": "api/v1/usage_billing/history"},
    {"method": "GET", "path": "api/v1/usage_billing/state"},
    {"method": "GET", "path": "api/v1/usage_billing/usage_summary"}
  ],
  "deny": []
}
```

## Endpoints

The Todoist endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/v1/tasks | read | tasks | Get all active tasks for the user. |
| POST | api/v1/tasks | write | tasks | Create a new task. |
| GET | api/v1/tasks/completed/by_completion_date | read | tasks | Retrieves a list of completed tasks strictly limited by the specified completion date range (up to 3 months). |
| GET | api/v1/tasks/completed/by_due_date | read | tasks | Retrieves a list of completed items strictly limited by the specified due date range (up to 6 weeks). |
| GET | api/v1/tasks/filter | read | tasks | Get all tasks matching the filter. |
| POST | api/v1/tasks/quick | write | tasks | Create a task from natural-language text with Quick Add. |
| GET | api/v1/tasks/{id} | read | tasks | Returns a single active (non-completed) task by ID. |
| POST | api/v1/tasks/{id} | write | tasks | Updates an existing task. |
| DELETE | api/v1/tasks/{id} | write | tasks | Delete a task and all of its subtasks. |
| POST | api/v1/tasks/{id}/close | write | tasks | Closes a task. |
| POST | api/v1/tasks/{id}/move | write | tasks | Moves task to another project, section or parent. |
| POST | api/v1/tasks/{id}/reopen | write | tasks | Reopens a task. |
| GET | api/v1/projects | read | projects | Get all active user projects, optionally filtered by folder or workspace. |
| POST | api/v1/projects | write | projects | Creates a new project and returns it. |
| GET | api/v1/projects/archived | read | projects | Get the user's archived projects. |
| POST | api/v1/projects/from_template | write | projects | Create a project from a template, returning only its ID and success status. |
| POST | api/v1/projects/import | write | projects | Create a project from CSV and return its ID and imported objects. |
| GET | api/v1/projects/permissions | read | projects | Returns a list of all the available roles and the associated actions they can perform in a project. |
| GET | api/v1/projects/search | read | projects | Search active user projects by name. |
| GET | api/v1/projects/{id} | read | projects | Returns a project object related to the given ID. |
| POST | api/v1/projects/{id} | write | projects | Updates a project and returns it. |
| DELETE | api/v1/projects/{id} | write | projects | Deletes a project and all of its sections and tasks. |
| POST | api/v1/projects/{id}/archive | write | projects | Marks a project as archived. |
| GET | api/v1/projects/{id}/collaborators | read | projects | Get all collaborators for a given project. |
| GET | api/v1/projects/{id}/full | read | projects | Get a project together with its sections, tasks, comments and collaborators. |
| POST | api/v1/projects/{id}/import | write | projects | Import CSV into an existing project and return the imported objects. |
| POST | api/v1/projects/{id}/import_template | write | projects | Import a project template, returning tasks, comments, reminders and applied defaults. |
| POST | api/v1/projects/{id}/join | write | projects | Join a workspace project as a workspace user. |
| POST | api/v1/projects/{id}/unarchive | write | projects | Marks a previously archived project as active again. |
| GET | api/v1/sections | read | sections | Get all active sections for the user, optionally filtered by project or workspace. |
| POST | api/v1/sections | write | sections | Create a new section. |
| GET | api/v1/sections/search | read | sections | Search active sections by name, optionally filtered by project or workspace. |
| GET | api/v1/sections/{id} | read | sections | Return the section for the given section ID. |
| POST | api/v1/sections/{id} | write | sections | Update a section. |
| DELETE | api/v1/sections/{id} | write | sections | Delete the section and all of its tasks. |
| POST | api/v1/sections/{id}/archive | write | sections | Marks a section as archived. |
| POST | api/v1/sections/{id}/unarchive | write | sections | Marks a section as active again. |
| GET | api/v1/labels | read | labels | Get all user labels. |
| POST | api/v1/labels | write | labels | Create a personal label. |
| GET | api/v1/labels/search | read | labels | Search user labels by name. |
| GET | api/v1/labels/shared | read | labels | Returns a set of unique strings containing shared labels from active tasks. |
| POST | api/v1/labels/shared/remove | write | labels | Remove the given shared label from all active tasks. |
| POST | api/v1/labels/shared/rename | write | labels | Rename the given shared label from all active tasks. |
| GET | api/v1/labels/{id} | read | labels | Return a personal label by ID. Returns NOTFOUND when the label does not exist or the ID is invalid. |
| POST | api/v1/labels/{id} | write | labels | Update a personal label. |
| DELETE | api/v1/labels/{id} | write | labels | Deletes a personal label. |
| GET | api/v1/comments | read | comments | Get all comments for a given task or project. |
| POST | api/v1/comments | write | comments | Creates a new comment on a project or task and returns it. |
| GET | api/v1/comments/{id} | read | comments | Returns a single comment by ID. |
| POST | api/v1/comments/{id} | write | comments | Update a comment by ID and returns its content. |
| DELETE | api/v1/comments/{id} | write | comments | Delete a comment by ID. |
| POST | api/v1/comments/{id}/reactions | write | comments | Adds the authenticated user's reaction to a task or project comment and returns the updated comment. |
| POST | api/v1/comments/{id}/reactions/remove | write | comments | Removes the authenticated user's reaction from a task or project comment. |
| GET | api/v1/reminders | read | reminders | Get all active reminders. |
| POST | api/v1/reminders | write | reminders | Create a new reminder for a task. |
| GET | api/v1/reminders/{id} | read | reminders | Return a single reminder by ID. |
| POST | api/v1/reminders/{id} | write | reminders | Update an existing reminder. |
| DELETE | api/v1/reminders/{id} | write | reminders | Delete a reminder by ID. |
| GET | api/v1/location_reminders | read | location-reminders | Get all active location reminders. |
| POST | api/v1/location_reminders | write | location-reminders | Create a new location reminder for a task. |
| GET | api/v1/location_reminders/{id} | read | location-reminders | Return a single location reminder by ID. |
| POST | api/v1/location_reminders/{id} | write | location-reminders | Update an existing location reminder. |
| DELETE | api/v1/location_reminders/{id} | write | location-reminders | Delete a location reminder by ID. |
| DELETE | api/v1/filters/{id} | write | filters | Delete a personal filter. |
| GET | api/v1/folders | read | folders | Get all folders for a workspace. |
| POST | api/v1/folders | write | folders | Create a new folder in the given workspace. |
| GET | api/v1/folders/{id} | read | folders | Return the folder for the given folder ID. |
| POST | api/v1/folders/{id} | write | folders | Update an existing folder. |
| DELETE | api/v1/folders/{id} | write | folders | Delete a folder. |
| GET | api/v1/workspaces | write | workspaces | List the user's workspaces; kept out of read because each workspace includes its invite code, which lets anyone join. |
| POST | api/v1/workspaces | write | workspaces | Creates a new workspace and returns it. |
| GET | api/v1/workspaces/invitations | read | workspaces | Return a list of user emails who have a pending invitation to a workspace. |
| GET | api/v1/workspaces/invitations/all | read | workspaces | Return a list containing details of all pending invitation to a workspace. |
| POST | api/v1/workspaces/invitations/delete | write | workspaces | Deletes a workspace invitation. |
| PUT | api/v1/workspaces/invitations/{id}/accept | write | workspaces | Accept a workspace invitation. |
| PUT | api/v1/workspaces/invitations/{id}/reject | write | workspaces | Reject a workspace invitation. |
| POST | api/v1/workspaces/join | write | workspaces | Join a workspace via link or via workspace ID, if the user can auto-join the workspace by domain. |
| GET | api/v1/workspaces/joinable | read | workspaces | List the workspaces the user could join by email domain. |
| POST | api/v1/workspaces/logo | write | workspaces | Upload an image to be used as the workspace logo. |
| GET | api/v1/workspaces/plan_details | read | workspaces | Lists details of the workspace's current plan and usage. |
| GET | api/v1/workspaces/users | read | workspaces | Returns all workspaceusers for a given workspace if workspaceid is provided. |
| GET | api/v1/workspaces/{id} | write | workspaces | Get a workspace; kept out of read because the response includes the workspace invite code, which lets anyone join. |
| POST | api/v1/workspaces/{id} | write | workspaces | Updates an existing workspace and returns it. |
| DELETE | api/v1/workspaces/{id} | write | workspaces | Deletes a workspace for all of its members. |
| GET | api/v1/workspaces/{id}/projects/active | read | workspaces | Returns all active workspace projects, including those visible but not joined by the user. |
| GET | api/v1/workspaces/{id}/projects/archived | read | workspaces | Return archived projects in a workspace. |
| POST | api/v1/workspaces/{id}/users/invite | write | workspaces | Invites users to a workspace by email. |
| POST | api/v1/workspaces/{id}/users/{id} | write | workspaces | Updates a workspace user's role. |
| DELETE | api/v1/workspaces/{id}/users/{id} | write | workspaces | Removes a user from a workspace. |
| PUT | api/v1/notification_setting | write | user | Update a notification delivery preference. |
| GET | api/v1/tasks/completed/stats | read | user | Get comprehensive productivity statistics for the authenticated user. |
| GET | api/v1/user | write | user | Get the current user; kept out of read because the response includes the user's API token and a tokenised websocket URL. |
| GET | api/v1/activities | read | activity | Get activity logs. |
| GET | api/v1/templates | read | templates | Discover templates or look up a bounded batch of IDs. |
| GET | api/v1/templates/categories | read | templates | List curated template categories. |
| POST | api/v1/templates/create_project_from_file | write | templates | A template can be imported in an existing project, or in a newly created one. |
| GET | api/v1/templates/file | read | templates | Download a project as a CSV template file. |
| POST | api/v1/templates/generate_description | write | templates | Generate an AI description for a project or saved template. |
| POST | api/v1/templates/import_into_project_from_file | write | templates | A template can be imported in an existing project, or in a newly created one. |
| POST | api/v1/templates/import_into_project_from_template_id | write | templates | Import a saved template into an existing project. |
| GET | api/v1/templates/preview | read | templates | Preview a project's template graph. |
| GET | api/v1/templates/url | write | templates | Publish a project as a shareable template URL; a GET that stores a public, non-expiring CSV copy of the project. |
| POST | api/v1/templates/user | write | templates | Creates a template from a project or a content graph. |
| POST | api/v1/templates/user/import | write | templates | Creates a personal template from CSV or a content graph. |
| POST | api/v1/templates/user/preview | write | templates | Stage and preview an uploaded project CSV; the upload is stored. |
| PUT | api/v1/templates/user/{id} | write | templates | Updates a template's metadata and, optionally, its content. |
| GET | api/v1/templates/{id} | write | templates | Get one template; kept out of read because the pattern would also match templates/url, which publishes a project. |
| GET | api/v1/templates/{id}/preview | read | templates | Preview a project or setup template without importing it. |
| POST | api/v1/templates/{id}/use | write | templates | Create a project or a complete setup from a template. |
| POST | api/v1/uploads | write | uploads | Upload a file to Todoist. |
| DELETE | api/v1/uploads | write | uploads | Delete an uploaded file. |
| PUT | api/v1/emails | write | emails | Get or create the forwarding email address of a project or task. |
| DELETE | api/v1/emails | write | emails | Disable the current email to a Todoist object. |
| GET | api/v1/backups | read | backups | List the available backup archives (versions and authenticated download addresses). |
| GET | api/v1/backups/download | write | backups | Download a backup archive; kept out of read because it redirects to a signed download URL for the full account archive. |
| GET | api/v1/id_mappings/{id}/{id} | read | ids | Translate object IDs between the old and new ID formats. |
| POST | api/v1/payments/cancel_plan_with_redirect_to_stripe | write | billing | Start a hosted cancellation flow and return the redirect URL. |
| POST | api/v1/payments/get_subscription_info | read | billing | Return the current user's subscription state (a lookup sent as POST). |
| POST | api/v1/payments/reactivate_plan | write | billing | Reactivate a previously canceled subscription. |
| GET | api/v1/usage_billing/history | read | billing | List the caller's usage-billing ledger entries, newest first. |
| GET | api/v1/usage_billing/state | read | billing | Read the caller's usage-billing credit state for a product. |
| POST | api/v1/usage_billing/top_up | write | billing | In V1, create a hosted Stripe Checkout session to top up the authenticated user's personal Todoist Wallet. |
| GET | api/v1/usage_billing/usage_summary | read | billing | Total the caller's settled usage over a window. |
| GET | api/v1/sync | write | sync | Sync endpoint called with GET; can carry write commands as parameters and returns the user's API token. |
| POST | api/v1/sync | write | sync | Sync endpoint: reads resources but also carries arbitrary write commands in the body, so it is not a read. |
| DELETE | api/v1/access_tokens | write | auth | Revoke OAuth access tokens. |
| POST | api/v1/access_tokens/migrate_personal_token | write | auth | Migrate a personal API token to an OAuth access token; returns a new token. |
| POST | api/v1/revoke | write | auth | Revoke an access token according to RFC 7009 OAuth Token Revocation. |
