## Description:

Searches and discovers OpenClaw skills from ClawHub, Skills CLI, and related skill directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenni666](https://clawhub.ai/user/chenni666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to find relevant OpenClaw skills, compare candidate options, and guide installation choices when a user needs additional agent capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends unpinned command-line package execution with `npx`, which can run changing third-party code.

Mitigation: Use pinned and trusted CLI versions, review commands before execution, and test in an isolated environment before use.

Risk: The skill includes silent global installation guidance with `-g -y`, which may install software broadly without interactive review.

Mitigation: Remove `-y`, avoid global installs unless required, and inspect the target skill before installing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenni666/skills/skill-find)
- [ClawHub](https://clawhub.ai)
- [OpenClaw Directory](https://www.openclawdirectory.dev/skills)
- [LobeHub Skills](https://lobehub.com/skills)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with inline shell commands and reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested search or installation commands; commands should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
