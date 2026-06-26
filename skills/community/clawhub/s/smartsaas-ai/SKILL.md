---
name: smartsaas
description: "Install via extraDirs (not clawhub). Never auto-add items: only add when user explicitly asks; user defines what to add. Scripts: create-dataset.sh, add-to-dataset.sh (positional only, no --name/--dataset). Run via execute_shell; never curl. Env: SMARTSAAS_BASE_URL, SMARTSAAS_API_KEY."
---

# SmartSaaS Skill

**When the user asks how to install or to install the smartsaas skill:** Do NOT run or suggest `clawhub install smartsaas` or `pwd` then clawhub install. This skill is not installed via clawhub. Tell the user: (1) Add the path to this repo's `skills` folder to `skills.load.extraDirs` in `~/.openclaw/openclaw.json`. (2) Set `skills.entries.smartsaas.env` with `SMARTSAAS_BASE_URL` and `SMARTSAAS_API_KEY`. (3) Restart OpenClaw. The skill is then loaded from that path. Do not run clawhub.

**Create dataset + add items — WRONG vs RIGHT (no flags, use schema):**
- **WRONG:** `create-dataset.sh --name smartsaas-home` (no `--name`; first arg is the title; dataset ends up with wrong title and empty schema). **WRONG:** `add-to-dataset.sh --dataset <id> --name "Investor 1" --location "London"` (no `--dataset`/`--name`/`--location`).
- **RIGHT create:** `create-dataset.sh "investor-list" "" '{"dataTitle":"investor-list","dataSchema":{"fields":[{"name":"name","type":"string"},{"name":"notes","type":"string"}]}}'` — **Arg1 is always the dataset title** (e.g. "investor-list"); the script sends it as dataTitle so the folder is never "untitled_folder". Arg2 = **""** for no parent. Arg3 = full JSON with dataTitle and dataSchema.fields.
- **RIGHT add:** `add-to-dataset.sh 69b66368aa4e413d0ab084b7 '{"Name":"Investor 1","City":"London"}'` — first arg = folder _id, second arg = **one JSON object** whose keys match the dataset's dataSchema (e.g. Name, City). No flags. The script sends it as the request body `{"data": <that object>}`. One call per item.

