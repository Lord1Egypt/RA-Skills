## Description:

Skill Sentinel audits newly installed or unfamiliar OpenClaw skills, flags high-risk behavior, and applies hard-floor safety rules before first use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kimmi2ue](https://clawhub.ai/user/kimmi2ue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Skill Sentinel to review newly installed or unfamiliar OpenClaw skills before first use, especially when a skill may transmit data, access credentials, create scheduled work, or claim broad authority. It produces user-facing audit summaries, red-flag findings, and approval or refusal guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives itself broad non-overridable control over when other skills may run.

Mitigation: Review before installation and prefer use as an explicit audit request or dedicated review hook rather than a standing blocker for unrelated skill workflows.

Risk: The skill is intended to act as an active gatekeeper for other skills, not merely as an audit checklist.

Mitigation: Install only when that gatekeeping behavior is desired, and require user review of quarantine summaries before allowing a newly installed skill to run.

## Reference(s):

- [Skill Sentinel on ClawHub](https://clawhub.ai/kimmi2ue/skills/skill-hardfloor)
- [Skill Audit Checklist](references/audit-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown audit summaries and safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include approval prompts, red-flag locations, and refusal rationale when unsafe behavior is detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
