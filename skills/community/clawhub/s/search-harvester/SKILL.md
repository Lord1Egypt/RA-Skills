---
name: search-harvester
description: Candidate discovery for link building and outreach. Harvests candidate URLs from DuckDuckGo HTML and Marginalia through a local privacy-preserving Tor circuit (server IP never contacts the engine), then dedupes, triages liveness/anti-bot barriers, and exports a scored candidate list. DISCOVERY ONLY — this skill never submits forms, posts listings, or performs any state-changing action on third-party sites. Use ONLY when the user explicitly asks to find directories, submission platforms, blogs, or link-building candidates (e.g. "find more places to submit", "find directories", "get candidate websites like scrapebox", "search for link building opportunities"). Requires explicit user confirmation before routing any query through Tor; never for generic web search, never for sensitive/personal queries.
metadata:
  version: 1.0.2
  openclaw:
    requires:
      bins:
        - tor
        - curl
        - python3
        - nc
    os:
      - linux
    homepage: https://github.com/toniilic/scraper-skill
    permissions:
      network:
        - "Outbound HTTP(S) via local Tor SOCKS5 127.0.0.1:19050 only: the configured search engines (html.duckduckgo.com, search.marginalia.nu) and liveness triage fetches of harvested candidate URLs. No other external endpoints."
      process:
        - "tor (local daemon, run as current user — no root)"
        - "curl (fetches through the Tor SOCKS proxy)"
        - "nc (control-port NEWNYM rotation signal)"
        - "python3 (the bundled discovery script)"
      fs:
        read:
          - "optional --queries-file (user-supplied query list)"
        write:
          - "explicit --out report path only; refuses to overwrite without --force"
---

# Search Harvester

Discover candidate websites (directories, submission platforms, blogs, listicles) for link building and outreach. Queries are sent through a **local, privacy-preserving Tor circuit**, so the server's datacenter IP never contacts the search engine directly. This is a scoped, user-initiated **discovery-only** tool — it harvests and triages candidates but **never submits to, posts on, or changes anything on third-party sites**.

> Direct searches from datacenter IPs (Hetzner, AWS, DO...) are aggressively captcha-walled (verified Aug 2026: Google /sorry, DDG "select all ducks", Brave 429, Ecosia 403, Bing useless results). Tor exits get real results from DuckDuckGo HTML and Marginalia; Marginalia is explicitly built for privacy-preserving and automated search, which makes it the safest primary engine.

## ⚠️ Security, Privacy & Legal — READ BEFORE USE

1. **Traffic passes through third-party Tor exit nodes.** Your queries and the URLs you fetch are visible to exit operators. **Never** route sensitive, personal, client-identifying, or proprietary queries through this skill.
2. **Consent is mandatory.** Before the first Tor query, confirm with the user: "This will send N search queries through the Tor network (queries visible to exit operators) — OK?" Run the bundled script only after explicit consent (`--yes` after consent; the script refuses to run non-interactively without it).
3. **Automated queries may violate engine ToS.** DuckDuckGo HTML and Marginalia tolerate low-volume automated access; Google/Brave/Bing/Ecosia do not and are NOT used by this skill. Keep volume low and rate-limited (one query per exit, 3-10s pacing, hard rotation cap). Review local law and each engine's terms before deploying.
4. **Output files contain your queries and harvested URLs.** The export is written only to the explicit `--out` path (never auto-overwrites without `--force`), and **prefer a private output directory** (e.g. `~/harvest/` or a project dir) over world-readable `/tmp`. Treat the report as sensitive prospecting data: review before sharing.
5. **Discovery only — no submissions.** This skill finds and triages candidates. It does NOT submit listings, POST forms, upload files, or perform any other state-changing action on third-party sites. If a downstream submission step is desired, that is a separate workflow requiring its own explicit per-site consent.
6. **Scope is narrow.** If the task isn't explicitly link-building/discovery, don't activate this skill — use normal search tools.

## When to Use

