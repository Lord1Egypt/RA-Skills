# Sentry access policy

An access policy limits which endpoints Sentry connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/sentry#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Sentry: its 151 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create sentry --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/0/organizations/{id}/agents/conversations"},
    {"method": "GET", "path": "api/0/organizations/{id}/agents/conversations/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/available-actions"},
    {"method": "GET", "path": "api/0/organizations/{id}/chunk-upload"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/code-mapping-prefixes/stack"},
    {"method": "GET", "path": "api/0/organizations/{id}/code-mappings"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/codeowners"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/codeowners/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/codeowners-associations"},
    {"method": "GET", "path": "api/0/organizations/{id}/config/integrations"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/custom-inbound-filters"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/custom-inbound-filters/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/dashboards"},
    {"method": "GET", "path": "api/0/organizations/{id}/dashboards/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/dashboards/{id}/revisions"},
    {"method": "GET", "path": "api/0/organizations/{id}/detectors"},
    {"method": "GET", "path": "api/0/organizations/{id}/detectors/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/discover/saved"},
    {"method": "GET", "path": "api/0/organizations/{id}/discover/saved/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/dsn-lookup"},
    {"method": "GET", "path": "api/0/organizations/{id}/environments"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/environments"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/environments/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/eventids/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/events"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/events"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/events/{id}"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/events/{id}/attachments"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/events/{id}/attachments/{id}"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/events/{id}/source-map-debug"},
    {"method": "GET", "path": "api/0/organizations/{id}/events-dropped"},
    {"method": "GET", "path": "api/0/organizations/{id}/events-timeseries"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/files/dsyms"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/filters"},
    {"method": "GET", "path": "api/0/organizations/{id}/flags/logs"},
    {"method": "GET", "path": "api/0/organizations/{id}/flags/logs/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/forwarding"},
    {"method": "GET", "path": "api/0/organizations/{id}/group-search-views"},
    {"method": "GET", "path": "api/0/organizations/{id}/integrations"},
    {"method": "GET", "path": "api/0/organizations/{id}/integrations/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/integrations/{id}/channel-validate"},
    {"method": "GET", "path": "api/0/organizations/{id}/integrations/{id}/channels"},
    {"method": "GET", "path": "api/0/organizations/{id}/integrations/{id}/repos"},
    {"method": "GET", "path": "api/0/organizations/{id}/issues"},
    {"method": "GET", "path": "api/0/organizations/{id}/issues/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/issues/{id}/autofix"},
    {"method": "GET", "path": "api/0/organizations/{id}/issues/{id}/events"},
    {"method": "GET", "path": "api/0/organizations/{id}/issues/{id}/events/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/issues/{id}/external-issues"},
    {"method": "GET", "path": "api/0/organizations/{id}/issues/{id}/hashes"},
    {"method": "GET", "path": "api/0/organizations/{id}/issues/{id}/integrations"},
    {"method": "GET", "path": "api/0/organizations/{id}/issues/{id}/integrations/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/issues/{id}/tags/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/issues/{id}/tags/{id}/values"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/issues"},
    {"method": "GET", "path": "api/0/organizations/{id}/members"},
    {"method": "GET", "path": "api/0/organizations/{id}/members/{id}"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/members"},
    {"method": "GET", "path": "api/0/teams/{id}/{id}/members"},
    {"method": "GET", "path": "api/0"},
    {"method": "GET", "path": "api/0/organizations/{id}/monitors"},
    {"method": "GET", "path": "api/0/organizations/{id}/monitors/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/monitors/{id}/checkins"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/monitors/{id}"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/monitors/{id}/checkins"},
    {"method": "GET", "path": "api/0/organizations/{id}/notebooks/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/notifications/actions"},
    {"method": "GET", "path": "api/0/organizations/{id}/notifications/actions/{id}"},
    {"method": "GET", "path": "api/0/organizations"},
    {"method": "GET", "path": "api/0/organizations/{id}"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/ownership"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/preprod/size-analysis/status-check-rules"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/preprod/snapshots/status-check-rules"},
    {"method": "GET", "path": "api/0/organizations/{id}/preprodartifacts/snapshots/latest-base"},
    {"method": "GET", "path": "api/0/organizations/{id}/preprodartifacts/snapshots/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/preprodartifacts/snapshots/{id}/archive"},
    {"method": "GET", "path": "api/0/organizations/{id}/preprodartifacts/snapshots/{id}/images/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/preprodartifacts/{id}/size-analysis"},
    {"method": "GET", "path": "api/0/organizations/{id}/profiling/chunks"},
    {"method": "GET", "path": "api/0/organizations/{id}/profiling/flamegraph"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/profiling/profiles/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/projects"},
    {"method": "GET", "path": "api/0/projects"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}"},
    {"method": "GET", "path": "api/0/teams/{id}/{id}/projects"},
    {"method": "GET", "path": "api/0/organizations/{id}/relay_usage"},
    {"method": "GET", "path": "api/0/organizations/{id}/release-threshold-statuses"},
    {"method": "GET", "path": "api/0/organizations/{id}/releases"},
    {"method": "GET", "path": "api/0/organizations/{id}/releases/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/releases/{id}/commitfiles"},
    {"method": "GET", "path": "api/0/organizations/{id}/releases/{id}/commits"},
    {"method": "GET", "path": "api/0/organizations/{id}/releases/{id}/deploys"},
    {"method": "GET", "path": "api/0/organizations/{id}/releases/{id}/files"},
    {"method": "GET", "path": "api/0/organizations/{id}/releases/{id}/files/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/releases/{id}/previous-with-commits"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/releases"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/releases/completion"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/releases/{id}/commits"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/releases/{id}/files"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/releases/{id}/files/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/replay-count"},
    {"method": "GET", "path": "api/0/organizations/{id}/replay-selectors"},
    {"method": "GET", "path": "api/0/organizations/{id}/replays"},
    {"method": "GET", "path": "api/0/organizations/{id}/replays/{id}"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/replays/jobs/delete"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/replays/jobs/delete/{id}"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/replays/{id}/clicks"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/replays/{id}/recording-segments"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/replays/{id}/recording-segments/{id}"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/replays/{id}/viewed-by"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/repo"},
    {"method": "GET", "path": "api/0/organizations/{id}/repos"},
    {"method": "GET", "path": "api/0/organizations/{id}/repos/{id}/commits"},
    {"method": "GET", "path": "api/0/organizations/{id}/scim/v2/Groups"},
    {"method": "GET", "path": "api/0/organizations/{id}/scim/v2/Groups/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/scim/v2/ResourceTypes"},
    {"method": "GET", "path": "api/0/organizations/{id}/scim/v2/ResourceTypes/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/scim/v2/Schemas/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/scim/v2/ServiceProviderConfig"},
    {"method": "GET", "path": "api/0/organizations/{id}/scim/v2/Users"},
    {"method": "GET", "path": "api/0/organizations/{id}/scim/v2/Users/{id}"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/seer/repos"},
    {"method": "GET", "path": "api/0/seer/models"},
    {"method": "GET", "path": "api/0/organizations/{id}/sentry-app-components"},
    {"method": "GET", "path": "api/0/organizations/{id}/sentry-app-installations"},
    {"method": "GET", "path": "api/0/sentry-app-installations/{id}/external-requests"},
    {"method": "GET", "path": "api/0/organizations/{id}/sessions"},
    {"method": "GET", "path": "api/0/organizations/{id}/shared/issues/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/shortids/{id}"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/stacktrace-link"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/stats"},
    {"method": "GET", "path": "api/0/organizations/{id}/stats-summary"},
    {"method": "GET", "path": "api/0/organizations/{id}/stats_v2"},
    {"method": "GET", "path": "api/0/organizations/{id}/tags"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/tags/{id}/values"},
    {"method": "GET", "path": "api/0/organizations/{id}/teams"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/teams"},
    {"method": "GET", "path": "api/0/teams/{id}/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/trace/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/trace-items/attributes"},
    {"method": "GET", "path": "api/0/organizations/{id}/trace-items/metrics"},
    {"method": "GET", "path": "api/0/organizations/{id}/trace-items/stats"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/trace-items/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/trace-logs"},
    {"method": "GET", "path": "api/0/organizations/{id}/trace-meta/{id}"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/user-feedback"},
    {"method": "GET", "path": "api/0/organizations/{id}/user-teams"},
    {"method": "GET", "path": "api/0/projects/{id}/{id}/users"},
    {"method": "GET", "path": "api/0/users/{id}"},
    {"method": "GET", "path": "api/0/organizations/{id}/workflows"},
    {"method": "GET", "path": "api/0/organizations/{id}/workflows/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Sentry endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/0/organizations/{id}/agents/conversations | read | agents | List an Organization's AI Conversations. |
| GET | api/0/organizations/{id}/agents/conversations/{id} | read | agents | Retrieve an Organization's AI Conversation. |
| POST | api/0/organizations/{id}/artifactbundle/assemble | write | artifactbundle | Assemble an Artifact Bundle. |
| GET | api/0/organizations/{id}/available-actions | read | available-actions | List Available Alert Actions. |
| GET | api/0/organizations/{id}/chunk-upload | read | chunk-upload | Retrieve Chunk Upload Options. |
| POST | api/0/organizations/{id}/chunk-upload | write | chunk-upload | Upload File Chunks. |
| GET | api/0/projects/{id}/{id}/code-mapping-prefixes/stack | read | code-mapping-prefixes | List Stack Trace Directory Prefixes for Code Mapping Autocomplete. |
| GET | api/0/organizations/{id}/code-mappings | read | code-mappings | List an Organization's Code Mappings. |
| POST | api/0/organizations/{id}/code-mappings | write | code-mappings | Create an Organization Code Mapping. |
| POST | api/0/organizations/{id}/code-mappings/bulk | write | code-mappings | Create or Update Organization Code Mappings in Bulk. |
| PUT | api/0/organizations/{id}/code-mappings/{id} | write | code-mappings | Update an Organization Code Mapping. |
| DELETE | api/0/organizations/{id}/code-mappings/{id} | write | code-mappings | Delete an Organization Code Mapping. |
| GET | api/0/projects/{id}/{id}/codeowners | read | codeowners | List a Project's CODEOWNERS Configurations. |
| POST | api/0/projects/{id}/{id}/codeowners | write | codeowners | Create a CODEOWNERS Configuration for a Project. |
| GET | api/0/projects/{id}/{id}/codeowners/{id} | read | codeowners | Retrieve a Project's CODEOWNERS Configuration. |
| PUT | api/0/projects/{id}/{id}/codeowners/{id} | write | codeowners | Update a Project's CODEOWNERS Configuration. |
| DELETE | api/0/projects/{id}/{id}/codeowners/{id} | write | codeowners | Delete a Project's CODEOWNERS Configuration. |
| GET | api/0/organizations/{id}/codeowners-associations | read | codeowners-associations | List Code Owner Associations. |
| GET | api/0/organizations/{id}/config/integrations | read | config | Get Integration Provider Information. |
| GET | api/0/projects/{id}/{id}/custom-inbound-filters | read | custom-inbound-filters | **Experimental:** This API is under active development and may change. |
| POST | api/0/projects/{id}/{id}/custom-inbound-filters | write | custom-inbound-filters | **Experimental:** This API is under active development and may change. |
| GET | api/0/projects/{id}/{id}/custom-inbound-filters/{id} | read | custom-inbound-filters | **Experimental:** This API is under active development and may change. |
| PUT | api/0/projects/{id}/{id}/custom-inbound-filters/{id} | write | custom-inbound-filters | **Experimental:** This API is under active development and may change. |
| DELETE | api/0/projects/{id}/{id}/custom-inbound-filters/{id} | write | custom-inbound-filters | **Experimental:** This API is under active development and may change. |
| GET | api/0/organizations/{id}/dashboards | read | dashboards | List an Organization's Custom Dashboards. |
| POST | api/0/organizations/{id}/dashboards | write | dashboards | Create a New Dashboard for an Organization. |
| GET | api/0/organizations/{id}/dashboards/{id} | read | dashboards | Retrieve an Organization's Custom Dashboard. |
| PUT | api/0/organizations/{id}/dashboards/{id} | write | dashboards | Edit an Organization's Custom Dashboard. |
| DELETE | api/0/organizations/{id}/dashboards/{id} | write | dashboards | Delete an Organization's Custom Dashboard. |
| GET | api/0/organizations/{id}/dashboards/{id}/revisions | read | dashboards | List a Custom Dashboard's Revisions. |
| POST | api/0/organizations/{id}/dashboards/{id}/revisions/{id}/restore | write | dashboards | Restore a Custom Dashboard Revision. |
| GET | api/0/organizations/{id}/detectors | read | detectors | Fetch an Organization's Monitors. |
| PUT | api/0/organizations/{id}/detectors | write | detectors | Mutate an Organization's Monitors. |
| DELETE | api/0/organizations/{id}/detectors | write | detectors | Bulk Delete Monitors. |
| GET | api/0/organizations/{id}/detectors/{id} | read | detectors | Fetch a Monitor. |
| PUT | api/0/organizations/{id}/detectors/{id} | write | detectors | Update a Monitor by ID. |
| DELETE | api/0/organizations/{id}/detectors/{id} | write | detectors | Delete a Monitor. |
| GET | api/0/organizations/{id}/discover/saved | read | discover | List an Organization's Discover Saved Queries. |
| POST | api/0/organizations/{id}/discover/saved | write | discover | Create a New Saved Query. |
| GET | api/0/organizations/{id}/discover/saved/{id} | read | discover | Retrieve an Organization's Discover Saved Query. |
| PUT | api/0/organizations/{id}/discover/saved/{id} | write | discover | Edit an Organization's Discover Saved Query. |
| DELETE | api/0/organizations/{id}/discover/saved/{id} | write | discover | Delete an Organization's Discover Saved Query. |
| GET | api/0/organizations/{id}/dsn-lookup | read | dsn-lookup | Resolve a DSN to Its Project. |
| GET | api/0/organizations/{id}/environments | read | environments | List an Organization's Environments. |
| GET | api/0/projects/{id}/{id}/environments | read | environments | List a Project's Environments. |
| PUT | api/0/projects/{id}/{id}/environments | write | environments | Bulk update the visibility for a project's environments. |
| GET | api/0/projects/{id}/{id}/environments/{id} | read | environments | Retrieve a Project Environment. |
| PUT | api/0/projects/{id}/{id}/environments/{id} | write | environments | Update a Project Environment. |
| GET | api/0/organizations/{id}/eventids/{id} | read | eventids | Resolve an Event ID. |
| GET | api/0/organizations/{id}/events | read | events | Query Explore Events in Table Format. |
| GET | api/0/projects/{id}/{id}/events | read | events | List a Project's Error Events. |
| GET | api/0/projects/{id}/{id}/events/{id} | read | events | Retrieve an Event for a Project. |
| GET | api/0/projects/{id}/{id}/events/{id}/attachments | read | events | List an Event's Attachments. |
| GET | api/0/projects/{id}/{id}/events/{id}/attachments/{id} | read | events | Retrieve an Event Attachment. |
| GET | api/0/projects/{id}/{id}/events/{id}/source-map-debug | read | events | Get Debug Information Related to Source Maps for a Given Event. |
| GET | api/0/organizations/{id}/events-dropped | read | events-dropped | Query Dropped and Accepted Events/Stats by Outcome and Reason. |
| GET | api/0/organizations/{id}/events-timeseries | read | events-timeseries | Query Explore Events in Timeseries Format. |
| POST | api/0/teams/{id}/{id}/external-teams | write | external-teams | Create an External Team. |
| PUT | api/0/teams/{id}/{id}/external-teams/{id} | write | external-teams | Update an External Team. |
| DELETE | api/0/teams/{id}/{id}/external-teams/{id} | write | external-teams | Delete an External Team. |
| POST | api/0/organizations/{id}/external-users | write | external-users | Create an External User. |
| PUT | api/0/organizations/{id}/external-users/{id} | write | external-users | Update an External User. |
| DELETE | api/0/organizations/{id}/external-users/{id} | write | external-users | Delete an External User. |
| POST | api/0/projects/{id}/{id}/files/difs/assemble | write | files | Assemble Debug Information Files. |
| GET | api/0/projects/{id}/{id}/files/dsyms | read | files | List a Project's Debug Information Files. |
| POST | api/0/projects/{id}/{id}/files/preprodartifacts/assemble | write | files | Assemble a Mobile Build. |
| GET | api/0/projects/{id}/{id}/filters | read | filters | List a Project's Data Filters. |
| PUT | api/0/projects/{id}/{id}/filters/{id} | write | filters | Update an Inbound Data Filter. |
| GET | api/0/organizations/{id}/flags/logs | read | flags | List an Organization's Flag Logs. |
| GET | api/0/organizations/{id}/flags/logs/{id} | read | flags | Retrieve an Organization's Flag Log. |
| GET | api/0/organizations/{id}/forwarding | read | forwarding | Retrieve Data Forwarders for an Organization. |
| POST | api/0/organizations/{id}/forwarding | write | forwarding | Create a Data Forwarder for an Organization. |
| PUT | api/0/organizations/{id}/forwarding/{id} | write | forwarding | Update a Data Forwarder for an Organization. |
| DELETE | api/0/organizations/{id}/forwarding/{id} | write | forwarding | Delete a Data Forwarder for an Organization. |
| GET | api/0/organizations/{id}/group-search-views | read | group-search-views | List Issue Views. |
| POST | api/0/organizations/{id}/group-search-views | write | group-search-views | Create an Issue View. |
| GET | api/0/projects/{id}/{id}/hooks | write | hooks | Return a list of service hooks bound to a project. Kept out of read: returns service hook secrets. |
| POST | api/0/projects/{id}/{id}/hooks | write | hooks | Register a new service hook on a project. |
| GET | api/0/projects/{id}/{id}/hooks/{id} | write | hooks | Return a service hook bound to a project. Kept out of read: returns service hook secrets. |
| PUT | api/0/projects/{id}/{id}/hooks/{id} | write | hooks | Update a service hook. |
| DELETE | api/0/projects/{id}/{id}/hooks/{id} | write | hooks | Remove a service hook. |
| GET | api/0/organizations/{id}/integrations | read | integrations | List an Organization's Available Integrations. |
| GET | api/0/organizations/{id}/integrations/{id} | read | integrations | Retrieve an Integration for an Organization. |
| DELETE | api/0/organizations/{id}/integrations/{id} | write | integrations | Delete an Integration for an Organization. |
| GET | api/0/organizations/{id}/integrations/{id}/channel-validate | read | integrations | Validate a Messaging Channel for an Integration. |
| GET | api/0/organizations/{id}/integrations/{id}/channels | read | integrations | List Messaging Channels for an Integration. |
| GET | api/0/organizations/{id}/integrations/{id}/repos | read | integrations | List Repositories Available to an Integration. |
| GET | api/0/organizations/{id}/issues | read | issues | List an Organization's Issues. |
| PUT | api/0/organizations/{id}/issues | write | issues | Bulk Mutate an Organization's Issues. |
| DELETE | api/0/organizations/{id}/issues | write | issues | Bulk Remove an Organization's Issues. |
| GET | api/0/organizations/{id}/issues/{id} | read | issues | Retrieve an Issue. |
| PUT | api/0/organizations/{id}/issues/{id} | write | issues | Update an Issue. |
| DELETE | api/0/organizations/{id}/issues/{id} | write | issues | Remove an Issue. |
| GET | api/0/organizations/{id}/issues/{id}/autofix | read | issues | Retrieve Seer Issue Fix State. |
| POST | api/0/organizations/{id}/issues/{id}/autofix | write | issues | Start Seer Issue Fix. |
| GET | api/0/organizations/{id}/issues/{id}/events | read | issues | List an Issue's Events. |
| GET | api/0/organizations/{id}/issues/{id}/events/{id} | read | issues | Retrieve an Issue Event. |
| GET | api/0/organizations/{id}/issues/{id}/external-issues | read | issues | Retrieve custom integration issue links for the given Sentry issue. |
| DELETE | api/0/organizations/{id}/issues/{id}/external-issues/{id} | write | issues | Unlink a Custom Integration's External Issue. |
| GET | api/0/organizations/{id}/issues/{id}/hashes | read | issues | List an Issue's Hashes. |
| GET | api/0/organizations/{id}/issues/{id}/integrations | read | issues | List an Issue's Tracker Integrations and Links. |
| GET | api/0/organizations/{id}/issues/{id}/integrations/{id} | read | issues | Retrieve the form fields needed to either link an existing external issue (such as a Jira ticket or GitHub issue) to a Sentry issue, or create a new one. |
| POST | api/0/organizations/{id}/issues/{id}/integrations/{id} | write | issues | Create a new issue in the external provider (such as a Jira ticket or GitHub issue) and link it to the given Sentry issue. |
| PUT | api/0/organizations/{id}/issues/{id}/integrations/{id} | write | issues | Link an issue that already exists in the external provider (such as a Jira ticket or GitHub issue) to the given Sentry issue. |
| DELETE | api/0/organizations/{id}/issues/{id}/integrations/{id} | write | issues | Remove the link between a Sentry issue and an external issue. |
| GET | api/0/organizations/{id}/issues/{id}/tags/{id} | read | issues | Retrieve Tag Details. |
| GET | api/0/organizations/{id}/issues/{id}/tags/{id}/values | read | issues | List a Tag's Values for an Issue. |
| GET | api/0/projects/{id}/{id}/issues | read | issues | **Deprecated**: This endpoint has been replaced with the [Organization Issues endpoint](/api/events/list-an-organizations-issues/) which supports filtering on project and additional functionality. |
| PUT | api/0/projects/{id}/{id}/issues | write | issues | Bulk mutate various attributes on issues. |
| DELETE | api/0/projects/{id}/{id}/issues | write | issues | Permanently remove the given issues. |
| GET | api/0/projects/{id}/{id}/keys | write | keys | List a Project's Client Keys. Kept out of read: returns client key secrets and DSNs. |
| POST | api/0/projects/{id}/{id}/keys | write | keys | Create a New Client Key. |
| GET | api/0/projects/{id}/{id}/keys/{id} | write | keys | Retrieve a Client Key. Kept out of read: returns client key secrets and DSNs. |
| PUT | api/0/projects/{id}/{id}/keys/{id} | write | keys | Update a Client Key. |
| DELETE | api/0/projects/{id}/{id}/keys/{id} | write | keys | Delete a Client Key. |
| GET | api/0/organizations/{id}/members | read | members | List an Organization's Members. |
| POST | api/0/organizations/{id}/members | write | members | Add a Member to an Organization. |
| GET | api/0/organizations/{id}/members/{id} | read | members | Retrieve an Organization Member. |
| PUT | api/0/organizations/{id}/members/{id} | write | members | Update an Organization Member's Roles. |
| DELETE | api/0/organizations/{id}/members/{id} | write | members | Delete an Organization Member. |
| POST | api/0/organizations/{id}/members/{id}/teams/{id} | write | members | Add an Organization Member to a Team. |
| PUT | api/0/organizations/{id}/members/{id}/teams/{id} | write | members | Update an Organization Member's Team Role. |
| DELETE | api/0/organizations/{id}/members/{id}/teams/{id} | write | members | Delete an Organization Member from a Team. |
| GET | api/0/projects/{id}/{id}/members | read | members | List a Project's Organization Members. |
| GET | api/0/teams/{id}/{id}/members | read | members | List a Team's Members. |
| GET | api/0 | read | misc | Retrieve the Current Credentials. |
| GET | api/0/organizations/{id}/monitors | read | monitors | Retrieve Monitors for an Organization. |
| POST | api/0/organizations/{id}/monitors | write | monitors | Create a Monitor. |
| GET | api/0/organizations/{id}/monitors/{id} | read | monitors | Retrieve a Monitor. |
| PUT | api/0/organizations/{id}/monitors/{id} | write | monitors | Update a Monitor. |
| DELETE | api/0/organizations/{id}/monitors/{id} | write | monitors | Delete a Monitor or Monitor Environments. |
| GET | api/0/organizations/{id}/monitors/{id}/checkins | read | monitors | Retrieve Check-Ins for a Monitor. |
| GET | api/0/projects/{id}/{id}/monitors/{id} | read | monitors | Retrieve a Monitor for a Project. |
| PUT | api/0/projects/{id}/{id}/monitors/{id} | write | monitors | Update a Monitor for a Project. |
| DELETE | api/0/projects/{id}/{id}/monitors/{id} | write | monitors | Delete a Monitor or Monitor Environments for a Project. |
| GET | api/0/projects/{id}/{id}/monitors/{id}/checkins | read | monitors | Retrieve Check-Ins for a Monitor by Project. |
| POST | api/0/organizations/{id}/notebooks | write | notebooks | **Experimental:** This API is under active development and may change. |
| GET | api/0/organizations/{id}/notebooks/{id} | read | notebooks | **Experimental:** This API is under active development and may change. |
| POST | api/0/organizations/{id}/notebooks/{id}/blocks | write | notebooks | **Experimental:** This API is under active development and may change. |
| PUT | api/0/organizations/{id}/notebooks/{id}/blocks/order | write | notebooks | **Experimental:** This API is under active development and may change. |
| PUT | api/0/organizations/{id}/notebooks/{id}/blocks/{id} | write | notebooks | **Experimental:** This API is under active development and may change. |
| DELETE | api/0/organizations/{id}/notebooks/{id}/blocks/{id} | write | notebooks | **Experimental:** This API is under active development and may change. |
| GET | api/0/organizations/{id}/notifications/actions | read | notifications | List Spike Protection Notifications. |
| POST | api/0/organizations/{id}/notifications/actions | write | notifications | Create a Spike Protection Notification Action. |
| GET | api/0/organizations/{id}/notifications/actions/{id} | read | notifications | Retrieve a Spike Protection Notification Action. |
| PUT | api/0/organizations/{id}/notifications/actions/{id} | write | notifications | Update a Spike Protection Notification Action. |
| DELETE | api/0/organizations/{id}/notifications/actions/{id} | write | notifications | Delete a Spike Protection Notification Action. |
| GET | api/0/organizations/{id}/org-auth-tokens | write | org-auth-tokens | List an Organization's Org Auth Tokens. Kept out of read: returns org auth tokens. |
| POST | api/0/organizations/{id}/org-auth-tokens | write | org-auth-tokens | Create an Org Auth Token. |
| DELETE | api/0/organizations/{id}/org-auth-tokens/{id} | write | org-auth-tokens | Revoke an Org Auth Token. |
| GET | api/0/organizations | read | organizations | List Your Organizations. |
| GET | api/0/organizations/{id} | read | organizations | Retrieve an Organization. |
| PUT | api/0/organizations/{id} | write | organizations | Update an Organization. |
| GET | api/0/projects/{id}/{id}/ownership | read | ownership | Retrieve Ownership Configuration for a Project. |
| PUT | api/0/projects/{id}/{id}/ownership | write | ownership | Update Ownership Configuration for a Project. |
| GET | api/0/projects/{id}/{id}/preprod/size-analysis/status-check-rules | read | preprod | Retrieve Size Analysis status check rules for a project. |
| POST | api/0/projects/{id}/{id}/preprod/size-analysis/status-checks/skip | write | preprod | Create a skipped Size Analysis status check. |
| GET | api/0/projects/{id}/{id}/preprod/snapshots/status-check-rules | read | preprod | Retrieve Snapshot status check rules for a project. |
| POST | api/0/projects/{id}/{id}/preprod/snapshots/status-checks/skip | write | preprod | Create a skipped Snapshot status check. |
| GET | api/0/organizations/{id}/preprodartifacts/snapshots/latest-base | read | preprodartifacts | Retrieve latest base Snapshot. |
| GET | api/0/organizations/{id}/preprodartifacts/snapshots/{id} | read | preprodartifacts | Retrieve Snapshot details. |
| DELETE | api/0/organizations/{id}/preprodartifacts/snapshots/{id} | write | preprodartifacts | Delete a Snapshot. |
| GET | api/0/organizations/{id}/preprodartifacts/snapshots/{id}/archive | read | preprodartifacts | Retrieve a Snapshot Archive's Status. |
| POST | api/0/organizations/{id}/preprodartifacts/snapshots/{id}/archive | write | preprodartifacts | Build a Snapshot Archive. |
| GET | api/0/organizations/{id}/preprodartifacts/snapshots/{id}/images/{id} | read | preprodartifacts | Retrieve Snapshot image detail. |
| GET | api/0/organizations/{id}/preprodartifacts/{id}/install-details | write | preprodartifacts | Retrieve install info for a given artifact. Kept out of read: returns an install URL. |
| GET | api/0/organizations/{id}/preprodartifacts/{id}/size-analysis | read | preprodartifacts | Retrieve Size Analysis results for a given artifact. |
| GET | api/0/projects/{id}/{id}/preprodartifacts/build-distribution/latest | write | preprodartifacts | Get the latest installable build for a project. Kept out of read: returns an installable build URL. |
| POST | api/0/projects/{id}/{id}/preprodartifacts/snapshots | write | preprodartifacts | Upload a Snapshot. |
| GET | api/0/organizations/{id}/profiling/chunks | read | profiling | Retrieve Profile Chunks for an Organization. |
| GET | api/0/organizations/{id}/profiling/flamegraph | read | profiling | Retrieve a Flamegraph for an Organization. |
| GET | api/0/projects/{id}/{id}/profiling/profiles/{id} | read | profiling | Retrieve a Profile. |
| GET | api/0/organizations/{id}/project-keys | write | project-keys | List an Organization's Client Keys. Kept out of read: returns client key secrets and DSNs. |
| GET | api/0/organizations/{id}/projects | read | projects | List an Organization's Projects. |
| POST | api/0/organizations/{id}/projects | write | projects | Create a Project for an Organization. |
| POST | api/0/organizations/{id}/projects/{id}/detectors | write | projects | Create a Monitor for a Project. |
| GET | api/0/projects | read | projects | List your projects. |
| GET | api/0/projects/{id}/{id} | read | projects | Retrieve a Project. |
| PUT | api/0/projects/{id}/{id} | write | projects | Update a Project. |
| DELETE | api/0/projects/{id}/{id} | write | projects | Delete a Project. |
| GET | api/0/teams/{id}/{id}/projects | read | projects | List a Team's Projects. |
| POST | api/0/teams/{id}/{id}/projects | write | projects | Create a New Project. |
| GET | api/0/organizations/{id}/relay_usage | read | relay_usage | List an Organization's trusted Relays. |
| GET | api/0/organizations/{id}/release-threshold-statuses | read | release-threshold-statuses | Retrieve Statuses of Release Thresholds (Alpha). |
| GET | api/0/organizations/{id}/releases | read | releases | List an Organization's Releases. |
| POST | api/0/organizations/{id}/releases | write | releases | Create a New Release for an Organization. |
| GET | api/0/organizations/{id}/releases/{id} | read | releases | Retrieve an Organization's Release. |
| PUT | api/0/organizations/{id}/releases/{id} | write | releases | Update an Organization's Release. |
| DELETE | api/0/organizations/{id}/releases/{id} | write | releases | Delete an Organization's Release. |
| GET | api/0/organizations/{id}/releases/{id}/commitfiles | read | releases | Retrieve files changed in a release's commits. |
| GET | api/0/organizations/{id}/releases/{id}/commits | read | releases | List an Organization Release's Commits. |
| GET | api/0/organizations/{id}/releases/{id}/deploys | read | releases | List a Release's Deploys. |
| POST | api/0/organizations/{id}/releases/{id}/deploys | write | releases | Create a Deploy. |
| GET | api/0/organizations/{id}/releases/{id}/files | read | releases | List an Organization's Release Files. |
| POST | api/0/organizations/{id}/releases/{id}/files | write | releases | Upload a New Organization Release File. |
| GET | api/0/organizations/{id}/releases/{id}/files/{id} | read | releases | Retrieve an Organization Release's File. |
| PUT | api/0/organizations/{id}/releases/{id}/files/{id} | write | releases | Update an Organization Release File. |
| DELETE | api/0/organizations/{id}/releases/{id}/files/{id} | write | releases | Delete an Organization Release's File. |
| GET | api/0/organizations/{id}/releases/{id}/previous-with-commits | read | releases | Retrieve an Organization's Previous Release with Commits. |
| GET | api/0/projects/{id}/{id}/releases | read | releases | List a Project's Releases. |
| GET | api/0/projects/{id}/{id}/releases/completion | read | releases | Retrieve a Project's Release Setup Progress. |
| GET | api/0/projects/{id}/{id}/releases/{id}/commits | read | releases | List a Project Release's Commits. |
| GET | api/0/projects/{id}/{id}/releases/{id}/files | read | releases | List a Project's Release Files. |
| POST | api/0/projects/{id}/{id}/releases/{id}/files | write | releases | Upload a New Project Release File. |
| GET | api/0/projects/{id}/{id}/releases/{id}/files/{id} | read | releases | Retrieve a Project Release's File. |
| PUT | api/0/projects/{id}/{id}/releases/{id}/files/{id} | write | releases | Update a Project Release File. |
| DELETE | api/0/projects/{id}/{id}/releases/{id}/files/{id} | write | releases | Delete a Project Release's File. |
| GET | api/0/organizations/{id}/replay-count | read | replay-count | Retrieve a Count of Replays for a Given Issue or Transaction. |
| GET | api/0/organizations/{id}/replay-selectors | read | replay-selectors | List an Organization's Selectors. |
| GET | api/0/organizations/{id}/replays | read | replays | List an Organization's Replays. |
| GET | api/0/organizations/{id}/replays/{id} | read | replays | Retrieve a Replay Instance. |
| GET | api/0/projects/{id}/{id}/replays/jobs/delete | read | replays | List Replay Batch-Deletion Jobs. |
| POST | api/0/projects/{id}/{id}/replays/jobs/delete | write | replays | Create Replay Batch Deletion Job. |
| GET | api/0/projects/{id}/{id}/replays/jobs/delete/{id} | read | replays | Retrieve a Replay Batch-Deletion Job. |
| DELETE | api/0/projects/{id}/{id}/replays/{id} | write | replays | Delete a Replay Instance. |
| GET | api/0/projects/{id}/{id}/replays/{id}/clicks | read | replays | List Clicked Nodes. |
| GET | api/0/projects/{id}/{id}/replays/{id}/recording-segments | read | replays | List Recording Segments. |
| GET | api/0/projects/{id}/{id}/replays/{id}/recording-segments/{id} | read | replays | Retrieve a Recording Segment. |
| GET | api/0/projects/{id}/{id}/replays/{id}/viewed-by | read | replays | List Users Who Have Viewed a Replay. |
| GET | api/0/projects/{id}/{id}/repo | read | repo | List Repositories Linked to a Project. |
| POST | api/0/projects/{id}/{id}/repo | write | repo | Link a Repository to a Project. |
| GET | api/0/organizations/{id}/repos | read | repos | List an Organization's Repositories. |
| PUT | api/0/organizations/{id}/repos/settings | write | repos | Update Settings for Organization Repositories. |
| GET | api/0/organizations/{id}/repos/{id}/commits | read | repos | List a Repository's Commits. |
| GET | api/0/organizations/{id}/scim/v2/Groups | read | scim | List an Organization's Paginated Teams. |
| POST | api/0/organizations/{id}/scim/v2/Groups | write | scim | Provision a New Team. |
| GET | api/0/organizations/{id}/scim/v2/Groups/{id} | read | scim | Query an Individual Team. |
| PATCH | api/0/organizations/{id}/scim/v2/Groups/{id} | write | scim | Update a Team's Attributes. |
| DELETE | api/0/organizations/{id}/scim/v2/Groups/{id} | write | scim | Delete an Individual Team. |
| GET | api/0/organizations/{id}/scim/v2/ResourceTypes | read | scim | List the SCIM Resource Types. |
| GET | api/0/organizations/{id}/scim/v2/ResourceTypes/{id} | read | scim | Query an Individual SCIM Resource Type. |
| GET | api/0/organizations/{id}/scim/v2/Schemas/{id} | read | scim | Query an Individual SCIM Schema. |
| GET | api/0/organizations/{id}/scim/v2/ServiceProviderConfig | read | scim | Retrieve the SCIM Service Provider Configuration. |
| GET | api/0/organizations/{id}/scim/v2/Users | read | scim | List an Organization's SCIM Members. |
| POST | api/0/organizations/{id}/scim/v2/Users | write | scim | Provision a New Organization Member. |
| GET | api/0/organizations/{id}/scim/v2/Users/{id} | read | scim | Query an Individual Organization Member. |
| PATCH | api/0/organizations/{id}/scim/v2/Users/{id} | write | scim | Update an Organization Member's Attributes. |
| DELETE | api/0/organizations/{id}/scim/v2/Users/{id} | write | scim | Delete an Organization Member via SCIM. |
| GET | api/0/projects/{id}/{id}/seer/repos | read | seer | List Repositories Configured for Seer. |
| POST | api/0/projects/{id}/{id}/seer/repos | write | seer | Add Repositories to Seer for a Project. |
| PUT | api/0/projects/{id}/{id}/seer/repos | write | seer | Replace Repositories Configured for Seer. |
| GET | api/0/seer/models | read | seer | List Seer AI Models. |
| GET | api/0/organizations/{id}/sentry-app-components | read | sentry-app-components | List an Organization's Installed Sentry App Components. |
| GET | api/0/organizations/{id}/sentry-app-installations | read | sentry-app-installations | Return a list of integration platform installations for a given organization. |
| POST | api/0/sentry-app-installations/{id}/external-issue-actions | write | sentry-app-installations | Create or Link an External Issue Through a Sentry App. |
| POST | api/0/sentry-app-installations/{id}/external-issues | write | sentry-app-installations | Create or update an external issue from an integration platform integration. |
| DELETE | api/0/sentry-app-installations/{id}/external-issues/{id} | write | sentry-app-installations | Delete an external issue. |
| GET | api/0/sentry-app-installations/{id}/external-requests | read | sentry-app-installations | Retrieve a Sentry App's Select Field Options. |
| GET | api/0/organizations/{id}/sentry-apps | write | sentry-apps | Retrieve the custom integrations created by an organization. Kept out of read: returns app client secrets. |
| GET | api/0/sentry-apps/{id} | write | sentry-apps | Retrieve a custom integration by ID or slug. Kept out of read: returns app client secrets. |
| PUT | api/0/sentry-apps/{id} | write | sentry-apps | Update an existing custom integration. |
| DELETE | api/0/sentry-apps/{id} | write | sentry-apps | Delete a custom integration. |
| GET | api/0/organizations/{id}/sessions | read | sessions | Retrieve Release Health Session Statistics. |
| GET | api/0/organizations/{id}/shared/issues/{id} | read | shared | Retrieve a Shared Issue. |
| GET | api/0/organizations/{id}/shortids/{id} | read | shortids | Resolve a Short ID. |
| POST | api/0/organizations/{id}/spike-protections | write | spike-protections | Enables Spike Protection feature for some of the projects within the organization. |
| DELETE | api/0/organizations/{id}/spike-protections | write | spike-protections | Disables Spike Protection feature for some of the projects within the organization. |
| GET | api/0/projects/{id}/{id}/stacktrace-link | read | stacktrace-link | Get a Source Code Link for a Stack Trace Frame. |
| POST | api/0/organizations/{id}/starred-service-spans | write | starred-service-spans | Star a Service Span. |
| DELETE | api/0/organizations/{id}/starred-service-spans | write | starred-service-spans | Unstar a Service Span. |
| GET | api/0/projects/{id}/{id}/stats | read | stats | Retrieve Event Counts for a Project. |
| GET | api/0/organizations/{id}/stats-summary | read | stats-summary | Retrieve an Organization's Events Count by Project. |
| GET | api/0/organizations/{id}/stats_v2 | read | stats_v2 | Retrieve Event Counts for an Organization (v2). |
| GET | api/0/projects/{id}/{id}/symbol-sources | write | symbol-sources | Retrieve a Project's Symbol Sources. Kept out of read: returns symbol source credentials. |
| POST | api/0/projects/{id}/{id}/symbol-sources | write | symbol-sources | Add a Symbol Source to a Project. |
| PUT | api/0/projects/{id}/{id}/symbol-sources | write | symbol-sources | Update a Project's Symbol Source. |
| DELETE | api/0/projects/{id}/{id}/symbol-sources | write | symbol-sources | Delete a Symbol Source from a Project. |
| GET | api/0/organizations/{id}/tags | read | tags | List an Organization's Tags. |
| GET | api/0/projects/{id}/{id}/tags/{id}/values | read | tags | Return a list of values associated with this key. |
| GET | api/0/organizations/{id}/teams | read | teams | List an Organization's Teams. |
| POST | api/0/organizations/{id}/teams | write | teams | Create a New Team. |
| GET | api/0/projects/{id}/{id}/teams | read | teams | List a Project's Teams. |
| POST | api/0/projects/{id}/{id}/teams/{id} | write | teams | Add a Team to a Project. |
| DELETE | api/0/projects/{id}/{id}/teams/{id} | write | teams | Delete a Team from a Project. |
| GET | api/0/teams/{id}/{id} | read | teams | Retrieve a Team. |
| PUT | api/0/teams/{id}/{id} | write | teams | Update a Team. |
| DELETE | api/0/teams/{id}/{id} | write | teams | Delete a Team. |
| GET | api/0/organizations/{id}/trace/{id} | read | trace | Retrieve a Trace. |
| GET | api/0/organizations/{id}/trace-items/attributes | read | trace-items | List Trace Item Attributes. |
| GET | api/0/organizations/{id}/trace-items/metrics | read | trace-items | List an Organization's Trace Metrics. |
| GET | api/0/organizations/{id}/trace-items/stats | read | trace-items | Compute statistics, such as attribute value distributions, over the trace items (spans or occurrences) matching the given query within the requested time range. |
| GET | api/0/projects/{id}/{id}/trace-items/{id} | read | trace-items | Retrieve a Trace Item. |
| GET | api/0/organizations/{id}/trace-logs | read | trace-logs | List Logs for Traces or a Replay. |
| GET | api/0/organizations/{id}/trace-meta/{id} | read | trace-meta | Retrieve Trace Metadata. |
| GET | api/0/projects/{id}/{id}/user-feedback | read | user-feedback | Return a list of user feedback items within this project. |
| POST | api/0/projects/{id}/{id}/user-feedback | write | user-feedback | *This endpoint is DEPRECATED. |
| GET | api/0/organizations/{id}/user-teams | read | user-teams | List a User's Teams for an Organization. |
| GET | api/0/projects/{id}/{id}/users | read | users | List a Project's Users. |
| GET | api/0/users/{id} | read | users | Retrieve a User's Details. |
| GET | api/0/organizations/{id}/workflows | read | workflows | Fetch Alerts. |
| POST | api/0/organizations/{id}/workflows | write | workflows | Create an Alert for an Organization. |
| PUT | api/0/organizations/{id}/workflows | write | workflows | Mutate an Organization's Alerts. |
| DELETE | api/0/organizations/{id}/workflows | write | workflows | Bulk Delete Alerts. |
| GET | api/0/organizations/{id}/workflows/{id} | read | workflows | Fetch an Alert. |
| PUT | api/0/organizations/{id}/workflows/{id} | write | workflows | Update an Alert by ID. |
| DELETE | api/0/organizations/{id}/workflows/{id} | write | workflows | Delete an Alert. |
