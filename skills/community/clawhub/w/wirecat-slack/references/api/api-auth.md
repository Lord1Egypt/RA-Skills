<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: auth

## `slk api auth revoke [options]`

- What: auth\_revoke — destructive (GET /auth.revoke)
- Call: `GET /auth.revoke`, effect: destructive
- Permission keys: `slack.delete`

| Flag | Required | What |
|---|---|---|
| `--test <value>` | no | Setting this parameter to \`1\` triggers a \_testing mode\_ where the specified token will not actually be revoked. |

## `slk api auth test`

- What: auth\_test — read (GET /auth.test)
- Call: `GET /auth.test`, effect: read
