<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: dnd

## `slk api dnd end-dnd`

- What: dnd\_endDnd — write (POST /dnd.endDnd)
- Call: `POST /dnd.endDnd`, effect: write

## `slk api dnd end-snooze`

- What: dnd\_endSnooze — write (POST /dnd.endSnooze)
- Call: `POST /dnd.endSnooze`, effect: write

## `slk api dnd info [options]`

- What: dnd\_info — read (GET /dnd.info)
- Call: `GET /dnd.info`, effect: read

| Flag | Required | What |
|---|---|---|
| `--user <value>` | no | User to fetch status for (defaults to current user) |

## `slk api dnd team-info [options]`

- What: dnd\_teamInfo — read (GET /dnd.teamInfo)
- Call: `GET /dnd.teamInfo`, effect: read

| Flag | Required | What |
|---|---|---|
| `--users <value>` | no | Comma-separated list of users to fetch Do Not Disturb status for |
