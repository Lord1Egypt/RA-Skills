## Description:

Continuous self-improvement through structured reflection and memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lokix94](https://clawhub.ai/user/lokix94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give agents a recurring self-reflection workflow for checking when reflection is due, reading prior lessons, and logging new mistakes and fixes into persistent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The submitted package instructs users to clone and periodically run a remote executable that is not included in the artifact.

Mitigation: Review the server-resolved GitHub repository, pin a trusted commit, and scan executable files before installing or enabling heartbeat execution.

Risk: Reflection logs may capture secrets, private user data, or sensitive operational details.

Mitigation: Store the memory file outside shared or synced workspaces, avoid logging secrets or private user data, and periodically review or delete stored lessons.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lokix94/skills/self-reflection-2)
- [Server-resolved GitHub source](https://github.com/lokix94/peru-ai/tree/main/skills/self-reflection)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, status text, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update local reflection memory and timer state files when the referenced CLI is installed and run.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
