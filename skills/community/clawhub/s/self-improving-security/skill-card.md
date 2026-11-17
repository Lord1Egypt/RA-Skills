## Description:

Helps agents record and review security findings, incidents, compliance gaps, and recurring remediation patterns in local Markdown logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use this skill to capture redacted vulnerability, access-control, incident-response, and compliance findings in workspace-local logs, then review recurring patterns for possible promotion into security guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent security logs could expose sensitive incident details or secrets.

Mitigation: Redact credentials and personal data before logging; keep learning files private unless reviewed and sanitized.

Risk: Optional hooks or automated detection could operate outside the intended workspace or encounter sensitive tool output.

Mitigation: Use project-scoped hooks only and avoid the optional PostToolUse detector in sensitive environments.

Risk: Promoted findings or generated skills could change agent behavior without sufficient review.

Mitigation: Require explicit approval of a reviewed diff before changing agent instructions, hooks, rules, or generated skills.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jose-compu/skills/self-improving-security)
- [Security logging examples](references/examples.md)
- [Hook setup](references/hooks-setup.md)
- [OpenClaw integration](references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown entries and instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workspace-local security logs; optional project-scoped reminder hooks and reviewed promotion of recurring findings.]

## Skill Version(s):

1.2.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
