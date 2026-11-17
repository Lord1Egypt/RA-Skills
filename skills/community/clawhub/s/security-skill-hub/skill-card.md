## Description:

安全技能插座 is a security skill hub that helps agents choose, combine, install, and update security-related skills for collection, vulnerability scanning, threat intelligence, malware analysis, defense, and audit workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caidongyun](https://clawhub.ai/user/caidongyun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security practitioners use this skill to route agent work to appropriate security skills, combine results across skills, and extend the local security-skill registry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to install or update persistent skills from ClawHub.

Mitigation: Install or update only trusted publishers and pinned versions after reviewing the target skill.

Risk: Bulk updates can change multiple agent skills without enough per-skill review.

Mitigation: Avoid bulk updates unless each changed skill is reviewed before use.

Risk: Downstream security scans or monitoring workflows may touch sensitive systems.

Mitigation: Confirm scope, authorization, and data sensitivity before running delegated security workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caidongyun/skills/security-skill-hub)
- [Publisher profile](https://clawhub.ai/user/caidongyun)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and skill-selection examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose installation, update, or registration of persistent agent skills; review selected publishers and versions before use.]

## Skill Version(s):

2.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
