---
name: seo-context
description: "Capture the facts every SEO workflow needs in one short file, seo-context.md: the site, market and language, audience, what the business sells, main competitors, goals and constraints, and the HarborRank project to use. Every other HarborRank skill reads it first, so answers fit the business instead of starting from zero each session. Use when the user starts SEO work on a site, says the agent keeps asking the same questions, wants to update their goals or competitors, or before running several workflows on a new client."
---

# HarborRank SEO Context

## Goal

Write and maintain `seo-context.md`: one page of facts about the site that every other workflow reads before it asks the user anything. It takes about five minutes, and it saves the same questions in every later session.

This is the short version of `seo-project-setup`. Use `seo-project-setup` when the user also wants a working folder, Search Console exports and an asset inventory; use this skill when they only need the context file, or want to update it.

## Step 0: Check connection

This skill works without HarborRank: it only needs the user's answers and what you can read on their site. If HarborRank tools are loaded (look for `list_projects` or `whoami`, including deferred tools you can load; the name may carry a prefix such as `mcp__harborrank__`), use `whoami` and `list_projects` to fill in the project. Both use no credits. Do not call research tools here.

If HarborRank isn't connected, write the file without the project line and mention once that connecting HarborRank adds live search data to every workflow (new accounts start with a 7-day free trial). Do not stop for it.

## Where the file lives

In the project's SEO folder if there is one (see `seo-project-setup`), as `seo-context.md`. If there is no folder, ask once where to save it; suggest `~/SEO/<site>/seo-context.md`. If the user prefers a doc and a docs tool is available, use that instead and tell them where it is. If the file already exists, read it, show what is there, and update only what changed.

## Workflow

1. **Read before asking.** If the user names the site, read its homepage and one or two key pages (pricing, services, about) with your web tools. Fill in what the site says plainly, and mark it "from the site" so the user can correct it.
2. **Ask only for what you couldn't find**, in one short batch:
   - Who the customers are, and who is a bad fit
   - The market: countries, languages, and for a local business the towns or area served
   - Main competitors, including the ones that outrank them in search
   - Goals with a number and a date, for example "20 leads a month from Google by March"
   - Constraints: topics to avoid, claims they can't make, regulated wording, brand voice
3. **Match the HarborRank project.** With HarborRank connected, call `list_projects` and pick the project whose domain matches the site. If several fit, ask. If none does, note it; `seo-project-setup` can create one.
4. **Write the file** in the format below. Keep it to one page; link to longer documents instead of copying them in.
5. **Confirm it with the user**, then save it. Tell them every HarborRank workflow will read it first, and that they can say "update my SEO context" any time.

## File format

```markdown
# SEO context: <site>
Updated: <YYYY-MM-DD>

## Site
- Domain: <domain> (plus subdomains or other sites in scope)
- What it sells: <products or services, one line each>
- Money pages: <the pages that convert, with URLs>
- HarborRank project: <project name> (<projectId>), or "not connected"

## Market
- Countries and languages: <e.g. US, English>
- Local area (if local): <towns, radius, service area>

## Audience
- Best customers: <who, what they need, how they search>
- Bad fit: <who to avoid attracting>

## Competitors
- <domain>: <why it matters: outranks us for X, same offer, local rival>

## Goals
- <metric, target, date>

## Constraints
- <topics to avoid, claims not allowed, voice notes>
```

Dated follow-ups don't go here: workflows keep them in the `Follow-ups` list of the SEO folder's `README.md`.

## How other workflows use it

- `keyword-research`, `keyword-clustering` and `content-brief` use the audience, market and money pages to judge intent and fit.
- `competitive-landscape` and `competitor-analysis` start from the competitor list.
- `local-seo` uses the local area.
- `client-seo-report` reports against the goals.
- `seo-coach` reads this file together with the README's Follow-ups list.

When a workflow learns something new (a competitor, a goal that changed), it offers to update this file rather than keeping the fact in chat.

## Output

- The saved file and where it is.
- **Next workflow:** one recommendation, the reason and the input it starts from. With Search Console connected and data in it, recommend `keyword-research` on striking-distance queries (positions 5 to 20). Without it, recommend `seo-audit` to check the site is crawlable, or `competitive-landscape` if the competitors are unclear.

## Guardrails

- Never invent facts about the business. Anything not stated by the user or visible on their site is left blank or marked "unknown".
- Don't store passwords, API keys, customer data or anything private in the file.
- Keep it short. If it grows past a page, move detail into linked files.
- Ask before overwriting an existing file; show the changes first.
