# Contributing to WorldLoops

WorldLoops is a safe-by-default execution governance layer for AI agents. Contributions are focused on making the adapter SDK easier to use, better documented, and more widely compatible.

The most impactful contribution you can make right now is submitting a community adapter fixture.

---

## Community Adapter Submissions

WorldLoops does not own every connector. If your tool, agent, or internal system can read a signal, it can join the WorldLoops runtime.

A community adapter submission is a validated `AdapterSignal` fixture that demonstrates how your source maps into the WorldLoops input contract. No code is required. No connector is added. No external writes occur.

Community adapters are examples and validation fixtures only.

---

## What to Submit

A community adapter submission consists of:

1. **One or more fixture files** in `examples/adapters/community/`
2. **Validation confirmation** — each fixture must pass `npm run adapter:validate`
3. **A pull request** using the adapter submission PR template

---

## Adapter Submission Checklist

Before opening a PR, confirm all of the following:

- [ ] Fixture file is in `examples/adapters/community/`
- [ ] Filename follows the naming convention: `<source>-<sourceType>.example.json`
- [ ] `source` is a non-empty string identifying your connector (e.g. `linear`, `notion`, `jira`, `pagerduty`)
- [ ] `sourceType` is a non-empty string identifying the signal type (e.g. `issue`, `task`, `alert`, `page`)
- [ ] `externalWrite` is `false`
- [ ] `text` is a non-empty string containing the signal content
- [ ] `observedAt` is a valid ISO 8601 timestamp (e.g. `2026-05-20T09:00:00.000Z`)
- [ ] Optional fields (`url`, `summary`, `metadata`) are included if available and meaningful
- [ ] `metadata.adapterStatus` is set to `"community"` if using the metadata field
- [ ] `npm run adapter:validate -- examples/adapters/community/<your-file>.example.json` exits with `ok: true`
- [ ] `npm run test:adapter-community` passes
- [ ] No real credentials, tokens, or personal data in the fixture

---

## Fixture Naming Convention

Community adapter fixtures follow this naming pattern:

```
examples/adapters/community/<source>-<sourceType>.example.json
```

Examples:

| Fixture file | source | sourceType |
|---|---|---|
| `linear-issue.example.json` | `linear` | `issue` |
| `notion-task.example.json` | `notion` | `task` |
| `jira-ticket.example.json` | `jira` | `ticket` |
| `pagerduty-alert.example.json` | `pagerduty` | `alert` |
| `github-issue.example.json` | `github` | `issue` |

Rules:
- Use lowercase, hyphen-separated names
- Use the `.example.json` suffix for community fixtures
- One fixture file per source+sourceType combination

---

## Adapter Status Labels

WorldLoops uses three adapter status labels:

| Label | Meaning |
|---|---|
| `core` | Shipped with WorldLoops. Maintained by the WorldLoops team. |
| `community` | Submitted by an external developer. Maintained by the submitter. |
| `experimental` | Submitted for preview or feedback. Not yet validated for production use. |

Community adapter fixtures should include `"adapterStatus": "community"` in their `metadata` field:

```json
{
  "metadata": {
    "adapterStatus": "community"
  }
}
```

---

## Step-by-Step: How to Submit

1. **Fork** this repository
2. **Create your fixture** in `examples/adapters/community/`
3. **Validate it locally**:
   ```bash
   npm run build
   npm run adapter:validate -- examples/adapters/community/your-source-type.example.json
   ```
4. **Run the community test suite**:
   ```bash
   npm run test:adapter-community
   ```
5. **Open a pull request** using the adapter submission PR template (`.github/PULL_REQUEST_TEMPLATE/adapter_submission.md`)

---

## Minimal Fixture Template

Copy and modify this template:

```json
{
  "source": "your-source",
  "sourceType": "your-type",
  "externalWrite": false,
  "text": "A description of the signal that WorldLoops will normalize into an open loop.",
  "observedAt": "2026-05-20T09:00:00.000Z",
  "url": "https://your-tool.example.com/your-item",
  "summary": "One-line human-readable summary of the signal",
  "metadata": {
    "adapterStatus": "community"
  }
}
```

See [ADAPTER_GUIDE.md](./ADAPTER_GUIDE.md) for the full field reference, payload mapping examples, and the complete validated flow.

---

## What Not to Submit

- Real connectors or integration code
- External writes of any kind
- Signals with `externalWrite: true`
- Signals with missing required fields
- Real credentials, tokens, user IDs, or personal data

If a fixture fails `adapter:validate`, the PR will not be merged.

---

## The Core Message

If your tool can read a signal, it can join the WorldLoops runtime.

`externalWrite: false` is preserved in every fixture, every test, and every pipeline run.

---

## Questions

Open an issue if you have questions about the adapter contract, fixture format, or submission process.
