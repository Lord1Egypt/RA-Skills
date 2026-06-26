# User expectations: WordPress Expert (skill `wordpress-expert` + tools)

From the perspective of someone using skill **`wordpress-expert`** (ClawHub display name **WordPress Expert**) and plugin **`wordpress-site-tools`** for a WordPress project: what they **expect**, how they **use** it, and what should be possible **later**.

**Maintenance:** Update this file when the skill/plugin changes significantly. Technical follow-ups and roadmap: maintainer docs in the source repo (`docs/openclaw-wordpress/`).

---

## 1. Who am I as a user?

Typical roles:

- **Site owner / agency:** I want to **chat in OpenClaw** (“Show latest drafts”, “Is plugin X active?”, “Create a draft news page”) without using WP Admin or terminal myself—as far as it is safe.
- **Developer with staging:** I have **OpenClaw gateway** on a machine/server, **WordPress** reachable by URL and/or **WP-CLI** on the same host as the install. I can maintain **environment variables** or `openclaw.json`.
- **Developer + operations (target picture):** I want the same agent to **operate WordPress broadly** *and* work like a **WordPress developer**: write **custom plugins**, **extend third-party plugins via hooks/APIs**, follow structure and best practices—on staging first, with clear security boundaries.

**Current scope note:** PHP runs **inside WordPress**, not “in” the OpenClaw process. The agent develops and deploys via **file access** (e.g. workspace/`exec`), **WP-CLI**, **REST**, and optionally **Git**—not an embedded PHP agent in core.

---

## 2. What I expect from the product (high level)

| Expectation | Short |
|-------------|--------|
| **Natural language** | I describe tasks in plain language; the agent chooses REST vs WP-CLI vs browser per docs. |
| **No secrets in chat** | Passwords and application passwords only in env / OpenClaw config, not prompts or Git. |
| **Read before write** | For changes, fetch current data first; no hallucinations about site state. |
| **Security** | No arbitrary shell; WP-CLI only with allowlist; REST only against configured site. |
| **WooCommerce / Elementor** | Skill knows limits; where APIs are missing, plan browser or manual steps. |
| **Traceability** | I see (or can ask) *which* path was used—tool call vs curl vs browser. |
| **Long term: near-full operation** | Content, media, plugins/themes (activate/deactivate), users/roles, many settings—as far as REST/WP-CLI/admin API allow; name gaps (Customizer-only, special page builders). |
| **Long term: developer role** | New plugins (own code), changes to **existing** plugins (hooks, filters, compatible APIs), optional **child themes**; no blind core hacks; staging, tests, rollback conceivable. |

---

## 2.1 Long-term target: operator *and* developer

Extended wish list used to compare development state (today vs target).

### As operator (“WordPress almost complete”)

- **Content:** Posts, pages, media, taxonomies, menus (as far as API/CLI allow).
- **Extensions:** Manage plugins and themes (list, install, activate, update—with explicit risk/backup logic in the skill).
- **Shop / builder:** Woo, Elementor, etc. **as far as REST or documented automation** goes; else browser or clear manual steps.
- **Tools:** Broader **profiled** WP-CLI allowlists or additional safe tools; REST coverage where useful; small **MU plugin** only for gaps (health, capabilities), not as a substitute for proper APIs.

### As developer (write plugins & extend third parties)

- **New plugins:** Scaffold (structure, `readme.txt`, main file, hooks), **PHP** per WordPress coding standards, **i18n**, **activation/deactivation**, custom REST routes only with permission checks.
- **Extend third-party plugins:** Only via **official/supported** means: `add_action` / `add_filter`, small **bridge** or **addon** plugins on documented hooks (Woo, ACF, etc.—project-specific in references).
- **Not expected:** Permanently “patching” third-party plugin files without an update-safe strategy (prefer child/addon).
- **Workflow:** Code ideally in **Git workspace** or synced `wp-content/plugins/...`; agent uses **Read – Plan – Write – Verify** ([WORKFLOWS.md](WORKFLOWS.md)); after deploy **activate/test** via WP-CLI or REST.
- **Quality:** Optional PHPCS/WP stubs, tests (PHPUnit), staging before production.

### Tension: security vs “complete”

