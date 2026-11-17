---
name: search-harvester
description: ScrapeBox-style candidate discovery for link building and outreach. Rotates Tor exit nodes (and optionally public HTTP proxies) so the server's datacenter IP never touches the search engine, harvests candidate URLs from multiple engines (DuckDuckGo html, Marginalia), dedupes, triages liveness/barriers, and exports a scored candidate list. Use when the user says "find more places to submit", "find directories", "scrape search results", "get candidate websites like scrapebox", "search for link building opportunities" — or whenever direct search from the server IP gets captcha/bot-blocked (Google, Brave, DuckDuckGo, Bing all block datacenter IPs).
metadata:
  version: 1.0.0
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
---

# Search Harvester (ScrapeBox-style)

Discover candidate websites (directories, submission platforms, blogs) by querying search engines THROUGH rotating exit IPs, so the server's own IP never gets banned. Direct searches from a Hetzner datacenter IP are ~100% captcha-walled (verified Aug 2026: Google /sorry, DDG "select all ducks", Brave slider, Ecosia 403, Bing ADHD-garbage). Tor rotation fixes this: DDG html and Marginalia return real results through Tor exits; ~2/3 of fresh exit nodes are clean, so a rotate-and-retry loop is required.

## When to Use

- User asks to find/submit to directories, "find more places to create links", "get candidate websites"
- Any search-engine query that gets blocked from the server IP
- Batch candidate discovery for a new site (directory listicles, submission pages)
- Replacing `delegate_task` research sweeps that hit captcha walls

## Core Architecture

```
Server IP (NEVER touches engines)
   └─ Tor SOCKS5 127.0.0.1:19050 (exit IP rotates per query)
        ├─ html.duckduckgo.com  ✅ works (200 + real results)
        ├─ search.marginalia.nu ✅ works (200 + real results, small index)
        └─ search.brave.com     ❌ 429 even via Tor
   └─ Optional: public HTTP proxies (mostly dead — Tor is primary)
```

## Setup (one-time)

```bash
# Config at /tmp/tor-harvestrc:
#   SOCKSPort 127.0.0.1:19050
#   ControlPort 127.0.0.1:19051
#   DataDirectory /tmp/tor-harvest-data
sudo tor -f /tmp/tor-harvestrc        # run as background process
# Verify listening:
sudo ss -tlnp | grep -E "19050|19051"
# Verify exit IP:
curl -s -m 45 --socks5-hostname 127.0.0.1:19050 https://api.ipify.org
```

⚠️ The systemd `tor.service` is a multi-instance master that shows "active (exited)" and listens on NOTHING. Don't rely on `sudo systemctl start tor` / port 9050 — use the dedicated instance above. First boot needs ~30-60s to build a circuit before curl works. Never start it with `sudo -b nohup tor ...` (silently fails) — use a proper background process.

## Harvesting (core loop)

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

**Rotation-retry rule (verified Aug 2026):** ~1/3 of fresh Tor exits are already flagged by DDG (403, 508-byte anomaly page). After ANY non-200 or 0-results response, rotate NEWNYM + sleep 12 + retry. Up to 3 rotations before accepting an engine as blocked for this run. Also: DDG blocks the SECOND query from the SAME exit — always rotate between queries, not just after failures.

**Rate limiting:** one query per exit node, then rotate. Space queries 3-6s. For 20+ queries, batch with sleeps; DDG tolerates ~1 query/10s per exit.

## Marginalia (second engine)

```bash
curl -s -L -m 30 --socks5-hostname 127.0.0.1:19050 \
  "https://search.marginalia.nu/search?query=%22submit+your+company%22" \
  -A "Mozilla/5.0" -o /tmp/mg.html
```
Parse `<a href="https://...">Title</a>` blocks, filtering out marginalia/github/creativecommons URLs. Marginalia's index is small (niche/old-web) but it surfaces directory listicles that DDG misses. Its result pages are `noindex` — fine for discovery, not for the final link.

## Engine Status (tested Aug 2026 via Tor)

