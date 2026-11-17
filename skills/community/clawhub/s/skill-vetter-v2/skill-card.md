## Description:

Verification-guided review workflow for inspecting skill packages before use or publication that classifies risk, flags claims that exceed evidence, and does not itself perform cryptographic verification, emit receipts, or prove a skill is safe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nutstrut](https://clawhub.ai/user/nutstrut)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and agent operators use this skill to review Claude/OpenClaw skill packages before installation or publication, producing a local risk classification and recommendations while preserving the final trust decision for the reviewer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local scan helper can print credential-like lines from the user-selected target, which may include sensitive values.

Mitigation: Run it only on intended skill folders and keep raw scan output out of public logs or external services.

Risk: The optional OpenClaw hook adds a persistent bootstrap reminder when enabled.

Mitigation: Enable the hook only when that reminder is desired and review the hook files before installation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nutstrut/skills/skill-vetter-v2)
- [README](README.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Examples](references/examples.md)
- [Review Checklist](assets/REVIEW-CHECKLIST.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON report templates and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local review findings, warnings, recommendations, and optional verification status metadata.]

## Skill Version(s):

0.0.6 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
