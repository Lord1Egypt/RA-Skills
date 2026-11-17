---
name: seo-proposal
description: "For agencies and freelancers: build a full SEO proposal for a prospect who replied or a client the user is pitching. Covers the current state with numbers and sources (visibility, rankings, Google Maps position for local businesses, technical issues, competitors who outrank them), the opportunity (keywords and pages with volume and difficulty, a realistic range of outcomes, never guaranteed rankings or traffic), a 90-day plan with monthly deliverables, what the client must provide, how results will be reported, and pricing options the user supplies. Ends with the proposal doc and a short cover email. Reuses the lead's teardown when one exists. Use when the user asks for an SEO proposal, to pitch a client, a scope of work, an SEO audit for a prospect, to win an SEO client, or an agency proposal. For cold outreach to new local leads, use lead-teardown instead."
---

# HarborRank SEO Proposal

## Goal

Turn a prospect's domain (and, for a local business, its Maps listing) into a proposal the prospect can read in ten minutes and say yes to: where they stand today, what is realistically within reach, what the agency will do in the first 90 days, what the client must provide, how progress will be reported, and the pricing options the agency offers. Every number has a source. Every estimate is labelled as an estimate with its basis. Nothing promises rankings or traffic.

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

A lead that already has a teardown costs nothing to reuse: read it with `get_lead_teardown` and spend credits only on the evidence it lacks.

- If `creditsRemaining` will not cover the planned calls, give the user the estimate and ask before spending. Use the free tools first.
- If a tool replies that a feature "is included in paid plans", tell the user once which feature needs a paid plan and pass on the upgrade link from the reply, skip that tool for the rest of the run, and finish with the other evidence. Do not retry it.
- If a tool fails for insufficient credits, stop making paid calls, tell the user, and finish with free tools and the data you already have. If `whoami` warns that credits are low, say so before a large run.
- If a HarborRank tool says the free trial hasn't started, or that credits ran out, give the user the link from that reply exactly as written, as a clickable link, and wait for them to say they're done before calling HarborRank again. Don't switch to answering without HarborRank data unless they ask you to.
- If the user asks to upgrade, change plan or buy credits, call `get_upgrade_link` (no credits) and give them the link. They pay on HarborRank by card; never say the upgrade is done until `whoami` shows the new plan.
- When `whoami` returns `mode: "self-hosted"`, there are no plan gates.

### Fallback mode (no HarborRank connection)

Use this mode only when Step 0 finds no connection. It works from web search, page reading, and files the user provides.

**Can still do**

- Read the prospect's site: services, pages, titles, service area, calls to action, and obvious gaps. Name each page you read.
- Compare it with the sites that appear at the top of web search for the prospect's main service queries.
- Use any Search Console or Analytics exports the prospect has shared. Those figures are their own data; report them with the file as the source.
- Write the 90-day plan, the client requirements, the reporting section and the pricing section with the user's own prices, and the cover email.

**Must not estimate**

Traffic, search volume, keyword difficulty, CPC, keyword counts, rankings, backlink counts, Maps pack positions, and Q&A counts. Write `unknown` for each. A web search shows which pages appeared for a query when you searched, not their Google ranking: report it as "appeared in web search", never as a position.

**Output**

- Start with the label **Web-evidence only: no HarborRank data.**
- Name the source (URL or file) of every figure you report.
- End, after any recommended next workflow, with one sentence that names the numbers this report is missing: "Connect HarborRank (start with a 7-day free trial) to add the prospect's rankings, keyword volume and difficulty, competitor footprint and a site crawl to this proposal." Do not add more sales copy than that.

## Required inputs

- `projectId` (from `list_projects`): the project that holds the lead, or the agency's own project. Do not create a client project before the prospect signs.
- The prospect's domain, and for a local business its name and city or Maps listing
- What the prospect asked for or cares about (from their reply, a call, or the user)
- The agency's pricing options, deliverables it does and does not offer, and the sender's name. Ask once; if the user has no prices yet, leave `[price]` placeholders.

## HarborRank MCP tools

- `list_leads`, `get_lead_teardown`: find the prospect among saved leads and reuse its teardown (Maps positions from three points, top-three competitors, money keywords, site findings).
- `research_lead`: build the teardown for a saved local lead that has none. Requires a paid plan on hosted HarborRank.
- `get_domain_overview`: the domain's organic footprint (keywords, estimated traffic, top pages).
- `get_ranked_keywords`: the keywords and pages the domain ranks for, with position, volume, KD and ranking URL. The source for striking-distance terms (positions 5 to 20).
- `get_keyword_metrics`: volume, KD, intent and CPC for the target keyword list.
- `get_serp_results`: who ranks for the main service queries and what the top pages are.
- `get_local_serp_results`: the Maps pack for one keyword near a coordinate, for local businesses without a teardown.
- `find_serp_competitors`: the domains that compete across the target keyword set.
- `get_backlinks_overview`: backlinks and referring domains for the prospect and its top competitor. A preview on Free.
- `run_site_audit`, `get_audit_status`, `get_audit_issues`: crawl the prospect's site for technical issues. Crawls use no credits; Lighthouse needs a paid plan.
- `update_lead`: set the lead's status and notes once the proposal is sent.
- `create_share_report`: publish the finished work as a read-only page at a shareable link (see "Shareable report" below). Only after the user agrees.

## Workflow

If the project's SEO folder has `seo-context.md`, read it first for the site, market, audience, competitors and goals; otherwise ask only what this workflow needs.

