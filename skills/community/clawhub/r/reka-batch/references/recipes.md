# Batch recipes

Each recipe says what goes in the shared prefix (identical in every row, so it can bill at the
cache-read rate), what goes in each row, and how to check the answers. Commands assume
`RB="python3 {baseDir}/scripts/reka_batch.py"`.

## Contents
1. Label or enrich a spreadsheet
2. Many questions over one long document or codebase (the cheapest shape)
3. Generate content in bulk, then let code decide what ships
4. Translate strings with a glossary
5. Per-file code sweeps overnight
6. Anti-patterns

## 1. Label or enrich a spreadsheet

Shared prefix: the labelling instructions, the allowed labels, two or three examples.
Each row: one spreadsheet row. Answer: a small JSON object.

```
cat > system.txt <<'EOF'
You label customer support tickets. Reply with JSON only: {"label": "billing" | "technical" | "account", "urgent": true | false}
Examples: "Charged twice this month" -> {"label": "billing", "urgent": true}
EOF
echo 'Ticket {{id}}: {{subject}} - {{body}}' > prompt.txt
$RB make --items tickets.csv --id-field id --system system.txt --prompt prompt.txt \
  --model glm5.3-flash --max-tokens 128 --reasoning none --json-mode --out requests.jsonl
$RB estimate requests.jsonl --avg-output 20
```

Check: parse every `content` as JSON; anything that fails to parse or has a label outside the
allowed set goes into a retry file with the row's original request.

## 2. Many questions over one long document or codebase

This is where batch pricing is strongest: the long context is the shared prefix, so after the
first rows it can bill at the cache-read rate, and each answer is short.

Shared prefix: the document (a contract, a policy, a code map, a design doc) and how to answer.
Each row: one question, or one item to check against the document.

Good fits: "check each of these 2,000 customer emails against our refund policy", "for each of
these 300 functions, say whether it follows the conventions in this style guide", "answer each
eval question using only this manual" (eval generation and grading).

Keep the prefix byte-identical: no timestamps, row numbers or per-row names in it. Put the
question last. `estimate` shows the shared prefix it detected and the cost with and without
cache hits; actual cache hits depend on how Reka schedules the rows and show up in `collect`.

## 3. Generate content in bulk, then let code decide what ships

Shared prefix: the style guide or "bible", the JSON schema for each content type, hard rules
(forbidden names, length limits). Each row: a content type, a count, a distinct brief (theme,
seed, difficulty band) and a unique id prefix.

Rows cannot see each other, so diversity has to come from the briefs and duplicates have to be
removed afterwards. Then validate locally, and only ship what passes: schema, lengths for the UI,
originality (no third-party names), uniqueness, and any domain check you can compute (for game
levels: simulate them). Keep rejected items with their reason; plan a top-up batch for gaps.

Use `response_format: {"type": "json_object"}` and ask for `{"items": [...]}`. Validate against
the schema yourself even when the model is asked to follow it.

## 4. Translate strings with a glossary

Shared prefix: the product glossary, do-not-translate terms, tone, placeholder rules, length
budgets. Keep the target locale out of the prefix, so every locale shares one cached prefix.
Each row: target locale plus 20-30 key/value pairs as JSON. Answer: the same keys, translated.

Check per key: same key set, identical `{placeholders}`, do-not-translate terms preserved, length
within the UI budget (allow some expansion for German, French and similar). Re-plan only the keys
that are still missing in each locale.

## 5. Per-file code sweeps overnight

A batch cannot run an agent loop, but many repo-wide changes are one independent edit per file:
adding docstrings or type hints, migrating an API call, replacing a logging pattern, writing a
test file per module, translating comments, extracting user-facing strings.

Shared prefix: the task, the repo's conventions (AGENTS.md, CLAUDE.md, CONTRIBUTING.md), a short
map of the files and their public functions, and the answer format. Each row: one file, read
from `git show HEAD:path` so uncommitted work is never involved.

Answer format: SEARCH/REPLACE edit blocks rather than whole files. They cost far fewer output
tokens, and a block that does not match the file exactly is rejected instead of corrupting it.

```
<<<<<<< SEARCH
exact lines from the file
=======
replacement lines
>>>>>>> REPLACE
```

Apply on a separate git worktree branch; reject edits that do not apply, do not parse, or shrink
the file suspiciously; run the test suite; isolate failures file by file; commit what passes;
send failures back as a second batch with the error text as feedback. Cap it at two or three
rounds and leave the rest for a human. The check command runs code the model edited, so run it
where you would run CI for an untrusted pull request.

## 6. Anti-patterns

- **An agent loop in disguise.** If request 2 needs the answer to request 1, it does not belong
  in the same batch. Each round trip can take hours.
- **Tiny jobs.** Ten requests are cheaper in engineering time on the live API, and come back in
  seconds.
- **Output-heavy jobs with no shared context.** Long free-form generation from short prompts gets
  only the flat 50% discount; compare against live prices before promising big savings.
- **Varying prefixes.** A date, a row number or a shuffled example list at the top of every row
  makes every row a cache miss.
- **Trusting "completed".** A completed batch can contain failed rows, empty answers (thinking used
  the budget) and answers cut off at `max_tokens` (`truncated` in results.jsonl). Check them.
- **Sending secrets.** Batch is not zero data retention. Strip or tokenize personal data first, or
  ask the user, and run `cleanup` when done.