- User explicitly asks to find/submit to directories: "find more places to submit", "find directories", "get candidate websites", "search for link building opportunities"
- Batch candidate discovery for a new site (directory listicles, submission pages)
- Replacing research sweeps that hit captcha walls — **only when the user asks for this specific workflow**

**Not for:** generic search queries, answering factual questions, personal/private lookups, submitting to or posting on any site, or any query the user wouldn't want routed through Tor. If in doubt, ask first.

## Capabilities & Guardrails (permission declaration)

| Capability | Scope |
|---|---|
| Network | Local Tor SOCKS5 `127.0.0.1:19050` only — outbound HTTP(S) to the configured search engines (html.duckduckgo.com, search.marginalia.nu) + triage fetches of harvested candidate URLs. No other external calls. |
| Process execution | `tor` (local daemon, current user — no root), `curl` (fetches via SOCKS), `nc` (control-port NEWNYM signal), `python3` (the bundled discovery script). |
| File reads | Only the optional user-supplied `--queries-file` and the skill's own documentation. No local project files, no vault access. |
| File writes | Only the explicit `--out` markdown report path; refuses to overwrite without `--force`. Temporary config in `/tmp` (user-owned). |
| Data sent out | Only the search queries and candidate-URL triage fetches described above — through the local Tor circuit. Nothing is sent to any other endpoint. |
| State-changing actions | **NONE.** No form submissions, no POSTs, no uploads, no listings, no account creation. This skill only reads search results and fetches pages for triage. |
| Guardrails | Consent gate before first query, hard rotation cap (max 3 per query), one query per exit node, pacing sleeps, no public HTTP proxies, discovery-only scope. |

## Setup (one-time, NO sudo)

Tor runs as the **current user** — no root required (SOCKS/control ports are high ports, DataDirectory is user-owned):

```bash
# Config at /tmp/tor-harvestrc (user-owned data dir under $HOME):
printf 'SOCKSPort 127.0.0.1:19050\nControlPort 127.0.0.1:19051\nDataDirectory %s/.tor-harvest\nLog notice file /tmp/tor-harvest.log\n' "$HOME" > /tmp/tor-harvestrc
mkdir -p "$HOME/.tor-harvest"

# Run as a background process (current user — no sudo):
tor -f /tmp/tor-harvestrc &

# Verify listening (no sudo needed to list ports):
ss -tln | grep -E "19050|19051"

# Verify exit IP:
curl -s -m 45 --socks5-hostname 127.0.0.1:19050 https://api.ipify.org
```

> ⚠️ The systemd `tor.service` is a multi-instance master that often shows "active (exited)". **Do NOT assume a port is down — probe first.** In practice (verified 2026-08) the default systemd instance listens on 127.0.0.1:9050 AND the dedicated harvest instance listens on 19050; both can be alive at once. If you need NEWNYM rotation you need the control port, which the dedicated instance provides on 19051 — the systemd master does not expose one. Fast probe: `curl -s -m 8 --socks5-hostname 127.0.0.1:<port> https://api.ipify.org` for each candidate port; use whichever answers. First boot needs ~30-60s to build a circuit before curl works. Never start it with `nohup tor ... &` from a login shell that then exits (silently dies) — use a proper background process (systemd user unit or `terminal(background=true)`).

## Harvesting (core loop)

**Consent gate (mandatory):** confirm with the user BEFORE the first query ("send N queries through Tor?") — then run.

```bash
# Rotate to a fresh exit node via control port:
(echo -e "AUTHENTICATE\r\nSIGNAL NEWNYM\r\nQUIT\r\n"; sleep 2) | nc 127.0.0.1 19051
sleep 12   # let the new circuit establish

# Query DDG html through Tor:
curl -s -m 30 --socks5-hostname 127.0.0.1:19050 \
  "https://html.duckduckgo.com/html/?q=%22submit+your+company%22+directory" \
  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" \
  -o /tmp/result.html

# Parse results (DDG uses /l/?uddg= redirect links):
python3 - <<'EOF'
import re, html as h, urllib.parse
raw = open('/tmp/result.html').read()
links = re.findall(r'href="//duckduckgo\.com/l/\?uddg=([^"]+)"', raw)
titles = re.findall(r'class="result__a"[^>]*>\s*([^<]+?)\s*</a>', raw)
for l, t in zip(links, titles):
    print(f"{h.unescape(t)[:70]} | {urllib.parse.unquote(l)}")
EOF
```