**Add-item shape:** The second argument to add-to-dataset.sh is the **item content object** (keys = field names from the dataset's dataSchema). **Before adding items**, run `get-dataset.sh <folderId>` to get the folder's dataSchema and use it to build itemJson. Example: if dataSchema has `name`, `notes`, use `'{"name":"John","notes":"Investor"}'`. The script wraps it in `{"data": ...}` for the API. No flags.

**Do NOT auto-add items.** Only add items when the user **explicitly asks** to add specific items. If the user only asked to create a dataset (e.g. "create a dataset called X"), create it and stop — do not proceed to add items or suggest "shall I add investors?" or add example data. The **user** defines what to add (if anything). "Investor-list" / "investors from London" in this doc are syntax examples only, not a directive to add that content.

## Skill summary (for explain / reference)

**What it does:** Interact with SmartSaaS via shell scripts: create datasets, add items, manage projects/tasks, knowledge, campaigns, templates, webhooks. Run scripts with **execute_shell**; do not run or show curl. Do not ask for an API token — the key is in the environment.

**Environment:** Scripts read **`SMARTSAAS_BASE_URL`** and **`SMARTSAAS_API_KEY`** (not `SMARTSAAS_API_TOKEN`). Both are required; set in OpenClaw config or system env. Never ask the user to provide the key in chat.

**Scripts (positional args only — no `--name`, `--dataset`, `--location`):**
- **create-dataset.sh** — Arg1: dataTitle. Arg2: use **""** for no parent (not the word "parentId"). Arg3: bodyJson with **dataTitle** and **dataSchema: {"fields":[...]}** (dataSchema must be object with "fields", not a string). Example: `create-dataset.sh "investor-list" "" '{"dataTitle":"investor-list","dataSchema":{"fields":[{"name":"Name","type":"string"},{"name":"City","type":"string"}]}}'`
- **add-to-dataset.sh** — `add-to-dataset.sh <folderId> '<itemJson>'`. No flags. itemJson = one object with keys matching the dataset's dataSchema (script sends body `{"data": itemJson}`). Example: `add-to-dataset.sh 507f1f77bcf86cd799439011 '{"Name":"John Doe","City":"London"}'`

**Example flow:** (1) Run create-dataset.sh with dataTitle and dataSchema. (2) From the response, take the top-level `_id`. (3) Only if the user asked to add items: run **get-dataset.sh** <folderId> to get dataSchema, then run add-to-dataset.sh with that _id and each item (itemJson keys match dataSchema.fields). Scripts in `skills/smartsaas/scripts/`; use full path if needed.

**Is the skill installed?** This skill is loaded from **extraDirs** (local path in openclaw.json). Do **NOT** suggest `clawhub install smartsaas` when scripts or `ls skills/` appear missing — the shell CWD is often not the repo root. **Still run the scripts** using the **full path** (e.g. `<workspace_root>/skills/smartsaas/scripts/create-dataset.sh`). Do not conclude "skill not installed" and suggest clawhub install.

**When the user asks to create a dataset:** If they only asked to create (e.g. "create a dataset called X"), run create-dataset.sh and stop; do not add items unless they explicitly asked to add something. If they asked to create and add items, only add what they specified — the user defines what to add (if anything). Do NOT reply with "we need your API token". Do NOT output curl. Run scripts via execute_shell; the key is in the environment.

**NEVER ask for "API token" or "YOUR_API_TOKEN". NEVER output curl or api.smartsaas.co.uk. ONLY run the scripts via execute_shell. The key is in env.**

**MANDATORY — read first.** You must NOT: use curl; use api.smartsaas.co.uk or api.smartsaas.com; send body `{"name":"investor-list"}` (API expects dataTitle + dataSchema); ask the user for "API token" or "YOUR_API_TOKEN". The only way to create a dataset and add items is to call **execute_shell** with the scripts: create-dataset.sh (args: title, "", bodyJson with dataTitle+dataSchema), then add-to-dataset.sh (args: the _id from the create response, itemJson). Base URL and API key come from env (openclaw.json); never ask for them in chat.

---

**Quick reference (32k window: read this first)**  
**Installation:** This skill is loaded **locally** via extraDirs in openclaw.json (this repo’s `skills` folder). **Never** run `clawhub install smartsaas` . If `ls skills/` shows nothing or scripts are "not found", do NOT suggest clawhub install; use the **full path** to the script (e.g. <workspace_root>/skills/smartsaas/scripts/create-dataset.sh) or run from workspace root. Do NOT search the web for SmartSaaS API docs.

You MUST run the **scripts** via **execute_shell** — do NOT run or output curl. Do NOT put the API key in chat. Scripts need env: SMARTSAAS_BASE_URL, SMARTSAAS_API_KEY (openclaw.json or system env). Wrong: curl, body {\"name\":\"...\"}, /folders/investor-list/items (use folder _id). Right: (1) create-dataset.sh "title" "" '{"dataTitle":"...","dataSchema":{...}}' — no --name (2) get _id (3) only if user asked to add items: add-to-dataset.sh <_id> '<itemJson>' — no --dataset/--name/--location. Do NOT auto-add items; user defines what to add.

---

Use this skill when the user asks to create or list datasets, create projects, work packages, tasks, assign tasks, add team members, sync or manage integrations, refresh user data, get favourites, companies, users, calendar, **research knowledge** (list/get/create knowledge articles, post research saved as knowledge), **look up data entries** (contacts, investors, companies, etc.) to add to datasets — find or validate entries then add via add-to-dataset.sh — start or create campaigns, create or update email templates, create or update website (webpage) templates, post events / configure cron jobs and dispatch to the SmartSaaS OpenClaw webhook.

**Never ask the user for an API key.** The scripts read `SMARTSAAS_BASE_URL` and `SMARTSAAS_API_KEY` from the **environment**. If a script fails with "must be set", tell the user to set these in OpenClaw config or in the system env (see **Environment** below) — not to paste the key in chat.

**You have direct access to the API via the scripts.** Do NOT say "we don't have direct access" or "I will provide you with the API calls". You MUST run the shell scripts yourself via execute_shell. Do NOT output curl for the user to run.

**Wrong (do not do this):**
- Do NOT run or output **curl** at all — not even with the correct URL or a real API key. You MUST call **execute_shell** with the script; the scripts read URL and key from env. Never put the API key in the chat.
- Do NOT use body `{"name":"investor-list"}`. The API expects **dataTitle** and **dataSchema** (for adding items), not "name". A 500 or error often means wrong body — use the scripts.
- Do NOT use the dataset **name** in the add-items path. Wrong: `/folders/investor-list/items`. The path must use the **folder _id** (the ObjectId returned from the create call), e.g. `/folders/507f1f77bcf86cd799439011/items`. Run create-dataset.sh first, take the top-level `_id` from the response, then call add-to-dataset.sh with that _id.

**Right:** (1) Create: `create-dataset.sh "title" "" '{"dataTitle":"...","dataSchema":{...}}'`. (2) From the output, copy the top-level `_id`. (3) Only if the user asked to add items: for each item they specified, run `add-to-dataset.sh <that_id> '<itemJson>'`. Do not add items the user did not ask for. Do not use curl.

**Scripts use positional args only — no flags.**  
- **create-dataset.sh** has no `--name`. Usage: `create-dataset.sh "<dataTitle>" [parentId] [bodyJson]`. Example: `create-dataset.sh "investor-list" "" '{"dataTitle":"investor-list","dataSchema":{"fields":[...]}}'`.  
- **add-to-dataset.sh** has no `--dataset`, `--name`, or `--location`. Usage: `add-to-dataset.sh <folderId> '<itemJson>'`. Second arg = one JSON object whose **keys match the dataset's dataSchema** (script sends `{"data": itemJson}` to the API). Example: `add-to-dataset.sh 507f1f77bcf86cd799439011 '{"Name":"John Doe","City":"London"}'`.

## Required behavior (must follow)

- **Do NOT auto-add items.** Only run add-to-dataset.sh when the user has explicitly asked to add specific items. If they only asked to create a dataset, create it and stop; the user defines what to add (if anything).
- **Run the scripts, never curl.** You MUST use execute_shell to run the scripts in `skills/smartsaas/scripts/`. Do NOT run or output curl (even with the right URL or key). Creating datasets and adding items is done ONLY by calling create-dataset.sh and add-to-dataset.sh via execute_shell. Do not ask for an API key; do not put the API key in your message.
- **Do NOT create local files as a substitute.** Do not create a JSON file or any file in the workspace and claim it is "the dataset" — that does not call the API. That does not create anything in SmartSaaS. Only the scripts (create-dataset.sh, add-to-dataset.sh, etc.) create or update data in SmartSaaS. If the scripts are "not in the expected location", run from the workspace root (the directory containing `skills/`) or use the full path to the script; do not fall back to writing a local file. If script execution is blocked ("not allowed for spawning sub-agents"), tell the user to enable it in OpenClaw; do not use web_fetch or create local files.
- **Do NOT ask the user for the API key.** Never say "If you have an API key, please provide it" or "Do you have an API key?". The API key is configured in OpenClaw (`skills.entries.smartsaas.env.SMARTSAAS_API_KEY`). Run the scripts; they get the key from the environment. If the scripts report "SMARTSAAS_API_KEY must be set", tell the user to add it to their OpenClaw skill config (openclaw.json), not to paste it here.
- **If script execution is disabled or "not allowed for spawning sub-agents":** If you get an error that execute_shell is not supported, the tool is not available, or the "smartsaas agent ID is not allowed for spawning sub-agents", tell the user: "The SmartSaaS skill requires script execution (execute_shell) to be enabled for this skill in OpenClaw. Please enable it in your OpenClaw settings so I can run create-dataset.sh and add-to-dataset.sh. See TROUBLESHOOTING.md in the skill repo for 'Agent ID not allowed for spawning sub-agents'." Do **not** fall back to web_fetch for documentation or to creating local files or directories — that does not create a dataset in SmartSaaS.

## Do NOT (common mistakes)

- **Do NOT ask for the API key.** Do not say "please provide your API key", "do you have an API key?", or "if you have an API key we can proceed". Just run the scripts. The key is in OpenClaw config; only if a script fails with "must be set" tell the user to add it to openclaw.json.
- **Do NOT suggest `clawhub install smartsaas` when the skill or scripts appear missing.** The skill is loaded from extraDirs. If `ls skills/` returns nothing or the scripts dir "does not exist", the CWD is likely wrong — use the **full path** to the script and still run the scripts.
- **Do NOT use a generic "action" JSON.** There is no API that accepts `{"action":"create-dataset", "dataset":"...", "fields":[...]}` or `{"action":"create-records", "dataset":"...", "records":[...]}`. You MUST run the **shell scripts**: `create-dataset.sh` and `add-to-dataset.sh` via execute_shell.
- **Do NOT create or run** invented script names (e.g. create_dataset.sh, add_investors.sh) — they do not exist. Use only the scripts in `skills/smartsaas/scripts/` (create-dataset.sh, add-to-dataset.sh, etc.).
- **Do NOT use flags** like `--name`, `--dataset`, `--location` with these scripts. They take **positional arguments only**: create-dataset.sh `<dataTitle>` `[parentId]` `[bodyJson]`; add-to-dataset.sh `<folderId>` `<itemJson>` (one JSON object as second arg).
- **Do NOT use wrong endpoints.** The API is **not** at `POST /datasets` or `POST /datasets/<name>/records`. It is at **POST /api/protected/data/folders** (create dataset) and **POST /api/protected/data/folders/:folderId/items** (add items). Base URL is **SMARTSAAS_BASE_URL** (set in env), not api.smartsaas.co.uk.
- **Do NOT suggest** `clawhub install smartsaas` to fix "skill not found" — the skill is installed via extraDirs; when scripts appear missing, use full path to scripts.
- **Do NOT search the web** for "SmartSaaS API documentation" or open smartsaas.com for API docs — that is a different product or public site. This skill’s endpoints and flow are in this SKILL.md; use the scripts only.
- **Do NOT skip running the scripts.** If the scripts "are not in the expected location", run from the workspace root (the directory that contains `skills/`) so that `./skills/smartsaas/scripts/create-dataset.sh` works, or use the full path to the script. Do not fall back to "API calls directly" with made-up endpoints, curl to the wrong host, or creating a local JSON file instead of calling the API.
- **Do NOT run or output curl.** Do not run curl yourself or give the user curl commands to run. You MUST call **execute_shell** with the script path and args. Do not put the API key in the message (scripts use env). **Do NOT prefix the script with placeholder env** (e.g. `SMARTSAAS_BASE_URL=https://your-smartsaas-url.com SMARTSAAS_API_KEY=your-api-key`); run the script alone so it uses the process environment. If scripts fail (env missing, HTTP 000), tell the user to set vars in ~/.openclaw/.env and restart OpenClaw; do not fall back to curl.

## Environment (env) — required for scripts

The scripts read **`SMARTSAAS_BASE_URL`** and **`SMARTSAAS_API_KEY`** from the environment. Without them, scripts exit with "SMARTSAAS_BASE_URL and SMARTSAAS_API_KEY must be set."

**NEVER run the script with placeholder values.** Do NOT prefix the command with `SMARTSAAS_BASE_URL=https://your-smartsaas-url.com SMARTSAAS_API_KEY=your-api-key` or any fake URL/key. Run the script **alone** (e.g. `./skills/smartsaas/scripts/create-dataset.sh "investor-list" "" '{"dataTitle":"investor-list","dataSchema":{...}}'`) so it uses the **process environment**. If the script then fails with "must be set" or connection errors, the sub-agent/shell is not receiving the vars — tell the user to set them in **`~/.openclaw/.env`** or export them before starting OpenClaw (see BLOCKED_ENV_FIX.md / TROUBLESHOOTING "Sub-agent not receiving env vars").

**Where env can be set (so sub-agents get them):**
1. **`~/.openclaw/.env`** — OpenClaw loads this; best so the process (and any sub-agent shell) has the vars.
2. **Export before starting OpenClaw** in the same shell: `export SMARTSAAS_BASE_URL=... SMARTSAAS_API_KEY=...` then start OpenClaw.
3. **OpenClaw skill config:** `~/.openclaw/openclaw.json` → `skills.entries.smartsaas.env` — may not be passed to sub-agent shells; if scripts fail with "must be set", use (1) or (2).

**If a script fails with "must be set" or HTTP 000 / connection errors:** Tell the user the sub-agent is likely not receiving env vars. Have them add `SMARTSAAS_BASE_URL` and `SMARTSAAS_API_KEY` to `~/.openclaw/.env` and restart OpenClaw. Do not ask the user to paste the API key in chat.

## Prerequisites

- `SMARTSAAS_BASE_URL` and `SMARTSAAS_API_KEY` must be available to the scripts (see **Environment** above). The API key is created in SmartSaaS APIScreen. You do not ask the user for it.

## Schema chain (retrieve schema before posting)

**Before any create or POST request, retrieve the expected shape so the request body matches backend expectations.**

1. Run **`scripts/get-schema.sh <resource>`** to get the schema for that resource. Resources: `dataset`, `data-item`, `project`, `work-package`, `task`, `campaign`, `email-template`, `webpage-template`.
2. Use the script output (JSON with `fields`, `endpoint`, `createScript`) to build the POST body. Include all required fields and only optional fields you need.
3. Then run the corresponding create script with the built body (e.g. `scripts/create-dataset.sh` with bodyJson, or `scripts/add-to-dataset.sh` with itemJson).

Example chain for creating a dataset that can hold content:  
`get-schema.sh dataset` → read `dataTitle` (required), `dataSchema` (required when adding content) →  
`create-dataset.sh "My Dataset" "" '{"dataTitle":"My Dataset","dataSchema":{"fields":[{"name":"name","type":"string"}]}}'`

If you skip the schema step and the backend returns 400 (e.g. missing field or wrong shape), run `get-schema.sh <resource>` and retry with a body that matches.

## Creating a dataset and adding items (two-step flow)

Only add items when the user **explicitly asked** to add something; they define what to add (if anything). Do not assume or add example data (e.g. "investors") unless the user asked for it.

Adding items to a dataset requires the **dataset id** from the create step. Follow this order:

1. **Create the dataset** (with dataSchema so items can be added):
   - Run `scripts/create-dataset.sh "<dataTitle>" "" '<bodyJson>'` where bodyJson includes `dataTitle` and `dataSchema.fields` for the fields the user wants. Use get-schema.sh dataset first if needed to build the body.
   - The script prints the API response. Response shape: `{ "success": true, "message": "Data posted", "data": { "_id": "...", "dataTitle": "...", ... }, "_id": "<folderId>" }`. **Use the top-level `_id`** as the dataset id (folderId) for add-to-dataset.sh.

2. **Before adding items (recommended):** Run `scripts/get-dataset.sh <folderId>` to fetch the folder; the response includes **dataSchema** so you can build itemJson with matching field names. If get-dataset.sh returns 404, the backend may not expose GET /folders/:id yet — use the dataSchema you used when creating the dataset, or list-datasets.sh and find the folder in the list by _id to read its dataSchema.

3. **Add each item:**
   - Run `scripts/add-to-dataset.sh <folderId> '<itemJson>'` for each item. `<itemJson>` must match the dataset's dataSchema (same field names as in dataSchema.fields). If you didn't create the dataset in this session, run get-dataset.sh first to get the structure.

**Looking up data entries:** You may look up contacts, investors, companies, or other entities (e.g. via web search or other tools) to find or validate data to add as dataset items. That is separate from research/knowledge: use whatever tools you have to gather entries, then add them via add-to-dataset.sh. **Research / knowledge** is different: use list-knowledge.sh, create-knowledge.sh, and post-research.sh to work with knowledge articles and save research as knowledge — that does not populate dataset items; it saves findings as knowledge content.

You cannot add items until the dataset exists and you have its id. Always use the top-level **`_id`** from the create-dataset.sh response as folderId.

**Where to run / why "scripts directory doesn't exist":** The shell used by execute_shell often does **not** start in the repo root. So `./skills/smartsaas/scripts/` or `ls skills/smartsaas/scripts/` may fail with "no such file" or "directory does not exist" because the **current working directory** is elsewhere. Fix: use the **full absolute path** to the script. The scripts live at `<repo_root>/skills/smartsaas/scripts/` where `<repo_root>` is the directory that contains the `skills` folder (e.g. the smartsaas-openclaw-tools repo). Example: `/Users/sarfrazhussain/smartsaas-openclaw-tools/skills/smartsaas/scripts/create-dataset.sh` (adjust if the user's repo is elsewhere). Or run `cd <repo_root> && ./skills/smartsaas/scripts/create-dataset.sh ...` with the real path to the repo. Do **not** conclude the scripts are missing; use the full path.

**Do NOT:** Invent script names (e.g. create_dataset.sh, add_investors.sh) or use api.smartsaas.co.uk or `/datasets`. Run only the existing scripts from `skills/smartsaas/scripts/`.

### Example: dataset + items (e.g. "Investor-List" with name/email/phone/city/country)

For "create dataset X" only: create and stop. For "create dataset X and add [specific items]": create then add only what the user specified. Example syntax for adding (when user asked) — dataset with fields Name, Email, Phone, City, Country:

1. Create: `create-dataset.sh "<Title>" "" '{"dataTitle":"<Title>","dataSchema":{"fields":[...]}}'` (replace with user's dataset name and desired fields).
2. From the output, take the top-level `_id` as folderId.
3. Before adding items: run `get-dataset.sh <folderId>` to get the folder's dataSchema so itemJson keys match.
4. For each item the user asked to add: `add-to-dataset.sh <folderId> '<itemJson>'` with itemJson keys matching dataSchema.fields.

Do not ask for an API key. Do not create a local file instead of running the scripts.

## Scripts (run via execute_shell)

Run scripts from this skill's `scripts/` directory (or use the full path to each script). All scripts use `SMARTSAAS_BASE_URL` and `SMARTSAAS_API_KEY` from the environment (except `get-schema.sh`, which needs no env). **Always report the script's full stdout and stderr to the user** so they can see success messages or errors. For dataset/project names with spaces, pass the title as a single quoted argument (e.g. `scripts/create-dataset.sh "hello world"`).

| Action | Script | Arguments / usage |
|--------|--------|-------------------|
| **Get schema (run first before create/post)** | `scripts/get-schema.sh` | 1) resource (dataset \| data-item \| project \| work-package \| task \| campaign \| email-template \| webpage-template). No arg = list resources. |
| Create dataset | `scripts/create-dataset.sh` | 1) dataTitle (required) 2) parentId (optional) 3) bodyJson (optional: full JSON per Data.mjs—dataTitle, **dataSchema** for content, dataTags, dataType, description, shared, etc.) |
| Get dataset (folder) by id | `scripts/get-dataset.sh` | 1) folderId. Returns folder including **dataSchema**; run before adding items to get correct structure for itemJson. |
| Add item to dataset | `scripts/add-to-dataset.sh` | 1) folderId 2) itemJson (keys match dataSchema.fields; use get-dataset.sh first if unsure of structure) |
| Get dataset content | `scripts/get-data-content.sh` | 1) folderId 2) type (optional: document \| invoice; omit for dataset + dataContent items). Backend: getDataContent.mjs. |
| List datasets | `scripts/list-datasets.sh` | 1) parentId (optional) |
| Create project | `scripts/create-project.sh` | 1) title 2) description (optional). Shape: Projects.mjs |
| List projects | `scripts/list-projects.sh` | (no args) |
| Create work package | `scripts/create-work-package.sh` | 1) projectId 2) work_package_title 3) description (optional). Shape: Projects.mjs WorkPackageSchema |
| Create task | `scripts/create-task.sh` | 1) projectId 2) workPackageId 3) task_title 4) description (optional). Shape: Projects.mjs TaskSchema |
| Assign task | `scripts/assign-task.sh` | 1) projectId 2) taskId 3) assignedTo (optional) |
| Add team member | `scripts/add-team-member.sh` | 1) projectId 2) userId 3) role (optional) |

