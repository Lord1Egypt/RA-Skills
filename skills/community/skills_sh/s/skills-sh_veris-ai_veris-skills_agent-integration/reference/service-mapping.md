# Veris Service Mapping Reference

Map real-world dependencies to the current canonical Veris service names.

Use this file when deciding what to put in `services:` and when migrating stale config that still uses old aliases like `crm`, `calendar`, or `oracle`.

## Canonical service names

| Real service | Canonical Veris service | Common detection signals |
| --- | --- | --- |
| Salesforce | `salesforce` | `simple-salesforce`, `salesforce-bulk`, `SALESFORCE_*`, `SFDC_*` |
| Google Calendar | `google/calendar` | `google-api-python-client`, calendar scopes, `GOOGLE_CALENDAR_*`, `GOOGLE_APPLICATION_CREDENTIALS` |
| PostgreSQL | `postgres` | `psycopg2`, `asyncpg`, `sqlalchemy`, `pg`, Prisma, `DATABASE_URL`, `POSTGRES_*` |
| Oracle Fusion Cloud | `oracle/fscm` | `ORACLE_*`, `FUSION_*` |
| Jira Cloud | `atlassian/jira` | `jira`, `atlassian-python-api`, `jira-client`, `JIRA_*`, `ATLASSIAN_*` |
| Confluence | `atlassian/confluence` | `atlassian-python-api`, `CONFLUENCE_*` |
| Stripe (MCP) | `mcp/stripe` | `stripe`, `STRIPE_*`, `mcp.stripe.com` |
| Shopify Storefront (MCP) | `mcp/shopify-storefront` | `SHOPIFY_*`, storefront APIs |
| Shopify Customer (MCP) | `mcp/shopify-customer` | customer account APIs, `account.myshopify.com` |
| Slack | `slack` | `slack_sdk`, `slack_bolt`, `@slack/web-api`, `SLACK_*` |
| Zendesk | `zendesk-support` | `zendesk`, `ZENDESK_*`, `*.zendesk.com` |
| Twilio | `twilio` | `twilio`, `TWILIO_*`, `api.twilio.com` |
| Microsoft Graph | `microsoft/graph` | `msgraph`, `O365`, `GRAPH_*`, `graph.microsoft.com` |
| Azure DevOps | `microsoft/devops` | `azure-devops`, `AZDO_*`, `dev.azure.com` |
| Google Drive | `google/drive` | drive scopes, `drive.googleapis.com` |
| HubSpot | `hubspot` | `hubspot-api-client`, `HUBSPOT_*`, `api.hubapi.com` |
| PagerDuty | `pagerduty` | `pagerduty`, `PAGERDUTY_*`, `api.pagerduty.com` |
| ServiceNow | `servicenow` | `SERVICENOW_*`, `*.service-now.com` |
| Epic / FHIR | `epic/fhir` | `fhirclient`, `EPIC_*`, `FHIR_*` |
| Splunk | `splunk` | `splunk-sdk`, `SPLUNK_*`, `*.splunkcloud.com` |
| Elastic / Elasticsearch | `elastic` | `elasticsearch`, `elastic-transport`, `ELASTIC_*`, `*.elastic-cloud.com` |
| Close CRM | `close` | `closeio`, `CLOSE_*`, `api.close.com` |
| SWIFT | `swift` | `SWIFT_*`, `api.swift.com` |
| OpenSanctions | `opensanctions` | `opensanctions`, `api.opensanctions.org` |
| You.com search | `you` | `YOU_*`, `api.you.com`, `ydc-index.io` |
| QuickBooks Online | `intuit/quickbooks-online` | `quickbooks`, `INTUIT_*`, `quickbooks.api.intuit.com` |
| Google Docs | `google/docs` | docs scopes, `docs.googleapis.com` |
| Zillow / Bridge | `zillow` | `api.bridgedataoutput.com`, real-estate MLS APIs |

## Protocol and transport limitations

Some services support multiple protocol variants in production. The Veris mock may only support one. When integrating, confirm the agent uses the supported variant.

| Service | Supported protocol | Not supported | Migration notes |
| --- | --- | --- | --- |
| Slack | HTTP Events API (Web API calls over HTTPS) | Socket Mode (WebSocket via `SLACK_APP_TOKEN`) | Reconfigure the agent to HTTP mode. Set `SLACK_SIGNING_SECRET` instead of `SLACK_APP_TOKEN`. Handler code typically needs only minor changes (switch `SocketModeHandler` to HTTP adapter). |
| Twilio | REST API (HTTP) | WebSocket media streams | Agents processing real-time voice via Twilio WS streams cannot use the mock. Keep Twilio external or use a function channel to bypass the voice path. |

**General rule:** If a service has multiple transport modes (HTTP vs WebSocket, polling vs streaming, REST vs GraphQL), check which one the Veris mock implements. When the agent uses an unsupported mode, either reconfigure the agent to use the supported mode or classify the dependency as "external."

## Legacy aliases to migrate away from

| Old alias | Current canonical name |
| --- | --- |
| `crm` | `salesforce` |
| `calendar` | `google/calendar` |
| `oracle` | `oracle/fscm` |

If you see these old names in existing `.veris/veris.yaml`, migrate them to the current canonical names.

## Auth helpers

These are platform-level helpers and usually should not be added manually:

- `google/auth`
- `microsoft/auth`
- `atlassian/auth`
- `intuit/auth`

If the main namespace service is active, Veris handles these helpers automatically where needed.

## Email service

`email` is special:
- it is usually auto-injected when the actor uses an email channel
- you generally do not add it manually unless you have a specific reason

## LLM providers

Do not add a service entry for OpenAI, Anthropic, Azure OpenAI, Google AI, Mistral, Groq, DeepSeek, Together, Fireworks, or Cohere.

The LLM proxy intercepts supported provider domains automatically.

## Choosing between mock, bundle, and external

Use this mapping only to answer "does Veris have a mock for this?" It does not decide whether the service is:

- required on the critical path
- safe to skip
- better bundled locally
- better kept external

You still need to read the source code and classify the dependency honestly.
