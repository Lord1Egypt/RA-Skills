# Rollover Rules

Run a daily rollover at 00:05 Asia/Shanghai.

## Steps

1. Scan `FOCUS`, `TODAY`, `UP NEXT` for explicitly completed items (`- [x] ...`) and treat them as done.
2. Append all human done items into `history/YYYY-MM.md` under `### Human Done`.
3. Append the full `AI DONE TODAY` snapshot into `history/YYYY-MM.md` under `### AI Done Today`.
4. Clear `DONE`.
5. Reset `AI DONE TODAY` to:
   - `- 暂无`
6. Move all unfinished `FOCUS` and unfinished `TODAY` items into the new day's `TODAY`.
7. Keep unfinished `UP NEXT` unchanged.
8. Reset `FOCUS` to empty placeholder.
9. Record `lastRolloverDate` in `todo/system/rollover-state.json` so rollover is idempotent.
