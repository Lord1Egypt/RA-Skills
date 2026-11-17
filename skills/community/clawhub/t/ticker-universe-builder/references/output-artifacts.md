# Standard output and delivery

`build` and `maintain` write an artifact bundle to the explicit `--output DIR`. The CLI has no
implicit output directory. When the user supplies no destination, the agent should use
`ticker-universes/<market>/<profile>/<as_of>/` inside the user's working project and pass its
absolute path. Keep user results outside the installed skill. Use a new empty directory for
each revision: the writer refuses to overwrite existing artifacts.

## Artifact bundle

The stem is `{market}-{profile}-{as_of}`; profiles are `light`, `medium`, `heavy`, `max`.

| File | Purpose |
|---|---|
| `{stem}.json` | Authoritative universe: members, roles, admissions, coverage plan, reference instruments, dated sources, measurements, rejection audit, limits, policy/content/version hashes and review history. Keep it for maintain/diff/evaluate. Max also retains its Heavy base. |
| `{stem}.validation.json` | Build verdict: `passed`, `qualified`, errors, warnings, entity/reference/export counts and coverage/expansion checks. |
| `{stem}.txt` | TradingView import: venue-prefixed tickers and `###` display groups, including references; at most 1,000 tokens including headings. |
| `{stem}.en.md` | Human report: structure, grouped members with brief reasons, material limits, coverage and Max additions/distribution when applicable. |
| `{stem}.<market-language>.md` | Companion report for non-English markets. CN uses `zh-Hans`. `--language` changes the companion; English remains. Fixed vocabulary comes from locales; human content uses authored snapshot `report_translations`. |
| `{stem}.en.html` / `{stem}.<market-language>.html` | Complete dark, responsive browser report in the same languages: every member with name, role and brief reason; separate reference cards, Max additions, visible warnings/partial status, folded research notes and relative artifact links. Inline CSS, no server or external assets needed. |

US/Crypto normally produce **five files**; CN produces **seven**. They are all script-generated.
HTML uses a CSS column waterfall: two independent columns on desktop, one on mobile, with
each theme card kept intact. Read down the left column, then the right. Rendering runs locally
without model calls; names, descriptions and translations come from existing researched inputs.
Member tables show ticker, name, role and one brief reason. Full reasoning, admissions, source
URLs, dated market-cap evidence and per-ticker measurement diagnostics stay in JSON, linked once
from the report. `reason_summary` supplies the short reason; older inputs use a first-sentence
excerpt capped at 160 characters. Partial delivery and material validation warnings remain visible.
Maintenance writes the same bundle, with review operations, turnover and deferred decisions in
its report/history. `snapshot.json`, `build-spec.json`, raw provider receipts and price CSVs are
research inputs, not extra final watchlists.

Example CN delivery:

```text
ticker-universes/cn/medium/2026-10-07/
  cn-medium-2026-10-07.json
  cn-medium-2026-10-07.validation.json
  cn-medium-2026-10-07.txt
  cn-medium-2026-10-07.zh-Hans.md
  cn-medium-2026-10-07.en.md
  cn-medium-2026-10-07.zh-Hans.html
  cn-medium-2026-10-07.en.html
```

Link the HTML report, Markdown and importable TXT in the user's reply, and include the JSON record
and validation paths. State the entity count separately from references, the effective data
cutoff, warnings and delivery status. An `as_of` filename is not a claim that every fact was
refreshed that day; per-source and measurement dates remain authoritative.

## Receipt and checkpoint

The CLI prints a **JSON receipt to stdout**, including `status`, `filled`, `unused_capacity`,
artifact paths, warnings, checkpoint and continuation command. It is not an additional file in
the final bundle; callers may redirect it to a receipt file.
`artifacts.reports` remains the language-keyed Markdown map; `artifacts.html_reports` is the
matching HTML map. Both participate in artifact hashes and same-input resume checks. Keep the
bundle together so HTML's relative links resolve. Open the HTML locally in a browser; GitHub
file views show its source rather than hosting the rendered page.

`build` also stores a resumable checkpoint next to the output, in `DIR.run/`, unless `--run-dir`
is supplied:

```text
DIR.run/
  run.json
  attempt-001/
    inputs.json
    result.json
  attempt-002/
    inputs.json
    result.json
    artifacts/     # new destination for a resumed attempt without --output
```

`inputs.json` archives the effective spec, snapshot, policy, seed and language. `result.json`
stores the receipt, validation outcome and repair diagnostics on a blocked/partial attempt.
Attempts are retained. Unchanged inputs do not consume another retry. Resume after repairing
facts or the researched bench:

```bash
python scripts/universe.py build --resume DIR.run --snapshot repaired.json
```

Read returned paths instead of assuming a resumed bundle lives in the first output directory.
Keep the original rendered directories in place: checkpoints and receipts refer to them.
Deliver through links or copies; do not move artifacts to a prettier directory. Revisions use
new empty directories. New receipts include `artifact_sha256` keyed by actual file path. A
same-input resume checks those files; missing/changed files return `needs_research` without
adding an attempt. Restore exact originals or resume with `--output NEW_EMPTY_DIR` to regenerate
from the saved inputs; this is delivery repair, not new research.
See [recovery.md](recovery.md) for the agent repair workflow.

## Delivery status

| Status | Exit | Meaning |
|---|---:|---|
| `complete` | 0 | Current coverage contract qualified; unused ceiling capacity is allowed. Max adds at least 30%, all new members Beta. |
| `partial` | 3 | Explicit Max count-only shortfall within 5% of required entities, positive growth and every other check passed. `passed: true`, `qualified: false`; all filenames carry `-partial` before the extension/language. Disclose the gap and continuation. |
| `needs_research` | 2 | No new qualified bundle; retain the checkpoint and diagnostics, research/repair and resume. |

Legacy replay can also return an under-target partial; it does not certify current economic
coverage. Validation checks the evidence contract, not the independent truth of research
judgements or whether every market leader was discovered.
