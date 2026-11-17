# Inbox, review, tasks and live updates

Read when the owner asks what is new, unread or unanswered, about tasks and promises, or to watch, serve or auto-reply.

- **`tg personal watch` starts from now; `tg personal serve` catches up.** `serve` runs until stopped and holds
  one lock per profile — start it only when the owner asked. The same goes for `tg <profile> server
  start`; `tg <profile> server status` is safe to read.
- **`tg personal inbox --new` moves the point where the owner stopped.** After it, the owner's next `--new`
  will not show what the agent already saw. Without moving it: plain `tg personal inbox` (unread) or
  `tg personal inbox 'date>2h'`. `date>` takes a time, never a message id.

The ids below are made up — use the real ones from the previous answer.

```sh
tg personal inbox --json                           # other people's unread messages; muted and archived chats
                                                   # only when they mention the owner — `quiet` counts the rest
tg personal inbox --all --json                     # every chat with unread messages, muted and archived too
tg personal inbox 'date>2h' --json           # everything that came in during the last two hours
tg personal review 'date>1d' --json          # every message, the owner's too, in chats that changed — who owes what;
                                                   # when complete, the next review starts at until
tg personal review --unanswered --json             # questions, including retained voice transcripts, nobody answered in 24 h
tg personal review --unanswered --transcribe --json  # hear new voices before filtering; keep the old boundary if incomplete
tg personal tasks list state:open --json         # what waits on the owner; review and serve open and close tasks
tg personal tasks categories --json                # choose a category before tasks add/plan
tg personal tasks scan <chat> --json               # a chat's history as tasks: lists only; add --yes after the owner agrees
# the first sync opens no task from history (task_first_pass_per_chat, 0) — ask before building a chat's tasks
# rules: one-to-one chats fully; groups only replies to the owner and mentions (tag watch-tasks for all); channels never
tg personal tasks add <ref> --type promise --category <name> --assignee sender --json  # someone owes the owner
tg personal tasks list "assignee:any state:open" --json   # what others owe the owner
# the owner edits the list in ~/.config/WireCat/config.json, section task_categories ("name": "meaning | words" or null)
tg personal tasks add <ref> --type request --category documents --json
# exit 2 task.duplicate-candidates: may be the same job as an open task; rerun with --into <id> or --new
tg personal tasks duplicates list --json              # pairs that may be one job; tasks merge <dup> --into <task>
tg personal tasks claim <task> --lease 30m --json     # take before work; tasks release <task> gives it back
# tasks agenda omits others’ claims unless claimed:any; the default claim lasts 30 minutes.
tg personal tasks close <task> --as dismissed --reason no-reply-needed --certainty <0..1> --json  # only after the owner says so
# below task_agent_close_min (0.8 by default) the task stays open with close_suggestion;
# the owner confirms with tasks close or refuses with tasks reject; tasks list close:suggested finds them
```

```sh
tg personal watch --jsonl                          # new messages as {"type":"item","data"} lines, then a {"type":"end"} line
```

## Reply rules

Reply controls: `tg personal replies add|edit|on|off` edit local rules; `replies audience` controls file-level
allow/deny lists (deny wins). `test` previews stored messages without sending; `status`, `pause` and
`resume` control the profile's rules. Liquid reads sender/chat facts only; incoming text goes to a
model only inside ai blocks. Ordinary previews show instruction/fallback with no model call;
`test --ai` explicitly uses a consented provider. `replies consents grant|revoke` controls profile/
endpoint consent and `deny|allow` controls native chat opt-outs. Never widen the audience or run live
scenarios without the owner's separate consent. Shared `serve` replies to everyone a rule matches unless the audience limits it, and only with explicit
`permissions.replies.send:allow`; the default is deny.
