---
name: upkuajing-global-company-people-search
description: "Search global companies and professional contacts for cross‑border B2B lead generation. Help exporters, sourcing agents and sales teams identify purchasing decision‑makers, source qualified suppliers and speed‑up international customer acquisition. Access business registration records, company intelligence and verified contact details including Emails, Phone numbers and WhatsApp profiles. Results must come only from the UpKuaJing API; never substitute Codex web search or other sources.\n\nTrigger: find companies, find people, export sales leads, B2B leads, verify a contact, get verified business emails, global supplier search"
metadata: {"version":"1.1.1","homepage":"https://developer.upkuajing.com/openapi/","clawdbot":{"emoji":"🏢","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# UpKuaJing Company and People Search

Query corporate business information and people data using the UpKuaJing Open Platform API. This skill uses an **entity-driven approach**: finding target entities directly through company attributes (product, industry, size) and people attributes (position, school, experience).

## Overview

This skill provides access to UpKuaJing's global company database and people data through five scripts: two list searches (companies, people) and three enhancement interfaces (company details, people details, contact information).
API key generation and top-up are provided through the `auth.py` script.

## Mandatory Pre-query Status Check

Before any paid query, read and complete [API Key status and balance workflow](references/api-key-onboarding.md):

1. On first activation, or when the user has not yet been introduced to the capability, briefly explain company search, people search, details, contact retrieval, and paid usage. Provide the API capability and pricing page: `https://developer.upkuajing.com/openapi/`.
2. Run `auth.py --key_status` before asking the user whether they have an UpKuaJing account. Explicitly report whether a local API Key exists and is valid.
3. Report the actual binding state and available balances. For a bound Key, explain that charges use the API balance first, then the UpKuaJing account balance.
4. Ask only the account, binding, Key-generation, or recharge question required by the detected state. Do not ask the user to classify a state that the script already established.
5. After the user completes a required binding or payment action, verify the status again before continuing.

Do not infer that a Key exists, is valid, or is bound from the user's statement alone. Never reveal a full API Key in chat. Do not start a paid search until the Key is valid and usable funds are sufficient. Then read [search input guidance and bounded clarification](references/search-query-readiness.md): if the user already supplied a request, assess it immediately; show the full input guide only when no concrete request exists or when the request is too vague to reach the readiness gate. A ready request goes directly to the natural-language query and fee brief.

## Search Source Boundary (Mandatory)

Search results from this skill must come only from the UpKuaJing API invoked by scripts in this directory. If results are poor or empty, the API fails, or the user is dissatisfied, never use Codex web search, browser tools, the public internet, model memory, another plugin, database, or skill to supplement or replace results. Report the actual UpKuaJing outcome, offer refinements supported by this API, and wait for a new fee confirmation before rerunning—or stop.

## Paid Result Delivery (Mandatory)

After every confirmed paid task, read and complete [paid query result delivery](references/result-delivery.md). A list request with automatic contact enrichment is one task even though it makes multiple billed API calls: do not deliver between those calls. Never respond with only a task ID, file path, “saved,” or “query complete.”

- List searches: show at most the first 10 records in one concise Markdown table. Choose columns flexibly from the user's question, using basic, meaningful fields only. Never show IDs, cursors, internal scores, or globally empty columns in this preview.
- Always provide both the complete raw JSONL and the complete readable XLSX for list searches. Do not automatically create CSV or Markdown reports.
- Partial success: show up to the first 10 paid records, actual count, fee, stop reason, and both files containing every saved record.
- List scripts keep the delivered record count at the confirmed quantity. Human searches with role conditions run a deterministic title-quality assessment; only target-role matches continue into paid contact enrichment, and target matches are prioritized in the preview.
- The user may ask follow-up questions based on the complete JSONL. Reading or analyzing the existing JSONL does not call the API and incurs no query fee. Answer only from that file; if information is absent, say so instead of guessing or using another source.
- If the user asks for email, phone, WhatsApp, or contact information, interpret this as a request for the actual values. Before execution, disclose the list fee, the contact endpoint's per-ID rule, the maximum contact fee, and the maximum total; obtain one confirmation for the complete task. Then run the list script with `--include_contacts` and the requested `--contact_types`. It must automatically continue into contact retrieval without an intermediate table or second confirmation. Show only the final enriched preview and merge complete values into JSONL and XLSX. Use existence filtering alone only when the user explicitly says they do not need actual values.
- For list searches involving email and phone, offer only three supported choices: email only, phone only, or both email and phone required. The list API cannot express a true “email OR phone” condition in one query. If the user asks for “email or phone”, “either one”, “any contact”, or “at least one”, explain this limitation, ask them to choose one of the three supported choices, and wait. Never silently choose the first type and never use `--contact_match any` for a paid list workflow. Use `--contact_match all` for every supported choice and state the selected choice in the confirmation brief. WhatsApp remains available when explicitly requested.
- Company details, people details, and contacts: show every returned object in the current response.
- Contact enrichment is successful only when concrete requested values are merged. Zero merged contacts is a failed contact stage; report the actual fee and the task-specific response audit file.
- The script's `delivery` object is mandatory. Do not end the task before user-visible delivery is complete.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/company_list_search.py`. **Do NOT use** shell compound commands like `cd scripts && python company_list_search.py`.

### Two Search Methods

**Company List Search** (`company_list_search.py`)
- **Return granularity**: Each company as one record
- **Use cases**: Focus on "which companies exist"
- **Examples**:
   - "Find manufacturers producing LED lights"
   - "Find tech companies with 100-500 employees"
- **Parameters**: See [Company List](references/company-list-api.md)
- **Automatic contact chain**: add `--include_contacts --contact_types email phone whatsapp` as needed when the original user request includes actual contact values

**People List Search** (`human_list_search.py`)
- **Return granularity**: Each person as one record
- **Use cases**: Focus on "which people exist"
- **Examples**:
  - "Find CTOs at XXXX"
  - "Find Sales Directors in China for XXX"
- **Parameters**: See [People List](references/human-list-api.md)
- **Automatic contact chain**: add `--include_contacts --contact_types ... --contact_match all` after the user selects a supported contact combination; do not expose the intermediate people list
- **Role targeting**: prefer stable business-role anchors such as Procurement, Purchasing, Supply Chain, Sales, or Technology. Do not rely on generic level words such as Manager, Director, or Head as the matching anchor.
- **Server anchor**: put role business words in `titleNames`. The script normalizes role-only inputs to `titleNames` before validation and network execution.

### Three Enhancement Interfaces

After obtaining company or people lists, use these interfaces to enrich information when necessary:

**Company Details** (`company_details.py --pids *`)
- Get company business registration information (excluding contact information)
- **Parameters**: `--pids` List of company IDs (space-separated, obtained from list search), max 20 at a time

**People Details** (`human_details.py --hids *`)
- Get detailed person information (education, work experience, etc.)
- **Parameters**: `--hids` List of people IDs (space-separated, obtained from list search), max 20 at a time

**Contact Information** (`get_contact.py --bus_type * --bus_ids * [--task_id *]`)
- Get contact information (email, phone, WhatsApp, social media, website)
- **Parameters**:
  - `--bus_type`: 1=company, 2=person
  - `--bus_ids`: List of company IDs or people IDs (space-separated, obtained from list search), max 20 at a time
  - `--task_id`: original list task ID; required in the list-to-contact workflow so returned contacts are merged into the final JSONL and XLSX

## API Key and Top-up

This skill requires an API key. It is normally stored in `~/.upkuajing/.env`:
```bash
cat ~/.upkuajing/.env
```
**Example file content**:
```
UPKUAJING_API_KEY=your_api_key_here
```

- Detect the Key, binding state, and both balances: `python scripts/auth.py --key_status`
- Create a Key: `python scripts/auth.py --new_key`
- Create a payment page: `python scripts/auth.py --new_rec_order`
- Bind an API Key in the [UpKuaJing account center](https://developer.upkuajing.com/account/)

Follow [API Key status and balance workflow](references/api-key-onboarding.md) for account classification, user-facing status, deduction order, and recharge handling.

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**API capabilities and latest pricing page**: [UpKuaJing Open API](https://developer.upkuajing.com/openapi/)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### List Search Billing Rules

Billed by **number of calls**, each call returns up to 20 records:
- Base number of calls: `ceil(query_count / 20)`
- When actual contact values are requested, reserve one additional list call for unique-ID refill. The confirmation brief must use a maximum of `ceil(query_count / 20) + 1` list calls, and the script must not exceed it.
- A checkpoint continuation is the same task, not a fresh budget. Before resuming, show the saved unique-record count, cumulative list calls and fees, remaining call allowance, unchanged query/contact settings, and the maximum remaining fee; wait for explicit confirmation again. Resume with `--task_id` and `--user_confirmed` only. The script restores the original quantity and contact settings, skips IDs whose requested contact values are already present, and never resets or expands the confirmed limits. If the checkpoint predates the cumulative accounting fields, do not resume it automatically; create a new task after a new confirmation.
- **Whenever query_count > 20, must before execution:**
  1. Inform user of expected number of calls
  2. Stop, wait for explicit user confirmation in a separate message, then execute script

### Enhancement Interface Billing Rules

Billed by **number of IDs passed**, max 20 IDs per call:
- Pass 1 ID = billed 1 time
- Pass 20 IDs = billed 20 times (single call limit)
- **Before batch retrieval must:**
  1. Inform user of number of IDs passed and corresponding fee count
  2. Stop, wait for explicit user confirmation in a separate message, then execute script

Exception for a list request that already includes actual contact values: include the contact endpoint's maximum ID count and maximum fee in the list task's single pre-query confirmation. After that confirmation, `--include_contacts` may automatically execute all contact batches within the approved maximum without another pause. This exception does not authorize unrelated detail or contact calls beyond that confirmed task.

### Fee Confirmation Principle

**Any operation that incurs fees must first inform and wait for explicit user confirmation. Do not execute in the same message as the notification.**

Every paid script requires `--user_confirmed`. Add it only after the user has reviewed the natural-language query brief and fees and explicitly agreed in a separate message. The flag never substitutes for conversational confirmation.

### Plan Billing and Balance Fallback

Search, customs and map calls are **plan-first**: scripts automatically send `"planMode": 2`.

- **Plan unavailable** (no valid plan, or quota exhausted): the script stops before executing the request, prints a line starting with `PLAN_UNAVAILABLE ` (single-line JSON) on stdout, and exits with **code 3**. Never retry automatically.
- **Ask the user first**: explain the reason in plain language (no plan / quota exhausted, plus the reset time when known), state that continuing will be charged to the API balance (unit price: `python scripts/auth.py --price_info`), then wait for an explicit answer in a separate message.
- **User agrees**: re-run the same command with `UPKUAJING_PLAN_MODE=1` (PowerShell: `$env:UPKUAJING_PLAN_MODE='1'`) and report `fee` from the response.
- **User declines**: stop; nothing is executed or charged. Offer three options — retry later / upgrade plan / use balance — and do not ask again in the same turn.
- **Insufficient balance after switching** (code 95): guide the user to top up and stop; do not retry.
- **Before a large or batch run**: check quota once with `python scripts/auth.py --plan_quota` (tier limits: `--plan_config`). If `available` is 0 or the target window has `remaining` 0, ask about balance up front instead of making a call that must fail.
- **On success**: relay the `[套餐] ...` usage line printed on stderr to the user.
- **Never** switch to balance silently, and never expose internal error codes verbatim.

Full contract: [references/plan-billing.md](references/plan-billing.md)

## Bounded Clarification Before Paid Search (Mandatory)

Before company or people list search, read and complete [bounded paid-search clarification](references/search-query-readiness.md):

- If the user has not supplied a concrete request, show the relevant company/people input guide and a realistic full example. If a request already exists, assess it first and skip the generic guide when it is ready.
- At most two clarification rounds: up to 3 grouped questions in round one and up to 2 only when a critical conflict remains in round two.
- Ask only high-impact questions that change the API, search anchor, main scope, or cost.
- Put safe defaults in the query brief instead of asking about every optional filter.
- If no reliable anchor exists after two rounds, stop without calling the API.
- Once the readiness gate is met, immediately present the natural-language query brief and stop asking questions.
- Run a paid script with `--user_confirmed` only after the user's separate explicit approval.


## Workflow

Choose the appropriate API based on user intent.

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Find companies producing XXX" | Company list |
| "Find companies with email/phone" | One confirmed company-list task with automatic contact enrichment and one final delivery |
| "Find CEO/CTO of XX company" | People list |
| "Find customers for XXX" | Company list using the product, industry, company-role, and region conditions supplied by the user |
| "Get person resume" | People details |
| "Get company contact information" | Contact information bus_type=1 |

## Usage Examples

### Scenario 1: Small Query — Search Companies

**User request**: "Find Chinese manufacturers producing LED lights"
```bash
python scripts/company_list_search.py \
  --params '{"products": ["LED lights"], "countryCodes": ["CN"]}' \
  --query_count 20 \
  --user_confirmed
```

### Scenario 2: Search People

**User request**: "Find CTOs at XXXX"
```bash
python scripts/human_list_search.py \
  --params '{"companyNames": ["XXXX"], "titleNames": ["CTO"]}' \
  --query_count 20 \
  --user_confirmed
```

### Scenario 3: Large Query — Multiple Script Calls Required

**User request**: "Find 1000 US electronics importers with email addresses"
**Before execution** inform user: up to ceil(1000/20) + 1 = 51 list API calls because contact refill is enabled, plus the contact endpoint's maximum ID fee; confirm before executing.
```bash
python scripts/company_list_search.py --params '{"products": ["electronics"], "countryCodes": ["US"]}' --query_count 1000 --include_contacts --contact_types email --user_confirmed
```
**After execution**: Script responds {"task_id":"a1b2-c3d4", "file_url": "xxxxx", ……}
**Continue the same task after interruption**: first disclose its saved cumulative usage and remaining allowance and obtain confirmation again. Specify only the task ID; the script restores the original quantity and contact configuration, continues from the saved cursor, and appends only new unique data.
```bash
python scripts/company_list_search.py --task_id 'task-id-here' --user_confirmed
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Plan unavailable (exit code 3 / `PLAN_UNAVAILABLE`)**: explain the reason and ask whether to continue with the API balance; do not retry automatically. See [Plan Billing](references/plan-billing.md)
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- Plan Billing and Balance Fallback: [references/plan-billing.md](references/plan-billing.md)

## Best Practices

### Choosing the Right Method

1. **Understand user intent**:
   - Find companies? → Use **company list search**
   - Find people? → Use **people list search**

2. **Check API documentation**:
   - **Before executing list queries, must first check the corresponding API reference documentation**
   - Company list: Check [references/company-list-api.md](references/company-list-api.md)
   - People list: Check [references/human-list-api.md](references/human-list-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

3. **Optimize query parameters**:
   - Always use exact matching for company and people lists; fuzzy matching is prohibited. Before execution, follow [bounded paid-search clarification](references/search-query-readiness.md) to generate minimal complete business phrases
   - Put products in `products` using common English industry terms. Use one primary query and at most two high-confidence equivalent queries per target; queries in the same field use exact OR matching. Never split a business phrase into standalone words or expand it to merely related products
   - Use `existEmail=1` or `existPhone=1` to filter entities with contact information
   - Use `countryCodes` to limit country scope

### Handling Results

3. **Handle jsonl files carefully**: For large data queries, pay attention to file size
4. **Enrich contacts as one confirmed task**: When the original request includes actual contact values, include the maximum contact cost in the single pre-query confirmation and let the list script continue automatically; do not pause at inventory counts or request a second confirmation
   - Company IDs returned by both list interfaces can be used for both detail interfaces
   - If user only needs a few companies, don't get details for all companies
5. **Keep source boundaries when results are poor**: Never use Codex search, browser tools, or another source as a fallback. Report the outcome, offer supported filter changes, and wait for a new paid-query confirmation.
6. **Deliver complete results**: Follow [paid query result delivery](references/result-delivery.md); never leave paid results only in `task_data`. Every list delivery includes both JSONL and XLSX.

## Notes
- Use hids for people search, pids for company search, be careful to distinguish
- All timestamps are in milliseconds
- Country codes use ISO 3166-1 alpha-2 format (e.g., CN, US, JP)
- File paths use forward slashes on all platforms
- Product names and industry names must be in **English**
- Search quantity affects API response time, recommend setting timeout:120
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not estimate or guess per-call fees** — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation
