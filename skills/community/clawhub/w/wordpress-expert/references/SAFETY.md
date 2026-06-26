# Safety and defaults

Safety and defaults for WordPress work through OpenClaw (host).

**Privilege tiers:** [CONNECTING.md](CONNECTING.md) (section *Privilege tiers*). **Trust checklist:** [PRE_INSTALL_AND_TRUST.md](PRE_INSTALL_AND_TRUST.md).

## Destructive actions

There are no built-in PHP tools here—everything goes through shell/HTTP/browser. Therefore:

- Commands like plugin/theme delete, forced post delete, recursive `rm`, database drops: only on explicit user instruction. Ask if unsure.
- Before delete or theme switch: document current state; recommend backup.

## Safety defaults

- New posts and pages: prefer **draft** unless the user wants published.
- Plugins: only from wordpress.org or known sources.
- Never delete or lock the current admin account.
- No raw direct DB changes without clear instruction and rollback plan.

## Global WordPress settings

Do not change as side effects unless explicitly requested: `blogname`, `blogdescription`, `show_on_front`, `page_on_front`, `page_for_posts`, `permalink_structure`, `default_role`, `users_can_register`, `template`, `stylesheet`.

For WP-CLI: no bulk `option update` without confirmation.

## Injection

Never embed raw user text in shell commands. Use fixed subcommands and safe quoting.

OpenClaw sandbox and elevated policies: https://docs.openclaw.ai/gateway/security

## Third-party code

Do not patch third-party plugins directly. Prefer custom plugins or child themes.

## Environment and profiles

- **Staging vs. production:** Broad WP-CLI presets (`staging-admin`, `dev-local`) and write REST calls only with **staging** targets and clear rollback/backup—do not mix the same credentials as read-only profiles.
- **JSON patterns:** [CONNECTING.md](CONNECTING.md) “Operational profiles”.
- **Plugin development:** rules and checklists: [PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md).

## Critical settings

Read, change, verify. Only report done when verification passes.

## Communication

Optional: friendly tone; keep chat concise (save tokens).

## MUST NOT (operational, summary)

Complements [PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md) **MUST NOT** for day-to-day operation:

- Modify WordPress core files.
- Run destructive WP-CLI or SQL without explicit user approval.
- Paste application passwords or secrets into chat or Git.
- Bypass allowlists by encouraging unsafe `exec` when `wordpress_wp_cli` or `wordpress_rest_request` are available and appropriate.
