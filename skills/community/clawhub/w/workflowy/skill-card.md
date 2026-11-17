## Description:

Workflowy outliner CLI for reading, searching, and editing nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waldyrious](https://clawhub.ai/user/waldyrious)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to let an agent read, search, and edit their Workflowy outline through the unofficial workflowy CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unofficial, unpinned third-party workflowy CLI that can access private outline data.

Mitigation: Review the CLI before installing it and pin or verify the exact release used in agent environments.

Risk: The Workflowy API key is a long-lived credential that can expose private outline data if mishandled.

Mitigation: Store the key with restrictive file permissions when possible, avoid broad environment exposure, and rotate it if compromise is suspected.

Risk: Write operations such as delete, move, replace, and transform can alter or remove outline content.

Mitigation: Require manual confirmation before destructive or bulk-changing commands, and prefer dry-run or interactive modes for replacements.

## Reference(s):

- [Workflowy ClawHub Skill](https://clawhub.ai/waldyrious/skills/workflowy)
- [workflowy CLI homepage](https://github.com/mholzen/workflowy)
- [workflowy CLI command reference](https://github.com/mholzen/workflowy/blob/main/docs/CLI.md)
- [Workflowy API reference](https://workflowy.com/api-reference/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide read, write, delete, move, replace, transform, report, and API-key setup operations for Workflowy outlines.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
