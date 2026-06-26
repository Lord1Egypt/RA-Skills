# WorldLoops Adapter Guide

Bring your own connector. WorldLoops provides the contract.

WorldLoops does not own every connector. If your tool, agent, or internal system can read a signal, it can pass that signal into WorldLoops using the **AdapterSignal** public input contract. WorldLoops then turns valid signals into governed open loops and proposals while preserving `externalWrite: false`.

---

## The AdapterSignal Contract

An `AdapterSignal` is a plain JSON object. Five fields are required.

### Required fields

| Field | Type | Description |
|---|---|---|
| `source` | string | Where the signal came from (e.g. `slack`, `gmail`, `github`, `linear`, `notion`) |
| `sourceType` | string | Signal type within the source (e.g. `message`, `thread`, `event`, `pr`, `issue`) |
| `externalWrite` | `false` | Must be `false`. WorldLoops does not accept signals that imply external writes. |
| `text` | string | The signal content WorldLoops will normalize into an open-loop candidate. |
| `observedAt` | string | ISO 8601 timestamp when the signal was observed (e.g. `2026-05-20T10:30:00.000Z`) |

### Optional fields

| Field | Type | Description |
|---|---|---|
| `url` | string | Link to the source item (message, thread, PR, issue, event) |
| `summary` | string | Human-readable one-line summary of the signal |
| `metadata` | object | Source-specific key/value pairs (e.g. PR number, assignee, priority) |

### Minimal valid example

```json
{
  "source": "slack",
  "sourceType": "message",
  "externalWrite": false,
  "text": "Hey, can you review the Q2 metrics dashboard before the planning meeting tomorrow?",
  "observedAt": "2026-05-20T10:30:00.000Z"
}
```

---

## JSON Schema

The AdapterSignal schema lives at:

```
src/schemas/adapterSignal.schema.json
```

It validates:
- All five required fields are present and non-empty
- `externalWrite` is strictly `false` (not `true`, not `null`, not missing)
- `observedAt` is a valid ISO 8601 datetime string
- `metadata`, if present, is a plain object (not an array or primitive)
- No additional properties beyond the documented fields

External tools integrating with WorldLoops can use this schema for pre-validation before calling `adapter:validate`.

---

## Full Validated Flow

The complete workflow from raw signal to proposal inspection:

```bash
# Step 1: Validate your adapter signal
npm run adapter:validate -- examples/adapters/slack-message.json

# Step 2: Pass the signal into the reconciliation pipeline
npm run brief:reconcile -- --adapter-signal examples/adapters/slack-message.json

# Step 3: Inspect detected open loops
npm run loop:list

# Step 4: Inspect persisted proposals
npm run proposal:list

# Step 5: Inspect a single proposal in detail
npm run proposal:show -- <proposalId>
```

---

## Valid Examples

The `examples/adapters/` directory includes five valid signal fixtures:

| File | source | sourceType | Notes |
|---|---|---|---|
| `slack-message.json` | `slack` | `message` | Review request with URL and summary |
| `gmail-thread.json` | `gmail` | `thread` | Follow-up thread with deadline context |
| `calendar-event.json` | `calendar` | `event` | Meeting prep signal |
| `github-pr.json` | `github` | `pr` | PR review request with metadata |
| `generic-signal.json` | `linear` | `issue` | Custom source — bridges to `manual` internally |

To validate all valid examples:

```bash
npm run adapter:validate -- examples/adapters/slack-message.json
npm run adapter:validate -- examples/adapters/gmail-thread.json
npm run adapter:validate -- examples/adapters/calendar-event.json
npm run adapter:validate -- examples/adapters/github-pr.json
npm run adapter:validate -- examples/adapters/generic-signal.json
```

---

## Invalid Examples

Three invalid fixtures demonstrate what the validator rejects:

