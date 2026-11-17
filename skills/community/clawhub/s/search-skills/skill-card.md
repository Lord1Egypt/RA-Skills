## Description:

Helps agents discover and install relevant agent skills when users ask for specialized capabilities or reusable workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to search for installable skills, present suitable options, and install a selected skill when the user confirms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage broad, unpinned package execution and global installs that change the user's agent environment.

Mitigation: Verify the CLI package and selected skill source, prefer pinned versions or reviewed local installs, avoid global persistent installs unless intended, and confirm each installation explicitly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openlang-cn/skills/search-skills)
- [Skills Directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party skill links and install commands; commands should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
