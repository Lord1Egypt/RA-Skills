---
name: reka-batch
description: Run large, non-urgent LLM jobs on Reka's Batch API at 50% of live token prices, with results within 24 hours. Use this whenever the user wants the same kind of prompt run over many items - labelling or enriching a CSV or dataset, generating content or test cases in bulk, translating many strings, summarising a folder of documents, or reviewing or transforming many files overnight - or mentions batch, bulk, overnight, "cheaper", or /reka-batch, even if they never say "batch". Not for chat, single questions, or multi-step agent loops.
license: MIT
compatibility: Python 3.9+ (standard library only), network access to api.reka.ai, and a REKA_API_KEY.
metadata: {"openclaw": {"emoji": "🌙", "homepage": "https://developer.reka.ai/batch", "primaryEnv": "REKA_API_KEY", "requires": {"bins": ["python3"], "env": ["REKA_API_KEY"]}}}
---

# Reka batch jobs

Reka's Batch API takes a JSONL file of independent Chat Completions requests and returns every
answer within 24 hours, billed at half the live rate (cached input too). It is the right tool when
there are many items, each request stands alone, and nobody is waiting on the answer.

`{baseDir}` below is this skill's folder. OpenClaw fills it in; elsewhere, use the folder this file
is in. Every command prints a human summary, or JSON with `--json`, which is easier for you to read.

```
python3 {baseDir}/scripts/reka_batch.py <make|validate|estimate|submit|status|wait|collect|cancel|cleanup|list> ...
```

## First, check that batch fits

Batch rows cannot see each other and cannot call tools across turns, so a batch is a fan-out, not an
agent. Use it when all of these hold:

- There are many items (roughly 50 or more; below that the live API is simpler and just as cheap).
- Each item can be answered in one request, from what you put in that request.
- The user can wait hours. Reka promises results within 24 hours, not a typical time.

If the job is a multi-step task (a refactor that needs to read, edit, test and fix), split it into
one self-contained request per unit of work (per file, per row, per document), check the answers
locally afterwards, and send failures back as a second batch with the error as feedback. Say so to
the user rather than promising an overnight agent.

Only two models are offered for batch: `glm5.3-flash` (default: cheaper and stronger in general)
and `qwen3.8-27b`. One model per file. See `references/api-notes.md` for limits and prices.

## Workflow

1. **Shape the job with the user.** What are the items, what should each answer look like, and how
   will they use the results? Prefer short, structured answers (JSON with a fixed set of keys).

2. **Build the request file.**
   - Tabular items (CSV/TSV/JSONL) plus one prompt: use `make`. Placeholders are `{{column}}`, so
     JSON examples with single braces stay intact.
     ```
     python3 {baseDir}/scripts/reka_batch.py make --items tickets.csv --id-field id \
       --system system.txt --prompt prompt.txt --model glm5.3-flash \
       --max-tokens 256 --reasoning none --json-mode --out requests.jsonl
     ```
   - Anything else (files in a repo, documents, generated briefs): write a short script that emits
     one row per item with `build_request(custom_id, model, messages, **params)` from the same
     module, or produce the JSONL directly. `references/recipes.md` has worked patterns.

3. **Validate and estimate, then confirm before spending.**
   ```
   python3 {baseDir}/scripts/reka_batch.py validate requests.jsonl
   python3 {baseDir}/scripts/reka_batch.py estimate requests.jsonl --avg-output 150
   ```
   Show the user the row count and the estimated batch cost range, say it is a rough estimate, and
   get a yes before submitting. Fix every validation error; take warnings seriously (see below).

4. **Submit** with a dedicated state folder per job:
   ```
   python3 {baseDir}/scripts/reka_batch.py submit requests.jsonl --state-dir runs/<job-name>
   ```
   Rerunning the same command is always safe: it never uploads or creates twice. If it reports
   the queue is full, rerun with `--wait-queue` or try later. If it reports an uncertain upload,
   rerun it; it looks for the earlier upload before sending another.

