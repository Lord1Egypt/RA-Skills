## Description:

Scaffolds OpenClaw workspaces with session, memory, safety, and collaboration conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jontsai](https://clawhub.ai/user/jontsai)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and workspace administrators use this skill to set up and maintain agent instructions, memory practices, safety rules, and optional workspace integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory instructions may expose private workspace context through remote pushes.

Mitigation: Remove automatic memory-file git pushes and review what is stored or shared before enabling them.

Risk: Generated instructions encourage broad searches of private files and services.

Mitigation: Require explicit approval before accessing credentials, dotfiles, cloud storage, email, calendars, or prior sessions.

Risk: Incident alerts could disclose sensitive details across unintended channels.

Mitigation: Define approved incident recipients and channels in the generated security instructions before use.

## Reference(s):

- [OpenClaw Spacesuit on ClawHub](https://clawhub.ai/jontsai/skills/spacesuit)
- [Release and rollback instructions](artifact/docs/releases/README.md)
- [Work graph documentation](artifact/docs/work-graph.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides workspace instruction templates and optional local snapshot workflows.]

## Skill Version(s):

0.4.0 (source: ClawHub release, SKILL.md, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
