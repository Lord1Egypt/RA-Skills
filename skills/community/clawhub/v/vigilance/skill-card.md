## Description:

Evaluate-before-Execute guardrail for OpenClaw agents that issues GO / NO-GO decisions before high-stakes tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanjeet-toosi](https://clawhub.ai/user/sanjeet-toosi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to evaluate planned web searches, shell commands, bookings, payments, and other high-stakes actions before execution. It returns ALLOW, ADVISE, or BLOCK decisions with a severity, reason, and suggested alternative.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad pre-execution gatekeeping can block or pause web search, shell command, booking, and payment workflows beyond the user's intended scope.

Mitigation: Install only where this level of gatekeeping is desired, review the configured trigger set, and require human confirmation for ADVISE decisions.

Risk: Exact action data may include sensitive prompts, commands, URLs, payment context, or travel details.

Mitigation: Avoid sending secrets or payment details through the evaluator and configure provider keys and endpoints deliberately before use.

Risk: Dependency and provider behavior can change over time.

Mitigation: Pin Python dependencies and prefer a validated local endpoint when using a local judge provider.

Risk: Diagnostic stderr output may expose sensitive evaluation details in logs.

Mitigation: Disable or restrict raw stderr logging in environments that handle sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanjeet-toosi/skills/vigilance)
- [Publisher profile](https://clawhub.ai/user/sanjeet-toosi)
- [Sentinel configuration reference](artifact/SENTINEL_CONFIG.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands, Configuration]

**Output Format:** [Structured JSON decision object with human-facing reason and alternatives fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented response includes decision, severity, reason, and alternatives.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
