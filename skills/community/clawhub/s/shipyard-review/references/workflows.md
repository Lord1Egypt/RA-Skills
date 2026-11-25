# Running the helper workflows

Four workflow files in `${CLAUDE_PLUGIN_ROOT}/skills/review/workflows/` hold the whole review. Each one is a recipe: who to start, with which instructions, in which order, and how to combine their answers.

| File | Step | What it does |
| --- | --- | --- |
| `review.js` | 3 | one reviewer per area, merge duplicates, one skeptic per finding that tries to disprove it (all read only) |
| `content-gaps.js` | 4 | shipped features against what the public pages and docs say, then a copy plan in every language |
| `fix-waves.js` | 6 | fixers in waves whose batches share no file, then a dead-code sweep with knip |
| `diff-review.js` | 7 | fresh reviewers on the fix diff, a skeptic per regression, fixes, then the checks |

Every result also lists what could not be checked: `failedAreas` (a reviewer died: run that area again) and `unverified` (a skeptic died: check those findings yourself). Save every result as a JSON file in a scratch folder outside the repo (`review.json`, `fixes.json`, `diff-review.json`). Later steps read them by path, and a result that only lives in the chat is lost when the chat gets long.

## Claude Code: the Workflow tool

Start each one with the Workflow tool and the file's absolute path: `Workflow({ scriptPath: "<absolute path of ${CLAUDE_PLUGIN_ROOT}/skills/review/workflows/review.js>", args: { ... } })`. If the path still shows the variable, run `echo "$CLAUDE_PLUGIN_ROOT"` to get it. Starting this skill is the student asking for a multi-agent review, but say how big the run will be before the first one.

The workflows set the models themselves. Opus: areas with `"strong": true`, every skeptic on a high, critical or security finding, every diff-review reviewer, every diff-review skeptic except on low findings, the diff-review fixes and the content-gaps copy plan. Sonnet: the other areas and skeptics, the dedup, the inventories, the knip sweep and the final check. Fixers follow their batch's `strong` flag. Results land in the run's journal too (`journal.jsonl` in the transcript folder), so a failed save can be recovered from there. To resume after a stop, start it again with `resumeFromRunId`.

## Without a workflow tool

Do the same steps yourself, in order. Open the workflow file and use its prompts, schemas and order as your instructions:

1. For each area (or each batch, or each group), start a helper agent if your agent has them, with the prompt from the file and the same rules (read only for reviewers, the absolute worktree path, files it must not touch). Without helpers, do the areas one at a time yourself, each in a fresh pass, and write each area's findings to the result file before the next.
2. Keep the skeptic step: for every finding, look again with the goal of disproving it, and drop it without concrete evidence. This is what makes the list trustworthy.
3. Run fix batches of one wave at the same time only if your helpers work in the same folder without touching each other's files; otherwise one batch at a time.

## What to pass

- `review.js`: `repo` (the worktree's absolute path), `app` (one paragraph: what it does, the stack), `areas` (the list from `references/areas.md`), and when you have them `skip` (switched-off features), `openItems` (the known-issues doc), `focusAuthor` (the email from step 2).
- `content-gaps.js`: `repo`, `app`, `since` (the date of the last release check), `languages`, `rules` (for example "only the free plan may be advertised"), `docs` (style and glossary files).
- `fix-waves.js`: `repo`, `reviewJson` (absolute path), `batches` and `waves` from `plan-waves.mjs`, `decisions` (`{ "<finding id>": "what the owner chose" }`), `rules` (the app's own rules, such as "every string in both languages").
- `diff-review.js`: `repo`, `groups` (`{ "area": ["changed/file.ts", ...] }`, from `git diff --name-only origin/main` plus the new files that are not committed yet, `git ls-files --others --exclude-standard`, sorted by area), `context` (paths of the saved results), `notes` (deploy facts, such as "new migrations are not applied yet"), `checks` (the commands that must pass).

`superpowers` (optional, every workflow): the absolute path of the superpowers skills folder, if it is installed. The prompts then point helpers at its review and debugging guides.