5. **Arrange the check-in.** There are no webhooks; someone has to poll.
   - OpenClaw: offer a one-shot automation for the morning (or a few hours out) that runs
     `status`, and `collect` once finished, and reports in this chat.
   - Hermes: offer a cron job doing the same.
   - Otherwise: give the user the `status` and `collect` commands, or run
     `wait --state-dir ... --notify-cmd '<their command>'` in a terminal they keep open. The notify
     command receives RB_BATCH_ID, RB_STATUS, RB_TOTAL, RB_COMPLETED, RB_FAILED and RB_STATE_DIR,
     never the API key.

6. **Collect and report honestly.**
   ```
   python3 {baseDir}/scripts/reka_batch.py collect --state-dir runs/<job-name>
   ```
   This writes `results.jsonl` (one line per request, in request order, with `ok`, `content` and
   any `error`), `retry.jsonl` (the original requests that did not succeed) and `summary.json`
   (counts, error codes, real tokens and cost at batch and live rates). Report succeeded and failed
   counts exactly. Read the error codes before retrying: a 4xx row fails again until it is fixed,
   while `batch_expired`, `batch_cancelled` and 5xx rows can be resubmitted as they are. For
   `empty_content` rows, retry with `--bump-max-tokens 2` or `reasoning_effort: "none"`.
   Retry with a new state folder: `submit runs/<job>/retry.jsonl --state-dir runs/<job>-retry`.

7. **Validate the answers themselves.** A completed row is not a correct row. Parse JSON answers,
   check them against what the user needs (schema, allowed values, lengths, uniqueness), and keep
   the failures for a retry round instead of silently dropping them.

8. **Clean up** when the user has the results: `cleanup --state-dir runs/<job-name>` deletes the
   input and result files from Reka, which otherwise keeps them for up to 31 days.

## Writing requests that are cheap and reliable

- **Put shared context first and keep it byte-identical.** Instructions, schemas, glossaries, style
  guides and reference documents go in the first message, exactly the same in every row; the item
  goes last. Repeated prefixes bill at the cache-read rate, 10x cheaper than input on
  `glm5.3-flash`, in batches as well as live. Caching starts at 1,024 prompt tokens and rounds down
  to 640-token blocks, so a short prefix earns nothing: move enough shared text up front to clear
  the minimum. `estimate` reports the shared prefix it found and says when it is too small.
- **Keep answers short.** Output tokens cost more than input, and reasoning tokens bill as output.
  Ask for JSON with fixed keys, or for edits rather than whole rewritten files.
- **Control thinking.** Both models think before answering. For labels and short JSON set
  `"reasoning_effort": "none"`; otherwise give `max_tokens` room (1,024 or more), or the answer can
  come back empty after the thinking uses the budget.
- **Make rows independent but diverse.** Rows cannot see each other, so generated items repeat
  unless each row gets its own brief (a different seed, theme or slice) and its own id prefix.
  De-duplicate afterwards.
- **Use meaningful `custom_id`s** (`ticket-4812`, `src/app.py`, `obstacle:007`). Results come back
  in any order and are matched by this id. Up to 512 characters, unique per file.
- **Split big jobs**: at most 50,000 rows and 100 MB per file. Give each file its own state folder.

## Safety and data

- Never print, log or write the API key, and never put it in a command line. The script reads
  `REKA_API_KEY` from the environment and refuses to send it to any host other than `*.reka.ai`
  (or a loopback address for testing).
- Batch is not zero data retention: Reka holds the requests until the batch finishes, and the input
  and result files stay for up to 31 days unless deleted. Tell the user before sending personal or
  confidential data, and offer `cleanup` afterwards.
- Submitting spends the user's money. Show the estimate and get confirmation first; cancel with
  `cancel --state-dir ...` (rows already finished are still billed and kept).

## References

- `references/recipes.md`: worked patterns (CSV labelling, many questions over one long document,
  content generation with local validation, localization with a glossary, per-file code sweeps)
  and the anti-patterns that waste money.
- `references/api-notes.md`: limits, statuses, result row shapes, errors, billing and retention.
