# WordPress Expert (`wordpress-expert`)

**Bundle version:** 1.1.1 (see `SKILL.md` `metadata.version`).

**Skill id / folder / ClawHub slug:** `wordpress-expert` — ClawHub display name: **WordPress Expert** (`clawhub publish --name "WordPress Expert"`). The **URL path** is `…/wordpress-expert`; the **page title** is set by `--name` or ClawHub settings.

**Migrating from v1.0.5 and earlier:** the skill was **`wordpress-site-ops`**. Remove `skills/wordpress-site-ops`, run [`sync-openclaw-wordpress.sh`](../scripts/sync-openclaw-wordpress.sh) (or copy into `skills/wordpress-expert`), and rename **`skills.entries["wordpress-site-ops"]` → `skills.entries["wordpress-expert"]`** in `openclaw.json`. Then `clawhub install wordpress-expert` / publish with `--slug wordpress-expert`—see [CLAWHUB_RELEASE_1.0.6.md](../docs/openclaw-wordpress/CLAWHUB_RELEASE_1.0.6.md).

**Quick read for humans:** **[SKILL.md](SKILL.md)** (companion plugin recommendation, setup, expectations)—then **Trust** and **Connect** below.

## At a glance (ClawHub & new users)

**Trust and risk first:** [references/PRE_INSTALL_AND_TRUST.md](references/PRE_INSTALL_AND_TRUST.md) (companion plugin, credentials, MU helper, `tools.allow`).

**What this skill does:** Gives your agent **instructions and reference docs** to **operate WordPress**—content, media, plugins, themes, WooCommerce, Elementor, REST, and code under `wp-content` (see `references/PLUGIN_DEV_PLAYBOOK.md`).

