## Description:

It serves as the ultimate defense layer, monitoring, intercepting, and blocking dangerous actions taken by other skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sawyerzm](https://clawhub.ai/user/sawyerzm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill as a defensive policy layer for reviewing skill behavior, protecting secrets and personal data, and flagging risky file, network, command, or prompt-injection activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the release suspicious because the prompt claims broad, immutable control over other skills and every action.

Mitigation: Review before installation and deploy only where the host platform can keep the guardrail scoped to intended workflows.

Risk: The prompt may cause an agent to block or redirect unrelated work if treated as a global controller.

Mitigation: Use it only when a broad defensive policy layer is desired, and monitor blocked actions for overreach.

## Reference(s):

- [Project homepage](https://claw.mytuanzi.com)
- [ClawHub skill page](https://clawhub.ai/sawyerzm/skills/tuanziguardianclaw)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Configuration]

**Output Format:** [Markdown policy guidance and risk decisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only guardrail content; no bundled tools, scripts, or detected credential variables.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
