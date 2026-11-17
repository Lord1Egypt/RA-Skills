## Description:

SkillForge watches how an agent user works, discovers repeated workflow patterns, and drafts reusable Skills for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jfranklee](https://clawhub.ai/user/jfranklee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent users use this skill to identify repeated work patterns, draft new Skills, and review existing Skill health before adopting changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may analyze broad work logs, long-term memory, current conversation history, and installed Skills that contain secrets, client data, internal procedures, or personal information.

Mitigation: Review configured sources before use, limit the date range and data sources where possible, and disable auto-scan or realtime detection until appropriate scope is confirmed.

Risk: Generated pattern reports, archives, or Skill health records may retain sensitive workflow summaries.

Mitigation: Periodically delete generated pattern archives, reports, and health records that should not be retained.

Risk: Drafted or merged Skills could introduce incorrect or misleading guidance if adopted without review.

Mitigation: Require explicit human review before installing generated Skills or modifying existing Skills.

## Reference(s):

- [SkillForge ClawHub Skill Page](https://clawhub.ai/jfranklee/skills/skillforge-meta)
- [jfranklee ClawHub Publisher Profile](https://clawhub.ai/user/jfranklee)
- [ALGORITHM.md](references/ALGORITHM.md)
- [CONFIG_FULL.md](references/CONFIG_FULL.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown reports, Skill drafts, configuration guidance, and proposed file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed by the user before installation or modification of active Skills.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
