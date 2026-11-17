## Description:

Skill Stress Test guides developers through pre-release stress checks for WorkBuddy Skills across boundary inputs, output consistency, and rapid sequential use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spiderzhcl](https://clawhub.ai/user/spiderzhcl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to manually evaluate another Skill before release, checking how it handles unusual inputs, whether repeated outputs stay structurally consistent, and whether rapid consecutive requests cause ordering or timeout issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation advertises automation commands for scripts/stress-test.py, but the artifact does not include that script.

Mitigation: Treat the release as a manual checklist unless a trusted script is supplied separately; avoid running the documented automation commands from this artifact as-is.

## Reference(s):

- [Server-resolved source repository](https://github.com/spiderzhcl/skill-stress-test)
- [ClawHub skill listing](https://clawhub.ai/spiderzhcl/skills/skill-stress-test)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with checklists, tables, report templates, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a stress-test report template; referenced automation commands require a separate script that is not present in the artifact.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
