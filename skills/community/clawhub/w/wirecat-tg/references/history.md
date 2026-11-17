# The local store, sync and offline reads

Read before downloading history, answering `--offline`, exporting, repairing gaps, or when a search says history is
`missing`.

- **`tg personal store export` exports only what was kept**, and never asks Telegram. `tg personal store status` says
  how much of each chat is kept.
- **`tg personal messages sync` makes many requests from the owner's account.** Only when the owner asked.
  `tg personal messages sync <chat> --dry-run` only estimates what it would cost and asks Telegram nothing —
  show the owner that first. A long one goes `--background`; `tg personal store jobs show` follows it.
  It skips groups of more than 50 people and history past the history limits, and says so under `limited`;
  `--full-history` on one chat reads past them, only when the owner asked for that chat in full.
- **`--offline` answers from the local store** and never connects. If nothing is kept, it fails.
  A send with `--offline` is always refused.

## Gaps in the stored history

First inspect local `store gaps show`,
then repair only with the owner's authorization using `store gaps repair --fingerprint <hash>`
and explicit gap/message/time/page/pause bounds. `--background` uses ordinary store jobs.
These commands and job metadata are also available through MCP discovery and read/write gateways.
Unknown edges and message-id holes do not prove missing history.
