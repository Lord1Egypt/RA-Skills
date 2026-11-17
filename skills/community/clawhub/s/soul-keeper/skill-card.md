## Description:

Soul Keeper monitors when long-lived workspace files may need maintenance and prompts the agent to propose focused updates based on workspace-file guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfang0126](https://clawhub.ai/user/mfang0126)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Soul Keeper to help an agent notice when persistent workspace-memory or configuration files such as SOUL.md, USER.md, AGENTS.md, MEMORY.md, and WORKING.md may be stale. The skill supports review-driven proposals for one workspace file at a time before applying updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may write a memory record even after the user refuses an update.

Mitigation: Before use, require refusal to mean no write of any kind, including memory records.

Risk: Broad activation triggers may cause the skill to inspect or propose changes unexpectedly.

Mitigation: Narrow activation to explicit workspace-memory or workspace-file maintenance requests.

Risk: Proposed changes to long-lived workspace files can make future agent behavior follow stale or incorrect assumptions.

Mitigation: Review each proposed change against the current workspace state before applying it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mfang0126/skills/soul-keeper)
- [Publisher profile](https://clawhub.ai/user/mfang0126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with proposed workspace-file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for confirmation and is intended to suggest one workspace-file update at a time.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