| Engine | Result | Notes |
|--------|--------|-------|
| html.duckduckgo.com | ✅ 200 + results | Primary. Rotate on 403/0-results |
| search.marginalia.nu | ✅ 200 + results | Secondary, small index, noindex pages |
| www.bing.com | ⚠️ 200, 0 results | Returns 200 but no result blocks via Tor curl — needs browser JS |
| search.brave.com | ❌ 429 always | Even via Tor |
| google.com | ❌ | /sorry captcha even via Tor |
| ecosia / startpage / presearch / yandex / searxng | ❌ | 403/302/captcha walls |

## Public Proxy Fallback

```bash
curl -s -m 15 "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=ipport&format=text&timeout=20000" | tr -d '\r' > /tmp/proxies.txt
# Test each proxy (200 = alive):
while read -r p; do code=$(curl -s -m 10 -x "http://$p" https://api.ipify.org -o /dev/null -w "%{http_code}"); [ "$code" = "200" ] && echo "$p ALIVE"; done < /tmp/proxies.txt
# Then: curl -x http://<ip:port> <engine-url>
```
Public HTTP proxies are mostly dead (verified: 2/8 alive from proxyscrape). Use only when Tor is unavailable. **Pitfall:** proxy lists end lines with `\r` — always `tr -d '\r'` before looping, or every proxy fails with 000.

## Query Design (ScrapeBox-style)

Generate query VARIATIONS, not one search per topic:
- `"submit your company"` / `"add your company"` / `"submit a company listing"` / `"get listed"`
- + niche qualifiers: `directory`, `free`, `web development`, `software agency`, `IT services`
- + intent qualifiers: `submit`, `add url`, `list your business`, `advertise`
- + platform families: `"submit your startup"`, `"submit your app"`, `"submit your tool"`, `"list your product"`
- + listicle finders: `"free directory list"`, `"best directories to submit"`, `"places to submit your site"`
- One query per exit node, rotate between queries.

## Candidate Scoring (after harvest)

For each harvested URL, quickly triage before visiting:
1. **Liveness**: `curl -o /dev/null -w "%{http_code}" <url>` via Tor — 000/526 = dead, 403 = alive-but-CF-walled, 200 = check content
2. **Parked detection**: 200 + registrar/for-sale title (GoDaddy `forsale.godaddy.com`, "Click here to Buy", `/lander` JS redirect) = dead domain, skip
3. **Relevance**: does the page accept company/website submissions? (submit/add/register path)
4. **Barrier**: reCAPTCHA v2 = manual; invisible recaptcha = manual; Turnstile-missing-iframe = manual; no captcha = automatable
5. **Score** candidates: free + no-captcha + relevant + live = TOP; paid/walled = skip; manual-tier = list for the human

Output a ranked markdown list: `# | candidate | URL | liveness | barrier | action (auto/manual/skip)`.

## Bundled Script

`scripts/search-harvester.py` automates the whole loop: rotate-before-each-query, retry-on-block, dedupe, optional liveness triage, markdown export.

```bash
python3 scripts/search-harvester.py '"submit your company" directory' '"add your company" free listing' \
  --engine ddg --max-rotations 3 --triage --out /tmp/harvest.md
```

Requires: tor on 127.0.0.1:19050 + control port 19051, curl, Python 3 stdlib only.

## Pitfalls

- **Don't hammer one exit node** — one query per exit, then NEWNYM. DDG 403s the second query from the same exit.
- **First circuit takes 30-60s** — don't declare Tor broken until bootstrap completes ("Bootstrapped 100%" in tor log).
- **`sudo -b nohup tor ...` silently fails** (no process, empty log). Use a background process manager.
- **Search engines interpret bare words oddly** (Bing turned "add" into ADHD medical results). Always quote phrases: `"add your company"`.
- **Don't mass-probe invented domain names** — only harvest from engine results + curated lists. Random guesses are almost all parked domains.
- **SearXNG public instances are rate-limited/403 from datacenter IPs** — don't rely on them as a rotation layer.

## Verification

- Confirm the exit IP actually changed after NEWNYM: `curl --socks5-hostname 127.0.0.1:19050 https://api.ipify.org` before/after.
- Confirm a result page contains `result__a` (DDG) or real anchors (Marginalia) before counting the harvest as successful.

## Related

- `seo-and-link-building` — the parent workflow (directory submission, article publishing, verification). This skill feeds it candidates.
- `directory-submission` — generating the submission copy per platform once candidates are live.
