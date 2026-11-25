<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: migration

## `slk api migration-exchange [options]`

- What: migration\_exchange — read (GET /migration.exchange)
- Call: `GET /migration.exchange`, effect: read

| Flag | Required | What |
|---|---|---|
| `--users <value>` | yes | A comma-separated list of user ids, up to 400 per request |
| `--team-id <value>` | no | Specify team\_id starts with \`T\` in case of Org Token |
| `--to-old <value>` | no | Specify \`true\` to convert \`W\` global user IDs to workspace-specific \`U\` IDs. Defaults to \`false\`. |
