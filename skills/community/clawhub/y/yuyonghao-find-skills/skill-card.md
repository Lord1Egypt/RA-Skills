## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to identify relevant installable agent skills, present options, and optionally install selected skills through the Skills CLI. It also helps decide when no existing skill is available and whether to proceed directly or create a new skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run mutable external CLI code and install third-party skills globally while skipping confirmation.

Mitigation: Install only from reviewed sources, avoid -y and global installation unless needed, pin or verify the CLI and skill source where possible, and review each candidate skill before adding it.

## Reference(s):

- [ClawHub Find Skills release page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-find-skills)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and skill links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party skill links and package install commands.]

## Skill Version(s):

0.1.0 (source: server release metadata, artifact _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
