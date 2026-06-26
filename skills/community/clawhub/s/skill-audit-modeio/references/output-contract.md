# skill-audit Output Contract

## Evaluate / Scan JSON

The deterministic audit JSON keeps the existing v2 report structure:

- `version`
- `tool`
- `target_repo`
- `run`
- `precheck`
- `context_profile`
- `integrity`
- `layers`
- `summary`
- `scoring`
- `required_highlight_evidence_ids`
- `highlights`
- `findings`

In this split release:

- `tool` is `skill-audit`
- `version` remains `skill-safety-assessment-v2`
- evidence ID generation, rule IDs, and benchmark manifest shape remain unchanged

## Prompt payload

`prompt` emits:

- `SCRIPT_SCAN_HIGHLIGHTS`
- `SCRIPT_SCAN_JSON`

When `--include-full-findings` is used, `SCRIPT_SCAN_JSON` also includes full deterministic findings so downstream evidence refs can be validated.

## Validate JSON

`validate --json` returns a machine-readable validation report and exits non-zero on contract failure.

## Adjudication JSON

`adjudicate --json` returns the merged deterministic result after applying context-aware adjudication decisions.
