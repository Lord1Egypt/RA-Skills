## Description:

Verifies that Sentinel's PII/secret redaction guardrail survives routing through CUSTOM_PROVIDERS to a self-hosted OpenAI-compatible backend by restarting the local gateway, sending a synthetic PII probe, and inspecting the backend's raw response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mark-stadtmueller](https://clawhub.ai/user/mark-stadtmueller)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to verify that a Sentinel gateway redacts synthetic PII before traffic reaches a custom self-hosted OpenAI-compatible model backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stops and restarts the local Sentinel gateway, which can interrupt local gateway traffic or reuse stale local configuration if the environment is not prepared.

Mitigation: Run it in a controlled local environment, confirm Docker and Sentinel are ready, and verify the intended CUSTOM_PROVIDER_* variables before execution.

Risk: The check contacts the configured custom backend and inspects raw backend output, which could expose sensitive content if used with real data.

Mitigation: Use only the built-in synthetic probe values and avoid running the check against sessions or backends that may return real sensitive data.

Risk: Optional Telegram delivery can forward backend response details outside the local environment.

Mitigation: Leave Telegram disabled when possible, or change notifications to include only minimal pass/fail status.

Risk: Dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Pin and review dependency versions before repeatable or production-adjacent use.

## Reference(s):

- [Sentinel Getting Started](https://docs.superwise.ai/docs/getting-started)
- [Superwise Sentinel MCP Server](https://docs.superwise.ai/mcp)
- [ClawHub Skill Page](https://clawhub.ai/mark-stadtmueller/skills/sentinel-custom-provider-check)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Analysis]

**Output Format:** [Markdown guidance with shell commands and a JSON-compatible pass/fail result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also print a pass/fail summary to stdout and optionally send a minimal Telegram notification.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill.py metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