The more the agent may **write** (files, DB, plugin lifecycle), the more important: **allowlists**, **environments** (staging only), **confirmations**, **backups**. The target picture wants **explicit profiles** (e.g. “read-only”, “content editor”, “dev-staging”)—not yet shipped as a finished product.

---

## 3. Usage: what I must do today

### 3.1 Prerequisites

- **OpenClaw** installed, gateway running.
- **WordPress:** HTTPS; for REST ideally **application passwords**; for WP-CLI: `wp` on the **same system as the gateway** (or equivalent), access to install files.
- Optional: `curl` and/or `wp` on `PATH` so the skill is **eligible** per metadata. Default stays **conservative** (`anyBins: ["wp","curl"]`) so environments matching documented shell fallbacks remain eligible; details: [README.md](../README.md) “Gating (metadata)”.

### 3.2 Installation (two parts)

Full guide for **existing** sites (REST-only vs REST+WP-CLI topology, `openclaw.json`, verification): **[CONNECTING.md](CONNECTING.md)**.

Short:

1. **Skill**—copy folder `openclaw-wordpress-skill` to `~/.openclaw/workspace/skills/wordpress-expert` (folder name = skill `name`).
2. **Plugin**—in `openclaw-wordpress-tools`: `npm install`, then `openclaw plugins install <path>`, `openclaw plugins enable wordpress-site-tools`, restart gateway.
3. **Allow tools**—in `openclaw.json` e.g. `tools.allow` with `wordpress_connection_check`, `wordpress_rest_request`, `wordpress_wp_cli`, optional `wordpress_media_upload`, `wordpress_plugin_files`, or `wordpress-site-tools`.
4. **Config**—in `skills.entries["wordpress-expert"].env` (and optionally `plugins.entries.wordpress-site-tools.config`):
   - REST: `WORDPRESS_SITE_URL`, `WORDPRESS_USER`, `WORDPRESS_APPLICATION_PASSWORD`
   - WP-CLI tool: `WORDPRESS_PATH` (or `wordpressPath` in plugin config)
5. **WP-CLI presets** if needed: [WPCLI_PRESETS.md](WPCLI_PRESETS.md)

Details: [README.md](../README.md), [AUTH.md](AUTH.md), `openclaw-wordpress-tools/README.md`.

### 3.3 How I “drive” it

- **Chat:** Normal instructions (“List active plugins”, “Get last 5 posts”, “Create a draft …”).
- **Development (today):** Instructions like “Create a plugin under `wp-content/plugins/my-addon` that hooks `woocommerce_order_status_changed`”—the agent typically uses **file tools / exec** in the OpenClaw workspace or on the host, **plus** skill rules ([SAFETY.md](SAFETY.md), [DOMAIN.md](DOMAIN.md)); WP-CLI tool supports only **allowlisted** commands.
- I **do not** need to memorize tool names—the agent uses them when allowed and sensible per skill.
- **WP-CLI tool limit:** Only commands matching the **allowlist**. Default is **read-heavy/conservative**; broader rights via **`wpCliProfile`** (preset) or explicit **`wpCliAllowPrefixes`** (replaces profile and defaults when non-empty).

### 3.4 What I can realistically do today

**Works well (with correct config):**

- **List/read** posts/pages (REST or WP-CLI depending on setup).
- **Plugin and theme lists** (WP-CLI with default allowlist).
- **Read options** (`option get` within allowlist).
- **REST CRUD** where role and endpoints allow (Woo: e.g. `wc/v3`).
- **Plugin development:** PHP/file work via workspace/`exec` or **`wordpress_plugin_files`** (when allowed and `WORDPRESS_PATH` set); **media upload** to library via **`wordpress_media_upload`** when allowed.

**Limited / not in default WP-CLI tool:**

- Arbitrary `wp post delete`, `wp plugin delete`, DB queries, `eval`—**not** without expanded allowlist config or REST/other path.
- Anything only in **Customizer** or **UI-only plugins**—prefer **browser** or manual (skill points this out).

**Gap to target “complete + developer”:**

