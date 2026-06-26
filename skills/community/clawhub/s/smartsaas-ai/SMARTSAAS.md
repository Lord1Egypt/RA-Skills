# SmartSaaS

![SmartSaaS Logo](assets/ss-logo.jpeg)

SmartSaaS is the backend this skill connects to. Use the SmartSaaS skill when the user asks to manage **datasets**, **projects**, **work packages**, **tasks**, **team members**, **integrations**, **core user tasks**, **knowledge & research**, **campaigns**, **email templates**, **website (webpage) templates**, or **events / cron** (dispatch to OpenClaw webhook).

## What this skill does

- **Knowledge & research**: List knowledge (paginated), get one article by id, create knowledge articles, post research (saved as knowledge). Permissions: knowledge:read, knowledge:write.
- **Data**: Create datasets (folders), add items, list datasets. Request shapes follow **smartsaas-backend/src/schema/** (Data.mjs, DataContent.mjs). Datasets that will hold content **must have a dataSchema**; see repo [SCHEMA_REQUIREMENTS.md](../../SCHEMA_REQUIREMENTS.md).
- **Projects**: Create projects, list projects
- **Work packages & tasks**: Create work packages under a project; create tasks under a work package; assign tasks to users
- **Team**: Add team members to a project
- **Integrations**: List/remove user integrations; sync Shopify products; pull/push products to integrations; get product sync status and available integrations
- **Core tasks**: Refresh user, get data/project favourites, user companies, users list, user hierarchy, calendar schema and content
- **Campaigns**: List active campaigns, create campaign, start campaign
- **Email templates**: List, create, update email templates; send test email
- **Website templates**: List, create, update webpage templates
- **Events & webhook**: Dispatch payloads to `{base}/api/protected/openclaw/webhook`; post events (e.g. cron); configure cron/schedule jobs

## Schema chain (retrieve schema before posting)

Before any **create** or **POST**, run **`./scripts/get-schema.sh <resource>`** to get the expected request shape. Resources: `dataset`, `data-item`, `project`, `work-package`, `task`, `campaign`, `email-template`, `webpage-template`. Use the JSON output (fields, endpoint, createScript) to build the request body, then run the create script. This ensures posts match backend expectations.

## How to run it

1. Ensure `SMARTSAAS_BASE_URL` and `SMARTSAAS_API_KEY` are set (e.g. in OpenClaw skill config or env).
2. Run the scripts in `scripts/` via **execute_shell** from this skill directory. Examples:
   - Get schema first: `./scripts/get-schema.sh dataset` then build body and run create.
   - Create dataset: `./scripts/create-dataset.sh "My Dataset"`
   - List datasets: `./scripts/list-datasets.sh`
   - Create project: `./scripts/create-project.sh "Project Name" "Optional description"`
   - List projects: `./scripts/list-projects.sh`
   - Create work package: `./scripts/create-work-package.sh "<projectId>" "WP Name"`
   - Create task: `./scripts/create-task.sh "<projectId>" "<workPackageId>" "Task title"`
   - Assign task: `./scripts/assign-task.sh "<projectId>" "<taskId>" "<userId>"`
   - Add team member: `./scripts/add-team-member.sh "<projectId>" "<userId>"`
   - List integrations: `./scripts/list-integrations.sh`
   - Sync Shopify: `./scripts/sync-shopify-products.sh`
   - Refresh user: `./scripts/refresh-user.sh`
   - Get calendar: `./scripts/get-calendar-content.sh "2025-03-15"`
   - List knowledge: `./scripts/list-knowledge.sh` or `./scripts/list-knowledge.sh 1 10 createdAt desc`; get one: `./scripts/get-knowledge.sh "<id>"`; create: `./scripts/create-knowledge.sh '{"title":"My article","content":"..."}'`; post research: `./scripts/post-research.sh '{"title":"Market study","findings":"..."}'`
   - List campaigns: `./scripts/list-active-campaigns.sh`
   - Start campaign: `./scripts/start-campaign.sh "<campaignId>"`
   - Create email template: `./scripts/create-email-template.sh '{"title":"...","subject":"...","content":"..."}'`
   - Create webpage template: `./scripts/create-webpage-template.sh '{"title":"...","description":"..."}'`
   - Send test email: `./scripts/send-test-email.sh "<templateId>" "email@example.com"`
   - Dispatch webhook: `./scripts/dispatch-openclaw-webhook.sh` or `./scripts/dispatch-openclaw-webhook.sh '{"event":"cron"}'`
   - Post event: `./scripts/post-openclaw-event.sh cron '{"schedule":"daily"}'`
   - Configure cron: `./scripts/configure-openclaw-cron.sh '{"schedule":"0 9 * * *","payload":{},"enabled":true}'`

## Script reference

### Data & projects

| Script | Arguments |
|--------|-----------|
| `get-schema.sh` | `<resource>` — run first to get expected POST shape (dataset, data-item, project, work-package, task, campaign, email-template, webpage-template). No arg = list. |
| `create-dataset.sh` | `dataTitle` [parentId] [bodyJson] — shape from Data.mjs; use dataSchema to add content |
| `add-to-dataset.sh` | `folderId` `itemJson` (data per DataContent.mjs) |
| `get-data-content.sh` | `folderId` [type] — get dataset + items (type: document \| invoice \| omit) |
| `list-datasets.sh` | [parentId] |
| `create-project.sh` | `title` [description] — Projects.mjs |
| `list-projects.sh` | — |
| `create-work-package.sh` | `projectId` `work_package_title` [description] — Projects.mjs |
| `create-task.sh` | `projectId` `workPackageId` `task_title` [description] — Projects.mjs TaskSchema |
| `assign-task.sh` | `projectId` `taskId` [assignedTo] |
| `add-team-member.sh` | `projectId` `userId` [role] |

### Integrations (sync with user integrations)

| Script | Arguments |
|--------|-----------|
| `list-integrations.sh` | — |
| `remove-integration.sh` | `integration` (e.g. gmail, shopify) |
| `sync-shopify-products.sh` | — |
| `get-product-sync-status.sh` | `dataId` |
| `pull-products-from-integration.sh` | `dataId` `integrationType` |
| `push-products-to-integration.sh` | `dataId` `integrationType` |
| `get-available-integrations.sh` | — |

### Core tasks

| Script | Arguments |
|--------|-----------|
| `refresh-user.sh` | — |
| `get-data-favourites.sh` | — |
| `get-project-favourites.sh` | — |
| `get-user-companies.sh` | — |
| `get-users.sh` | [page] [pageSize] |
| `get-user-hierarchy.sh` | — |
| `get-calendar-schema.sh` | — |
| `get-calendar-content.sh` | `date` (e.g. 2025-03-15) |

### Knowledge & research

| Script | Arguments |
|--------|-----------|
| `list-knowledge.sh` | [page] [limit] [sortBy] [sortOrder] — GET /api/protected/knowledge. knowledge:read. |
| `get-knowledge.sh` | `id` — GET /api/protected/knowledge/:id. knowledge:read. |
| `create-knowledge.sh` | `articleJson` (title, content, featuredImage, …). knowledge:write. |
| `post-research.sh` | `researchJson` (title, findings/content/summary, source, url). Saves as knowledge. knowledge:write. |

### Campaigns

| Script | Arguments |
|--------|-----------|
| `list-active-campaigns.sh` | — |
| `create-campaign.sh` | `campaignJson` [userId] — SalesSchemas/Campaign.mjs |
| `start-campaign.sh` | `campaignId` |

### Email templates

| Script | Arguments |
|--------|-----------|
| `list-email-templates.sh` | — |
| `create-email-template.sh` | `templateJson` — TemplateModels/Email.mjs |
| `update-email-template.sh` | `templateJson` (_id + fields) |
| `send-test-email.sh` | `templateId` `toEmail` [subject] |

### Website (webpage) templates

| Script | Arguments |
|--------|-----------|
| `list-webpage-templates.sh` | — |
| `create-webpage-template.sh` | `templateJson` — TemplateModels/Webpage.mjs |
| `update-webpage-template.sh` | `templateJson` (_id + fields) |

### Events & webhook (cron, dispatch)

| Script | Arguments |
|--------|-----------|
| `dispatch-openclaw-webhook.sh` | [jsonPayload] — POST to `/api/protected/openclaw/webhook` |
| `post-openclaw-event.sh` | `eventType` [jsonPayload] |
| `configure-openclaw-cron.sh` | `configJson` (schedule, payload, enabled, etc.) |

Webhook URL: `{SMARTSAAS_BASE_URL}/api/protected/openclaw/webhook`.

The API key is created in SmartSaaS (APIScreen) with permissions such as `data:read`, `data:write`, `projects:read`, `projects:write`. Do not log or echo the API key.
