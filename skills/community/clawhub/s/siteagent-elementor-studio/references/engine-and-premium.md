# Engine & the Premium plugin — what runs the build

**Engine = our fork `Digitizers/elementor-mcp` (v1.34.1, the release this kit's installer
pins)** — Elementor 4.x-correct. It bundles the WordPress MCP Adapter, so it installs as a
**single plugin** — no separate adapter plugin needed.

Tool counts scale with the site. The figures here were measured on **v1.24.0 with every
applicable tool enabled**: **61 / 100 / 105** on a classic (v3) install (free / Pro / Pro +
WooCommerce), and **74 / 113 / 118** when the Elementor 4.0+ atomic engine is active (the
+13 atomic tools). They are neither a count of v1.34.1 nor a minimum for it: releases since
have added tools, and a site can expose far fewer — the admin's per-tool toggles and
Low-tools mode both trim the registered list. The live `tools/list` is the count; when it
looks short, check those two before concluding a tool does not exist:

- **Per-tool toggles** live in the `elementor_mcp_disabled_tools` option, and nothing in
  the MCP handshake, the tool list or the logs says that abilities were suppressed — a
  fresh install has presented as **zero tools exposed** with 104 slugs in that list.
  Diagnose: `wp option get elementor_mcp_disabled_tools --format=json`. **Clearing it alone
  does not stick**: a seeder in the plugin's admin re-disables every Pro-badged tool
  whenever `elementor_mcp_defaults_applied` is below its `DEFAULTS_VERSION` — deliberately,
  so new Pro batches ship off by default — and after a plugin upgrade the counter is behind
  again, so a list emptied while the seeder is armed is silently refilled on the next
  wp-admin request. The order is: (1) load any wp-admin page once — that request runs the
  seeder and bumps the counter; (2) confirm `wp option get elementor_mcp_defaults_applied`
  now matches `DEFAULTS_VERSION`; (3) back the list up to the project, then
  `wp option update elementor_mcp_disabled_tools '[]' --format=json` (or curate it — see the
  next point); (4) restart Claude Code, since the tool list is read at startup.
- **Low-tools mode** (EMCP Tools → Tools screen) filters the list down to a curated
  ~50-slug essentials set for clients with a tool cap. On such a client do **not** clear
  the whole disabled list: the full Pro + atomic set (~113 tools) overruns a ~100 cap, the
  client silently truncates, and the atomic essentials can be what falls off — "no tools"
  turns into the subtler "writes don't persist".

The v1.13–v1.34 fork work adds the design-system CRUD + governance surface on top (see
below).

## What the fork adds over the upstream base (the reason we run it)

The fork started from upstream's 1.x line and has diverged substantially:

- **Elementor 4.x GA atomic correctness** — `is_v4()` schema gating, corrected `$$type` prop
  shapes, style-controls compiled into local style classes, atomic detection by
  element-type registration. Upstream's classic-only schema breaks on 4.1.x.
- **GPL tool set enabled** (v1.13.0) — the brand-kit / SEO / a11y / Widget-Builder tools
  register for everyone (no license gate).
- **v4 design-system CRUD** (v1.14–v1.16) — Global Classes, Variables (with
  `restore-variable`), Interactions (with `edit-interaction`).
- **SiteAgent-governed writes** — page writes are snapshot-first + optional Ed25519
  approval grants + optional post-write render-check auto-revert (v1.17–v1.19); **design-token
  writes (system kit, global palette, Variables) are snapshot-governed too** (v1.24.0).
- **Schema-in-error** (v1.20–v1.21) + **numeric range constraints** in `get-widget-schema`
  (v1.23) — one-round-trip self-correction.

## No Freemius / no phone-home

The vendored Freemius SDK and the upstream hosted "Pro marketplace" (Templates / Skills
fetchers that pulled licensed content from `emcp.msrbuilds.com`) were **removed in v1.22.0**.
The fork has **no license gate and no phone-home**. It is distributed via GitHub
releases: this skill's installer installs the release it pins, and **since fork v1.28.0
the plugin carries its own update checker** (`includes/class-updater.php`, loaded from
the main plugin file), so later releases appear on the site's normal *Plugins* /
*Dashboard → Updates* screens. Be precise about what that is and is not:

- It **offers** updates; it does not install them. Installing one is WordPress's
  ordinary plugin-update flow — an admin clicks *Update*, or has turned on WordPress's
  per-plugin auto-update toggle for it. The fork does not turn that toggle on.
- It offers a **published GitHub Release** only (release-only detection: a pushed tag
  with no Release offers nothing), served from the Release's `elementor-mcp*.zip` asset.
- The check contacts `api.github.com`, and the download `github.com`, with a user agent
  that names only the plugin and its version — never the site URL WordPress's default
  agent would send. What GitHub does receive is what any update check hands the host it
  asks: the request's source IP, and here the plugin's name and version. What it does not
  receive is the site URL, and there is no vendor endpoint and no telemetry of any kind —
  that is the sense in which "no phone-home" holds.

Those later updates run outside this kit's pin-and-digest check: the wizard verifies
what it installs today, and WordPress's update flow governs what replaces it. An
operator who wants every version reviewed leaves the auto-update toggle off (the
default) and reviews the Release before clicking *Update*. The **free** bundled
sample-prompts + brand-kit apply/backup/restore are retained.

## Do NOT run the paid "MCP Tools for Elementor (Premium)" (`emcp-pro`) at the same time

The fork and upstream Premium share the same code lineage (same class names
`Elementor_MCP_*`, same `ELEMENTOR_MCP_VERSION` constant, no PHP namespace). Activating both
= `Cannot redeclare class` fatal. **Only one can be active.**

| | Upstream Premium `emcp-pro` (3.0.0) | fork `elementor-mcp` (1.34.1) |
|---|---|---|
| Elementor 4.x GA atomic engine | ❌ classic-only schema (breaks on 4.1.x) | ✅ 4.x-correct |
| v4 design-system CRUD (classes / variables / interactions) | ❌ | ✅ |
| Governed writes (snapshot + grant + render-check) | ❌ | ✅ (page **and** design-token) |
| Schema-in-error + numeric-range hints | ❌ | ✅ |
| Freemius license / hosted marketplace / phone-home | ✅ | ❌ (removed v1.22) |
| Direction | horizontal (WP content/plugin/theme CRUD, PHP-snippet authoring) | Elementor-4 depth + governance |

**We run the fork.** It is the Elementor-4-correct, design-system-capable, governed engine
this skill is built around. There is no reason to switch to Premium for Elementor page
building; Premium went horizontal (site-wide CRUD) rather than deepening Elementor 4.

## Switching (one active at a time)

```bash
wp plugin deactivate elementor-mcp && wp plugin activate emcp-pro    # → Premium
wp plugin deactivate emcp-pro && wp plugin activate elementor-mcp    # → fork
```

Both share the options `elementor_mcp_disabled_tools` and `elementor_mcp_low_tool_mode` —
a low-tools/disabled-tools state set under one carries to the other.

## Production hygiene

Neither plugin should stay active on a client's **production** server — both are build-time
authoring tools. Deactivate (or remove) at handoff. (The fork's governance — grants +
render-check — is opt-in and needs SiteAgent; it makes *authoring* writes reversible, not a
reason to leave the tool live in production.)
