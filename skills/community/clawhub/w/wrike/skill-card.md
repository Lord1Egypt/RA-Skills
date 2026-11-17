## Description:

Manage Wrike tasks, projects, folders, and comments via the Wrike REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tallhamn](https://clawhub.ai/user/tallhamn)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent manage Wrike spaces, folders, projects, tasks, comments, contacts, workflows, and custom fields through the Wrike CLI and REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on the claw-wrike npm package, which is not pinned in the release evidence.

Mitigation: Install only from a trusted package source and review the selected package version before use.

Risk: Wrike tokens are stored locally by the CLI configuration flow.

Mitigation: Use a least-privilege Wrike token and protect the local configuration file that stores it.

Risk: Create, update, and delete commands can change live Wrike tasks, folders, projects, and comments.

Mitigation: Use dry-run where available, read current state before updates, and require confirmation before bulk changes.

## Reference(s):

- [ClawHub Wrike skill page](https://clawhub.ai/tallhamn/skills/wrike)
- [Publisher profile](https://clawhub.ai/user/tallhamn)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON response patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require claw-wrike and a Wrike token; use dry-run and read-before-update workflows before changing live Wrike data.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
