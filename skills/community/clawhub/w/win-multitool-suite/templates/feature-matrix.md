# Feature matrix - Windows Multi-Tool Suite

Three things, compared honestly. No tier that does not exist, no price that
is not published.

| Capability | Windows kit (today) | Agent skills (today) | Desktop app (separate download) |
| --- | --- | --- | --- |
| Price | Free | Free | See the publisher's GitHub release |
| Install | One PowerShell setup | One CLI command per skill | One `.zip` from the publisher's GitHub release |
| OS | Windows 10/11, 64-bit | Anywhere the agent runs | Windows 10/11, 64-bit |
| Admin rights | Not needed | Not needed | Not needed |
| Creative brief to ad copy | via the Creative skill | yes | not built around it |
| Social posts, UGC scripts, image and video prompts | via the Creative skill | yes | not built around it |
| US market snapshot, technicals, fundamentals | via the Market skill | yes | not built around it |
| Backtests and risk-first position sizing | via the Market skill | yes | not built around it |
| Written trade plan with a human approval gate | via the Market skill | yes | not built around it |
| ICP builder, company research, scored prospect list | via the Lead skill | yes | not built around it |
| Outreach drafts with CAN-SPAM linting | via the Lead skill | yes | not built around it |
| GUI | no | no | yes |
| Scheduled jobs | no | depends on your agent runtime | not verified |
| Local workspace and local output files | yes | yes | not verified |
| API keys stay on your machine | yes | yes | not verified |
| Telemetry | none | none | not verified |
| Sends email on your behalf | no | no | no |
| Places trades | no | no | no |

## Notes

**Windows kit (today).** The kit does not reimplement the workflows. It
installs the three skills from this catalog, creates a workspace and a config
file, and gives you a launcher menu. It is the Windows path, not a separate
product.

**Agent skills (today).** The same three workflows, run inside your AI
assistant. If you already have a setup, use these and skip the kit.

**Desktop app.** The publisher's Windows Multi-Tool Suite app, published on the
GitHub release as `multitool.zip` with its SHA-256 in this skill's `SKILL.md`
so you can check the file before you unpack it. No skill bundle carries it: a
registry blocks a skill that ships an unsigned binary. The installer asks for a
password; ask the publisher for it. It is not part of this kit.

## Every version includes

- SHA-256 checksums for any binary that is ever published.
- No installer that pipes a download into a shell.
- No telemetry, no usage ping, no account requirement.
- Local workspace; nothing is uploaded unless you point a workflow at a
  provider you configured.
- Release notes for every change.

## No version includes

- Investment advice or order placement.
- Sending email or messages on the user's behalf.
- Bulk sending, list buying, or scraping of personal data.
- Access to leaked or breach-derived data.
- Claims about results, returns, or uptime that are not measured and
  published.

Say what a version does not do. Buyers who know the boundary trust the product
more.