- WP-CLI presets: [WPCLI_PRESETS.md](WPCLI_PRESETS.md); runtime selection in plugin via **`wpCliProfile`** (config + gateway restart).
- Developer playbooks: [PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md); WooCommerce: [WOOCOMMERCE.md](WOOCOMMERCE.md); Elementor: [ELEMENTOR.md](ELEMENTOR.md).
- Optional: additional controlled tools instead of generic `exec` only.
- Tests/review: manual tests per [CONNECTING.md](CONNECTING.md); full matrix in source repo (`docs/openclaw-wordpress/TEST_MATRIX.md`); **no** automatic CI in the skill.

---

## 4. Wishes for later (target vs state)

User perspective—compare with technical state: maintainer doc `docs/openclaw-wordpress/ROADMAP_RESEARCH.md`.

| Wish | State today (short) |
|------|---------------------|
| **One-click install** (ClawHub + npm plugin) | Skill via ClawHub possible; plugin separate from Git/monorepo; see skill README and `docs/openclaw-wordpress/`. |
| **Broader WP-CLI profiles** (“staging only”, content, admin, dev) | **Presets** in [WPCLI_PRESETS.md](WPCLI_PRESETS.md); selectable in plugin via **`wpCliProfile`**. |
| **Operate WordPress “almost completely”** | Partly (REST + limited WP-CLI); write/admin gaps and builder limits remain. |
| **Agent as plugin developer + extender** | Possible via workspace/exec; references extensible; media upload tool optional; controlled plugin file writes still evolving. |
| **MU plugin** for health/capabilities | Implemented (`bundled/mu-plugin/`); optional on site. |
| **Fixed test matrix** | Documented under `docs/openclaw-wordpress/TEST_MATRIX.md` (maintainer). |
| **Skill gating without curl** if only REST tool | Metadata still `anyBins: wp,curl`; optional tuning. |
| **Validation** (skills-ref) | Before ClawHub publish: `docs/openclaw-wordpress/QA.md`. |

---

## 5. Maintainer checklist (development alignment)

On release or major feature, verify and update **sections 2.1, 3–4** above if needed.

- [ ] Skill installable as in [README.md](../README.md).
- [ ] Plugin installable; all tools documented with correct names (`wordpress_connection_check`, `wordpress_rest_request`, `wordpress_wp_cli`, optional `wordpress_media_upload`, `wordpress_plugin_files`).
- [ ] `tools.allow` and env vars consistent with code ([AUTH.md](AUTH.md), plugin README).
- [ ] Default allowlist and blocklist for `wordpress_wp_cli` match plugin README and section 3.4 here.
- [ ] [CONNECTING.md](CONNECTING.md) and [WPCLI_PRESETS.md](WPCLI_PRESETS.md) aligned with OpenClaw docs and code.
- [ ] **Target operator+developer** (section 2.1): gaps vs current state in 3.4 / 4 stay current.
- [ ] Maintainer roadmap (`docs/openclaw-wordpress/ROADMAP_RESEARCH.md`) reflects open vs done work.
- [ ] **USER_EXPECTATIONS.md** (this file): update when scope changes.

---

## 6. Related files

| File | Content |
|------|---------|
| [../README.md](../README.md) | Skill + plugin install, `openclaw.json` examples |
| [CONNECTING.md](CONNECTING.md) | Connect existing site, OpenClaw requirements |
| [WPCLI_PRESETS.md](WPCLI_PRESETS.md) | WP-CLI allowlist presets |
| [NATIVE_VS_PLUGIN.md](NATIVE_VS_PLUGIN.md) | Plugin tools vs OpenClaw `exec` / browser / workspace |
| [TOOLING.md](TOOLING.md) | Order REST vs WP-CLI vs browser |
| [AUTH.md](AUTH.md) | Secrets, env, plugin overrides |
| [SAFETY.md](SAFETY.md) | Defaults, destructive actions |
| [WORKFLOWS.md](WORKFLOWS.md) | Read – Plan – Write – Verify |
| [DOMAIN.md](DOMAIN.md) | Blocks, plugins, CPT, REST |
| [PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md) | Plugin development under OpenClaw |
| `openclaw-wordpress-tools/README.md` | Plugin and tool details |

---

*Alignment: skill `wordpress-expert` + plugin `wordpress-site-tools` (connection check, REST, WP-CLI, optional media upload, optional plugin files); long-term goal: broad WordPress operation and developer role per section 2.1.*
