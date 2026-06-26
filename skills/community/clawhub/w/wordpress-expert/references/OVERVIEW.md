# WordPress Expert – reference index

Skill id **`wordpress-expert`** (ClawHub display name **WordPress Expert**). Short map of `references/` (progressive disclosure).

| File | Content |
|------|---------|
| [PRE_INSTALL_AND_TRUST.md](PRE_INSTALL_AND_TRUST.md) | Before install: trust plugin/MU helper, credentials, ClawHub bundle vs full repo, least privilege |
| [CONNECTING.md](CONNECTING.md) | Connect existing site to OpenClaw: topologies, app password, `openclaw.json`, MU bundle, `wordpress_plugin_files`, verification, **gateway restart vs `/new`** |
| [../bundled/mu-plugin/README.md](../bundled/mu-plugin/README.md) | Optional MU helper (PHP)—copy to `wp-content/mu-plugins/`; route reference |
| [MU_HELPER.md](MU_HELPER.md) | **When** the MU helper helps (REST-only, sandbox, vs WP-CLI / `wordpress_plugin_files`) |
| [OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md) | OpenClaw: global tool policy, sandbox allowlists, `group:openclaw` vs plugin tools, env host vs container, official doc links |
| [DDEV.md](DDEV.md) | Local DDEV sites: REST URL, `wpCliRunner` / `ddev wp`, `WORDPRESS_PATH` |
| [NATIVE_VS_PLUGIN.md](NATIVE_VS_PLUGIN.md) | When plugin tools vs OpenClaw `exec` / browser / workspace |
| [WPCLI_PRESETS.md](WPCLI_PRESETS.md) | `wpCliProfile` presets and manual `wpCliAllowPrefixes` for the plugin |
| [USER_EXPECTATIONS.md](USER_EXPECTATIONS.md) | User expectations, UX, target picture vs implementation |
| [FOR_SITE_OWNERS.md](FOR_SITE_OWNERS.md) | Plain language for non-technical site owners |
| [TOOLING.md](TOOLING.md) | WP-CLI vs REST vs browser; pointer to NATIVE_VS_PLUGIN |
| [AUTH.md](AUTH.md) | URLs, application passwords, environment variables |
| [WORKFLOWS.md](WORKFLOWS.md) | Read, Plan, Write, Verify |
| [SAFETY.md](SAFETY.md) | Draft defaults, risky options, destructive actions, MUST NOT summary |
| [DOMAIN.md](DOMAIN.md) | Blocks, plugins, CPT, REST, common pitfalls |
| [PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md) | Plugin development: hooks, REST, security, layout, OpenClaw workflow |
| [BLOCK_EDITOR.md](BLOCK_EDITOR.md) | Block editor: scaffold, static vs dynamic, `block.json`, REST vs files |
| [THEME_AND_TEMPLATES.md](THEME_AND_TEMPLATES.md) | Classic vs block themes, hierarchy, child themes, FSE |
| [PERFORMANCE_AND_SECURITY.md](PERFORMANCE_AND_SECURITY.md) | Query/cache/asset hygiene, REST and upload hardening |
| [WOOCOMMERCE.md](WOOCOMMERCE.md) | WooCommerce limits and workflows (REST, WP-CLI) |
| [ELEMENTOR.md](ELEMENTOR.md) | Elementor layouts and constraints |

Content: curated WordPress / OpenClaw working rules for agents on the host.

**Maintainer** (ClawHub, test matrix, roadmap, release): in monorepo `docs/openclaw-wordpress/`—not in the ClawHub skill bundle.
