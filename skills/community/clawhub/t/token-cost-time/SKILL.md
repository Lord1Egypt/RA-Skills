---
name: token-cost-time
version: 0.1.3
description: "Estimate LLM task token usage, cost, and duration using rule-based classification and optional local profile data without external dependencies."
homepage: https://github.com/highnoonoffice/hno-skills
source: https://github.com/highnoonoffice/hno-skills/tree/main/token-cost-time
license: MIT-0
---

# token-cost-time

`token-cost-time` is a lightweight, dependency-free estimator for LLM task token usage, cost, and duration.

It uses rule-based task classification plus baseline priors and optional local profile data.

## Features

- Rule-based task classification (no LLM calls)
- Cost + duration estimation by model
- Confidence ramp from cold-start to learned profile data
- Quality confidence adjusted by retry behavior
- Local execution recording for continuous calibration

## Install / Run

From this module directory:

```text
npm test
node cli/index.js calibrate --objective "summarize this document" --model claude-haiku-3
node cli/index.js compare --objective "implement a React component" --models claude-haiku-3,claude-sonnet-4,gpt-4o
node cli/index.js record --model claude-haiku-3 --task-class summarization --input-tokens 1340 --output-tokens 290 --duration-ms 4100 --cost 0.00071
```

## API

- `calibrate(objective, model, profilePath = null)`
- `record(executionData, profilePath = null)`
- `compare(objective, models, profilePath = null, sortBy = 'cost')`

Library usage example:

```text
import { calibrate } from './src/calibrate.js';
const result = calibrate('summarize this architecture memo', 'claude-haiku-3');
// result.taskClass => 'summarization'
// result.estimate.costUsd => estimated dollar cost
// result.confidence => 0.2 cold start, rises to 0.95 with 50+ recorded runs
```

If `profilePath` is omitted, profile defaults to:

- `~/.token-cost-time/profile.json`

Execution log defaults to:

- `~/.token-cost-time/execution-log.jsonl`

## Task Classes

- `summarization`
- `code_generation`
- `code_audit`
- `reasoning`
- `creative`
- `extraction`
- `conversation` (fallback)

## Notes

- ESM modules throughout.
- Node built-ins only.
- File paths are resolved with `os.homedir()` for cross-platform compatibility.

### License

MIT-0. Copyright (c) 2026 @highnoonoffice. No attribution required.

---

Built by Joseph Voelbel / High Noon Office. Questions or want to build on this? josephvoelbel.com/contact