**Block recovery (not evasion — capped and polite):** some Tor exits are flagged by DDG (403 or 508-byte anomaly page). On ANY non-200 or 0-results response, rotate NEWNYM + sleep 12 + retry, **up to a hard cap of 3 rotations** per query, then accept the engine as unavailable for this run and stop. DDG also blocks the second query from the SAME exit — always rotate between queries. If *every* exit returns the anomaly page, DDG is rate-limiting the whole Tor pool: **stop for 30-60 min** (do not keep retrying) or switch to `--engine marginalia`.

**Rate limiting (compliance-critical):** one query per exit node, then rotate. Space queries 3-6s minimum. For 20+ queries, batch with sleeps; DDG tolerates ~1 query/10s per exit. Never scale this up — the skill is a low-volume discovery tool by design.

## Marginalia (primary-safe engine)

```bash
curl -s -L -m 30 --socks5-hostname 127.0.0.1:19050 \
  "https://search.marginalia.nu/search?query=%22submit+your+company%22" \
  -A "Mozilla/5.0" -o /tmp/mg.html
```
Parse `<a href="https://...">Title</a>` blocks, filtering out marginalia/github/creativecommons URLs. Marginalia is built for privacy-preserving/automated search, is the most tolerant of Tor exits, and its index (niche/old-web) surfaces directory listicles that DDG misses. Its result pages are `noindex` — fine for discovery, not for the final link. **Prefer Marginalia; use DDG HTML only when Marginalia returns nothing.**

## Engine Status (tested Aug 2026 via Tor)

| Engine | Result | Notes |
|--------|--------|-------|
| search.marginalia.nu | ✅ 200 + results | Preferred — privacy-preserving engine, tolerates automation |
| html.duckduckgo.com | ✅ 200 + results | Secondary. Rotate on 403/0-results; stop on whole-pool degradation |
| www.bing.com | ⚠️ 200, 0 results | Not usable via curl — skip |
| search.brave.com | ❌ 429 always | Not used |
| google.com | ❌ | /sorry captcha — not used |
| ecosia / startpage / presearch / yandex / searxng | ❌ | 403/302/captcha walls — not used |

**Public HTTP proxies are NOT used (removed in v1.0.1):** free proxy lists (proxyscrape etc.) are unreliable and the proxies themselves are untrusted third parties that can see your traffic — strictly worse than Tor for privacy. Tor is the only transport.

## Query Design (ScrapeBox-style)

Generate query VARIATIONS, not one search per topic:
- `"submit your company"` / `"add your company"` / `"submit a company listing"` / `"get listed"`
- + niche qualifiers: `directory`, `free`, `web development`, `software agency`, `IT services`
- + intent qualifiers: `submit`, `add url`, `list your business`, `advertise`
- + platform families: `"submit your startup"`, `"submit your app"`, `"submit your tool"`, `"list your product"`
- + listicle finders: `"free directory list"`, `"best directories to submit"`, `"places to submit your site"`
- One query per exit node, rotate between queries.

## Candidate Scoring (after harvest) — DISCOVERY ONLY

For each harvested URL, quickly triage before visiting:
1. **Liveness**: `curl -o /dev/null -w "%{http_code}" <url>` via Tor — 000/526 = dead, 403 = alive-but-CF-walled, 200 = check content
2. **Parked detection**: 200 + registrar/for-sale title (GoDaddy `forsale.godaddy.com`, "Click here to Buy", `/lander` JS redirect) = dead domain, skip
3. **Relevance**: does the page appear to accept company/website submissions? (submit/add/register path present?)
4. **Barrier**: reCAPTCHA v2 = manual; invisible recaptcha = manual; Turnstile-missing-iframe = manual; no captcha = potentially automatable elsewhere

