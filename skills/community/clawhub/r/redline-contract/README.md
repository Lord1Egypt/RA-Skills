# redline

`redline` is a standalone Codex skill for paragraph-by-paragraph contract review and DOCX redlining.

It is built to avoid coarse section-level comments by extracting one review unit per non-empty paragraph, then generating:

- a tracked-changes amended `.docx`
- a `.risk-report.docx`
- a `.review.json` dataset for the review

## Contents

- `SKILL.md`: skill instructions and workflow
- `scripts/contract_review_pipeline.py`: review extraction and materialization tool
- `references/review-json-schema.md`: review JSON field guide
- `agents/openai.yaml`: UI metadata

## Core Behavior

- review contracts paragraph by paragraph
- preserve heading context in each review unit
- draft distinct amendment text for each paragraph
- support opponent Word comment response drafting
- generate tracked changes and risk reports from the review JSON

## Usage

Initialize a review file:

```bash
python scripts/contract_review_pipeline.py init-review \
  --input <contract.docx> \
  --output <contract.review.json> \
  --supported-party "<party>" \
  --focus-area "<area-1>"
```

Materialize the outputs:

```bash
python scripts/contract_review_pipeline.py materialize \
  --input <contract.docx> \
  --review-json <contract.review.json> \
  --amended-output <contract.amended.docx> \
  --report-output <contract.risk-report.docx> \
  --author "Codex Redline Reviewer"
```

## License

MIT. See `LICENSE`.