**Why add the companion plugin?** The skill alone does **not** register OpenClaw tools. Install **[wordpress-site-tools](https://github.com/realM1lF/openclaw-wordpress-tool)** on the **gateway host** so the agent gets **`wordpress_rest_request`**, **`wordpress_wp_cli`**, **`wordpress_connection_check`**, and optional **`wordpress_media_upload`** / **`wordpress_plugin_files`**. That is **safer and more reliable** than stitching together `exec` + `curl` for every call.

**Integrate in a few steps (after installing this skill from ClawHub):**

1. On the machine that runs OpenClaw:
   ```bash
   git clone https://github.com/realM1lF/openclaw-wordpress-tool.git
   cd openclaw-wordpress-tool && npm install
   openclaw plugins install -l "$(pwd)"
   openclaw plugins enable wordpress-site-tools
   openclaw gateway restart
   ```
2. Allow the tools in `~/.openclaw/openclaw.json` (see **Plugin** section below).
3. Set **`WORDPRESS_SITE_URL`**, **`WORDPRESS_USER`**, **`WORDPRESS_APPLICATION_PASSWORD`** (REST) and optionally **`WORDPRESS_PATH`** (WP-CLI)—details in **`references/CONNECTING.md`**.

Reference docs in this bundle are mostly **English**; a few filenames or examples may still use German words—behavior is unchanged.

---

WordPress operations from **OpenClaw**: instructions and references for the agent. Execution is typically via plugin tools (**`wordpress_connection_check`**, **`wordpress_rest_request`**, **`wordpress_wp_cli`**, optional **`wordpress_media_upload`**, optional **`wordpress_plugin_files`**) when allowed; otherwise **`exec`** / **`curl`** / **browser** / workspace—see [references/NATIVE_VS_PLUGIN.md](references/NATIVE_VS_PLUGIN.md).

Compatible with [AgentSkills](https://agentskills.io/specification) layout (`references/`, short `SKILL.md`) and [OpenClaw Skills](https://docs.openclaw.ai/tools/skills).

## Connect WordPress (existing site)

**Before credentials/plugin:** **[references/PRE_INSTALL_AND_TRUST.md](references/PRE_INSTALL_AND_TRUST.md)**.  
Step-by-step including **REST-only** vs **REST+WP-CLI** topology, OpenClaw `openclaw.json`, and verification: **[references/CONNECTING.md](references/CONNECTING.md)**.  
WP-CLI presets (`wpCliProfile` / `wpCliAllowPrefixes`): **[references/WPCLI_PRESETS.md](references/WPCLI_PRESETS.md)**.  
**OpenClaw policy (sandbox, allowlists, `group:*`, `deny`):** **[references/OPENCLAW_INTEGRATION.md](references/OPENCLAW_INTEGRATION.md)**.  
**Plugin development under OpenClaw:** **[references/PLUGIN_DEV_PLAYBOOK.md](references/PLUGIN_DEV_PLAYBOOK.md)**.  
**Optional WordPress MU helper (PHP, copy onto the site):** **[bundled/mu-plugin/README.md](bundled/mu-plugin/README.md)** (routes `openclaw-helper/v1/status`, `health`, `me/capabilities`). **When it helps:** **[references/MU_HELPER.md](references/MU_HELPER.md)**.

## Installation

### From monorepo clone (recommended: one command, stays current)

The parent repo has [`scripts/sync-openclaw-wordpress.sh`](../scripts/sync-openclaw-wordpress.sh): symlinks the skill to `~/.openclaw/workspace/skills/wordpress-expert` and installs the plugin with `openclaw plugins install -l`. After `git pull`, run again.

```bash
cd /path/to/personal-ki-agents
./scripts/sync-openclaw-wordpress.sh --restart
```

Different workspace: `OPENCLAW_WORKSPACE=/path/to/workspace ./scripts/sync-openclaw-wordpress.sh`

### Manual (copy)

1. Target folder in the **active agent workspace** (often `~/.openclaw/workspace`):

   ```bash
   cp -r /path/to/personal-ki-agents/openclaw-wordpress-skill ~/.openclaw/workspace/skills/wordpress-expert
   ```

   The folder name **`wordpress-expert`** must match the **`name`** field in `SKILL.md` (AgentSkills convention).

2. **`openclaw gateway restart`** so the gateway reloads skills/plugins. (Optional: **`/new`** in chat only if the UI still shows stale data—see below.)

3. Verify:

   ```bash
   openclaw skills list
   openclaw skills list --eligible
   openclaw skills info wordpress-expert
   openclaw skills check
   ```

   CLI: [skills](https://docs.openclaw.ai/cli/skills)

### Gateway restart vs. new chat (`/new`)

| Situation | Recommendation |
|-----------|----------------|
| `tools.allow` / `plugins.allow` changed, plugin **enabled**/installed, plugin code updated | **`openclaw gateway restart`**—otherwise new tools are often not registered. |
| Skill folder only copied/symlink updated | **Gateway restart** too; then `openclaw skills list`. |
| Env in `skills.entries…env` changed | Often test in the **same session**; if the agent does not see tools/env, **restart**. |
| Plugin tools missing despite correct config after restart | **New chat (`/new`)** or new web session—some clients cache the tool list per thread. **`/new` does not replace restart.** |

For agents: see also [SKILL.md](SKILL.md) (gateway vs. session).

## Plugin: `wordpress-site-tools` (optional)

This monorepo contains the OpenClaw plugin **[`openclaw-wordpress-tools/`](../openclaw-wordpress-tools/)** (plugin ID **`wordpress-site-tools`**). **ClawHub-only install?** Use the standalone repo: **[github.com/realM1lF/openclaw-wordpress-tool](https://github.com/realM1lF/openclaw-wordpress-tool)**. It registers **`wordpress_connection_check`**, **`wordpress_rest_request`**, **`wordpress_wp_cli`**, optional **`wordpress_media_upload`**, optional **`wordpress_plugin_files`** (see plugin README).

**Skill from ClawHub only:** The plugin is **not** in the skill bundle. Install separately from GitHub or a local clone (`openclaw plugins install …`, `enable`, `tools.allow`, gateway restart).

1. In the plugin directory: `npm install`
2. Install and enable:

   ```bash
   openclaw plugins install /path/to/openclaw-wordpress-tool
   openclaw plugins enable wordpress-site-tools
   openclaw gateway restart
   ```

3. **Allow tools** (optional tools need an allowlist), e.g. in `~/.openclaw/openclaw.json`:

   ```json5
   {
     tools: {
       allow: [
         "wordpress_connection_check",
         "wordpress_rest_request",
         "wordpress_wp_cli",
         "wordpress_media_upload",
         "wordpress_plugin_files",
       ],
       // or all tools from this plugin:
       // allow: ["wordpress-site-tools"],
     },
   }
   ```

4. Env per [references/AUTH.md](references/AUTH.md): **`WORDPRESS_SITE_URL`**, **`WORDPRESS_USER`**, **`WORDPRESS_APPLICATION_PASSWORD`** (REST); **`WORDPRESS_PATH`** (WP-CLI cwd for `wp`). Optional overrides under `plugins.entries.wordpress-site-tools.config`.

Full plugin docs: **`openclaw-wordpress-tools/README.md`** in the monorepo, or after cloning **[openclaw-wordpress-tool](https://github.com/realM1lF/openclaw-wordpress-tool)**—use an **absolute** path with `openclaw plugins install`.

## Gating (metadata)

**OpenClaw UI:** `metadata.openclaw.homepage` in `SKILL.md` is the **Website** link in the Skills UI ([OpenClaw docs](https://docs.openclaw.ai/skills/)). It points to the **[wordpress-site-tools](https://github.com/realM1lF/openclaw-wordpress-tool)** GitHub repo so users go straight to the recommended plugin; the YAML **`description`** is also included in the gateway’s **skill list** shown to the model (plugin recommendation appears there too).

`SKILL.md` sets:

- `metadata.openclaw.requires.anyBins: ["wp","curl"]` — **at least one** of these binaries on **PATH** (host or sandbox).
- `metadata.openclaw.requires.env: ["WORDPRESS_SITE_URL","WORDPRESS_USER","WORDPRESS_APPLICATION_PASSWORD"]` — must be set (host env or `skills.entries["wordpress-expert"].env`) for the skill to be **eligible**, aligned with typical REST use.

**Decision (conservative):** Keep both `wp` and `curl` for documented **fallbacks** ([references/TOOLING.md](references/TOOLING.md)). Narrow `anyBins` only if you verify with `openclaw skills list --eligible`.

Documentation-only use **without** WordPress credentials requires a **local fork** of `SKILL.md` metadata (remove or relax `requires.env`)—not the stock ClawHub bundle.

## OpenClaw configuration (snippet)

Example **snippet** for skill + plugin + tool allowlist (secrets as placeholders; file usually `~/.openclaw/openclaw.json`, JSON5):

```json5
{
  skills: {
    entries: {
      "wordpress-expert": {
        enabled: true,
        env: {
          WORDPRESS_SITE_URL: "https://staging.example.com",
          WORDPRESS_USER: "…",
          WORDPRESS_APPLICATION_PASSWORD: "…",
          // Only if gateway has filesystem access to WordPress:
          // WORDPRESS_PATH: "/var/www/html",
        },
      },
    },
  },
  plugins: {
    entries: {
      "wordpress-site-tools": {
        enabled: true,
        config: {
          // Optional: wordpressPath, wpCliRunner ("ddev" for DDEV), baseUrl, wpCliProfile, wpCliAllowPrefixes – see WPCLI_PRESETS.md / DDEV.md
        },
      },
    },
  },
  tools: {
    allow: [
      "wordpress_connection_check",
      "wordpress_rest_request",
      "wordpress_wp_cli",
      "wordpress_media_upload",
      "wordpress_plugin_files",
    ],
  },
}
```

- Key **`wordpress-expert`** matches `metadata.openclaw.skillKey` in `SKILL.md`.
- `env` is injected only if the variable is not already set ([Skills](https://docs.openclaw.ai/tools/skills)).
- Optional plugin tools are **not** visible without `tools.allow` ([Agent Tools](https://docs.openclaw.ai/plugins/agent-tools)).
- **Sandbox:** containers do not automatically inherit host `process.env`; also respect sandbox tool allowlists. Details: [references/OPENCLAW_INTEGRATION.md](references/OPENCLAW_INTEGRATION.md); short: [Skills Config](https://docs.openclaw.ai/tools/skills-config).

## Local `.env`

See [`.env.example`](.env.example). Do not commit `.env`.

## Quality assurance

After install: checks and REST/WP-CLI smoke tests in **[references/CONNECTING.md](references/CONNECTING.md)** (verification).

## Maintainer (monorepo)

ClawHub publish, release checklist, test matrix, roadmap, and `skills-ref validate`: in git under `docs/openclaw-wordpress/` (not part of the ClawHub skill bundle).

**ClawHub upload:** the web UI accepts **text files only**—build a package with [`scripts/package-wordpress-expert-for-clawhub.sh`](../scripts/package-wordpress-expert-for-clawhub.sh), then upload the generated **`wordpress-expert`** folder.

**Plugin GitHub repo** (`wordpress-site-tools`): [github.com/realM1lF/openclaw-wordpress-tool](https://github.com/realM1lF/openclaw-wordpress-tool)—export/push from monorepo: [`scripts/export-openclaw-wordpress-tools-for-github.sh`](../scripts/export-openclaw-wordpress-tools-for-github.sh), details in `docs/openclaw-wordpress/CLAWHUB_PUBLISH.md`.

**ClawHub listing:** [clawhub.ai/realM1lF/wordpress-expert](https://clawhub.ai/realM1lF/wordpress-expert)

**ClawHub page title:** must be set with **`clawhub publish --name "WordPress Expert"`** (not from `SKILL.md` H1)—[docs/openclaw-wordpress/CLAWHUB_DISPLAY_NAME.md](../docs/openclaw-wordpress/CLAWHUB_DISPLAY_NAME.md).

## Repo layout (parent repository)

```
openclaw-wordpress-skill/     # this skill (AgentSkills layout)
openclaw-wordpress-tools/     # OpenClaw plugin: wordpress-site-tools
docs/openclaw-wordpress/      # maintainer: ClawHub, QA, test matrix, roadmap
```

Skill files (excerpt):

```
openclaw-wordpress-skill/
├── SKILL.md
├── README.md
├── .env.example
├── .gitignore
├── bundled/mu-plugin/
└── references/
```