### Integrations (sync with user integrations)

| Action | Script | Arguments / usage |
|--------|--------|-------------------|
| List integrations | `scripts/list-integrations.sh` | (no args) |
| Remove integration | `scripts/remove-integration.sh` | 1) integration name (e.g. gmail, shopify) |
| Sync Shopify products | `scripts/sync-shopify-products.sh` | (no args) |
| Get product sync status | `scripts/get-product-sync-status.sh` | 1) dataId |
| Pull products from integration | `scripts/pull-products-from-integration.sh` | 1) dataId 2) integrationType (e.g. shopify) |
| Push products to integration | `scripts/push-products-to-integration.sh` | 1) dataId 2) integrationType |
| Get available integrations | `scripts/get-available-integrations.sh` | (no args) |

### Core tasks (user, favourites, companies, calendar)

| Action | Script | Arguments / usage |
|--------|--------|-------------------|
| Refresh user | `scripts/refresh-user.sh` | (no args) |
| Get data favourites | `scripts/get-data-favourites.sh` | (no args) |
| Get project favourites | `scripts/get-project-favourites.sh` | (no args) |
| Get user companies | `scripts/get-user-companies.sh` | (no args) |
| Get users | `scripts/get-users.sh` | 1) page (optional) 2) pageSize (optional) |
| Get user hierarchy | `scripts/get-user-hierarchy.sh` | (no args) |
| Get calendar schema | `scripts/get-calendar-schema.sh` | (no args) |
| Get calendar content | `scripts/get-calendar-content.sh` | 1) date (e.g. 2025-03-15) |

