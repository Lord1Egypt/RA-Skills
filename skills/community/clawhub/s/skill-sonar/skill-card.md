## Description:

Lifecycle guard for skill-augmented coding agents covering preflight and runtime phases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxf203](https://clawhub.ai/user/yxf203)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review skill packages before installation and to apply advisory guard checks around active skill use, tool calls, file edits, command execution, data access, and final outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advisory and may slow workflows by requiring extra review or confirmation around tools, writes, credential access, external calls, and other sensitive actions.

Mitigation: Install it when stricter review is desired, and keep user confirmation as the authority for sensitive or irreversible actions.

Risk: Security-example text in the documentation may trigger scanner alerts even though server security evidence found no hidden execution, exfiltration, destructive behavior, or persistence.

Mitigation: Use the server security summary as the risk source and review scanner alerts as documentation examples unless concrete behavior is identified.

Risk: Guard recommendations can be mistaken for runtime enforcement.

Mitigation: Treat the skill's outputs as guidance; the agent or user must still apply host controls, authorization checks, and sandbox limits.

## Reference(s):

- [ClawHub SKILL Sonar](https://clawhub.ai/yxf203/skills/skill-sonar)
- [SKILL.md](SKILL.md)
- [Preflight Guard](preflight/preflight-guard.md)
- [Runtime Guard](runtime/runtime-guard.md)
- [Triage Checklist](runtime/checklists/triage-checklist.md)
- [Sensitive Resource Check](runtime/checklists/sensitive-resource-check.md)
- [Execution Guard](runtime/stages/execution-guard.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown guard assessments and concise advisory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk levels, guard actions, confirmation prompts, and safer alternatives when runtime checks are triggered.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
