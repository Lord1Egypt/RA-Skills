## Description:

Initializes a user-named OpenClaw workspace with a standard directory layout, persistent workspace rules, and multi-agent configuration safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsola](https://clawhub.ai/user/dtsola)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users who explicitly request workspace initialization or repair use this skill to create a standard directory layout, add workspace rules, and record the work. It requires the user to name the workspace root and presents proposed changes for review before writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace rules and memory entries can persist and affect future sessions.

Mitigation: Review proposed content and the named write scope before confirming; keep sensitive information out of persistent logs.

Risk: The security assessment is benign but incomplete, and some bundled content was not covered.

Mitigation: Treat the assessment as advisory and review the bundled files before deployment.

## Reference(s):

- [Project documentation](https://github.com/dtsola/xiaoyaoclaw-workspace-initializer)
- [ClawHub skill page](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-workspace-initializer)

## Skill Output:

**Output Type(s):** [Files, Markdown, Configuration instructions, Guidance]

**Output Format:** [Workspace directories and Markdown files, plus a Markdown change summary and proposed configuration diff]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes are scoped to the named workspace root; proposed changes require user review.]

## Skill Version(s):

1.0.11 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
