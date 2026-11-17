## Description:

Audit, score, and improve agent skills before publishing, sharing, or installing them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to review AgentSkills-style skill folders for trigger quality, compatibility, safety, install friction, marketplace positioning, and launch readiness before publishing, sharing, or installing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's safety score is a launch-readiness aid, not a full security review.

Mitigation: Use findings as review guidance, then run an independent security review before relying on a skill in sensitive or production workflows.

Risk: The auditor evaluates the skill directory it is pointed at, so reviewing the wrong path can produce misleading readiness results.

Mitigation: Run it only on the specific SKILL.md file or skill directory intended for release and confirm the target path in the report.

## Reference(s):

- [Skill Launch Rubric](references/launch-rubric.md)
- [Description Patterns](references/description-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown audit report with optional JSON output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include score, verdict, P0/P1 findings, concrete fixes, suggested description rewrites, compatibility notes, remaining launch risks, and a smallest next action.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
