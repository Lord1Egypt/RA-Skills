# Ready prompts for Claude Code

Use these prompts inside Claude Code when working in the `webtop-galim` repo.

## Daily status

```text
Open CLAUDE.md in this repo, then run:
bash scripts/claude-code-wrapper.sh expanded --days 7 --limit 3

Summarize the result in Hebrew.
Put overdue or urgent items first.
If there are no urgent items, say that clearly.
```

## Full combined report

```text
Use the wrapper in this repo to run a combined school-task check.
Run:
bash scripts/claude-code-wrapper.sh report

Then summarize the results in Hebrew for a parent.
Keep it concise and practical.
```

## Ofek only

```text
Run:
bash scripts/claude-code-wrapper.sh ofek --json

Then summarize per child in Hebrew:
- לביצוע
- לתיקון
- ממתינות
- נבדקו
- משימות גלויות באופק עם כותרת, מקצוע, מורה ויעד אם קיימות

Flag anything unusual.
```

## Ofek detailed parent report

```text
Run:
bash scripts/claude-code-wrapper.sh ofek --json

Build a Hebrew parent-friendly report for each child.
Include:
- counts (לביצוע / לתיקון / ממתינות / נבדקו)
- visible urgent items if present
- visible overdue items if present
- for each visible item: title, subject, teacher, due date

Keep the structure concise and easy to read in WhatsApp.
```

## Galim only

```text
Run:
bash scripts/claude-code-wrapper.sh galim --json --hide-overdue --due-within-days 14

Summarize in Hebrew by child.
List the next due tasks first.
```

## Webtop only

```text
Run:
bash scripts/claude-code-wrapper.sh webtop

Return a short Hebrew summary of today's homework state.
```

## Calendar sync

```text
Open CLAUDE.md in this repo and run:
bash scripts/claude-code-wrapper.sh sync --days 30

Then tell me in Hebrew whether the sync succeeded and what changed.
If it failed, show the real error briefly.
```

## Troubleshooting

```text
Check the local setup for this repo.
Run:
bash scripts/claude-code-wrapper.sh env-check

If anything important is missing, explain exactly what is missing without exposing secrets.
Then suggest the next command to run.
```
