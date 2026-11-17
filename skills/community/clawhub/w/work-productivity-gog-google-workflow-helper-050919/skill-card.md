## Description:

Helps agent users, skill authors, maintainers, and teams create practical Gog-style Google Workspace workflows for bug fixes, setup hardening, safety improvements, reliability work, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn Gog-style Google Workspace productivity requests into actionable plans, checklists, implementation support, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may activate the skill for ordinary Google or CLI requests where the user did not intend to use it.

Mitigation: Prefer explicit skill invocation or tighten routing keywords before deployment in environments with many Google Workspace or CLI workflows.

Risk: The skill can produce workflow, code, shell command, or configuration suggestions that may be incorrect for a user's environment.

Mitigation: Review generated artifacts before use and validate them against the stated success criteria and local constraints.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Release Page](https://clawhub.ai/kyro-ma/skills/work-productivity-gog-google-workflow-helper-050919)
- [Gog Demand Signal](https://clawhub.ai/skills/gog)
- [Self-Improving Agent Demand Signal](https://clawhub.ai/skills/self-improving-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, limits, validation notes, and any remaining follow-up work when helpful.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
