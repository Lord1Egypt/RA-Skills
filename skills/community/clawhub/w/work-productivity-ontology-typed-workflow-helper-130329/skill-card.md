## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical ontology-style workflows, artifacts, checklists, analysis, and implementation support for work-productivity use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn ontology-style work-productivity needs into concrete workflows, checklists, templates, analysis, code changes, or decision support. The skill emphasizes local-hardware-friendly execution and validation against explicit success criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation terms may cause the skill to activate more often than intended.

Mitigation: Review whether implicit invocation is desired and narrow triggers to ontology-style work-productivity tasks before deployment.

Risk: Workflow guidance can produce incorrect or misleading recommendations if the user goal, constraints, or validation criteria are underspecified.

Mitigation: Require the agent to restate assumptions, success criteria, validation steps, and remaining risks in user-facing output.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-ontology-typed-workflow-helper-130329)
- [Popular ClawHub skill demand: ontology](https://clawhub.ai/skills/ontology)
- [OntologyOps complete plan](https://segmentfault.com/a/1190000047947726)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code, shell command, configuration, checklist, and template blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, visible limits, validation notes, and remaining risks when helpful.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
