## Description:

Add 8 security governance layers to your OpenClaw agent: budget controls, permissions, audit logging, kill switch, identity signing, skill vetting, process isolation, and gateway protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onezeroeight-ai](https://clawhub.ai/user/onezeroeight-ai)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to install and configure Sammā Suit governance controls for permissions, budgets, audit logging, identity signing, skill vetting, process limits, and kill-switch behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad control over agent behavior and complete audit logging may affect privacy, availability, and operational control if installed without clear boundaries.

Mitigation: Use a dedicated least-privilege SAMMA_API_KEY, confirm log storage, access, redaction, and retention settings, and keep an uninstall or rollback path for lifecycle hooks and skill-blocking controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onezeroeight-ai/skills/samma-suit)
- [ClawHub publisher profile](https://clawhub.ai/user/onezeroeight-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SAMMA_API_KEY for installation or configuration workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