**⚠️ Invisible reCAPTCHA = the silent killer (verified 2026-08 SuperbCompanies, TopDevelopers).** Invisible v2 has NO widget on screen — the form looks clean and even fills perfectly, but on submit the `g-recaptcha-response` token never populates from a datacenter IP (low score), so the site's validation silently fails ("all fields required" / nothing happens / same URL). Before burning tool calls on a "React form bug", run this JS in the page:
```js
(() => {
  const token = document.querySelector('textarea[name="g-recaptcha-response"]');
  return {
    hasGrecaptcha: typeof window.grecaptcha !== 'undefined',
    recaptchaIframes: [...document.querySelectorAll('iframe')].filter(f => (f.src||'').includes('recaptcha/api2/anchor')).length,
    token: token ? (token.value ? token.value.slice(0,20) : 'EMPTY') : 'NO_ELEMENT'
  };
})()
```
`hasGrecaptcha:true` + recaptcha anchor iframe + `token:"EMPTY"` = invisible reCAPTCHA wall → mark the candidate as MANUAL tier. Distinguish from a genuine form bug: if the input DOM values are correct after real typing AND there's a recaptcha iframe, it's the captcha, not the form.

**⚠️ Curl triage is a PRE-FILTER, not a guarantee (verified Aug 2026):** a curl-via-Tor 200 with no captcha signatures does NOT mean the site is browser-submittable — and **submitting is out of scope for this skill anyway**. Expect heavy attrition: of ~25 candidates that triaged as reachable/no-captcha, only a handful were actually submittable — most had login/account gates, paid upsells, or email-verification requirements. This skill's job is to hand the human a ranked candidate list; the submission step (if any) is a separate workflow with its own per-site consent.

Output a ranked markdown list: `# | candidate | URL | liveness | barrier | tier (promising / manual / skip)`.

## Bundled Script

`scripts/search-harvester.py` automates the whole loop: rotate-before-each-query, capped retry-on-block, dedupe, optional liveness triage, markdown export. **Discovery only — it never POSTs or submits anything.**

```bash
# After the user has explicitly consented to Tor routing:
python3 scripts/search-harvester.py '"submit your company" directory' '"add your company" free listing' \
  --engine marginalia --max-rotations 3 --triage --out ~/harvest/harvest.md --yes

# Human at the keyboard: omit --yes and the script prompts for confirmation.
```

**Safety flags (v1.0.1+):** the script REFUSES to run non-interactively without `--yes` (which you pass only after user consent). It prints the privacy warning and the query plan before starting. `--out` refuses to overwrite an existing file unless `--force` is given, and the save message reminds you the file contains queries + harvested URLs (review before sharing; use a private output dir).

Requires: tor on 127.0.0.1:19050 + control port 19051, curl, Python 3 stdlib only.

## Pitfalls

