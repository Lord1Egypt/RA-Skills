# Meetings and contacts in Zoom

The core rules in [SKILL.md](../SKILL.md) apply. These commands ask Zoom live, not the local store.

## Change a meeting in Zoom

`meetings update`, `meetings cancel` and `meetings invitation` take Zoom's own meeting id (a number), not a stored
meeting id. Change a meeting only when the owner asked for this exact change.

- A create needs `--start-time`; zm does not start an instant meeting.
- `meetings cancel` without `--occurrence-id` cancels the whole repeating meeting; pass `--occurrence-id` to cancel
  one occurrence.

- Create, update and cancel ask first. Without a terminal, `--yes` applies an authorized change once (else exit `7`).
  `--dry-run` (`zm personal meetings cancel 123456789 --dry-run --json`) shows the command and its permission, not
  what Zoom would receive, and does not check the change; a change Zoom cannot take is refused when it runs.
- Their permission keys are `meetings.create`, `meetings.update` and `meetings.cancel`. A saved `remote-meetings`
  permission key stops every command until the owner removes it with
  `zm personal config unset permissions.remote-meetings`.
- Exit `14` means an uncertain dispatched write: inspect the remote state before retrying. Never automatically replay
  a creation or a cancellation.
- Over MCP a change at level `ask` runs without a question: ask the owner yourself first.

## Contacts

`zm personal contacts list` reads company and external Zoom contacts live (`name:`, `email:`, `type:` narrow it).
`contacts show` takes the `id` it returns, a Zoom user id or an email.
