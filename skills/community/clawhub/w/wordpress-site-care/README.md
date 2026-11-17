# WordPress Site Care

An OpenClaw skill for looking after a WordPress site safely.

- **Checks** WordPress, PHP, plugins, themes, offered updates, Site Health, the error log, a
  stuck maintenance file, the backup state, and the front end, without changing anything.
- **Plans** updates in a safe order (security first, base plugins before add-ons, parent theme
  before child, major core releases last) with a check and a rollback for every step.
- **Confirms a recent, complete, off-server backup** before every change.
- **Changes one approved step at a time**, using dry runs where the tool has them, and verifies
  after each step. An approval covers only the exact step shown.
- **Never** stores or prints credentials and gives no removal steps for databases, users, or
  files. Personal data from the site leaves it only when the owner explicitly agrees.
- **Works only on the sites the owner names** for the task, even when a dashboard lists more.

Works with no extra tools (the owner pastes Site Health info). Optional sections for WP-CLI,
Novamira, WPCodeBox, Modular DS, and Cloudflare apply only when the owner has them.

Everything is in the skill file itself. Tested read-only against a live WordPress 7.1 site, November 2026.
