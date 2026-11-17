---
name: seo-project-setup
description: "Set up an SEO project: a local SEO workspace folder, website scope, goals, positioning, the HarborRank project, and Google Search Console (connected, or CSV exports). Use when the user starts SEO for a new site or client, onboards a website, wants to connect Search Console, or has no HarborRank project yet. The other HarborRank workflows build on this setup."
---

# HarborRank SEO Project Setup

## Goal

Help the user set up a local SEO workspace for one website or SEO project. The folder is where the agent saves notes, goals, exports, briefs, reports, preferences, and project context over time. This is a workspace and context setup workflow, not a full audit.

## Step 0: Check connection

Before any other step, confirm the HarborRank MCP tools are loaded. Look for `get_domain_overview` or `list_leads` among your tools, including deferred tools you can load (the name may carry a prefix such as `mcp__harborrank__`). If they are there, call `whoami`: it uses no credits, confirms the user is signed in, and returns `creditsRemaining` for budgeting the run. Do not call a research tool to test the connection.

If neither tool is available, or `whoami` fails because the user is not signed in, tell the user plainly: "HarborRank isn't connected, so I can't pull live HarborRank data yet." Then tell them how to connect it:

- Claude Code with the HarborRank plugin: run `/mcp`, choose `harborrank`, and sign in.
- Claude Code without the plugin: run `claude mcp add --transport http --scope user harborrank https://app.harborrank.com/mcp`, then `/mcp` to sign in.
- Claude on the web, desktop or Cowork: open Customize, then Connectors, search for HarborRank, choose Connect, and sign in. New accounts start with a 7-day free trial.
- Cursor with the HarborRank plugin: open Cursor Settings, then MCP, and sign in to `harborrank`.
- Gemini CLI with the HarborRank extension: run `/mcp auth harborrank`.
- Other clients: add `https://app.harborrank.com/mcp` as a remote MCP server. Setup for each client is at https://harborrank.com/docs/mcp.

Tell them what happens when they connect: they sign in to HarborRank with Google or email and start a 7-day free trial. Then they come back to this conversation and say "connected", and you pick up the task where it stopped.

Do not stop there. Continue in fallback mode (below). If the user connects HarborRank mid-task, run Step 0 again and switch to the full workflow.

### Plan limits

On hosted HarborRank, research tools spend credits. New accounts start with a 7-day free trial (1,000 research credits, one project); paid plans start at $29/month with 15,000 credits. Search Console, saved keywords, rank tracker reads, and site crawls use no credits. A keyword search costs about 50 credits and a domain overview about 80. Full backlinks, lead research (`research_lead`), and Lighthouse checks need a paid plan; on Free, the backlinks tools return a preview (totals and the top 3 referring domains, about 50 credits) with an upgrade link.

- If `creditsRemaining` will not cover the planned calls, give the user the estimate and ask before spending. Use the free tools first.
- If a tool replies that a feature "is included in paid plans", tell the user once which feature needs a paid plan and pass on the upgrade link from the reply, skip that tool for the rest of the run, and finish with the other evidence. Do not retry it.
- If a tool fails for insufficient credits, stop making paid calls, tell the user, and finish with free tools and the data you already have. If `whoami` warns that credits are low, say so before a large run.
- If a HarborRank tool says the free trial hasn't started, or that credits ran out, give the user the link from that reply exactly as written, as a clickable link, and wait for them to say they're done before calling HarborRank again. Don't switch to answering without HarborRank data unless they ask you to.
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Run every setup step except the HarborRank check: working folder, website scope, goals, positioning, asset inventory, and the first workflow.
- Research positioning by reading the user's site, competitor pages, and public reviews.
- Take Search Console data through CSV exports (the step 6 fallback path).
- In step 5, mark HarborRank "Not connected" in the checklist, with the connection steps as the next action.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to read Search Console directly and save this setup to a project." Do not add more sales copy than that.

## Tone

Be friendly, practical, and structured. Ask questions in small batches. Explain why each item matters only when useful. Do not overwhelm a beginner with jargon.

## Checklist

### 1. Pick a working folder

Suggest that the user choose or create a local folder for SEO work, for example:

- `~/SEO/<company-or-site>/`
- `~/Documents/SEO/<company-or-site>/`
- A repo or workspace folder if SEO work should live beside website/content files

Explain that keeping notes, exports, briefs, scraped pages, reports, and preferences in one folder helps the agent build context over time. Future SEO workflows can use that folder rather than starting from a blank conversation.

Recommended starter structure:

```text
seo-workspace/
  README.md
  gsc/
  keywords/
  competitors/
  content/
  outreach/
  reports/
```