| File | Error | Why |
|---|---|---|
| `invalid-external-write.json` | `externalWrite must be false` | Signal sets `externalWrite: true` — WorldLoops will not accept signals that imply external writes |
| `invalid-missing-required-field.json` | `observedAt: required` | Missing `observedAt` — all five required fields must be present |
| `invalid-date.json` | `observedAt must be ISO 8601` | `observedAt` is a human-readable date string, not a valid ISO 8601 timestamp |

To verify each invalid example is correctly rejected:

```bash
npm run adapter:validate -- examples/adapters/invalid-external-write.json
# Expected: ok: false — error includes "externalWrite"

npm run adapter:validate -- examples/adapters/invalid-missing-required-field.json
# Expected: ok: false — error includes "observedAt"

npm run adapter:validate -- examples/adapters/invalid-date.json
# Expected: ok: false — error includes "observedAt"
```

Each command will exit with a non-zero code and return structured JSON errors, for example:

```json
{
  "ok": false,
  "errors": [
    "externalWrite: must be false — AdapterSignal does not permit external writes"
  ],
  "safety": { "externalWrite": false }
}
```

---

## Mapping Raw Payloads to AdapterSignal

WorldLoops does not parse raw connector payloads. Your connector is responsible for extracting the relevant fields and shaping them into an `AdapterSignal`.

Here is how common source payloads map:

### Slack

```json
// Raw Slack event (simplified)
{
  "type": "message",
  "channel": "C01ABC",
  "text": "Hey, can you review the Q2 metrics dashboard before tomorrow?",
  "ts": "1716115800.000000"
}

// → AdapterSignal
{
  "source": "slack",
  "sourceType": "message",
  "externalWrite": false,
  "text": "Hey, can you review the Q2 metrics dashboard before tomorrow?",
  "observedAt": "2026-05-19T10:30:00.000Z",
  "url": "https://your-workspace.slack.com/archives/C01ABC/p1716115800000000"
}
```

### Gmail

```json
// Raw Gmail message (simplified)
{
  "id": "msg-abc123",
  "threadId": "thread-xyz",
  "snippet": "Re: Partnership proposal — can you send the updated deck before EOD Friday?",
  "internalDate": "1716105300000"
}

// → AdapterSignal
{
  "source": "gmail",
  "sourceType": "thread",
  "externalWrite": false,
  "text": "Re: Partnership proposal — can you send the updated deck before EOD Friday?",
  "observedAt": "2026-05-19T08:15:00.000Z",
  "url": "https://mail.google.com/mail/u/0/#inbox/thread-xyz"
}
```

### Google Calendar

```json
// Raw Calendar event (simplified)
{
  "summary": "Quarterly planning meeting",
  "start": { "dateTime": "2026-05-22T10:00:00-07:00" },
  "description": "Confirm agenda and circulate notes template."
}

// → AdapterSignal
{
  "source": "calendar",
  "sourceType": "event",
  "externalWrite": false,
  "text": "Quarterly planning meeting on 2026-05-22 at 10:00 AM — confirm agenda and circulate notes template.",
  "observedAt": "2026-05-19T09:00:00.000Z",
  "url": "https://calendar.google.com/calendar/event?eid=..."
}
```

### GitHub

```json
// Raw GitHub pull_request event (simplified)
{
  "action": "review_requested",
  "number": 487,
  "pull_request": {
    "title": "Add rate limiting to /api/v1/signals",
    "html_url": "https://github.com/example-org/signals-api/pull/487"
  }
}

// → AdapterSignal
{
  "source": "github",
  "sourceType": "pr",
  "externalWrite": false,
  "text": "PR #487: Add rate limiting to /api/v1/signals — review requested.",
  "observedAt": "2026-05-19T11:45:00.000Z",
  "url": "https://github.com/example-org/signals-api/pull/487",
  "metadata": { "prNumber": 487, "repo": "example-org/signals-api" }
}
```

### Linear / Custom Sources

`source` is open-ended — any string is accepted. Sources outside the `slack | gmail | calendar | github | manual` set are bridged to `manual` internally. Your signal is still governed and persisted correctly.

