## Description:

OpenClaw Cognitive Operating & Skill Governance Kernel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxime-xian](https://clawhub.ai/user/maxime-xian)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use this skill to govern higher-complexity work, manage cognitive load, coordinate skill usage, and require closure artifacts for governance-heavy tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask agents to persist task records or memory archives without clear approval.

Mitigation: Require explicit user approval before writing archives, memories, decision records, or other persistent files.

Risk: The skill may ask agents to sync summaries about financial, strategic, or major decisions to external notes or mobile channels.

Mitigation: Review summaries for sensitive information and require explicit approval before any external sync or sharing.

Risk: The skill may ask agents to manage skill lifecycle actions such as archiving or deletion candidates automatically.

Mitigation: Treat lifecycle actions as recommendations that require human review before changing installed skills.

Risk: Archived decisions and next actions could be reused as instructions by future agents.

Mitigation: Treat archived records as historical context for review, not as executable instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maxime-xian/skills/skill-governance)
- [Manifest Homepage](https://clawhub.com/skills/skill-governance)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or structured text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for task records, structured notes, decision records, and confidence statements as closure artifacts.]

## Skill Version(s):

2.1.0 (source: manifest.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