- **Consent first.** Confirm Tor routing with the user before the first query, not after.
- **Don't hammer one exit node** — one query per exit, then NEWNYM. DDG 403s the second query from the same exit.
- **Harvester runtime scales badly — run in background for 6+ queries (verified 2026-08).** Each query costs rotate (12s) + fetch (up to 30s) + retry sleeps; 9 queries with `--max-rotations 3` exceeded a 400s foreground timeout and the killed process wrote NOTHING because output is only flushed at the end via `--out`. For any run with more than ~5 queries: `terminal(background=true, notify_on_complete=true)` and poll the session; or split into batches of 3-4 queries per foreground call. The script prints progress per query to stdout, so `poll` shows live status even before `--out` is written.
- **First circuit takes 30-60s** — don't declare Tor broken until bootstrap completes ("Bootstrapped 100%" in tor log).
- **`nohup tor ... &` from a login shell silently dies** (no process, empty log). Use a background process manager or `terminal(background=true)`.
- **Search engines interpret bare words oddly** (Bing turned "add" into ADHD medical results). Always quote phrases: `"add your company"`.
- **Don't mass-probe invented domain names** — only harvest from engine results + curated lists. Random guesses are almost all parked domains.
- **Listicle mining returns heavy AI-tool-directory noise (verified Aug 2026):** mining startup-directory listicles (digitalbiztalk, enumhq, startup-list.org) surfaces 100+ domains where ~80% are AI-tool directories (aipure, aitoolhunt, tooldirectory.ai, futuretools.io…) that only accept AI *products*, not service businesses or dev studios. Filter BEFORE triaging: drop anything matching `ai|tool|gpt|llm` in the domain unless the target site itself ships an AI product, and dedupe against known blocks (producthunt/hn/indiehackers/saashub/uneed = manual-tier anyway). The 20% that remain (startupstash, tinystartups, launchingnext, promoteproject, alltopstartups, betapage…) are the real triage list.
- **SearXNG public instances are rate-limited/403 from datacenter IPs** — don't rely on them as a rotation layer.
- **Curl-triage is optimistic about walls** — LaunchingNext.com passed curl-via-Tor (200, no captcha sigs) but the real browser hit Cloudflare "Just a moment". Use curl triage as a pre-filter only; verify with a real browser before acting on any candidate.
- **But the reverse happens too: curl-via-Tor 403 ≠ browser-blocked.** blog.duda.co 403'd through Tor (twice, even after NEWNYM) yet loaded fine in the real browser, yielding the full 10-directory listicle. Tor exit IPs are themselves flagged by CF — a 403 from a Tor exit only proves that exit is blocked, not the site. For high-value listicles/directories that curl-via-Tor 403s, try the real browser before writing the candidate off.
- **"Alive" ≠ actually useful** — AllTopStartups is paid-only now (Stripe/PayPal), Uneed.best is product-only (no services), Unixtools.com is a dead email-capture page. When triaging, check three things: does a real submit form exist, is it free, and does it accept service businesses (not just products)?
- **DDG degradation mode: 200 + empty result sets (verified Aug 2026):** after extended Tor harvesting, html.duckduckgo.com starts returning HTTP 200 with a shell page containing zero `result__a` elements — no 403, no anomaly signature. The script's retry loop treats this as "0 results" and rotates, but if *every* exit returns it, DDG is rate-limiting the whole Tor pool for the session. **Stop for 30-60 min and retry, or switch to `--engine marginalia`** (Marginalia is far more tolerant of Tor exits and returned 200 + real links even when DDG was degraded).
- **Non-UTF8 bytes crash triage (fixed Aug 2026):** `search-harvester.py` `fetch()` previously used `text=True` (strict UTF-8 decode) — a single latin-1/gzip byte in any triaged response killed the entire run with `UnicodeDecodeError`. The script now decodes `errors="replace"`. If you see `UnicodeDecodeError` in an old copy, re-pull the script from the repo.
- **Marginalia returns 302 without `-L`** — always follow redirects (`curl -s -L`), or the harvest script's fetch already handles it. Raw 302 probe = "code=302 size=145", not a block.
- **Don't fight the harvest for the Tor circuit** — while `search-harvester.py` runs in the background, manual `SIGNAL NEWNYM` rotates from other shells make the script's exits inconsistent (000s, wrong-IP retries). Wait for the background run to finish before doing manual Tor fetches.
- **Use a private output directory.** Default examples use `/tmp`; for real runs prefer `~/harvest/` (chmod 700) — reports contain your queries + candidate URLs.

## Verification

- Confirm the exit IP actually changed after NEWNYM: `curl --socks5-hostname 127.0.0.1:19050 https://api.ipify.org` before/after.
- Confirm a result page contains `result__a` (DDG) or real anchors (Marginalia) before counting the harvest as successful.

## Related

- `seo-and-link-building` — the parent workflow. This skill feeds it a ranked candidate list.
- `directory-submission` — a SEPARATE skill/workflow for the submission phase; run it only with explicit per-site user consent. This skill (search-harvester) does NOT submit anything.
- `references/clawhub-publishing.md` — ClawHub package format, `metadata.openclaw` frontmatter, category slugs, and GitHub-import rules (see the scraper-skill repo root).
