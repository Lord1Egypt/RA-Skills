## Description:

Execute tasks with reliability-first behavior under flaky conditions. Use when commands fail due to transient errors (network, timeouts, rate limits, temporary locks), when deciding whether to retry vs escalate, or when the user asks for risk-based judgment (engineer around low risk issues, notify on medium/high risk).

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinguy](https://clawhub.ai/user/pinguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to keep work moving through transient command, network, package, git, or rate-limit failures while pausing for destructive, security-sensitive, or otherwise high-risk actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic retries can increase runtime or repeat low-risk work longer than expected.

Mitigation: Use the documented attempt budget, exponential backoff, explicit per-attempt timeouts, and status updates when operations exceed expected duration.

Risk: Retrying commands with side effects can duplicate work or messages.

Mitigation: Classify those cases as medium risk, send a brief risk note, state a mitigation and rollback path, and proceed only when aligned with user preference.

Risk: Retry logic could otherwise mask destructive, security-sensitive, or irreversible actions.

Mitigation: Pause and ask for explicit confirmation for high-risk actions, and treat unclear blast radius as at least medium risk.

## Reference(s):

- [Server-resolved GitHub provenance: pinguy/Skills risk-aware-retry](https://github.com/pinguy/Skills/tree/main/skills/risk-aware-retry)
- [ClawHub skill page](https://clawhub.ai/pinguy/skills/risk-aware-retry)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown status updates with inline command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DONE or BLOCKED summaries with evidence, blockers, next steps, and notable retry recoveries.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
