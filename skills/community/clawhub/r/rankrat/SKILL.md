---
name: rankrat
description: Query Google Search Console, Google Tag Manager, Bing Webmaster Tools, GA4, Microsoft Clarity, PageSpeed, CrUX, Cloudflare analytics, and Bing backlink intelligence; manage typed tags and safe edge redirects; run Lighthouse and bounded whole-site/internal-link audits; persist monitors and issue history; automate ownership and finite remediation through one self-hosted MCP server. Speaks MCP over Streamable HTTP at /mcp, plus a FastAPI JSON API. Use when the user wants to inspect or improve SEO, indexing, ownership, internal links, tags, redirects, backlinks, browser scores, performance history, or search traffic for sites they control.
homepage: https://github.com/psyb0t/rankrat
user-invocable: true
metadata:
  openclaw:
    emoji: "🐀"
    requires:
      bins: [docker]
permissions:
  network: "outbound HTTPS to configured Google Search Console, Google Analytics, Google Tag Manager, Bing Webmaster Tools, Microsoft Clarity, PageSpeed/CrUX, Cloudflare, public DNS, public pages beneath configured sites, and IndexNow endpoints; optional Lighthouse browser traffic to explicitly requested bounded pages; inbound only on the port you bind."
  shell: "docker run invocations for the published image or the installed rankrat launcher; no other host access is required."
  filesystem: "reads provider-account config and credentials; writes the configured OAuth token store, persistent SQLite monitor state, locally initialized IndexNow key, and discovered resource inventory in the config file when writable."
---

# rankrat

A self-hosted MCP server over the SEO and search-analytics APIs you already have
accounts on (Google Search Console, Google Tag Manager, Bing Webmaster Tools,
GA4, Microsoft Clarity, and PageSpeed Insights), so an agent can read and,
when trusted, manage your own provider resources without you handing it a
browser session or a service-account key.

