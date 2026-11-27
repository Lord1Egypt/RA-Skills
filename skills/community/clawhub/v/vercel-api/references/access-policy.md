# Vercel access policy

An access policy limits which endpoints Vercel connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/vercel#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Vercel: its 189 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create vercel --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1/access-groups"},
    {"method": "GET", "path": "v1/access-groups/{id}"},
    {"method": "GET", "path": "v1/access-groups/{id}/members"},
    {"method": "GET", "path": "v1/access-groups/{id}/projects"},
    {"method": "GET", "path": "v1/access-groups/{id}/projects/{id}"},
    {"method": "GET", "path": "ai-gateway/budgets/defaults/list"},
    {"method": "GET", "path": "ai-gateway/budgets/list"},
    {"method": "GET", "path": "ai-gateway/rules"},
    {"method": "GET", "path": "ai-gateway/virtual-model-configs"},
    {"method": "GET", "path": "ai-gateway/virtual-model-configs/list"},
    {"method": "GET", "path": "ai-gateway/virtual-model-configs/{id}"},
    {"method": "GET", "path": "v1/ai-gateway/routers"},
    {"method": "GET", "path": "v4/aliases"},
    {"method": "GET", "path": "v4/aliases/{id}"},
    {"method": "GET", "path": "v8/artifacts/status"},
    {"method": "GET", "path": "v8/artifacts/{id}"},
    {"method": "GET", "path": "v1/billing/charges"},
    {"method": "GET", "path": "v1/bulk-redirects"},
    {"method": "GET", "path": "v1/bulk-redirects/versions"},
    {"method": "GET", "path": "v8/certs"},
    {"method": "GET", "path": "v8/certs/{id}"},
    {"method": "GET", "path": "v1/connect/connectors/{id}"},
    {"method": "GET", "path": "v1/connect/connectors/{id}/projects/{id}"},
    {"method": "GET", "path": "v1/connect/networks"},
    {"method": "GET", "path": "v1/connect/networks/{id}"},
    {"method": "GET", "path": "v2/connect/connectors"},
    {"method": "GET", "path": "v2/connect/connectors/{id}/projects"},
    {"method": "GET", "path": "v2/connect/projects/{id}/connectors"},
    {"method": "GET", "path": "v1/deployments/{id}/checks"},
    {"method": "GET", "path": "v1/deployments/{id}/checks/{id}"},
    {"method": "GET", "path": "v1/deployments/{id}/feature-flags"},
    {"method": "GET", "path": "v13/deployments/{id}"},
    {"method": "GET", "path": "v2/deployments/{id}/aliases"},
    {"method": "GET", "path": "v2/deployments/{id}/check-runs"},
    {"method": "GET", "path": "v2/deployments/{id}/check-runs/{id}"},
    {"method": "GET", "path": "v3/deployments/{id}/events"},
    {"method": "GET", "path": "v6/deployments/{id}/files"},
    {"method": "GET", "path": "v7/deployments"},
    {"method": "GET", "path": "v8/deployments/{id}/files/{id}"},
    {"method": "GET", "path": "domains/records/{id}"},
    {"method": "GET", "path": "v1/domains/{id}/project-domains"},
    {"method": "GET", "path": "v5/domains"},
    {"method": "GET", "path": "v5/domains/{id}"},
    {"method": "GET", "path": "v5/domains/{id}/records"},
    {"method": "GET", "path": "v6/domains/{id}/config"},
    {"method": "GET", "path": "v9/domains/{id}/verification"},
    {"method": "GET", "path": "v1/drives"},
    {"method": "GET", "path": "v1/drives/{id}"},
    {"method": "GET", "path": "v1/events/types"},
    {"method": "GET", "path": "v3/events"},
    {"method": "GET", "path": "v1/global-config"},
    {"method": "GET", "path": "v1/global-config/{id}"},
    {"method": "GET", "path": "v1/global-config/{id}/backups"},
    {"method": "GET", "path": "v1/global-config/{id}/backups/{id}"},
    {"method": "GET", "path": "v1/global-config/{id}/item/{id}"},
    {"method": "GET", "path": "v1/global-config/{id}/items"},
    {"method": "GET", "path": "v1/global-config/{id}/schema"},
    {"method": "GET", "path": "v1/installations/{id}/account"},
    {"method": "GET", "path": "v1/installations/{id}/billing/invoices/{id}"},
    {"method": "GET", "path": "v1/installations/{id}/member/{id}"},
    {"method": "GET", "path": "v1/installations/{id}/resources"},
    {"method": "GET", "path": "v1/installations/{id}/resources/{id}"},
    {"method": "GET", "path": "v1/installations/{id}/resources/{id}/experimentation/global-config"},
    {"method": "GET", "path": "v1/integrations/configuration/{id}"},
    {"method": "GET", "path": "v1/integrations/configuration/{id}/products"},
    {"method": "GET", "path": "v1/integrations/configurations"},
    {"method": "GET", "path": "v1/integrations/git-namespaces"},
    {"method": "GET", "path": "v1/integrations/integration/{id}/products/{id}/plans"},
    {"method": "GET", "path": "v1/integrations/search-repo"},
    {"method": "GET", "path": "v1/kms/issuers"},
    {"method": "GET", "path": "v1/kms/issuers/{id}"},
    {"method": "GET", "path": "v1/microfrontends/groups"},
    {"method": "GET", "path": "v1/microfrontends/groups/{id}/projects"},
    {"method": "GET", "path": "v1/microfrontends/projects/{id}/production-mfe-config"},
    {"method": "GET", "path": "v1/microfrontends/{id}/config"},
    {"method": "GET", "path": "v1/networking/privatelink/endpoints"},
    {"method": "GET", "path": "v1/networking/privatelink/endpoints/{id}"},
    {"method": "GET", "path": "v1/observability/manage/configuration/projects"},
    {"method": "POST", "path": "v2/observability/query"},
    {"method": "GET", "path": "v2/observability/schema"},
    {"method": "GET", "path": "v2/observability/schema/{id}"},
    {"method": "GET", "path": "v1/organizations"},
    {"method": "GET", "path": "v1/organizations/{id}"},
    {"method": "GET", "path": "v1/organizations/{id}/dsync/groups"},
    {"method": "GET", "path": "v1/organizations/{id}/dsync/groups/{id}"},
    {"method": "GET", "path": "v1/organizations/{id}/teams"},
    {"method": "GET", "path": "v1/projects/traces"},
    {"method": "GET", "path": "v1/projects/{id}/daemons"},
    {"method": "GET", "path": "v1/projects/{id}/deployments/{id}/runtime-logs"},
    {"method": "GET", "path": "v1/projects/{id}/feature-flags/connections"},
    {"method": "GET", "path": "v1/projects/{id}/feature-flags/flags"},
    {"method": "GET", "path": "v1/projects/{id}/feature-flags/flags/{id}"},
    {"method": "GET", "path": "v1/projects/{id}/feature-flags/flags/{id}/versions"},
    {"method": "GET", "path": "v1/projects/{id}/feature-flags/labels"},
    {"method": "GET", "path": "v1/projects/{id}/feature-flags/labels/counts"},
    {"method": "POST", "path": "v1/projects/{id}/feature-flags/labels/lookup"},
    {"method": "GET", "path": "v1/projects/{id}/feature-flags/segments"},
    {"method": "GET", "path": "v1/projects/{id}/feature-flags/segments/{id}"},
    {"method": "GET", "path": "v1/projects/{id}/feature-flags/settings"},
    {"method": "GET", "path": "v1/projects/{id}/members"},
    {"method": "GET", "path": "v1/projects/{id}/promote/aliases"},
    {"method": "GET", "path": "v1/projects/{id}/rolling-release"},
    {"method": "GET", "path": "v1/projects/{id}/rolling-release/billing"},
    {"method": "GET", "path": "v1/projects/{id}/rolling-release/config"},
    {"method": "GET", "path": "v1/projects/{id}/routes"},
    {"method": "GET", "path": "v1/projects/{id}/routes/versions"},
    {"method": "GET", "path": "v10/projects"},
    {"method": "GET", "path": "v2/projects/{id}/checks"},
    {"method": "GET", "path": "v2/projects/{id}/checks/{id}"},
    {"method": "GET", "path": "v2/projects/{id}/checks/{id}/runs"},
    {"method": "GET", "path": "v2/projects/{id}/feature-flags/flags"},
    {"method": "GET", "path": "v9/projects/{id}"},
    {"method": "GET", "path": "v9/projects/{id}/custom-environments"},
    {"method": "GET", "path": "v9/projects/{id}/custom-environments/{id}"},
    {"method": "GET", "path": "v9/projects/{id}/domains"},
    {"method": "GET", "path": "v9/projects/{id}/domains/{id}"},
    {"method": "GET", "path": "v1/query/web-analytics/events/aggregate"},
    {"method": "GET", "path": "v1/query/web-analytics/events/count"},
    {"method": "GET", "path": "v1/query/web-analytics/visits/aggregate"},
    {"method": "GET", "path": "v1/query/web-analytics/visits/count"},
    {"method": "POST", "path": "v1/registrar/domains/availability"},
    {"method": "POST", "path": "v1/registrar/domains/price"},
    {"method": "POST", "path": "v1/registrar/domains/search"},
    {"method": "GET", "path": "v1/registrar/domains/{id}/availability"},
    {"method": "GET", "path": "v1/registrar/domains/{id}/contact-info/schema"},
    {"method": "GET", "path": "v1/registrar/domains/{id}/contact-verification"},
    {"method": "GET", "path": "v1/registrar/domains/{id}/price"},
    {"method": "GET", "path": "v1/registrar/domains/{id}/transfer"},
    {"method": "GET", "path": "v1/registrar/orders/{id}"},
    {"method": "GET", "path": "v1/registrar/tlds/supported"},
    {"method": "GET", "path": "v1/registrar/tlds/{id}"},
    {"method": "GET", "path": "v1/registrar/tlds/{id}/price"},
    {"method": "GET", "path": "v2/sandboxes"},
    {"method": "GET", "path": "v2/sandboxes/drives"},
    {"method": "GET", "path": "v2/sandboxes/drives/{id}"},
    {"method": "GET", "path": "v2/sandboxes/sessions"},
    {"method": "GET", "path": "v2/sandboxes/sessions/{id}"},
    {"method": "GET", "path": "v2/sandboxes/sessions/{id}/cmd"},
    {"method": "GET", "path": "v2/sandboxes/sessions/{id}/cmd/{id}"},
    {"method": "GET", "path": "v2/sandboxes/sessions/{id}/cmd/{id}/logs"},
    {"method": "GET", "path": "v2/sandboxes/snapshots"},
    {"method": "GET", "path": "v2/sandboxes/snapshots/{id}"},
    {"method": "GET", "path": "v2/sandboxes/{id}"},
    {"method": "GET", "path": "v1/security/firewall/attack-status"},
    {"method": "GET", "path": "v1/security/firewall/bypass"},
    {"method": "GET", "path": "v1/security/firewall/bypass/rules"},
    {"method": "GET", "path": "v1/security/firewall/config"},
    {"method": "GET", "path": "v1/security/firewall/config/{id}"},
    {"method": "GET", "path": "v1/security/firewall/events"},
    {"method": "GET", "path": "v1/security/firewall/events/summary"},
    {"method": "GET", "path": "storage/stores/{id}"},
    {"method": "GET", "path": "v1/teams/{id}/feature-flags/flags"},
    {"method": "GET", "path": "v1/teams/{id}/feature-flags/settings"},
    {"method": "GET", "path": "v1/teams/{id}/request/{id}"},
    {"method": "GET", "path": "v2/teams"},
    {"method": "GET", "path": "v2/teams/{id}"},
    {"method": "GET", "path": "v2/teams/{id}/feature-flags/flags"},
    {"method": "GET", "path": "v3/teams/{id}/members"},
    {"method": "GET", "path": "v2/user"},
    {"method": "GET", "path": "v5/user/tokens/{id}"},
    {"method": "GET", "path": "v6/user/tokens"},
    {"method": "GET", "path": "v1/vcr/repository"},
    {"method": "GET", "path": "v1/vcr/repository/{id}"},
    {"method": "GET", "path": "v1/vcr/repository/{id}/images"},
    {"method": "GET", "path": "v1/vcr/repository/{id}/images/{id}"},
    {"method": "GET", "path": "v1/vcr/repository/{id}/permissions"},
    {"method": "GET", "path": "v1/vcr/repository/{id}/tags"},
    {"method": "GET", "path": "v1/vcr/repository/{id}/tags/{id}"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/attempts"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/attempts/{id}"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}/runs"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}/runs/{id}"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}/runs/{id}/logs"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}/runs/{id}/task-definitions"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}/runs/{id}/task-definitions/{id}/runs/{id}/logs"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}/runs/{id}/task-runs"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/attempts/{id}/logs"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/attempts/{id}/task-logs"},
    {"method": "GET", "path": "v1/vercel-ci/invocations/{id}/tree"},
    {"method": "GET", "path": "v1/vercel-ci/log-search"},
    {"method": "GET", "path": "v1/vercel-ci/repository-settings"},
    {"method": "GET", "path": "v1/vercel-ci/task-analyses/{id}"},
    {"method": "GET", "path": "v1/vercel-ci/task-analyses/{id}/tasks"},
    {"method": "GET", "path": "v2/vercel-ci/branches"},
    {"method": "GET", "path": "v2/vercel-ci/invocations"},
    {"method": "GET", "path": "v1/webhooks"},
    {"method": "GET", "path": "v1/webhooks/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Vercel endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1/access-groups | read | access-groups | List access groups for a team, project or member. |
| POST | v1/access-groups | write | access-groups | Creates an access group. |
| GET | v1/access-groups/{id} | read | access-groups | Reads an access group. |
| POST | v1/access-groups/{id} | write | access-groups | Update an access group. |
| DELETE | v1/access-groups/{id} | write | access-groups | Deletes an access group. |
| GET | v1/access-groups/{id}/members | read | access-groups | List members of an access group. |
| GET | v1/access-groups/{id}/projects | read | access-groups | List projects of an access group. |
| POST | v1/access-groups/{id}/projects | write | access-groups | Create an access group project. |
| GET | v1/access-groups/{id}/projects/{id} | read | access-groups | Reads an access group project. |
| PATCH | v1/access-groups/{id}/projects/{id} | write | access-groups | Update an access group project. |
| DELETE | v1/access-groups/{id}/projects/{id} | write | access-groups | Delete an access group project. |
| PUT | ai-gateway/budgets | write | ai-gateway | Upsert AI Gateway budget. |
| DELETE | ai-gateway/budgets | write | ai-gateway | Archive AI Gateway budget. |
| PUT | ai-gateway/budgets/defaults | write | ai-gateway | Upsert AI Gateway budget default. |
| DELETE | ai-gateway/budgets/defaults | write | ai-gateway | Archive AI Gateway budget default. |
| GET | ai-gateway/budgets/defaults/list | read | ai-gateway | List AI Gateway budget defaults. |
| GET | ai-gateway/budgets/list | read | ai-gateway | List AI Gateway budgets. |
| POST | ai-gateway/byok-credentials | write | ai-gateway | Create a BYOK credential. |
| GET | ai-gateway/byok-credentials/list | write | ai-gateway | List BYOK credentials. Kept out of read: returns provider credentials. |
| GET | ai-gateway/byok-credentials/{id} | write | ai-gateway | Get a BYOK credential. Kept out of read: returns provider credentials. |
| PATCH | ai-gateway/byok-credentials/{id} | write | ai-gateway | Update a BYOK credential. |
| DELETE | ai-gateway/byok-credentials/{id} | write | ai-gateway | Delete a BYOK credential. |
| GET | ai-gateway/rules | read | ai-gateway | List rules. |
| POST | ai-gateway/rules | write | ai-gateway | Create rule. |
| PATCH | ai-gateway/rules | write | ai-gateway | Update rule. |
| DELETE | ai-gateway/rules | write | ai-gateway | Delete rule. |
| GET | ai-gateway/virtual-model-configs | read | ai-gateway | Get virtual model config. |
| POST | ai-gateway/virtual-model-configs | write | ai-gateway | Create virtual model config. |
| PATCH | ai-gateway/virtual-model-configs | write | ai-gateway | Update virtual model config. |
| DELETE | ai-gateway/virtual-model-configs | write | ai-gateway | Delete virtual model config. |
| GET | ai-gateway/virtual-model-configs/list | read | ai-gateway | List virtual model configs. |
| GET | ai-gateway/virtual-model-configs/{id} | read | ai-gateway | Get virtual model config. |
| PATCH | ai-gateway/virtual-model-configs/{id} | write | ai-gateway | Update virtual model config. |
| DELETE | ai-gateway/virtual-model-configs/{id} | write | ai-gateway | Delete virtual model config. |
| GET | v1/ai-gateway/routers | read | ai-gateway | List AI Gateway routers. |
| PATCH | aliases/{id}/protection-bypass | write | aliases | Update the protection bypass for a URL. |
| DELETE | v2/aliases/{id} | write | aliases | Delete an Alias. |
| GET | v4/aliases | read | aliases | List aliases. |
| GET | v4/aliases/{id} | read | aliases | Get an Alias. |
| POST | api-keys | write | api-keys | createApiKeys. |
| PATCH | api-keys/{id}/quota | write | api-keys | Update an AI Gateway API key budget. |
| POST | v8/artifacts | write | artifacts | Query information about an artifact. |
| DELETE | v8/artifacts | write | artifacts | Delete all cache artifacts. |
| POST | v8/artifacts/events | write | artifacts | Record an artifacts cache usage event. |
| GET | v8/artifacts/status | read | artifacts | Get status of Remote Caching for this principal. |
| GET | v8/artifacts/{id} | read | artifacts | Download a cache artifact. |
| PUT | v8/artifacts/{id} | write | artifacts | Upload a cache artifact. |
| POST | v1/billing/buy | write | billing | Purchase credits. |
| GET | v1/billing/charges | read | billing | List FOCUS billing charges. |
| GET | v1/bulk-redirects | read | bulk-redirects | Gets project-level redirects. |
| PUT | v1/bulk-redirects | write | bulk-redirects | Stages new redirects for a project. |
| PATCH | v1/bulk-redirects | write | bulk-redirects | Edit a project-level redirect. |
| DELETE | v1/bulk-redirects | write | bulk-redirects | Delete project-level redirects. |
| POST | v1/bulk-redirects/restore | write | bulk-redirects | Restore staged project-level redirects to their production version. |
| GET | v1/bulk-redirects/versions | read | bulk-redirects | Get the version history for a project's redirects. |
| POST | v1/bulk-redirects/versions | write | bulk-redirects | Promote a staging version to production or restore a previous production version. |
| GET | v8/certs | read | certs | Get certs. |
| POST | v8/certs | write | certs | Issue a new cert. |
| PUT | v8/certs | write | certs | Upload a cert. |
| GET | v8/certs/{id} | read | certs | Get cert by id. |
| DELETE | v8/certs/{id} | write | certs | Remove cert. |
| POST | v1/connect/authorize/{id} | write | connect | Create a Connect authorization request. |
| POST | v1/connect/connectors | write | connect | Create a connector. |
| GET | v1/connect/connectors/{id} | read | connect | Get a connector. |
| DELETE | v1/connect/connectors/{id} | write | connect | Delete a connector. |
| POST | v1/connect/connectors/{id}/managed/eject | write | connect | Eject a managed connector. |
| GET | v1/connect/connectors/{id}/projects/{id} | read | connect | Get a connector project connection. |
| POST | v1/connect/connectors/{id}/projects/{id} | write | connect | Create or update a connector project connection. |
| DELETE | v1/connect/connectors/{id}/projects/{id} | write | connect | Disconnect a connector from a project. |
| DELETE | v1/connect/connectors/{id}/projects/{id}/environments/{id} | write | connect | Disconnect a connector from a project environment. |
| PATCH | v1/connect/connectors/{id}/trigger-destinations | write | connect | Update connector trigger destinations. |
| GET | v1/connect/networks | read | connect | List Secure Compute networks. |
| POST | v1/connect/networks | write | connect | Create a Secure Compute network. |
| GET | v1/connect/networks/{id} | read | connect | Read a Secure Compute network. |
| PATCH | v1/connect/networks/{id} | write | connect | Update a Secure Compute network. |
| DELETE | v1/connect/networks/{id} | write | connect | Delete a Secure Compute network. |
| POST | v1/connect/token/{id} | write | connect | Get a Connect token. |
| GET | v2/connect/connectors | read | connect | List connectors. |
| PATCH | v2/connect/connectors/{id} | write | connect | Update a connector. |
| GET | v2/connect/connectors/{id}/projects | read | connect | List projects for a connector. |
| GET | v2/connect/projects/{id}/connectors | read | connect | List connectors for a project. |
| GET | v1/deployments/{id}/checks | read | deployments | Retrieve a list of all checks. |
| POST | v1/deployments/{id}/checks | write | deployments | Creates a new Check. |
| GET | v1/deployments/{id}/checks/{id} | read | deployments | Get a single check. |
| PATCH | v1/deployments/{id}/checks/{id} | write | deployments | Update a check. |
| POST | v1/deployments/{id}/checks/{id}/rerequest | write | deployments | Rerequest a check. |
| GET | v1/deployments/{id}/feature-flags | read | deployments | Retrieve the feature flags of a deployment. |
| PATCH | v1/deployments/{id}/integrations/{id}/resources/{id}/actions/{id} | write | deployments | Update deployment integration action. |
| PATCH | v12/deployments/{id}/cancel | write | deployments | Cancel a deployment. |
| POST | v13/deployments | write | deployments | Create a new deployment. |
| GET | v13/deployments/{id} | read | deployments | Get a deployment by ID or URL. |
| DELETE | v13/deployments/{id} | write | deployments | Delete a Deployment. |
| GET | v2/deployments/{id}/aliases | read | deployments | List Deployment Aliases. |
| POST | v2/deployments/{id}/aliases | write | deployments | Assign an Alias. |
| GET | v2/deployments/{id}/check-runs | read | deployments | List check runs for a deployment. |
| POST | v2/deployments/{id}/check-runs | write | deployments | Create a check run. |
| GET | v2/deployments/{id}/check-runs/{id} | read | deployments | Get a check run. |
| PATCH | v2/deployments/{id}/check-runs/{id} | write | deployments | Update a check run. |
| GET | v3/deployments/{id}/events | read | deployments | Get deployment events. |
| GET | v6/deployments/{id}/files | read | deployments | List Deployment Files. |
| GET | v7/deployments | read | deployments | List deployments. |
| GET | v8/deployments/{id}/files/{id} | read | deployments | Get Deployment File Contents. |
| GET | domains/records/{id} | read | domains | getDomainsRecordsByRecordId. |
| PUT | domains/{id}/records | write | domains | replaceDomainsByDomainRecords. |
| PATCH | v1/domains/records/{id} | write | domains | Update an existing DNS record. |
| GET | v1/domains/{id}/project-domains | read | domains | List Project Domains by Apex Domain. |
| POST | v2/domains/{id}/records | write | domains | Create a DNS record. |
| DELETE | v2/domains/{id}/records/{id} | write | domains | Delete a DNS record. |
| PATCH | v3/domains/{id} | write | domains | Update or move apex domain. |
| GET | v5/domains | read | domains | List all the domains. |
| GET | v5/domains/{id} | read | domains | Get Information for a Single Domain. |
| GET | v5/domains/{id}/records | read | domains | List existing DNS records. |
| DELETE | v6/domains/{id} | write | domains | Remove a domain by name. |
| GET | v6/domains/{id}/config | read | domains | Get a Domain's configuration. |
| POST | v7/domains | write | domains | Add an existing domain to the Vercel platform. |
| POST | v9/domains/{id}/claim | write | domains | Claim Domain Ownership. |
| GET | v9/domains/{id}/verification | read | domains | Get Domain Verification Record. |
| GET | v1/drains | write | drains | Retrieve a list of all Drains. Kept out of read: returns drain secrets. |
| POST | v1/drains | write | drains | Create a new Drain. |
| POST | v1/drains/test | write | drains | Validate Drain delivery configuration. |
| GET | v1/drains/{id} | write | drains | Find a Drain by id. Kept out of read: returns drain secrets. |
| PATCH | v1/drains/{id} | write | drains | Update an existing Drain. |
| DELETE | v1/drains/{id} | write | drains | Delete a drain. |
| GET | v1/drives | read | drives | List drives. |
| GET | v1/drives/{id} | read | drives | Get a drive. |
| POST | v1/drives/{id} | write | drives | Get or create a drive. |
| DELETE | v1/drives/{id} | write | drives | Delete a drive. |
| POST | v1/drives/{id}/fork | write | drives | Fork a drive. |
| POST | v1/edge-cache/dangerously-delete-by-src-images | write | edge-cache | Dangerously delete by source image. |
| POST | v1/edge-cache/dangerously-delete-by-tags | write | edge-cache | Dangerously delete by tag. |
| POST | v1/edge-cache/invalidate-by-src-images | write | edge-cache | Invalidate by source image. |
| POST | v1/edge-cache/invalidate-by-tags | write | edge-cache | Invalidate by tag. |
| GET | v1/env | write | env | Lists all Shared Environment Variables for a team. Kept out of read: returns shared environment variable values. |
| POST | v1/env | write | env | Create one or more shared environment variables. |
| PATCH | v1/env | write | env | Updates one or more shared environment variables. |
| DELETE | v1/env | write | env | Delete one or more Env Var. |
| GET | v1/env/{id} | write | env | Retrieve the decrypted value of a Shared Environment Variable by id. Kept out of read: returns decrypted shared environment variable values. |
| PATCH | v1/env/{id}/unlink/{id} | write | env | Disconnects a shared environment variable for a given project. |
| GET | v1/events/types | read | events | List Event Types. |
| GET | v3/events | read | events | List User Events. |
| POST | v2/files | write | files | Upload Deployment Files. |
| GET | v1/global-config | read | global-config | Get Global Configs. |
| POST | v1/global-config | write | global-config | Create a Global Config. |
| GET | v1/global-config/{id} | read | global-config | Get a Global Config. |
| PUT | v1/global-config/{id} | write | global-config | Update a Global Config. |
| DELETE | v1/global-config/{id} | write | global-config | Delete a Global Config. |
| GET | v1/global-config/{id}/backups | read | global-config | Get Global Config backups. |
| GET | v1/global-config/{id}/backups/{id} | read | global-config | Get Global Config backup. |
| POST | v1/global-config/{id}/backups/{id}/restore | write | global-config | Restore Global Config backup. |
| GET | v1/global-config/{id}/item/{id} | read | global-config | Get a Global Config item. |
| GET | v1/global-config/{id}/items | read | global-config | Get Global Config items. |
| PATCH | v1/global-config/{id}/items | write | global-config | Update Global Config items in batch. |
| GET | v1/global-config/{id}/schema | read | global-config | Get Global Config schema. |
| POST | v1/global-config/{id}/schema | write | global-config | Update Global Config schema. |
| DELETE | v1/global-config/{id}/schema | write | global-config | Delete a Global Config's schema. |
| POST | v1/global-config/{id}/token | write | global-config | Create a Global Config token. |
| GET | v1/global-config/{id}/token/{id} | write | global-config | Get Global Config token meta data. Kept out of read: returns Edge Config tokens. |
| GET | v1/global-config/{id}/tokens | write | global-config | Get all tokens of a Global Config. Kept out of read: returns Edge Config tokens. |
| DELETE | v1/global-config/{id}/tokens | write | global-config | Delete one or more Global Config tokens. |
| PATCH | v1/installations/{id} | write | installations | Update Installation. |
| GET | v1/installations/{id}/account | read | installations | Get Account Information. |
| POST | v1/installations/{id}/billing | write | installations | Submit Billing Data. |
| POST | v1/installations/{id}/billing/balance | write | installations | Submit Prepayment Balances. |
| POST | v1/installations/{id}/billing/finalize | write | installations | Finalize Installation. |
| POST | v1/installations/{id}/billing/invoices | write | installations | Submit Invoice. |
| GET | v1/installations/{id}/billing/invoices/{id} | read | installations | Get Invoice. |
| POST | v1/installations/{id}/billing/invoices/{id}/actions | write | installations | Invoice Actions. |
| POST | v1/installations/{id}/credentials/revoke | write | installations | Revoke Installation Credential. |
| POST | v1/installations/{id}/credentials/rotate | write | installations | Rotate Installation Credential. |
| POST | v1/installations/{id}/events | write | installations | Create Event. |
| GET | v1/installations/{id}/member/{id} | read | installations | Get Member Information. |
| PUT | v1/installations/{id}/products/{id}/resources/{id}/secrets | write | installations | Deprecated: true. |
| GET | v1/installations/{id}/resources | read | installations | Get Integration Resources. |
| GET | v1/installations/{id}/resources/{id} | read | installations | Get Integration Resource. |
| PUT | v1/installations/{id}/resources/{id} | write | installations | Import Resource. |
| PATCH | v1/installations/{id}/resources/{id} | write | installations | Update Resource. |
| DELETE | v1/installations/{id}/resources/{id} | write | installations | Delete Integration Resource. |
| GET | v1/installations/{id}/resources/{id}/experimentation/global-config | read | installations | Get the data of a user-provided Global Config. |
| PUT | v1/installations/{id}/resources/{id}/experimentation/global-config | write | installations | Push data into a user-provided Global Config. |
| POST | v1/installations/{id}/resources/{id}/experimentation/items | write | installations | Create one or multiple experimentation items. |
| PATCH | v1/installations/{id}/resources/{id}/experimentation/items/{id} | write | installations | Patch an existing experimentation item. |
| DELETE | v1/installations/{id}/resources/{id}/experimentation/items/{id} | write | installations | Delete an existing experimentation item. |
| PUT | v1/installations/{id}/resources/{id}/secrets | write | installations | Update Resource Secrets. |
| GET | v1/integrations/configuration/{id} | read | integrations | Retrieve an integration configuration. |
| DELETE | v1/integrations/configuration/{id} | write | integrations | Delete an integration configuration. |
| GET | v1/integrations/configuration/{id}/products | read | integrations | List products for integration configuration. |
| GET | v1/integrations/configurations | read | integrations | Get configurations for the authenticated user or team. |
| GET | v1/integrations/git-namespaces | read | integrations | List git namespaces by provider. |
| POST | v1/integrations/installations/{id}/resources/{id}/connections | write | integrations | Connect integration resource to project. |
| GET | v1/integrations/integration/{id}/products/{id}/plans | read | integrations | List integration billing plans. |
| DELETE | v1/integrations/log-drains/{id} | write | integrations | Deletes the Integration log drain with the provided `id` (deprecated). |
| GET | v1/integrations/search-repo | read | integrations | List git repositories linked to namespace by provider. |
| POST | v1/integrations/sso/token | write | integrations | SSO Token Exchange. |
| GET | v2/integrations/log-drains | write | integrations | Retrieves a list of Integration log drains (deprecated). Kept out of read: returns log drain secrets. |
| POST | v2/integrations/log-drains | write | integrations | Creates a new Integration Log Drain (deprecated). |
| GET | v1/kms/issuers | read | kms | List issuers. |
| POST | v1/kms/issuers | write | kms | Create an issuer. |
| GET | v1/kms/issuers/{id} | read | kms | Get an issuer. |
| PATCH | v1/kms/issuers/{id} | write | kms | Update an issuer. |
| DELETE | v1/kms/issuers/{id} | write | kms | Delete an issuer. |
| POST | v1/kms/issuers/{id}/keys | write | kms | Create a signing key. |
| POST | v1/kms/issuers/{id}/keys/{id}/activate | write | kms | Activate a signing key. |
| POST | v1/kms/issuers/{id}/keys/{id}/revoke | write | kms | Revoke a signing key. |
| POST | v1/kms/issuers/{id}/policies | write | kms | Create an issuer policy. |
| PATCH | v1/kms/issuers/{id}/policies/{id}/{id} | write | kms | Update an issuer policy. |
| DELETE | v1/kms/issuers/{id}/policies/{id}/{id} | write | kms | Delete an issuer policy. |
| POST | v1/kms/issuers/{id}/sign/message | write | kms | Sign a message. |
| POST | v1/kms/issuers/{id}/sign/token | write | kms | Sign a token. |
| GET | v1/log-drains | write | log-drains | Retrieves a list of all the Log Drains (deprecated). Kept out of read: returns log drain secrets. |
| POST | v1/log-drains | write | log-drains | Creates a Configurable Log Drain (deprecated). |
| GET | v1/log-drains/{id} | write | log-drains | Retrieves a Configurable Log Drain (deprecated). Kept out of read: returns log drain secrets. |
| DELETE | v1/log-drains/{id} | write | log-drains | Deletes a Configurable Log Drain (deprecated). |
| POST | v1/microfrontends/group | write | microfrontends | Create a microfrontends group with applications. |
| GET | v1/microfrontends/groups | read | microfrontends | List microfrontends groups. |
| GET | v1/microfrontends/groups/{id}/projects | read | microfrontends | List projects in a microfrontends group. |
| GET | v1/microfrontends/projects/{id}/production-mfe-config | read | microfrontends | Get microfrontends config for a project. |
| GET | v1/microfrontends/{id}/config | read | microfrontends | Get microfrontends config for a deployment. |
| GET | v1/networking/privatelink/endpoints | read | networking | List PrivateLink endpoints. |
| POST | v1/networking/privatelink/endpoints | write | networking | Create a PrivateLink endpoint. |
| GET | v1/networking/privatelink/endpoints/{id} | read | networking | Read a PrivateLink endpoint. |
| PATCH | v1/networking/privatelink/endpoints/{id} | write | networking | Update a PrivateLink endpoint. |
| DELETE | v1/networking/privatelink/endpoints/{id} | write | networking | Delete a PrivateLink endpoint. |
| GET | v1/observability/manage/configuration/projects | read | observability | Lists disabled Observability Plus projects. |
| PUT | v1/observability/manage/configuration/projects/{id} | write | observability | Updates a disabled Observability Plus project setting. |
| POST | v2/observability/query | read | observability | createObservabilityQuery. |
| GET | v2/observability/schema | read | observability | getObservabilitySchema. |
| GET | v2/observability/schema/{id} | read | observability | getObservabilitySchemaByMetricId. |
| GET | v1/organizations | read | organizations | List Organizations. |
| POST | v1/organizations | write | organizations | Create an Organization. |
| GET | v1/organizations/{id} | read | organizations | Get an Organization. |
| PATCH | v1/organizations/{id} | write | organizations | Update an Organization. |
| GET | v1/organizations/{id}/dsync/groups | read | organizations | List Organization Directory Sync Groups. |
| GET | v1/organizations/{id}/dsync/groups/{id} | read | organizations | Get Organization Directory Sync Group. |
| PUT | v1/organizations/{id}/dsync/groups/{id} | write | organizations | Create or Replace Organization Directory Sync Group Configuration. |
| DELETE | v1/organizations/{id}/dsync/groups/{id} | write | organizations | Delete Organization Directory Sync Group Configuration. |
| GET | v1/organizations/{id}/teams | read | organizations | List Organization Teams. |
| POST | v1/organizations/{id}/teams | write | organizations | Create or Add Team to Organization. |
| DELETE | v1/organizations/{id}/teams/{id} | write | organizations | Delete Team from Organization. |
| PUT | v1/organizations/{id}/teams/{id}/dsync | write | organizations | Update Organization Team Directory Sync Mode. |
| PUT | projects/transfer-request/{id} | write | projects | Accept project transfer request. |
| POST | projects/{id}/transfer-request | write | projects | Create project transfer request. |
| GET | v1/projects/traces | read | projects | Get a project trace by request ID. |
| POST | v1/projects/traces/session | write | projects | Create a trace session token for a deployment. |
| POST | v1/projects/{id}/avatar | write | projects | Upload a project avatar. |
| DELETE | v1/projects/{id}/avatar | write | projects | Delete a project avatar. |
| GET | v1/projects/{id}/daemons | read | projects | Get project daemons. |
| PUT | v1/projects/{id}/daemons/{id}/instances | write | projects | Override a project daemon's instance counts. |
| POST | v1/projects/{id}/daemons/{id}/instances/{id}/restart | write | projects | Force restart a project daemon instance. |
| GET | v1/projects/{id}/deployments/{id}/runtime-logs | read | projects | Get logs for a deployment. |
| POST | v1/projects/{id}/domains/{id}/move | write | projects | Move a project domain. |
| DELETE | v1/projects/{id}/env | write | projects | Batch remove environment variables. |
| GET | v1/projects/{id}/env/{id} | write | projects | Retrieve the decrypted value of an environment variable of a project by id. Kept out of read: returns decrypted environment variable values. |
| GET | v1/projects/{id}/feature-flags/connections | read | projects | List flags project connections. |
| PUT | v1/projects/{id}/feature-flags/connections | write | projects | Connect a project to the flags of this project. |
| DELETE | v1/projects/{id}/feature-flags/connections/{id} | write | projects | Disconnect a project from the flags of this project. |
| GET | v1/projects/{id}/feature-flags/flags | read | projects | List flags. |
| PUT | v1/projects/{id}/feature-flags/flags | write | projects | Create a flag. |
| GET | v1/projects/{id}/feature-flags/flags/{id} | read | projects | Get a flag. |
| PATCH | v1/projects/{id}/feature-flags/flags/{id} | write | projects | Update a flag. |
| DELETE | v1/projects/{id}/feature-flags/flags/{id} | write | projects | Delete a flag. |
| GET | v1/projects/{id}/feature-flags/flags/{id}/versions | read | projects | List flag versions. |
| GET | v1/projects/{id}/feature-flags/labels | read | projects | List attribute labels. |
| GET | v1/projects/{id}/feature-flags/labels/counts | read | projects | List attribute label counts. |
| POST | v1/projects/{id}/feature-flags/labels/lookup | read | projects | Look up attribute labels. |
| POST | v1/projects/{id}/feature-flags/overrides/sign | write | projects | Sign flag overrides. |
| GET | v1/projects/{id}/feature-flags/sdk-keys | write | projects | Get all SDK keys. Kept out of read: returns SDK keys. |
| PUT | v1/projects/{id}/feature-flags/sdk-keys | write | projects | Create an SDK key. Kept out of read: returns SDK keys. |
| DELETE | v1/projects/{id}/feature-flags/sdk-keys/{id} | write | projects | Delete an SDK key. |
| GET | v1/projects/{id}/feature-flags/segments | read | projects | List segments. |
| PUT | v1/projects/{id}/feature-flags/segments | write | projects | Create a segment. |
| GET | v1/projects/{id}/feature-flags/segments/{id} | read | projects | Get a segment. |
| PATCH | v1/projects/{id}/feature-flags/segments/{id} | write | projects | Update a segment. |
| DELETE | v1/projects/{id}/feature-flags/segments/{id} | write | projects | Delete a segment. |
| GET | v1/projects/{id}/feature-flags/settings | read | projects | Get project flag settings. |
| PATCH | v1/projects/{id}/feature-flags/settings | write | projects | Update project flag settings. |
| GET | v1/projects/{id}/members | read | projects | List project members. |
| POST | v1/projects/{id}/members | write | projects | Adds a new member to a project. |
| DELETE | v1/projects/{id}/members/{id} | write | projects | Remove a Project Member. |
| PATCH | v1/projects/{id}/microfrontends | write | projects | Update the microfrontends settings. |
| POST | v1/projects/{id}/pause | write | projects | Pause a project. |
| GET | v1/projects/{id}/promote/aliases | read | projects | Gets a list of aliases with status for the current promote. |
| PATCH | v1/projects/{id}/protection-bypass | write | projects | Update Protection Bypass for Automation. |
| POST | v1/projects/{id}/rollback/{id} | write | projects | Point production traffic to a previous production deployment by ID. |
| PATCH | v1/projects/{id}/rollback/{id}/update-description | write | projects | Updates the description for a rollback. |
| GET | v1/projects/{id}/rolling-release | read | projects | Get the active rolling release information for a project. |
| POST | v1/projects/{id}/rolling-release/approve-stage | write | projects | Update the active rolling release to the next stage for a project. |
| GET | v1/projects/{id}/rolling-release/billing | read | projects | Get rolling release billing status. |
| POST | v1/projects/{id}/rolling-release/complete | write | projects | Complete the rolling release for the project. |
| GET | v1/projects/{id}/rolling-release/config | read | projects | Get rolling release configuration. |
| PATCH | v1/projects/{id}/rolling-release/config | write | projects | Update the rolling release settings for the project. |
| DELETE | v1/projects/{id}/rolling-release/config | write | projects | Delete rolling release configuration. |
| POST | v1/projects/{id}/rolling-release/start | write | projects | Start a rolling release for the project. |
| GET | v1/projects/{id}/routes | read | projects | Get project routing rules. |
| POST | v1/projects/{id}/routes | write | projects | Add a routing rule. |
| PUT | v1/projects/{id}/routes | write | projects | Stage routing rules. |
| DELETE | v1/projects/{id}/routes | write | projects | Delete routing rules. |
| POST | v1/projects/{id}/routes/generate | write | projects | Generate a routing rule from natural language. |
| GET | v1/projects/{id}/routes/versions | read | projects | Get routing rule version history. |
| POST | v1/projects/{id}/routes/versions | write | projects | Promote, restore, or discard a routing rule version. |
| PATCH | v1/projects/{id}/routes/{id} | write | projects | Edit a routing rule. |
| PATCH | v1/projects/{id}/shared-connect-links | write | projects | Configures Static IPs for a project. |
| POST | v1/projects/{id}/token | write | projects | Generate a project OIDC token. |
| POST | v1/projects/{id}/unpause | write | projects | Unpause a project. |
| GET | v10/projects | read | projects | Retrieve a list of projects. |
| POST | v10/projects/{id}/domains | write | projects | Add a domain to a project. |
| GET | v10/projects/{id}/env | write | projects | Retrieve the environment variables of a project by id or name. Kept out of read: returns environment variable values. |
| POST | v10/projects/{id}/env | write | projects | Create one or more environment variables. |
| POST | v10/projects/{id}/promote/{id} | write | projects | Point production traffic to a given deployment. |
| POST | v11/projects | write | projects | Create a new project. |
| GET | v2/projects/{id}/checks | read | projects | List all checks for a project. |
| POST | v2/projects/{id}/checks | write | projects | Create a check. |
| GET | v2/projects/{id}/checks/{id} | read | projects | Get a check. |
| PATCH | v2/projects/{id}/checks/{id} | write | projects | Update a check. |
| DELETE | v2/projects/{id}/checks/{id} | write | projects | Delete a check. |
| GET | v2/projects/{id}/checks/{id}/runs | read | projects | List runs for a check. |
| GET | v2/projects/{id}/feature-flags/flags | read | projects | List flags. |
| GET | v9/projects/{id} | read | projects | Find a project by id or name. |
| PATCH | v9/projects/{id} | write | projects | Update an existing project. |
| DELETE | v9/projects/{id} | write | projects | Delete a Project. |
| GET | v9/projects/{id}/custom-environments | read | projects | Retrieve custom environments. |
| POST | v9/projects/{id}/custom-environments | write | projects | Create a custom environment for the current project. |
| GET | v9/projects/{id}/custom-environments/{id} | read | projects | Retrieve a custom environment. |
| PATCH | v9/projects/{id}/custom-environments/{id} | write | projects | Update a custom environment. |
| DELETE | v9/projects/{id}/custom-environments/{id} | write | projects | Remove a custom environment. |
| GET | v9/projects/{id}/domains | read | projects | Retrieve project domains by project by id or name. |
| GET | v9/projects/{id}/domains/{id} | read | projects | Get a project domain. |
| PATCH | v9/projects/{id}/domains/{id} | write | projects | Update a project domain. |
| DELETE | v9/projects/{id}/domains/{id} | write | projects | Remove a domain from a project. |
| POST | v9/projects/{id}/domains/{id}/verify | write | projects | Verify project domain. |
| PATCH | v9/projects/{id}/env/{id} | write | projects | Edit an environment variable. |
| DELETE | v9/projects/{id}/env/{id} | write | projects | Remove an environment variable. |
| GET | v1/query/web-analytics/events/aggregate | read | query | Aggregates custom events. |
| GET | v1/query/web-analytics/events/count | read | query | Counts custom events. |
| GET | v1/query/web-analytics/visits/aggregate | read | query | Aggregates page views. |
| GET | v1/query/web-analytics/visits/count | read | query | Counts page views. |
| POST | v1/registrar/domains/availability | read | registrar | Get availability for multiple domains. |
| POST | v1/registrar/domains/buy | write | registrar | Buy multiple domains. |
| POST | v1/registrar/domains/price | read | registrar | Get price data for multiple domains. |
| POST | v1/registrar/domains/search | read | registrar | Get Domain Availability and Pricing. |
| GET | v1/registrar/domains/{id}/auth-code | write | registrar | Get the auth code for a domain. Kept out of read: returns the domain transfer auth code. |
| PATCH | v1/registrar/domains/{id}/auto-renew | write | registrar | Update auto-renew for a domain. |
| GET | v1/registrar/domains/{id}/availability | read | registrar | Get availability for a domain. |
| POST | v1/registrar/domains/{id}/buy | write | registrar | Buy a domain. |
| GET | v1/registrar/domains/{id}/contact-info/schema | read | registrar | Get contact info schema. |
| GET | v1/registrar/domains/{id}/contact-verification | read | registrar | Get contact verification status for a domain. |
| PATCH | v1/registrar/domains/{id}/nameservers | write | registrar | Update nameservers for a domain. |
| GET | v1/registrar/domains/{id}/price | read | registrar | Get price data for a domain. |
| POST | v1/registrar/domains/{id}/renew | write | registrar | Renew a domain. |
| GET | v1/registrar/domains/{id}/transfer | read | registrar | Get a domain's transfer status. |
| POST | v1/registrar/domains/{id}/transfer | write | registrar | Transfer-in a domain. |
| GET | v1/registrar/orders/{id} | read | registrar | Get a domain order. |
| GET | v1/registrar/tlds/supported | read | registrar | Get supported TLDs. |
| GET | v1/registrar/tlds/{id} | read | registrar | Get TLD. |
| GET | v1/registrar/tlds/{id}/price | read | registrar | Get TLD price data. |
| GET | v2/sandboxes | read | sandboxes | List sandboxes. |
| POST | v2/sandboxes | write | sandboxes | Create a named sandbox. |
| GET | v2/sandboxes/drives | read | sandboxes | Deprecated: Use GET /v1/drives. |
| GET | v2/sandboxes/drives/{id} | read | sandboxes | Deprecated: Use GET /v1/drives/:nameOrId. |
| POST | v2/sandboxes/drives/{id} | write | sandboxes | Deprecated: Use POST /v1/drives/:name. |
| DELETE | v2/sandboxes/drives/{id} | write | sandboxes | Deprecated: Use DELETE /v1/drives/:nameOrId. |
| POST | v2/sandboxes/drives/{id}/fork | write | sandboxes | Deprecated: Use POST /v1/drives/:name/fork. |
| GET | v2/sandboxes/sessions | read | sandboxes | List sessions. |
| GET | v2/sandboxes/sessions/{id} | read | sandboxes | Get a session. |
| GET | v2/sandboxes/sessions/{id}/cmd | read | sandboxes | List commands. |
| POST | v2/sandboxes/sessions/{id}/cmd | write | sandboxes | Execute a command. |
| GET | v2/sandboxes/sessions/{id}/cmd/{id} | read | sandboxes | Get a command. |
| POST | v2/sandboxes/sessions/{id}/cmd/{id}/kill | write | sandboxes | Kill a command. |
| GET | v2/sandboxes/sessions/{id}/cmd/{id}/logs | read | sandboxes | Stream command logs. |
| POST | v2/sandboxes/sessions/{id}/cmd/{id}/stdin | write | sandboxes | Write to command stdin. |
| POST | v2/sandboxes/sessions/{id}/extend-timeout | write | sandboxes | Extend session timeout. |
| POST | v2/sandboxes/sessions/{id}/fs/mkdir | write | sandboxes | Create a directory. |
| POST | v2/sandboxes/sessions/{id}/fs/read | write | sandboxes | Read a file. |
| POST | v2/sandboxes/sessions/{id}/fs/write | write | sandboxes | Write files. |
| POST | v2/sandboxes/sessions/{id}/network-policy | write | sandboxes | Update network policy. |
| POST | v2/sandboxes/sessions/{id}/snapshot | write | sandboxes | Create a snapshot. |
| POST | v2/sandboxes/sessions/{id}/stop | write | sandboxes | Stop a session. |
| GET | v2/sandboxes/snapshots | read | sandboxes | List snapshots. |
| GET | v2/sandboxes/snapshots/{id} | read | sandboxes | Get a snapshot. |
| DELETE | v2/sandboxes/snapshots/{id} | write | sandboxes | Delete a snapshot. |
| GET | v2/sandboxes/{id} | read | sandboxes | Get a named sandbox. |
| PATCH | v2/sandboxes/{id} | write | sandboxes | Update a sandbox. |
| DELETE | v2/sandboxes/{id} | write | sandboxes | Delete a sandbox. |
| POST | v2/sandboxes/{id}/fork | write | sandboxes | Fork a named sandbox. |
| POST | v3/sandboxes | write | sandboxes | Create a named sandbox. |
| POST | v3/sandboxes/sessions/{id}/snapshot | write | sandboxes | Create a snapshot. |
| POST | v3/sandboxes/{id}/fork | write | sandboxes | Fork a named sandbox. |
| POST | v4/sandboxes | write | sandboxes | Create a named sandbox. |
| POST | v1/security/attack-mode | write | security | Update Attack Challenge mode. |
| GET | v1/security/firewall/attack-status | read | security | Read active attack data. |
| GET | v1/security/firewall/bypass | read | security | Read System Bypass. |
| POST | v1/security/firewall/bypass | write | security | Create System Bypass Rule. |
| DELETE | v1/security/firewall/bypass | write | security | Remove System Bypass Rule. |
| GET | v1/security/firewall/bypass/rules | read | security | Get conditional firewall bypasses. |
| POST | v1/security/firewall/bypass/rules | write | security | Create conditional firewall bypass. |
| PUT | v1/security/firewall/bypass/rules | write | security | Update conditional firewall bypass. |
| DELETE | v1/security/firewall/bypass/rules | write | security | Delete conditional firewall bypass. |
| GET | v1/security/firewall/config | read | security | Returns activated WAF config. |
| PUT | v1/security/firewall/config | write | security | Put Firewall Configuration. |
| PATCH | v1/security/firewall/config | write | security | Update Firewall Configuration. |
| POST | v1/security/firewall/config/generate-rule | write | security | Generate a firewall rule from natural language. |
| GET | v1/security/firewall/config/{id} | read | security | Read Firewall Configuration. |
| DELETE | v1/security/firewall/config/{id} | write | security | Returns activated WAF config. |
| POST | v1/security/firewall/config/{id}/activate | write | security | Returns activated WAF config. |
| GET | v1/security/firewall/events | read | security | Read Firewall Actions by Project. |
| GET | v1/security/firewall/events/summary | read | security | Read Firewall Actions Summary by Project. |
| POST | speed-insights/toggle | write | speed-insights | createSpeedInsightsToggle. |
| POST | storage/stores/blob | write | storage | Create a Blob store. |
| DELETE | storage/stores/blob/{id} | write | storage | Delete a Blob store. |
| GET | storage/stores/{id} | read | storage | Get a store. |
| POST | v1/storage/stores/integration/direct | write | storage | Create integration store (free and paid plans). |
| POST | v1/teams | write | teams | Create a Team. |
| DELETE | v1/teams/{id} | write | teams | Delete a Team. |
| POST | v1/teams/{id}/dsync-roles | write | teams | Update Team Directory Sync Role Mappings. |
| GET | v1/teams/{id}/feature-flags/flags | read | teams | List all flags for a team. |
| GET | v1/teams/{id}/feature-flags/settings | read | teams | List team project flag settings. |
| DELETE | v1/teams/{id}/invites/{id} | write | teams | Delete a Team invite code. |
| POST | v1/teams/{id}/members/teams/join | write | teams | Join a team. |
| PATCH | v1/teams/{id}/members/{id} | write | teams | Update a Team Member. |
| DELETE | v1/teams/{id}/members/{id} | write | teams | Remove a Team Member. |
| PATCH | v1/teams/{id}/microfrontends/{id} | write | teams | Update a microfrontends group. |
| DELETE | v1/teams/{id}/microfrontends/{id} | write | teams | Delete a microfrontends group. |
| POST | v1/teams/{id}/request | write | teams | Request access to a team. |
| GET | v1/teams/{id}/request/{id} | read | teams | Get access request status. |
| GET | v2/teams | read | teams | List all teams. |
| GET | v2/teams/{id} | read | teams | Get a Team. |
| PATCH | v2/teams/{id} | write | teams | Update a Team. |
| GET | v2/teams/{id}/feature-flags/flags | read | teams | List all flags for a team. |
| POST | v2/teams/{id}/members | write | teams | Invite a user. |
| GET | v3/teams/{id}/members | read | teams | List team members. |
| DELETE | v1/user | write | user | Delete User Account. |
| GET | v2/user | read | user | Get the User. |
| POST | v3/user/tokens | write | user | Create an Auth Token. |
| DELETE | v3/user/tokens/{id} | write | user | Delete an authentication token. |
| GET | v5/user/tokens/{id} | read | user | Get Auth Token Metadata. |
| GET | v6/user/tokens | read | user | List Auth Tokens. |
| GET | v1/vcr/repository | read | vcr | List repositories. |
| POST | v1/vcr/repository | write | vcr | Create a repository. |
| GET | v1/vcr/repository/{id} | read | vcr | Get a repository. |
| DELETE | v1/vcr/repository/{id} | write | vcr | Delete a repository. |
| GET | v1/vcr/repository/{id}/images | read | vcr | List repository images. |
| GET | v1/vcr/repository/{id}/images/{id} | read | vcr | Get a repository image. |
| DELETE | v1/vcr/repository/{id}/images/{id} | write | vcr | Delete a repository image. |
| GET | v1/vcr/repository/{id}/permissions | read | vcr | List repository permissions. |
| POST | v1/vcr/repository/{id}/permissions | write | vcr | Add a repository permission. |
| DELETE | v1/vcr/repository/{id}/permissions | write | vcr | Remove a repository permission. |
| DELETE | v1/vcr/repository/{id}/permissions/all | write | vcr | Clear all repository permissions. |
| GET | v1/vcr/repository/{id}/tags | read | vcr | List repository tags. |
| GET | v1/vcr/repository/{id}/tags/{id} | read | vcr | Get a repository tag. |
| GET | v1/vercel-ci/invocations/{id}/attempts | read | vercel-ci | List all attempts for an invocation. |
| GET | v1/vercel-ci/invocations/{id}/attempts/{id} | read | vercel-ci | Get a specific invocation attempt. |
| GET | v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions | read | vercel-ci | List job definitions for an invocation attempt. |
| GET | v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id} | read | vercel-ci | Get a specific job definition. |
| GET | v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}/runs | read | vercel-ci | List all runs for a job definition. |
| GET | v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}/runs/{id} | read | vercel-ci | Get a specific job run attempt. |
| GET | v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}/runs/{id}/logs | read | vercel-ci | Get log lines for a specific job run attempt. |
| GET | v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}/runs/{id}/task-definitions | read | vercel-ci | List all task definitions for a job run. |
| GET | v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}/runs/{id}/task-definitions/{id}/runs/{id}/logs | read | vercel-ci | Get log lines for a specific task run attempt. |
| GET | v1/vercel-ci/invocations/{id}/attempts/{id}/job-definitions/{id}/runs/{id}/task-runs | read | vercel-ci | List task runs for a job run. |
| GET | v1/vercel-ci/invocations/{id}/attempts/{id}/logs | read | vercel-ci | Get log lines for an invocation attempt. |
| POST | v1/vercel-ci/invocations/{id}/attempts/{id}/retry | write | vercel-ci | Retry a terminal Vercel CI invocation attempt. |
| GET | v1/vercel-ci/invocations/{id}/attempts/{id}/task-logs | read | vercel-ci | Get log lines for the tasks of an invocation attempt. |
| GET | v1/vercel-ci/invocations/{id}/tree | read | vercel-ci | Get an invocation with its jobs and tasks. |
| GET | v1/vercel-ci/log-search | read | vercel-ci | Search the setup and task logs of several invocation attempts. |
| GET | v1/vercel-ci/repository-settings | read | vercel-ci | Get Vercel CI settings for a connected repository. |
| PATCH | v1/vercel-ci/repository-settings | write | vercel-ci | Enable or disable Vercel CI for a connected repository. |
| POST | v1/vercel-ci/task-analyses | write | vercel-ci | Start an asynchronous Vercel CI task analysis. |
| GET | v1/vercel-ci/task-analyses/{id} | read | vercel-ci | Get the current status of a Vercel CI task analysis. |
| POST | v1/vercel-ci/task-analyses/{id}/pull-request | write | vercel-ci | Create a GitHub pull request that adds Vercel CI tags for the completed analysis. |
| GET | v1/vercel-ci/task-analyses/{id}/tasks | read | vercel-ci | List discovered tasks for a completed Vercel CI task analysis. |
| GET | v2/vercel-ci/branches | read | vercel-ci | List Vercel CI branch suggestions for a team. |
| GET | v2/vercel-ci/invocations | read | vercel-ci | List invocations for a team, optionally filtered by repository and invocation metadata. |
| POST | web/insights/toggle | write | web | createWebInsightsToggle. |
| GET | v1/webhooks | read | webhooks | Get a list of webhooks. |
| POST | v1/webhooks | write | webhooks | Creates a webhook. |
| GET | v1/webhooks/{id} | read | webhooks | Get a webhook. |
| DELETE | v1/webhooks/{id} | write | webhooks | Deletes a webhook. |
