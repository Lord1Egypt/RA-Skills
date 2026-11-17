# Templates

Adapt these templates to the destination's established format. Do not force a
new schema into an existing document.

Use an ISO 8601 UTC timestamp and a collision-resistant identifier such as
`ERR-20260820T221239Z-a3f1`.

## Chronological learning

```markdown
### Learning: concise title
- Captured: 2026-08-20T22:12:39Z
- Source: task, issue, or document reference
- Classification: chronological
- Evidence: concise factual observation
- Candidate lesson: prevention-oriented statement
- Occurrences: 1
- Confidence: low | medium | high
- Privacy review: clear | redacted | restricted
- Status: pending-review | retained | rejected | promoted
- Promoted to: path or N/A
```

## Incident or failure

```markdown
### ERR-20260820T221239Z-a3f1: concise title
- Captured: 2026-08-20T22:12:39Z
- Owner: person or team
- Source: task, issue, or document reference
- Context: operation that failed
- Evidence: reproducible facts, without secrets or noisy output
- Reproduction: known | unknown
- Occurrences: 1
- Impact: low | medium | high
- Confidence: low | medium | high
- Resolution: pending or concise fix
- Prevention: candidate reusable rule
- Privacy review: clear | redacted | restricted
- Status: open | resolved | needs-review | superseded
- Supersedes: identifier or N/A
- Superseded by: identifier or N/A
```

## Feature request

```markdown
### FEAT-20260820T221239Z-b7c2: concise title
- Captured: 2026-08-20T22:12:39Z
- Requested by: user | operator | agent
- Owner: person or team
- Source: task, issue, or document reference
- Problem: capability gap, not a proposed implementation
- Evidence: affected workflow or repeated demand
- Occurrences: 1
- Scope: small | medium | large
- Priority: low | medium | high
- Confidence: low | medium | high
- Privacy review: clear | redacted | restricted
- Status: proposed | accepted | rejected | delivered | superseded
- Supersedes: identifier or N/A
- Superseded by: identifier or N/A
```

## Durable rule or decision

```markdown
### Concise rule title
- Approved: 2026-08-20
- Owner: person or team
- Authority: guidance | decision | policy
- Source evidence: identifiers or links
- Confidence: high
- Supersedes: identifier or N/A

**Rule:** When [condition], always [preventive action].

**Rationale:** One concise sentence.

**Review condition:** Event or date that should trigger reconsideration.
```
