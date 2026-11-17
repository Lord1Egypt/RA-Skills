# rankrat: setup reference

Everything the [skill](../SKILL.md) needs but does not need loaded up front:
configuration, credentials, and how to run it.

This file is the self-contained agent reference shipped with the skill. Human
operators can use the topic-based
[public manual](https://github.com/psyb0t/rankrat/tree/main/docs), especially
[Getting started](https://psyb0t.github.io/rankrat/getting-started/),
[Providers and credentials](https://psyb0t.github.io/rankrat/providers/),
and [Troubleshooting](https://psyb0t.github.io/rankrat/troubleshooting/).

## Contents

- [Configuration](#configuration)
- [The boundary file](#the-boundary-file)
- [Write access](#write-access)
- [Guided setup](#guided-setup)
- [Provider credentials](#provider-credentials)
- [Running it](#running-it)
- [Onboarding](#onboarding)
- [Complete MCP tool catalog](#complete-mcp-tool-catalog)
- [Checking it works](#checking-it-works)

## Configuration

All settings are read from the environment with the `RANKRAT_` prefix, so a
field named `http_port` is set by `RANKRAT_HTTP_PORT`. The defaults below are
the ones in the settings model, not example values.

| Variable | Default | Purpose |
|---|---|---|
| `RANKRAT_HTTP_HOST` | `127.0.0.1` | Listen address in `http` mode. Loopback by default. Bind wider only deliberately. |
| `RANKRAT_HTTP_PORT` | `8080` | Listen port in `http` mode. |
| `RANKRAT_BOUNDARY_FILE` | `/run/config/boundaries.json` | Provider accounts plus discovered resource inventory and URL-containment roots. |
| `RANKRAT_SECRET_ROOT` | `/run/secrets` | Directory holding provider credentials. |
| `RANKRAT_OAUTH_TOKEN_ROOT` | `/run/oauth` | Directory holding stored Google OAuth tokens. |
| `RANKRAT_LOG_FILE` | `/tmp/rankrat/rankrat.log` | Log destination. |
| `RANKRAT_LOG_LEVEL` | `INFO` | Standard Python log levels. |
| `RANKRAT_LIGHTHOUSE_WORKER_SOCKET` | `/run/lighthouse/lighthouse.sock` | Optional Unix socket for the isolated local Lighthouse worker. Empty disables it. |
| `RANKRAT_STATE_DATABASE` | unset | Absolute SQLite path for monitors, snapshots, and issue events. Empty/unset disables persistence. The wrapper sets `/run/state/rankrat.sqlite3`. |
| `RANKRAT_SCHEDULER_INTERVAL_SECONDS` | `60` | How often the HTTP process claims due monitors; accepted range 10 to 3600 seconds. |
| `RANKRAT_STATE_RETENTION_DAYS` | `180` | Snapshot/event retention after a monitor run; accepted range 1 to 3650 days. |
| `RANKRAT_ENABLE_OPENAPI` | `false` | Serve the OpenAPI document. |
| `RANKRAT_READ_ONLY` | `false` | See "Write access" below. |
| `RANKRAT_HTTP_BEARER_SECRET_FILE` | unset | File holding the bearer token required on HTTP requests. Unset means no auth, so only do that on loopback. |

The supported names and safe defaults are in `.env.example`. Invalid values for
supported settings fail startup instead of being silently accepted.
`make run-http` always supplies a bearer-secret file, including for loopback
use; a custom loopback launch may deliberately omit it.

`RANKRAT_DATA_DIR` is an optional compatibility environment override consumed
by host launchers, not by the Python process. Prefer the explicit
`rankrat --data-dir /absolute/profile ...` form when choosing a non-default
profile. The profile contains `config/boundaries.json`, `secrets/`, `oauth/`,
`state/`, and, for HTTP, an operator-owned `docker-compose.yml`. `rankrat setup`
creates every required path and secret safely; do not create a profile tree or
copy an example file by hand. With no override, launchers use
`$HOME/.config/rankrat` and never mount the root wholesale.

## The boundary file

`boundaries.json` fixes credential accounts and records resource inventory.
Each credential authorizes every supported operation and resource that its
provider account can reach. Resource arrays cache discovered sites, properties,
zones, and targets; they are not per-resource permission lists. Fixed provider
origins, public-URL validation, and child-URL containment remain enforced.
Writable discovery and onboarding persist inventory only after the config mount
passes ownership and mode checks.

## Write access

`RANKRAT_READ_ONLY` defaults to `false`. The trusted caller gets direct access
to every supported operation permitted by each configured provider account.
This is the only capability switch. HTTP uses its normal bearer for transport
authentication.

Set it to `true` and the effect is stronger than a refusal at call time: write
tools are absent from `tools/list` and REST write routes are not mounted. An
agent cannot discover them, let alone call them.
Writes cover IndexNow submission, Bing URL/sitemap/property changes, Google
Indexing notifications, Search Console site/sitemap changes, DNS-provider-backed
ownership verification, discovery remediation, and new-site onboarding, and
monitor lifecycle operations plus typed Google Tag Manager changes, safe Bing
content submission, provider-neutral managed edge redirects, and finite
Cloudflare cache purges/templates, and are marked as writes in MCP. The human
may operate Rankrat interactively or delegate fully autonomous work; use
read-only mode when that caller must not mutate provider or local state.

## Guided setup

From a checkout, the human runs one command:

```bash
make setup
```

The command initializes owner-only `config/`, `secrets/`, `oauth/`, and
`state/` paths without replacing existing values. It asks for a comma-separated
provider set, prints each provider's credential console and account-wide
permissions, then accepts secrets through non-echoing prompts. Standard paths
are used automatically:

Reruns are additive. Selected providers are added or refreshed in place;
unselected provider accounts and their inventory are preserved. When a
selected provider has multiple account entries, setup rejects the ambiguous
refresh before asking for a secret; edit `config/boundaries.json` to identify
the intended account first.

| Provider | Host credential path |
|---|---|
| Google | `secrets/google/oauth-client.json` |
| Bing | `secrets/bing/api-key` |
| Cloudflare | `secrets/cloudflare/api-token` |
| Microsoft Clarity | `secrets/clarity/api-token` |

Google accepts only an installed/Desktop OAuth client JSON. The same setup
command prints the consent URL, waits for the loopback callback, and stores the
full Rankrat grant under `oauth/`. PageSpeed's separate API key is prompted at
the same time because that API does not use OAuth.

After storage, setup runs account readiness. It does not create site properties,
submit sitemaps/URLs, or send IndexNow notifications. Secret values are never
printed or written into `.env`.

## Provider credentials

Each provider is optional. Read tools stay discoverable regardless of local
credential state and return a finite unavailable/configuration error when their
provider cannot run. Ask `provider_readiness` which providers are live rather
than inferring it from discovery or an empty result. Write tools are the
exception: they are absent unless writable mode enables them.

- **Google Search Console / Google Analytics 4 / Google Tag Manager / Google
  Indexing**: create a Google project and Desktop OAuth client JSON using the
  exact [Google OAuth guide](https://psyb0t.github.io/rankrat/providers/#google-oauth).
  Run setup and paste the client JSON's single line at the hidden prompt:

  ```sh
  rankrat setup
  ```

  The CLI validates the pasted JSON, writes it into `RANKRAT_SECRET_ROOT`, runs
  one authorization flow, and stores the resulting token under
  `RANKRAT_OAUTH_TOKEN_ROOT`. It
  requests Search Console management, Google Indexing, GA4 read/edit, and Tag
  Manager container edit, delete, version-edit, and publish scopes; provider-side
  ownership still controls what the account can do.
- **Bing Webmaster Tools**: open
  [Bing Webmaster Tools](https://www.bing.com/webmasters/home), add and verify
  one site, then **Settings → API Access → API Key → Generate API Key**. The
  resulting key is account-wide, not site-specific; setup stores it under
  `RANKRAT_SECRET_ROOT`.
- **Cloudflare**: create one dedicated **User API Token**, not an Account API
  Token: [open User API Tokens](https://dash.cloudflare.com/profile/api-tokens)
  → **Create Token → Create Custom Token** → name it `rankrat`. Add **Zone →
  Zone → Read**, **Zone → DNS → Edit**, **Zone → Analytics → Read**, **Zone →
  Cache Purge → Purge**, **Zone → Cache Rules → Edit**, **Zone → Single
  Redirect → Edit**, **Account → Account Rulesets → Edit**, and **Account →
  Account Filter Lists → Edit**. Set **Zone Resources → Include → All zones**
  and **Account Resources → Include → All accounts**, then **Continue to
  summary → Create Token**. Copy the one-time value into Rankrat's hidden
  prompt. This covers all current Cloudflare features. Rankrat discovers zone
  IDs; it exposes no arbitrary DNS record, whole-zone purge, arbitrary
  cache-rule body, or arbitrary ruleset replacement. Ownership records are
  DNS-only and untagged, so no Cloudflare DNS-tag quota is needed. Readiness
  confirms account reachability but deliberately does not create a throwaway
  record to test DNS write access.
- **Microsoft Clarity**: open [Microsoft Clarity](https://clarity.microsoft.com/),
  choose a project, then **Settings → Data Export → Generate new API token**.
  The token belongs to that project; setup stores it at the configured account
  credential path. One Clarity account represents one project and is read-only
  in Rankrat. The upstream API allows at most ten requests per project/day; see
  [Microsoft's documentation](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api).
- **PageSpeed Insights and CrUX**: setup separately asks for one optional API
  key. Create it through [Google API Credentials](https://console.cloud.google.com/apis/credentials)
  and restrict it to **PageSpeed Insights API** and **Chrome UX Report API**.
  OAuth does not grant it. Without the key, PageSpeed runs under a tighter
  anonymous quota and `crux_history` is unavailable.
- **Local Lighthouse**: no credential. The optional companion image receives
  only a shared Unix socket and outbound browser network access. Rankrat accepts
  only requested URLs beneath the account's `pagespeed_sites` and rejects a
  report whose final URL escapes that boundary. A public cross-origin redirect
  can be fetched before this post-navigation check, while private and special
  destinations are blocked by the worker's enforced proxy.

Credentials stay on the host running rankrat. They are used to call the provider
APIs over HTTPS and are not sent anywhere else.

## Running it

An agent runs the published image directly. A human creates the profile,
credentials, and Google authorization with `rankrat setup` beforehand, after
installing the launcher. Download the installer, read it, then run it, per-user
(no root) or system-wide:

```bash
curl -fsSL https://raw.githubusercontent.com/psyb0t/rankrat/main/install.sh \
  -o rankrat-install.sh
less rankrat-install.sh
bash rankrat-install.sh                # per-user   -> ~/.local/bin/rankrat
sudo bash rankrat-install.sh --system  # system-wide -> /usr/local/bin/rankrat
```

The single public launcher is named `rankrat`; it is not duplicated into agent
skills, so the shipped code cannot drift from what operators install:

```bash
# Attached Rankrat + Lighthouse:
rankrat --data-dir /absolute/path/to/rankrat-profile http
# Detached, restarts unless stopped:
rankrat --data-dir /absolute/path/to/rankrat-profile http -d
```

HTTP treats the profile as its Compose project directory. It atomically creates
the embedded reviewed `docker-compose.yml` when absent, preserves an existing
safe regular file, rejects symlinked/non-regular paths, and exports the chosen
image, port, UID/GID, and read-only values from its environment. The project
directory and Compose file must be owned by the current UID and not group/world
writable. Only the four fixed children below are mounted into containers.

The server takes four mounts. Container-side paths are the
server's defaults, so only the host side changes:

| Host | Container | Access | Holds |
|---|---|---|---|
| `$RANKRAT_DATA_DIR/config` | `/run/config` | writable normally; read-only with `RANKRAT_READ_ONLY=true` | account registry and inventory |
| `$RANKRAT_DATA_DIR/secrets` | `/run/secrets` | read-only | provider credentials, HTTP bearer secret |
| `$RANKRAT_DATA_DIR/oauth` | `/run/oauth` | writable | stored Google OAuth token; refresh may rotate it |
| `$RANKRAT_DATA_DIR/state` | `/run/state` | writable, owner-only | SQLite monitor definitions, snapshots, issues, and events |

**Manual single-container Streamable HTTP**: for a shared server that does not
need local Lighthouse. MCP lands at `/mcp` and the REST API shares the port:

```bash
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

`RANKRAT_HTTP_HOST=0.0.0.0` binds inside the container while `-p` keeps it on
loopback. MCP is then at `http://127.0.0.1:8080/mcp`; send
`Authorization: Bearer <token>` whenever a bearer secret is configured.

The commands above use the writable default. Before mounting config writable,
verify that the resolved directory is owner-only, `boundaries.json` is not a
symlink, both are owned by the current UID, and the file is not group- or
world-writable. The public `rankrat` launcher performs those checks. For a read-only
caller, set `RANKRAT_READ_ONLY=true` and make only `/run/config` read-only.
Never make the provider-secret mount writable during normal service operation.

Local Lighthouse audits require the separate published browser image. Start it
once against a private named volume:

```bash
docker volume create rankrat-lighthouse-runtime
docker run --rm --network none --user 0:0 --read-only \
  --cap-drop=ALL --cap-add=CHOWN --cap-add=FOWNER \
  --security-opt no-new-privileges:true \
  --pids-limit 16 --memory 64m --cpus 0.25 \
  --mount type=volume,src=rankrat-lighthouse-runtime,dst=/run/lighthouse \
  --entrypoint /bin/sh psyb0t/rankrat-lighthouse \
  -c 'chmod 1777 /run/lighthouse \
    && touch /run/lighthouse/.initialized \
    && chown -R 10001:10001 /run/lighthouse \
    && chmod 0750 /run/lighthouse'
docker run --rm -d --name rankrat-lighthouse-worker --init --read-only \
  --user 10001:10001 --cap-drop=ALL --security-opt no-new-privileges:true \
  --pids-limit 256 --memory 2g --cpus 2 --shm-size 1g \
  --tmpfs /tmp:rw,noexec,nosuid,size=1g,mode=1777 \
  --mount type=volume,src=rankrat-lighthouse-runtime,dst=/run/lighthouse \
  psyb0t/rankrat-lighthouse
```

The self-removing initializer assigns the private volume root to the non-root
UID shared by Rankrat and the worker. When using a different UID/GID, change the
initializer's `chown` pair and the worker's `--user` pair to the same values.
Run Rankrat under that pair as well if the primary image's built-in `10001:10001`
user is overridden. The provided Compose file applies `RANKRAT_UID` and
`RANKRAT_GID` consistently to both long-lived services after running this
hardened initializer.

Add this read-only volume mount to the published Rankrat invocation above:

```bash
--mount type=volume,src=rankrat-lighthouse-runtime,dst=/run/lighthouse,readonly
```

The normal `psyb0t/rankrat http` command then exposes the five Lighthouse tools
over Streamable HTTP at `/mcp` and REST under `/v1/lighthouse/`. Leave
`RANKRAT_LIGHTHOUSE_WORKER_SOCKET` empty to disable the worker explicitly. Stop
and remove only the worker and volume you created when they are no longer
needed.

The worker is for pages you control and trust. Chromium runs with
`--no-sandbox` because its built-in namespace/setuid sandbox cannot coexist with
the documented non-root, capability-free, `no-new-privileges` container. The
credential-free, read-only worker and public-address-only proxy reduce blast
radius but do not replace the renderer sandbox after a browser exploit. Use an
outer sandbox such as gVisor or Kata Containers before auditing hostile content.

| MCP tool | REST route |
|---|---|
| `lighthouse_audit` | `POST /v1/lighthouse/audits` |
| `lighthouse_seo_findings` | `POST /v1/lighthouse/seo-findings` |
| `lighthouse_accessibility_findings` | `POST /v1/lighthouse/accessibility-findings` |
| `lighthouse_performance_findings` | `POST /v1/lighthouse/performance-findings` |
| `lighthouse_best_practices_findings` | `POST /v1/lighthouse/best-practices-findings` |

Every operation accepts the same strict body: `account_id`, a configured
`site_url`, a child `page_url`, and optional `timeout_seconds` in the inclusive
5 to 300 second range. The aggregate audit returns all four category scores and
failed findings; the other four operations return only that category's failed
findings.

## Onboarding

`site_onboarding_submit` is part of normal writable mode. It creates or reuses
GA4, Search Console, and Bing resources, then records discovered IDs in the
config file. It is absent from `tools/list` and REST when
`RANKRAT_READ_ONLY=true`. The config directory must be safely writable; the
bundled wrapper validates its ownership/mode.

The guidance is available either way, read-only, on every server:

| Surface | What it gives |
|---|---|
| `rankrat://onboarding` resource | The whole procedure and this server's onboarding posture |
| `rankrat://onboarding/{site_url}` template | Same, narrowed to one percent-encoded site |
| `onboarding_guide` tool | The identical document, for clients without resource support |

With a configured DNS provider account, `site_ownership_verify` requests the
real Google TXT and Bing CNAME proofs, publishes only those records through the
adapter selected by the account's `provider`, checks public DNS, and redeems
each provider. Poll `site_ownership_check` until it reports `complete`; DNS
propagation is asynchronous. Cloudflare is the currently shipped DNS adapter.
Without a supported adapter, a `sc-domain:` property accepts only DNS TXT,
while a `https://` URL-prefix property also accepts the GA4 tag, an HTML file,
or a meta tag.

The SEO expansion has these MCP tool names and REST routes:

| MCP tool | REST route |
|---|---|
| `site_ownership_check` | `POST /v1/site-ownership-checks` |
| `site_ownership_verify` | `POST /v1/site-ownership-verifications` |
| `site_audit` | `POST /v1/site-audits` |
| `site_remediation_apply` | `POST /v1/site-remediations` |
| `bing_backlink_intelligence` | `POST /v1/bing/backlink-intelligence` |
| `internal_link_graph` | `POST /v1/internal-link-graphs` |
| `orphan_page_report` | `POST /v1/orphan-page-reports` |
| `internal_link_opportunities` | `POST /v1/internal-link-opportunity-reports` |
| `crux_history` | `POST /v1/crux/history-reports` |
| `cloudflare_analytics` | `POST /v1/cloudflare/analytics-reports` |
| `content_opportunities` | `POST /v1/content-opportunity-reports` |

## Complete MCP tool catalog

`tools/list` is authoritative for a running server because startup settings
decide which tools exist. The grouped inventory below mirrors the tool catalog
in the source. The exact REST paths and schemas live in the committed
[merged OpenAPI document](https://github.com/psyb0t/rankrat/blob/main/openapi.json),
composed from the
[base](https://github.com/psyb0t/rankrat/blob/main/src/rankrat/api/openapi.yaml)
and
[SEO intelligence](https://github.com/psyb0t/rankrat/blob/main/src/rankrat/api/seo-openapi.yaml)
and
[free provider SEO](https://github.com/psyb0t/rankrat/blob/main/src/rankrat/api/free-seo-openapi.yaml)
YAML sources. When enabled, the runtime `/openapi.json` removes write routes
from a read-only server.

### Read-only tools

- **Server, boundaries, and guidance:** `server_info`, `accounts_list`,
  `sites_list`, `diagnostics`, `provider_readiness`, `onboarding_guide`.
- **Site, ownership, schema, links, and opportunities:** `site_audit`,
  `site_ownership_check`, `schema_validate_url`, `schema_validate_html`,
  `schema_validate_json_ld`, `bing_backlink_intelligence`,
  `internal_link_graph`, `orphan_page_report`,
  `internal_link_opportunities`, `content_opportunities`.
- **Persistent monitoring:** `monitors_list`, `monitor_snapshots_list`,
  `monitor_issues_list`, `issue_events_list`.
- **Google Search Console and Indexing metadata:**
  `google_search_analytics_summary`, `google_search_analytics_comparison`,
  `google_search_analytics_dimension_report`,
  `google_search_analytics_drop_attribution`, `google_search_analytics_trend`,
  `google_search_analytics_anomalies`,
  `google_search_analytics_page_performance`,
  `google_search_analytics_query`, `google_sites_list`, `google_site_get`,
  `google_sitemaps_list`, `google_sitemap_get`, `google_url_inspection`,
  `google_url_inspection_batch`, `google_indexing_metadata`.
- **Google Analytics 4:** `google_analytics_account_inventory`,
  `google_analytics_data_streams`, `google_analytics_report`,
  `google_analytics_realtime_report`, `google_analytics_content_performance`,
  `google_analytics_landing_page_performance`,
  `google_analytics_organic_search_landing_pages`,
  `google_analytics_traffic_source_performance`,
  `google_analytics_ecommerce_performance`,
  `google_analytics_audience_segments`, `google_analytics_user_behavior`,
  `google_analytics_conversion_funnel`.
- **Google Tag Manager, Microsoft Clarity, and managed redirects:**
  `google_tag_manager_accounts_list`, `google_tag_manager_containers_list`,
  `google_tag_manager_workspaces_list`, `google_tag_manager_entities_list`,
  `clarity_insights`, `edge_redirects_list`.
- **PageSpeed, CrUX, Cloudflare, and local Lighthouse:** `pagespeed_analyze`,
  `pagespeed_core_web_vitals`, `lighthouse_audit`,
  `lighthouse_seo_findings`, `lighthouse_accessibility_findings`,
  `lighthouse_performance_findings`,
  `lighthouse_best_practices_findings`, `crux_history`,
  `cloudflare_analytics`.
- **Cross-provider analysis:** `ga4_pagespeed_correlation`,
  `ga4_search_console_comparison`, `search_engine_comparison`,
  `search_engine_traffic_health`.
- **Bing Webmaster Tools:** `bing_keyword_statistics`,
  `bing_related_keywords`, `bing_traffic_trend`, `bing_traffic_anomalies`,
  `bing_traffic_comparison`, `bing_query_performance`,
  `bing_page_performance`, `bing_brand_analysis`, `bing_ranking_buckets`,
  `bing_query_opportunities`, `bing_page_opportunities`,
  `bing_opportunity_matrix`, `bing_query_page_performance`,
  `bing_query_cannibalization`, `bing_page_query_performance`,
  `bing_url_submission_quota`, `bing_crawl_issues`, `bing_crawl_stats`,
  `bing_feeds`, `bing_link_counts`, `bing_url_information`.

### Writable tools

These appear only when `RANKRAT_READ_ONLY=false`:

- **IndexNow:** `indexnow_submit`. IndexNow is an open change-notification
  protocol, not a dashboard: one participating endpoint shares an accepted
  notification with the other participating engines, while each engine makes
  its own crawl and indexing decisions.
- **Bing:** `bing_url_submit`, `bing_sitemap_submit`, `bing_site_submit`.
- **Bing content:** `bing_content_submission_create` fetches an allowed public
  page itself, then submits that fresh HTML to Bing.
- **Google Search Console and Indexing:** `google_indexing_submit`,
  `google_indexing_batch_submit`, `google_site_submit`,
  `google_sitemap_submit`.
- **Google Analytics 4:** `google_analytics_account_rename`,
  `google_analytics_property_rename`.
- **Google Tag Manager:** `google_tag_manager_container_create`,
  `google_tag_manager_container_delete`, `google_tag_manager_workspace_create`,
  `google_tag_manager_workspace_delete`, `google_tag_manager_entity_create`,
  `google_tag_manager_entity_update`, `google_tag_manager_entity_delete`,
  `google_tag_manager_workspace_version_create`,
  `google_tag_manager_version_publish`.
- **Ownership and discovery remediation:** `site_ownership_verify`,
  `site_remediation_apply`.
- **Persistent monitoring:** `monitor_create`, `monitor_update`,
  `monitor_delete`, `monitor_run`, `issue_status_update`.
- **Cloudflare performance:** `cloudflare_cache_purge`,
  `cloudflare_cache_template_apply`.
- **Provider-neutral managed redirects:** `edge_redirect_upsert`,
  `edge_redirect_delete`. Cloudflare is the currently shipped adapter.
- **Site onboarding:** `site_onboarding_submit`.

## Checking it works

- `server_info`: the server is up and which mode it is in.
- `provider_readiness`: which providers are actually configured.
- `accounts_list` / `sites_list`: the boundary as the server sees it.
- `diagnostics`: deeper detail when one of the above is not what you expected.
- `monitors_list` and `monitor_issues_list`: whether scheduled audit history
  is accumulating and which lifecycle issues remain open.

If a provider-specific tool returns nothing, check `provider_readiness` before
assuming the data is missing upstream.

Automatic due-monitor execution belongs to the long-running HTTP process.
Stdio exposes the same monitor CRUD, manual-run, snapshot, issue, and event
tools, but its process lifetime is controlled by the MCP client and it does not
leave a background scheduler behind. Persist `/run/state` for either transport.
For backups, use SQLite's online-backup mechanism or stop Rankrat first; copying
only a live database file can omit WAL state.
