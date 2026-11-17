## Description:

Quick workspace health check - list workspace contents, git status, recent memory notes, and deliverable outputs in one pass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to quickly orient in a workspace before starting work, reviewing results, or checking whether expected deliverables exist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running this skill may expose top-level filenames, git status, deliverable filenames, and recent memory note filenames in the conversation or logs.

Mitigation: Avoid using it in shared or untrusted contexts when filenames could reveal private project or client information.

## Reference(s):

- [WS QuickStatus reference notes](references/DESCRIPTION.md)
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/ws-quickstatus)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text summary with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external services required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
