---
name: website-audit
description: Audit a website across technical SEO, security headers, performance, accessibility, and content quality, and produce a prioritized report where every finding is backed by measured evidence. Use this skill whenever the user asks to audit, review, check, scan, or "health check" a website or URL, asks why a site is slow, not ranking, insecure, or inaccessible, or wants a technical SEO, Core Web Vitals, security header, or WCAG review, even if they only mention one of these areas. Also use it to compare a site before and after changes.
---

# Website Audit

Audit a public website across five areas (SEO, security, performance, accessibility, content) and deliver a report the owner can act on. This is technical work where a wrong claim sends someone to "fix" a problem that does not exist, so the job is to **measure, then interpret**: scripts collect facts, you explain them. A short honest report beats a long confident one.

## Evidence rules (read these first)

These exist because the failure mode of an AI audit is plausible-sounding invention.

1. **Every finding traces to evidence you can quote**: a field from script output, a header value, an HTML snippet, or a URL with its status. If you cannot point to it, do not write it.
2. **Never fill gaps from memory or "typical" setups.** Do not say a site uses WordPress, Cloudflare, nginx, or a given framework unless a header, meta tag, or file name in the output says so, and then quote it.
3. **Never state a number you did not get from a script.** Counts, sizes, timings, and percentages are copied from JSON output or from `merge_reports.py`, not estimated or recounted by hand.
4. **Missing means missing in what was observed.** "No CSP header on this response" is true. "The site has no CSP" is not, unless several pages agree. Use the wording the script's `message` uses.
5. **A failed or skipped check is a finding about coverage, not a pass.** If a script errored, was blocked, or the tier does not allow it, list it under "What was not checked". Never write "no issues" for something that was not run.
6. **No outcome claims.** Do not say a fix will improve rankings, speed, or conversions. Say what the defect is and the standard fix.
7. **No guessed vulnerabilities.** A version string in a file name is a lead, not proof. Say "possibly outdated, check advisories". Call something vulnerable only if you verified a specific advisory and can cite it.
8. **Fixes must match what you observed.** Give the generic fix (the exact header or tag). Give stack-specific instructions only if the stack is evidenced in the output; otherwise say the stack was not identified.
9. **Show your uncertainty in the labels.** Use the confidence field (below). Do not upgrade `needs_manual_check` or `likely` to certain in the prose.

## Ground rules

- **Passive and read-only.** Scripts send ordinary GET/HEAD requests, cap their volume, and refuse private addresses unless the user owns the site and you pass `--allow-private`. Do not port-scan, fuzz, guess hidden paths, attempt logins, or send payloads. This is not a penetration test.
- **Stay polite.** Same-origin, about 10 representative pages unless asked for more, and the scripts' built-in delays and caps stay on.

## Scripts

All are in `scripts/`, use only the Python standard library, and print JSON. Run them with `python3`. Each issue in the output has `id`, `category`, `severity_hint`, `confidence`, `message`, and `evidence`/`examples`.

| Script | Does | Needs tier |
|--------|------|-----------|
| `detect_env.py <url>` | Tests whether this environment can reach the target; reports tier and tools | any |
| `check_headers.py <url>` | Redirects, http→https, TLS, security headers, cookies, delivery headers | B |
| `check_html.py <url>` or `--file` | SEO, accessibility, content and static performance signals of one page | B (or A with `--file`) |
| `check_links.py <url>` | Status codes and redirect chains of links on a page | B |
| `check_crawl.py <origin>` | robots.txt, sitemap(s), security.txt | B |
| `check_rendered.py <url>` | Core Web Vitals (lab) and rendered accessibility via Lighthouse | C |
| `merge_reports.py *.json` | Combines outputs; computes counts and cross-page duplicates | any |

## Workflow

### 1. Scope
Confirm the target URL. Choose pages to sample: homepage, one or two top templates (article, product, category), and anything the user cares about. If the user named one area, run that area and still mention anything glaring from the others.

### 2. Detect the tier
Run `python3 scripts/detect_env.py <url>`. Do not assume network access; the script tests it with a real request.

- **Tier A**: scripts cannot reach the target. Use the page-fetch tool only. Static checks from the reference files can be done by hand on fetched HTML, quoting what you saw; header, redirect, TLS and link checks are **Not checked**. Say why, and quote the network error from the output.
- **Tier B**: scripts can reach the target. Run them.
- **Tier C**: B plus a browser or Lighthouse. Run `check_rendered.py` for lab Core Web Vitals and rendered accessibility (including contrast). Its numbers are one emulated lab run — label them that way, and if it returns `not_checked`, rendered checks are **Not checked**, not passed.

If the output has `proxy_variables_set` or `tls_interception_suspected`, the environment sits behind a proxy or TLS inspection. Report TLS certificate details as unconfirmed, and suggest re-running from another network.

### 3. Collect
Create a working folder and save each script's JSON there, one file per page per script:

```
python3 scripts/check_crawl.py  https://site.example  > work/crawl.json
python3 scripts/check_headers.py https://site.example/ > work/headers-home.json
python3 scripts/check_html.py    https://site.example/ > work/html-home.json
python3 scripts/check_links.py   https://site.example/ > work/links-home.json
python3 scripts/check_rendered.py https://site.example/ > work/rendered-home.json   # Tier C only
```
Repeat `check_html.py` for each sampled page. A non-zero exit with `"status": "not_checked"` means the check did not happen; keep that file, because `merge_reports.py` lists it under not checked.

### 4. Merge
`python3 scripts/merge_reports.py work/*.json > work/merged.json`. This gives distinct issues sorted by severity, how many pages each affects, duplicate titles/descriptions/H1s across pages, coverage, and the not-checked list. Take all counts from here.

### 5. Interpret
Read the matching reference file for areas in scope: `references/seo.md`, `security.md`, `performance.md`, `accessibility.md`, `content.md`. They say what each script covers, what it cannot see, and how to word findings.

- **severity_hint** is a deterministic starting point. You may adjust it only with a stated reason tied to evidence (for example `canonical.differs` is low by default, but if the evidence shows every page canonicalizing to the homepage, say so and raise it).
- **Confidence** values: `verified` (direct evidence), `likely` (strong signal that depends on something unobserved), `needs_manual_check` (cannot be confirmed here). Keep the label in the report.

Severity meanings: **Critical** blocks users, indexing or safety; **High** significant harm probably affecting many pages or users; **Medium** real but bounded; **Low** hygiene.

### 6. Report
Fill `assets/report-template.md`. Write in the language the user is using and translate the headings. Put the few most important findings first. Group repeats ("14 pages share this title") using the merged output. Always fill "What was not checked" from the merged `not_checked` list plus anything a tier prevented (for example Core Web Vitals, contrast, keyboard use).

## Finding format

```
### [Severity] Short title  (Confidence)
- Where: URL(s) or "site-wide"
- Evidence: the quoted header / snippet / measurement from the output
- Why it matters: one sentence, no exaggeration
- Fix: the specific change
```

## Done when
Every in-scope area has findings, an explicit "no issues found in the checks performed" tied to which checks ran, or a "Not checked" entry with the reason. The report states the tier, the pages sampled, and the date.