Install, credentials and the full environment reference:
[`references/setup.md`](references/setup.md).
For a human-readable operator manual organized by topic, use the public
[Rankrat documentation](https://psyb0t.github.io/rankrat/).

## Contents

- [Security and safety](#security-and-safety)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Usage](#usage)

## Security and safety

Configured provider credentials are Rankrat's authority. A Google OAuth account,
Bing key, Cloudflare token, or Clarity project token can reach every supported
resource that provider exposes to it. Resource arrays in the config are
discovered inventory and URL-containment data, not a second permission system.
Fixed provider origins, typed requests, public-URL validation, and child-URL
containment still apply.

Rankrat is **writable by default**. `RANKRAT_READ_ONLY=true` removes every write
tool from `tools/list` and every write route from runtime OpenAPI, including
site onboarding. This is the only capability switch. The human decides whether
the caller is a careful human-directed agent or a fully autonomous one; if that
caller should not mutate the account, run a read-only process.

Your provider credentials stay on the host running rankrat. Requests go to the
provider APIs over HTTPS. The optional Lighthouse companion opens only an
explicitly requested page beneath a configured PageSpeed site and receives no
provider credentials. Credentials, OAuth records and raw provider bodies are
never returned or logged. Bind Rankrat to loopback or a private network, and use
the bearer token if anything else can reach it.

## When to use

- Reading Search Console performance: queries, pages, countries, devices, dates
  (as raw rows, summaries, trends, period comparisons, or anomaly and
  traffic-drop attribution).
- Diagnosing indexing: URL inspection (single or batch), sitemap listings,
  crawl issues, crawl stats.
- Bing Webmaster Tools equivalents, plus keyword statistics, related keywords,
  ranking buckets, query/page opportunity reports and cannibalization analysis.
- GA4 reporting: realtime, content and landing-page performance, organic search
  landing pages, traffic sources, ecommerce, audience segments, user behavior,
  conversion funnels.
- Google Tag Manager account discovery plus typed containers, workspaces, tags,
  triggers, variables, versions, and publication in writable mode.
- Microsoft Clarity Data Export project insights in read-only mode.
- PageSpeed Insights, CrUX history, and fetching a page's structured-data schema.
- Whole-site crawling for deterministic metadata, canonical, robots, sitemap,
  duplicate-title, link, and structured-data findings with remediation text.
- Google/Bing ownership checks and narrowly scoped verification through the
  configured DNS adapter; Cloudflare is currently supported.
- IndexNow change notifications for bounded URLs. This is a writable push
  protocol, not a reporting dashboard or an indexing guarantee.
- Backlink intelligence from configured Bing Webmaster sites.
- Internal-link graphs, same-site orphan-page joins, lexical link suggestions
  limited to pages sharing normalized title/path tokens, and ranked content
  opportunities joined across search, analytics, and crawl data.
- Cloudflare hourly traffic/cache analytics, plus exact purges and two finite
  cache templates in writable mode. Template mutations are serialized per zone
  within the running Rankrat process.
- Provider-neutral managed edge redirects. Cloudflare is the current adapter;
  Rankrat never replaces unrelated provider rulesets.
- Safe Bing content submission: Rankrat fetches the bounded public HTML page
  itself rather than accepting caller-provided content or headers.
- Persistent site-audit monitors, immutable snapshots, issue lifecycle events,
  and explicit acknowledge/resolve operations. The background scheduler runs
  inside the long-lived HTTP process. Poll these tools because Rankrat does not send external notifications.
- Local Lighthouse performance, accessibility, best-practices, and SEO scores
  or category-specific failed findings when the companion worker is configured.
- Checking which providers are actually wired up (`provider_readiness`,
  `diagnostics`) before trusting a report.

## When NOT to use

- **Sites you don't control.** Everything is scoped to configured provider
  accounts and site boundaries. It is not a competitor crawler or arbitrary
  backlink scraper.
- **A caller that should not have account-wide write access.** Start that caller
  with `RANKRAT_READ_ONLY=true`; the write schemas will not be discoverable.
- **Realtime dashboards.** Provider APIs lag (Search Console notably so), and
  rankrat reports what they return.
- **Editing an arbitrary CMS or repository.** Audits return deterministic fixes;
  provider remediation resubmits sitemaps and URLs but does not rewrite pages.

## Usage

The MCP server runs from the published image. Read tools have a stable
discovery surface even when their provider is not configured; ask
`provider_readiness` before interpreting an empty or unavailable result. Only
write-tool discovery changes, and only with `RANKRAT_READ_ONLY`.

The public `rankrat` launcher runs HTTP through Docker Compose so Rankrat and
Lighthouse share one lifecycle. Connect MCP clients to
`http://127.0.0.1:8080/mcp` with the profile's bearer
(`secrets/rankrat/http-bearer-token`). The stdio transport was removed in
0.21.0:

```bash
rankrat --data-dir /absolute/path/to/rankrat-profile http -d
```

HTTP uses the profile as its Compose project directory. The launcher creates
the reviewed `docker-compose.yml` there when missing, preserves an existing
safe regular file, and mounts only the fixed profile children, not the root
itself. The project directory and Compose file must be owned by the current UID
and not group/world writable.
Omit `-d` to attach to logs; detached services restart unless stopped.

**Manual single-container Streamable HTTP** is available when local Lighthouse
is not needed. MCP is at `/mcp`, and the REST API is on the same port:

```bash
export RANKRAT_DATA_DIR=/absolute/path/to/rankrat-profile
docker run --rm --init --read-only \
  --user "$(id -u):$(id -g)" \
  --cap-drop=ALL --security-opt no-new-privileges:true \
  --pids-limit 128 --memory 512m --cpus 1 \
  --tmpfs /tmp:rw,noexec,nosuid,size=32m \
  -p 127.0.0.1:8080:8080 \
  -e RANKRAT_HTTP_HOST=0.0.0.0 \
  -e RANKRAT_HTTP_BEARER_SECRET_FILE=/run/secrets/rankrat/http-bearer-token \
  --mount type=bind,src="$RANKRAT_DATA_DIR/config",dst=/run/config \
  --mount type=bind,src="$RANKRAT_DATA_DIR/secrets",dst=/run/secrets,readonly \
  --mount type=bind,src="$RANKRAT_DATA_DIR/oauth",dst=/run/oauth \
  --mount type=bind,src="$RANKRAT_DATA_DIR/state",dst=/run/state \
  -e RANKRAT_STATE_DATABASE=/run/state/rankrat.sqlite3 \
  psyb0t/rankrat http
```

`RANKRAT_HTTP_HOST=0.0.0.0` binds inside the container; the `-p` publishes it on
loopback only. Send `Authorization: Bearer <token>` when a bearer secret is
configured.

These examples use the writable default, so config inventory can be updated.
Google OAuth storage is writable because token refresh may rotate and persist a
refresh token; provider secrets stay read-only. For a read-only agent, set
`RANKRAT_READ_ONLY=true` and make the config mount read-only as described in the
setup reference.

The repository ships one public launcher named `rankrat`; install it before
asking an agent to use a human-managed profile. It uses direct Docker for
operator commands and Compose for HTTP; agents can still invoke either
image directly. Omit `--data-dir` for the default `$HOME/.config/rankrat`
profile. A chosen profile's fixed `config/`, `secrets/`, `oauth/`, and `state/`
children preserve provider sessions and inventory when launched from different
site repositories.

The one-container manual examples return `UNAVAILABLE` for Lighthouse because
Chromium is deliberately isolated in `psyb0t/rankrat-lighthouse`. Use the
wrapper's Compose-backed HTTP mode or the published two-image commands in
`references/setup.md` when local browser audits are required. The worker shares
only a Unix socket and receives no provider credential mounts.

Use the browser worker only for operator-controlled sites. Its documented
non-root, capability-free container needs Chromium's `--no-sandbox`; a hostile
page therefore requires a stronger outer sandbox such as gVisor or Kata. The
worker blocks private/special-address egress, while public cross-origin
subresources (and a public redirect before Rankrat rejects its final URL) remain
possible.

The browser surface is exactly `lighthouse_audit`,
`lighthouse_seo_findings`, `lighthouse_accessibility_findings`,
`lighthouse_performance_findings`, and
`lighthouse_best_practices_findings`. Every call takes `account_id`, a
configured `site_url`, a child `page_url`, and an optional timeout from 5 to 300
seconds. The REST equivalents live under `/v1/lighthouse/`.

### Finding where a site lives, and matching its tag

GA4 nests every property under an *account*, and properties routinely sit under
an unrelated one because that is whatever the dropdown defaulted to when they
were created. `google_analytics_account_inventory` lists every account the
credential can see with its properties. That is the tool for "which account is
this site under", and the answer is often surprising.

`google_analytics_data_streams` returns a configured property's streams and their
`G-` measurement IDs. Use it before telling anyone their tag is installed
correctly: a tag whose measurement ID belongs to a different property looks
perfectly installed and reports into a property nobody is reading.

`google_analytics_account_rename` and `google_analytics_property_rename` exist in
writable mode. Account names are cosmetic (the numeric ID is what boundaries,
measurement IDs and reports bind to), so renaming is safe and is the usual fix
for a misfiled property. There is no GA4 account-creation or Analytics deletion
tool. Property creation is available through writable site onboarding.

### Onboarding a site

Read the `rankrat://onboarding` resource before saying anything about onboarding,
or call the `onboarding_guide` tool if the client does not support resources.
Pass `site_url` to get the methods that site's property form actually accepts.
Both are read-only and present on every server, including read-only ones, and
`POST /v1/onboarding-guides` serves the same document over REST.

Check what already exists before creating anything. `accounts_list` shows how
many resources each account carries; `google_sites_list` lists the Search Console
properties the credential sees upstream, broader than the cached boundary; and
`site_ownership_check` reports whether Google and Bing already treat the site as
verified. A site that is already a verified Search Console and Bing property does
not need onboarding. Onboarding always resolves or creates a GA4 property. When
you only need Rankrat to operate on existing properties, register them in the
account's `search_console_sites`, `pagespeed_sites`, and Bing `sites` inventory
in `boundaries.json`, plus the site's zone in the Cloudflare `dns_zones` if you
will DNS-verify Bing, then restart so the boundary reloads. A Bing site stays
unverified until `site_ownership_verify` or a manual method redeems its proof,
and Bing rejects sitemap writes until then.

If the user has no GA4 account yet, do not attempt to create one and do not
guess the steps. No tool can create a GA4 account: the Admin API has no
`accounts.create`, and the flow ends at a Terms of Service page. The guide's
`manual_provisioning` block carries the start URL and the exact ordered clicks;
relay those, then ask the user for the numeric account ID, which
`google_analytics_account_inventory` can also read back once it exists.

Creating provider resources and proving ownership are separate. When a DNS
provider account is configured, call `site_ownership_verify` after onboarding,
then poll `site_ownership_check` until `complete` is true. Cloudflare is the
currently shipped DNS adapter; without a supported adapter, the guide lists the
manual methods accepted by the property form. Site onboarding does not deploy a
GA4 tag, but writable typed Tag Manager tools can do so when the caller supplies
an explicit container, workspace, tag definition, version, and publication
request. Rankrat still cannot create a GA4 account. `site_onboarding_submit`
exists in writable mode; when the process is read-only, guide the user through a
separate writable Rankrat process or the `rankrat onboard-site` terminal command.

Typical flow for "why did traffic drop":

1. `google_search_analytics_summary`: establish the baseline.
2. `google_search_analytics_comparison`: the affected period against the prior one.
3. `google_search_analytics_drop_attribution`: which queries and pages account for it.
4. `google_url_inspection` on the worst pages: whether it is an indexing problem.

Tool names are prefixed by provider (`google_*`, `bing_*`), with a handful of
server-level ones (`server_info`, `accounts_list`, `sites_list`, `diagnostics`,
`provider_readiness`). The complete grouped tool catalog, environment, and
credential setup live in [`references/setup.md`](references/setup.md).
