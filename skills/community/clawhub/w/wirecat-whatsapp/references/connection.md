# One connection: serve, watch and the device lock

- **One connection per linked device.** WhatsApp drops the older of two connections.
- **While `serve` runs, every command for that profile that connects runs inside `serve`**, on its connection: sends,
  edits, deletions, reactions, mark-read, downloads, group and people commands, `watch`, `doctor --online` and
  `wa <profile> mcp serve`. Permissions and the send guard still apply. It never asks: a write at permission level
  `ask` needs `--yes` (`--allow-dangerous` for a deletion), or it is refused and says so. Those flags are the owner's
  word: never add them on your own.
- **Never stop the owner's `serve`.** If `serve` is starting or does not answer, the command fails; tell the owner.
- With no `serve`, `watch` and every command that connects take the device's lock; a second one is refused with exit
  `12` and names the holder (`device.in-use`: stop it or use `serve`, but never the owner's `serve`). Exit `12` also
  means another connection took the device over (`device.replaced`), the engine stopped (`engine.stopped`), or
  WhatsApp refuses this version (`client.outdated`: tell the owner to update).
- **On Windows nothing goes through `serve` yet**, so there a command that connects is refused that way while `serve`
  runs (`serve (pid 4242)`): tell the owner, do not stop it.
- `wa personal mcp serve` keeps a connection it opened until two minutes pass without a call, and `serve` cannot start
  meanwhile.
- **`wa personal watch` starts from now and holds the connection; `wa personal serve` does too and fills the store.**
  Start either only when the owner asked. The same goes for `wa <profile> server start`; `wa <profile> server status`
  is safe to read. Its `current_at` is when the store was last current: messages newer than that are not in it
  until `serve` runs again.
- `serve` never answers by itself: WhatsApp bans accounts that answer like a bot, so nothing sends unless the owner
  asked for that message. `wa` has no `replies`.

## watch --jsonl

`wa personal watch --jsonl` prints new messages as they arrive and holds the connection. Read each message from the
item record's `data` field, using snake_case keys. With `--events`, `data.event` names the change. Wait for the final
`type: "end"` record and check `complete`; an absent end means the stream was cut. A source failure also returns a
nonzero exit code.
