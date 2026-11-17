# History: what the store holds and how to get more

- **History comes from the phone, not from a server.** WhatsApp's servers have no "give me older messages" request.
  The phone pushes history once, seconds after the device links, and `wa <profile> serve` keeps receiving after that.
  Every read — `chats list`, `messages list`, `inbox`, `search` — answers from the local store and never connects. A
  search answer may suggest `messages sync` to fill a gap: it asks the phone, for one chat only.
- **Older history** can only be asked of the owner's phone, 50 messages at a time, counting back from the oldest
  stored message of one chat: `wa <profile> messages sync <chat>`. The phone answers only with WhatsApp open on it:
  ask the owner to open it first. No answer is exit `timeout`, not an empty chat; a late answer is still saved by
  `serve`. `--all` is refused: there is no chat list to walk. A chat with nothing stored (`not_found`) cannot be
  asked about until `serve` saves its next message; tell the owner that, do not retry.
- **Not all history is stored, on purpose.** The phone's history is saved within the profile's limits: one-to-one
  chats 3 years (`history_dialog_days`), groups of more than 2 people 1 year (`history_group_days`), and nothing of
  a group above 50 people (`history_group_members_max`). An answer that read a chat with skipped history says so:
  `meta.complete: false`, `missing` with `field: "history_limits"`, and a `next` step. Say that to the owner
  instead of "no messages"; `wa <profile> store status` lists the chats.
- **A chat in full.** When the owner asks for a chat in full, `wa <profile> messages sync <chat> --full-history` keeps
  it whole from then on and fetches what the phone still answers — only recent messages: the phone answers older
  history only once, when a device is linked. What the limits skipped before comes back with the next link
  (`wa <profile> session end`, then `session start`), not by asking.
- **A read with no `serve` behind it may be stale**, and says so on stderr. Start `serve` only when the owner asks
  ([connection](connection.md)); never stop the owner's. `wa personal doctor` shows whether the
  engine is installed, whether the device keys exist with private file modes, and who last held the lock.
- **Starred messages are read from the store.** `messages list <chat> starred:true` and `search messages is:starred`
  answer offline; while `serve` runs, the store follows stars set or taken off on the phone too.
- **Poll counts are what the store heard.** WhatsApp has no request for votes: `serve` and `watch` keep each
  person's newest vote as it arrives, and `polls show` and `polls voters` count those. A vote cast while nothing
  listened is missing.
- **Group events are what the store heard.** `chats events` answers from the store: the joins, leaves, adds,
  removals, admin changes and titles the phone pushed and `serve` saw, which `stats chats show` counts in `members`;
  one from before the link the phone did not push is missing. `chats members history` shows who joined or left
  between member fetches.
- **`wa personal store status` says how much of each chat is kept**; `wa personal store export` exports only that.