Do not create folders unless the user asks. If file tools are available and the user asks, create a simple structure and a short `README.md` with the current goals, known sites, and user preferences for how the agent should approach SEO for this project.

### 2. Collect website scope

Ask for:

- Primary website/domain
- Additional domains or subdomains
- Important products, services, categories, or pages
- Target countries/languages
- Whether the site is new, established, migrating, or recovering from a drop
- CMS or publishing workflow, if relevant

### 3. Capture goals

Ask the user what they want from SEO:

- More qualified leads
- More signups/trials
- More ecommerce revenue
- More newsletter/audience growth
- More brand/category awareness
- Recovery from traffic loss
- Better ranking for specific pages

Ask for success metrics and timeframe. If goals are vague, help turn them into measurable goals such as "increase non-branded organic signups" or "rank top 10 for 20 buying-intent terms."

### 4. Capture positioning and strategy context

Ask what research they have already done about the company, product, audience, and competitors. Request any notes, docs, customer interviews, positioning docs, pitch decks, landing pages, or strategy memos they can share.

Probe for:

- Who the product or site is for
- What pain it solves
- Why users choose it over alternatives
- Competitors and substitutes
- Strong opinions or positioning claims
- Best customers and bad-fit customers
- Existing content that already converts
- Topics they do not want to target

If the user has not done this yet, offer to help research positioning using the company website, competitor pages, reviews, forums, and web search.

### 5. Verify HarborRank MCP

After the user has described the company, website, goals, and positioning, check that HarborRank MCP is configured and mapped to the right project:

1. Use `whoami` if available.
2. Use `list_projects` to confirm the user can access projects.
3. Match the project to the website/domain they want to rank for.
4. If the project list is ambiguous, ask the user which project should be used. If no project matches the site, offer `create_project`. Free and Basic plans include one project, so if the only project belongs to a different site, ask the user before replacing or reusing it.
5. If the MCP is unavailable, follow Step 0: give the user the connection steps and continue setup in fallback mode.

Do not run research tools just to test connectivity; `whoami` and `list_projects` are enough.

### 6. Connect Google Search Console

GSC is the richest first-party signal: existing impressions, near-ranking terms, cannibalization, and pages that already have search demand.

**Preferred (hosted): connect it natively.** On the project's Integrations page, connect Google Search Console and pull live data with `get_search_console_performance`. Once connected, the agent reads it directly in `keyword-research` and `keyword-clustering` — no manual files to maintain.

**Fallback (self-hosted, or if the user prefers files):** ask the user to export CSVs from Search Console into the SEO working folder.

Recommended exports:

- Queries: last 3 months and last 16 months if available
- Pages: last 3 months and last 16 months if available
- Query + page combinations when possible
- Countries/devices if relevant

Ask them to drop files into `gsc/` and use names like:

```text
gsc/queries-last-3-months.csv
gsc/pages-last-3-months.csv
gsc/queries-last-16-months.csv
gsc/pages-last-16-months.csv
```

### 7. Inventory existing assets

Ask for or discover:

- Sitemap or important URL list
- Current blog/resources/content library
- Product/category/feature pages
- Existing keyword lists
- Current rank trackers
- Backlink or PR assets
- Linkable assets such as studies, templates, tools, datasets, calculators, or original opinions

### 8. Recommend first workflow

After intake, recommend one next HarborRank workflow:

- `keyword-research`: when the user needs ideas from seed topics
- `keyword-clustering`: when they have keywords or GSC data to map to pages
- `competitive-landscape`: when the market is unclear
- `competitor-analysis`: when they know a competitor to study
- `link-prospecting`: when they have a linkable asset or target page

## Output format

Use a checklist with statuses:

| Step | Status | Notes | Next action |
| ---- | ------ | ----- | ----------- |

Then summarize:

- Working folder
- HarborRank MCP/project status
- Sites in scope
- Goals
- Known positioning
- Uploaded data/files

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Use the step 8 choice.
- **Check back:** end with one dated follow-up: the date (today plus 7 days, written out, for example "Monday, November 9") and the exact question to ask then: "What should I work on first for <site>?" Say in one line why it needs that wait: by then Search Console has a week of data for the coach to start from. Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the checklist and summary in the folder's `README.md`, and the site, market, audience, competitors, goals and constraints in `seo-context.md` in the format the `seo-context` skill defines, which every later workflow reads first. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved.

## Guardrails

- Keep setup lightweight. The user should feel oriented, not assigned homework.
- Do not pretend a GSC CSV has been uploaded unless you can see it, and do not claim Search Console is connected unless `get_search_console_performance` confirms it (it returns a "not connected" message otherwise).
- Keep project setup focused on setup and context unless the user asks for live research.
- If web search or scraping is used for positioning research, distinguish source evidence from inference.