### Knowledge & research

| Action | Script | Arguments / usage |
|--------|--------|-------------------|
| List knowledge | `scripts/list-knowledge.sh` | 1) page (optional) 2) limit (optional) 3) sortBy (optional) 4) sortOrder (optional). Permission: knowledge:read. |
| Get knowledge article | `scripts/get-knowledge.sh` | 1) id. Permission: knowledge:read. |
| Create knowledge article | `scripts/create-knowledge.sh` | 1) articleJson (title, content, featuredImage, …). Permission: knowledge:write. |
| Post research (saved as knowledge) | `scripts/post-research.sh` | 1) researchJson (title, findings/content/summary, source, url, …). Adapter maps to knowledge. Permission: knowledge:write. |

### Campaigns

| Action | Script | Arguments / usage |
|--------|--------|-------------------|
| List active campaigns | `scripts/list-active-campaigns.sh` | (no args) |
| Create campaign | `scripts/create-campaign.sh` | 1) campaignJson (campaign_title, stages, etc.) 2) userId (optional). Shape: SalesSchemas/Campaign.mjs |
| Start campaign | `scripts/start-campaign.sh` | 1) campaignId |

### Email templates

| Action | Script | Arguments / usage |
|--------|--------|-------------------|
| List email templates | `scripts/list-email-templates.sh` | (no args) |
| Create email template | `scripts/create-email-template.sh` | 1) templateJson (title required; content, description, tags). Shape: TemplateModels/Email.mjs |
| Update email template | `scripts/update-email-template.sh` | 1) templateJson (_id required; title, content, description, etc.) |
| Send test email | `scripts/send-test-email.sh` | 1) templateId 2) toEmail 3) subject (optional) |

### Website (webpage) templates

| Action | Script | Arguments / usage |
|--------|--------|-------------------|
| List webpage templates | `scripts/list-webpage-templates.sh` | (no args) |
| Create webpage template | `scripts/create-webpage-template.sh` | 1) templateJson (title required; description, content, urlSlug, isPublished). Shape: TemplateModels/Webpage.mjs |
| Update webpage template | `scripts/update-webpage-template.sh` | 1) templateJson (_id required; title, description, content, isPublished, urlSlug) |

### Events & webhook (cron, dispatch)

| Action | Script | Arguments / usage |
|--------|--------|-------------------|
| Dispatch to OpenClaw webhook | `scripts/dispatch-openclaw-webhook.sh` | 1) optional JSON payload (default: ping event) |
| Post event to webhook | `scripts/post-openclaw-event.sh` | 1) eventType (e.g. cron, daily_sync) 2) optional JSON payload |
| Configure cron / schedule | `scripts/configure-openclaw-cron.sh` | 1) config JSON (schedule, payload, enabled, etc.) |

Webhook URL: `{SMARTSAAS_BASE_URL}/api/protected/openclaw/webhook`. Use for cron jobs, scheduled tasks, or custom event dispatch.

## Examples

- **Create dataset then add items:** (1) Create with `scripts/create-dataset.sh "<title>" "" '<bodyJson>'` (bodyJson includes dataTitle and dataSchema.fields). (2) Parse the response: use the **top-level `_id`** as folderId. (3) Add each item: `scripts/add-to-dataset.sh <folderId> '<itemJson>'` (itemJson matches schema). (4) Fetch: `scripts/get-data-content.sh <folderId>`.
- **Schema chain:** Run `scripts/get-schema.sh dataset` first to see required/optional fields, then build the body and run `scripts/create-dataset.sh "My Dataset" "" '<bodyJson>'`.
- Create a dataset (no items): `scripts/create-dataset.sh "My Dataset"`. To allow adding content later, include dataSchema: `scripts/create-dataset.sh "My Dataset" "" '{"dataTitle":"My Dataset","dataSchema":{"fields":[{"name":"name","type":"string"}]}}'`.
- List datasets: run `scripts/list-datasets.sh`.
- Create a project: run `scripts/create-project.sh "Project Alpha" "Description"`.
- Create a task: run `scripts/create-task.sh "<projectId>" "<workPackageId>" "Task title"`.
- Assign a task: run `scripts/assign-task.sh "<projectId>" "<taskId>" "<userId>"`.
- List user integrations: run `scripts/list-integrations.sh`.
- Sync Shopify products: run `scripts/sync-shopify-products.sh`.
- Refresh user: run `scripts/refresh-user.sh`.
- Get calendar for a date: run `scripts/get-calendar-content.sh "2025-03-15"`.
- List campaigns: run `scripts/list-active-campaigns.sh`.
- Start a campaign: run `scripts/start-campaign.sh "<campaignId>"`.
- Create email template: run `scripts/create-email-template.sh '{"title":"Welcome","subject":"Hi","content":"..."}'`.
- Create webpage template: run `scripts/create-webpage-template.sh '{"title":"Landing","description":"..."}'`.
- Send test email: run `scripts/send-test-email.sh "<templateId>" "user@example.com" "Test"`.
- List knowledge: `scripts/list-knowledge.sh` or `scripts/list-knowledge.sh 1 10 createdAt desc`. Get one: `scripts/get-knowledge.sh "<id>"`. Create: `scripts/create-knowledge.sh '{"title":"My article","content":"..."}'`. Post research: `scripts/post-research.sh '{"title":"Market study","findings":"..."}'`.
- Dispatch to webhook: run `scripts/dispatch-openclaw-webhook.sh` or `scripts/dispatch-openclaw-webhook.sh '{"event":"cron","job":"daily"}'`.
- Post event: run `scripts/post-openclaw-event.sh cron '{"schedule":"daily"}'`.
- Configure cron: run `scripts/configure-openclaw-cron.sh '{"schedule":"0 9 * * *","payload":{},"enabled":true}'`.

**Schema requirements (valid posts):** Use the **schema chain**: run `get-schema.sh <resource>` before any create/post to retrieve the expected shape, then build the request from that output. Schemas are in this skill's `schemas/` (JSON per resource); they mirror `smartsaas-backend/src/schema/` and repo **SCHEMA_REQUIREMENTS.md**. Use the correct field names (e.g. task_title, campaign_title, dataSchema) when sending full JSON; scripts may accept friendly names and the API may map them.

Do not log or echo the API key. Never ask the user to provide the API key in chat. If the scripts report missing config, tell the user to set `SMARTSAAS_BASE_URL` and `SMARTSAAS_API_KEY` in OpenClaw (e.g. in `skills.entries.smartsaas.env` in ~/.openclaw/openclaw.json).
