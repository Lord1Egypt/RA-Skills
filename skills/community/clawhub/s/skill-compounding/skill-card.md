## Description:

Helps an agent identify reusable solutions, extract them into skill documentation, register them in a skill index, and iterate them over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipoon](https://clawhub.ai/user/sipoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team agents use this skill after solving a non-trivial or repeated problem to decide whether the workflow should become a reusable skill. It guides them through documenting the skill, registering it in local skill indexes, and improving it from future use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to create or rewrite persistent skill instructions too broadly or without explicit approval.

Mitigation: Require explicit approval before creating or modifying skill files, avoid automatic SOUL.md updates, and review full diffs before accepting changes.

Risk: Untrusted task content or sensitive project details could be preserved as reusable guidance.

Mitigation: Sanitize source material before adding it to a skill and exclude commercial-sensitive, one-off, personal-preference, or untrusted instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sipoon/skills/skill-compounding)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance, Files]

**Output Format:** [Markdown skill documentation, directory structure guidance, and concise maintenance instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or modify skill files such as SKILL.md, optional examples or templates, and local skill index entries.]

## Skill Version(s):

0.1.0 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
