## Description:

Token Guard helps agents reduce LLM API 429 errors by estimating token usage, tracking local quotas, throttling requests, detecting duplicate calls, caching responses, and suggesting fallback models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Token Guard as a local quota helper before LLM API calls to estimate token demand, track per-model limits, throttle high-volume requests, and avoid repeated or runaway calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may write a local state.json file containing model usage counters.

Mitigation: Review where the state file is stored and include it in normal local data handling, backup, and cleanup practices.

Risk: The skill is a local quota helper and does not automatically enforce provider-side API limits unless it is integrated before calls.

Mitigation: Invoke Token Guard deliberately before API requests and keep provider retry and rate-limit handling in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edmonddantesj/skills/token-guard)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Token Guard Python script](artifact/scripts/token_guard.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and YAML examples; the CLI emits JSON decision objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local state counters and has no external Python dependencies.]

## Skill Version(s):

1.5.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
