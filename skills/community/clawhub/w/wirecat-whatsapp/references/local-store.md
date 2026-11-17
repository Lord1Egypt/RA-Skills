# What the local store adds: reviews, tasks, threads, notes, labels

These work on what `wa` has stored and never connect. Counts and results describe only stored history. The ids are
made up — use the real ones from the previous answer.

## Reviews and tasks

```sh
wa personal review 'date>1d' --json                # every message, the owner's too, in chats that changed
wa personal review --unanswered --json             # questions nobody answered in 24 h
wa personal tasks list state:open --json           # what waits on the owner; review and serve open and close tasks
wa personal tasks scan 100000000000001@lid --json  # a chat's history as tasks: lists only; --yes once the owner agrees
# rules: one-to-one chats fully; groups only replies to the owner and mentions (tag watch-tasks for all); channels never
wa personal tasks add "$LOCATOR" --type promise --category money --assignee sender --json  # LOCATOR: a hit's msg:…
wa personal tasks list "assignee:any state:open" --json   # what others owe the owner
wa personal tasks close 12 --as dismissed --reason no-reply-needed --json  # only after the owner says so
```

## Threads, people, labels, mentions, statistics

- **Conversations:** `wa personal conversations links rebuild --chat 120363000000000001@g.us --json` finds the threads
  in a group, then `conversations list` and `conversations show`.
- **People:** `contacts aliases set|remove` is a local name, `contacts notes add|list|show|edit|remove` private notes;
  both stay on this computer and change nothing on WhatsApp. `contacts show --with-notes` includes the notes.
- **Labels:** `wa personal tags add work --chat 120363000000000001@g.us` labels a chat, person, message or task;
  `tag:work` finds it in a search. `searches create` saves a search; `search messages --saved <name>` runs it.
- **Mentions:** phones, e-mail addresses and links written in stored messages, by `mentions list kind:phone`,
  `kind:email`, `kind:url`. Mention text goes to the owner only.
- **Statistics:** `stats messages show --by sender`, `stats messages unanswered`, `stats contacts top`. Counts
  describe only stored history.
