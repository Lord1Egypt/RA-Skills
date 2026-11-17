## Description:

Use only when the user explicitly asks to inspect or compare coding-agent skills before installation or invocation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[three-liu](https://clawhub.ai/user/three-liu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill as a local preflight tool to inspect installed and candidate coding-agent skills for name shadowing, capability overlap, policy conflicts, and behavioral interference before installation or invocation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads SKILL.md files from known local agent skill directories and supplied candidate paths.

Mitigation: Run it only when local skill inventory inspection is intended, and review reported paths before acting on recommendations.

Risk: Remote candidate checks can clone user-supplied Git references for read-only inspection.

Mitigation: Use remote inspection only for references the user intentionally provides, and treat the resulting comparison as evidence for review rather than an automatic install decision.

Risk: Session suppression stores selected skill names or paths and timestamps in local state.

Mitigation: Use suppression for reversible session-scoped decisions and clear or restore suppressions when they are no longer needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/three-liu/skills/skill-collision-guard)
- [Publisher profile](https://clawhub.ai/user/three-liu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON CLI reports with comparison summaries and recommended shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports relationships, severity, evidence source, affected workflows, opposing policies, and recommendations; JSON output is available with --json.]

## Skill Version(s):

0.1.1 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