```json
{
  "source": "linear",
  "sourceType": "issue",
  "externalWrite": false,
  "text": "Issue WL-291: Adapter SDK validation errors need better user-facing messages — blocking release, no activity for 72 hours.",
  "observedAt": "2026-05-16T14:00:00.000Z",
  "url": "https://linear.app/your-org/issue/WL-291",
  "metadata": { "issueId": "WL-291", "priority": "high", "assignee": "joshlee" }
}
```

---

## Safety: Why externalWrite Must Be False

`externalWrite: false` is a hard requirement in the AdapterSignal contract.

The field exists not as a flag your connector controls, but as a declaration that WorldLoops enforces. It means:

- Your connector did not write to an external system before passing the signal to WorldLoops.
- WorldLoops will not write to an external system when processing the signal.
- No email is sent. No Slack message is posted. No calendar event is created. No GitHub PR is modified.
- All state changes are local (`.worldloops/`).

If `externalWrite` is missing, `true`, or any value other than `false`, the validator rejects the signal before it reaches the pipeline. The reconciliation pipeline is never reached.

```bash
# This will fail with a validation error and exit non-zero
npm run adapter:validate -- examples/adapters/invalid-external-write.json
```

---

## Idempotency

Running the same adapter signal through `brief:reconcile` multiple times will not create duplicate proposals.

WorldLoops generates an `idempotencyKey` for each proposal candidate based on its source, entity type, and current state. Before persisting a new proposal, the pipeline checks whether a proposal with that key already exists in `.worldloops/proposals.json`.

If it already exists, reconciliation reports `proposalsAlreadyTracked` and skips the write.

This means you can safely re-run the same signal as many times as needed without polluting the proposal store.

---

## The Internal Bridge

When WorldLoops accepts a valid `AdapterSignal`, it bridges it into the same internal `Signal` type used by all other sources:

| AdapterSignal field | Internal Signal field |
|---|---|
| `source` | `source` (known sources pass through; unknown sources fall back to `manual`) |
| `text` | `text` |
| `observedAt` | `createdAt` |
| `url` | `url` (optional) |

`sourceType`, `summary`, and `metadata` are not forwarded to the brief API — they remain in the `AdapterSignal` for validation and audit purposes only. No new runtime model is created. `AdapterSignal` is a public input contract that bridges into the existing pipeline, not a parallel implementation.

---

## Known Sources

| source value | Internal mapping |
|---|---|
| `slack` | passes through as `slack` |
| `gmail` | passes through as `gmail` |
| `calendar` | passes through as `calendar` |
| `github` | passes through as `github` |
| `manual` | passes through as `manual` |
| anything else | falls back to `manual` |

---

## Adapter Status Labels

WorldLoops uses three adapter status labels to categorize fixtures and connectors:

| Label | Meaning |
|---|---|
| `core` | Shipped with WorldLoops. Maintained by the WorldLoops team. |
| `community` | Submitted by an external developer. Maintained by the submitter. |
| `experimental` | Submitted for preview or feedback. Not yet validated for production use. |

The label is not a required field in the `AdapterSignal` contract. For community fixtures, include it in the `metadata` field:

```json
{
  "metadata": {
    "adapterStatus": "community"
  }
}
```

The `AdapterStatus` TypeScript type is exported from `src/types/adapterSignal.ts` for tooling use.

---

## Community Adapters

Community adapters are `AdapterSignal` fixtures submitted by external developers. They live in `examples/adapters/community/` and must pass `adapter:validate` before submission.

Community adapters are **examples and validation fixtures only**. They do not add connectors, external writes, or runtime behavior.

### Included community fixtures

| File | source | sourceType | Notes |
|---|---|---|---|
| `community/linear-issue.example.json` | `linear` | `issue` | Blocked issue with priority metadata |
| `community/notion-task.example.json` | `notion` | `task` | Stalled task with due date metadata |

To validate all community examples:

```bash
npm run adapter:validate -- examples/adapters/community/linear-issue.example.json
npm run adapter:validate -- examples/adapters/community/notion-task.example.json
```

### Fixture naming convention

Community fixtures follow this naming pattern:

