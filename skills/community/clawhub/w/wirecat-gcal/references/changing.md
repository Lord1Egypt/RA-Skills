# Changing events

Make a change only when the owner asked for it. The rules in [SKILL.md](../SKILL.md) hold for every command here.

- `events create <calendar>`, `events update event:<id>`, `events delete event:<id>`,
  `events move event:<id> --to-calendar <id>` and `events respond event:<id> accepted|tentative|declined` change Google
  Calendar. They need a profile signed in with `session start --grant write`; without it they fail with
  `permission_error`. Ask the owner to sign in again.
- Create, update, move and respond run without a question by default; a delete asks, and over MCP runs.
- With attendees other than the owner, pass `notify: false` (`--no-notify`) unless the owner asked you to mail them.
  `events.notify` is denied by default; do not ask to loosen it on your own.
- `event.conflict` means the event changed in Google since the last sync: run `sync`, read the event again, then
  decide. `outcome_unknown` on a create names an id: repeat the create with `--operation-id <id>`, never without it.
- `--series` changes or deletes every occurrence, and `--following` this one and every later one; use them only when
  the owner said so. `outcome_unknown` on `update --following` names the new series' id: repeat with
  `--operation-id <id>`. A new `--repeat` rule that ends a series sooner needs `events.delete.series`, which is denied
  by default.
- `events move` keeps the event's id; an occurrence moves only with `--series`, the whole repeating event.

## Google Meet links

`events create … --conference google-meet` gives the new event a Google Meet link (its `join_url`);
`events update event:<id> --conference google-meet` adds one to an event that has none. Both need `--grant write`.
Meet rooms without an event are in [meet.md](meet.md).

## Quick add, import, repeating events

- `events create <calendar> --text "<line>"` lets Google read the title, day, time and place from one line, with no
  other field options. On `outcome_unknown`, repeat it with the same line and `--operation-id <the operation_id it
  named>`: gcal looks for the event that attempt made before it adds another.
- `events import <calendar> <file.ics>` adds a file's events under their UIDs and mails nobody; it asks by default
  (`events.import`). Read `skipped` for events it left out, and on a failure `details.imported` for what went in.
- `--repeat "FREQ=WEEKLY;BYDAY=MO;COUNT=10"` makes or changes a repeating event (on update, with `--series`); run
  `sync` after it. New dates on a timed event make it all-day, and new times make it timed again.

## Permissions

A write runs only as far as the profile's permissions (`events.*` and `api.<method>` keys) allow. `--dry-run` shows
what a command would do first: the permission key it checks and its level. It sends nothing.