1. Call `list_projects`, then `list_leads`. If the prospect is a saved lead with a teardown, read it with `get_lead_teardown` and the earlier email in `outreach/leads/<business-slug>.md`, so the proposal continues that conversation. If it is a local lead with no teardown, offer `research_lead` (paid plan) before the steps below.
2. Collect the inputs above. Tell the user which calls you plan and the approximate credit cost before spending.
3. Current visibility: `get_domain_overview` and `get_ranked_keywords` for the prospect's domain in its market. Note keyword count, the pages that earn the most, and the terms in positions 5 to 20.
4. Local businesses: take Maps positions from the teardown. Without one, run `get_local_serp_results` for the primary service keyword at the business location and record its position and who holds the top three.
5. Competitors: `find_serp_competitors` on the target keyword set, then `get_domain_overview` for the one or two that outrank the prospect most often. Add `get_backlinks_overview` for the prospect and the top competitor when links look like the gap.
6. Technical state: `run_site_audit` on the prospect's site, poll `get_audit_status`, then read `get_audit_issues`. Keep the issues that affect rankings or leads, with page counts. Skip if the teardown's crawl already covers the site and the prospect wants local work only.
7. The opportunity: build a target list of 10 to 30 keywords from the striking-distance terms, competitor-owned terms and the prospect's services. Hydrate it with `get_keyword_metrics` and check two or three of the main ones with `get_serp_results`. Group them into pages: existing pages to improve and new pages to build.
8. The range of outcomes: give a low and high case, never one number and never a guarantee. Base it on the data: the summed volume of the target keywords, the positions now, and the positions the top competitors hold. If you convert positions to visits, state the click-through assumption and label the result "estimate". Say what the range depends on (the client's approvals, content, reviews, competition).
9. The 90-day plan: month 1 fixes and foundations (top audit issues, tracking, Google Business Profile for local), month 2 the highest-value pages, month 3 the next pages, links or citations, and the first full report. List concrete deliverables per month that the agency actually offers.
10. Draft the proposal and cover email and show them to the user before saving, sharing or sending.

## Output format

Plain language for a business owner, each SEO term glossed once.

- **Summary:** three lines. Where they stand, the main opportunity, and what the first 90 days deliver.
- **Where you stand today:** visibility, rankings, Maps positions (local), technical issues, and competitors who outrank them, each with the number and its source (tool or file, date checked).

| Competitor | Keywords | Est. traffic | Referring domains | Where they beat you |
| ---------- | -------: | -----------: | ----------------: | ------------------- |

- **The opportunity:**

| Page (existing or new) | Target keywords | Volume | KD | Position now | Priority |
| ---------------------- | --------------- | -----: | --: | -----------: | -------- |

  Then the low and high case, labelled estimates, with the basis and what they depend on.
- **90-day plan:** month by month, deliverables only.
- **What we need from you:** access (Search Console, Analytics, site or CMS, Google Business Profile), a contact who approves content, photos or reviews for local, and turnaround times.
- **How we'll report:** a monthly report in plain language with clicks, impressions, positions, tracked keywords and conversions when Analytics is connected (built with `client-seo-report`), delivered as a shareable link.
- **Pricing options:** only the user's own options, in their words; `[price]` placeholders otherwise. Never invent the agency's prices.
- **Cover email:** about 120 words. The prospect's name, one finding from the proposal with its number, what the 90 days deliver, the link or attachment, and one clear next step (a call). No pricing beyond what the user approves.

- **Next workflow:** end with one recommended next workflow, the reason for it, and the input it starts from. Default: `seo-project-setup` once the prospect signs, so the work starts with goals, positioning and Search Console, using this proposal's keyword list. If the prospect is local, recommend `local-seo` for the Maps work in month 1 instead.
- **Check back:** end with one dated follow-up: the date (today plus 5 days, written out, for example "Monday, November 9") and the exact question to ask then: "Has <prospect> replied to the SEO proposal?" Say in one line why it needs that wait: prospects usually answer a proposal within a few days, and the lead's status stays in HarborRank (`list_leads`). Add it to the `Follow-ups` list in the SEO folder's `README.md` (create the list if it is missing) so the next session finds it. One follow-up only; don't add reminders or repeat it. If scheduled tasks are available (Cowork and the Claude apps on paid plans), offer once to make this a weekly scheduled task instead, named for the site, so the check runs by itself; the user reviews and confirms the schedule.
- **Where the output goes:** the proposal as `proposals/<prospect-slug>-<YYYY-MM-DD>.md` and the cover email as `proposals/<prospect-slug>-email.md`. Save it in the project's SEO folder (see `seo-project-setup`); if there is none, ask once whether to create one or where to save instead. If the user prefers a doc or a sheet and a docs or spreadsheet tool is available, put reports in a doc and tables in a sheet instead. Tell the user where it was saved. When the user sends it, `update_lead` with a note that the proposal went out.
- **Shareable report:** once the work is done, offer one time to publish the proposal as a shareable report with `create_share_report`: a read-only page at a link the prospect can open without signing in. Write it from this output: summary first, then the 90-day plan, then the supporting tables. Include pricing only if the user wants it on the page. Publish only after the user says yes, and never include the prospect's private contact details or account data. Give them the link to paste into the cover email; `delete_share_report` removes it.

## Guardrails

- Never invent a number. Every figure comes from a tool result, the teardown, or a file the user provided; write `unknown` otherwise.
- Never promise or guarantee rankings, traffic, leads or revenue. Ranges are estimates, labelled with their basis.
- Never invent the agency's prices, packages, deliverables or past results. Ask, or leave placeholders.
- Do not overstate the problem to win the deal. Report issues at their real scale, with page counts.
- State the credit cost before the research calls, and reuse the teardown before running new ones.