```
examples/adapters/community/<source>-<sourceType>.example.json
```

Rules:
- Lowercase, hyphen-separated
- `.example.json` suffix
- One file per source+sourceType combination

### Validation test template

Copy this template to add a new community adapter test:

```javascript
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const { validateAdapterSignal } = require('../dist/adapter/validateAdapterSignal');

const fixture = JSON.parse(
  fs.readFileSync(
    path.resolve(__dirname, '../examples/adapters/community/your-source-type.example.json'),
    'utf8'
  )
);

const result = validateAdapterSignal(fixture);
assert.strictEqual(result.ok, true, JSON.stringify(result.errors));
assert.strictEqual(result.signal.externalWrite, false);
assert.strictEqual(result.signal.source, 'your-source');
assert.strictEqual(result.signal.sourceType, 'your-type');

console.log('your-source adapter test passed');
```

The existing `tests/adapterCommunity.test.cjs` automatically discovers and validates every `.example.json` file in `examples/adapters/community/` — no additional test file is required for new community fixtures.

### How to submit a community adapter

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full submission guide and PR checklist.

---

## Adapter Compatibility Report

Before submitting a community adapter, run `adapter:test` to confirm your fixture passes the full local pipeline:

```bash
npm run adapter:test -- examples/adapters/community/your-source-type.example.json
```

Example output for a passing adapter:

```
Adapter compatibility report

file: examples/adapters/community/your-source-type.example.json
validate: passed
reconcile: passed
openLoopPersisted: true
proposalPersisted: true
idempotency: passed
externalWrite: false
```

### Pass/fail criteria

| Check | Pass | Fail |
|---|---|---|
| `validate` | AdapterSignal passes all five required fields and contract rules | Missing required field, `externalWrite: true`, or invalid `observedAt` format |
| `reconcile` | Signal produces an open loop and a proposal locally | No open loop or proposal produced |
| `openLoopPersisted` | Open loop was written to local state | Reconciliation did not produce a loop |
| `proposalPersisted` | Proposal was written to local state | Reconciliation did not produce a proposal |
| `idempotency` | Running the same signal twice creates zero duplicate loops or proposals | Second run creates additional entries for the same key |
| `externalWrite` | Always `false` | Never fails — this is a guarantee, not a check |

If any check fails, the command exits with a non-zero code and shows which check failed and why.

### JSON output

For programmatic use or CI integration:

```bash
npm run adapter:test -- examples/adapters/community/your-source-type.example.json --json
```

Returns:

```json
{
  "ok": true,
  "report": {
    "file": "...",
    "validate": "passed",
    "reconcile": "passed",
    "openLoopPersisted": true,
    "proposalPersisted": true,
    "idempotency": "passed",
    "externalWrite": false
  },
  "safety": { "externalWrite": false }
}
```

`ok: false` is returned when any check fails, allowing CI pipelines to gate on this field.

### Safety

`adapter:test` is local-only. It runs in an isolated temporary directory and never writes to your `.worldloops/` project state. `externalWrite: false` is preserved throughout.

---

## Inspecting Adapter-Generated State

Loops and proposals generated from adapter signals are stored in the same local `.worldloops` state files as all other WorldLoops state. You can inspect them with `state:check` and `receipts:verify`:

```bash
npm run state:check
npm run receipts:verify
```

`state:check` will detect any malformed JSON, duplicate ids, `externalWrite` violations, or broken cross-references in loops and proposals created by adapter-driven reconciliation. This applies equally to single-agent and multi-agent workflows where multiple adapters may be writing to the same world.

---

## Smoke Tests

The test suite verifies adapter validation behavior:

```bash
npm run test:adapter-signal          # core validator and bridge logic
npm run test:adapter-signal-proposal # proposal persistence and idempotency
npm run test:adapter-signal-invalid  # invalid example fixtures are correctly rejected
npm run test:adapter-community       # all community adapter fixtures pass adapter:validate
npm run test:adapter-test            # adapter:test compatibility report checks
```

To run the full suite:

```bash
npm run smoke
```
