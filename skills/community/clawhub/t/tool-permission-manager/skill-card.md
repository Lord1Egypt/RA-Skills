## Description:

Manages per-tool permission levels so an agent can distinguish public, warning, approval, and forbidden tool use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soroyue](https://clawhub.ai/user/soroyue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace administrators use this skill to describe per-tool permission tiers and guide how an agent should handle reads, searches, command execution, file writes, messaging, scheduled tasks, session controls, gateway configuration, and deletion actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad natural-language permission changes could loosen permissions for sensitive tools without adequate safeguards.

Mitigation: Define a narrow command format, require explicit confirmation, maintain allowed tool lists and role checks, log permission changes, and provide rollback behavior before trusting the skill to manage command execution, file writes, messaging, cron jobs, or session controls.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, configuration]

**Output Format:** [Markdown with inline JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes tiered permission handling and a sample permission map.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
