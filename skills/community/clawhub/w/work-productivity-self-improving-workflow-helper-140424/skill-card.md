## Description:

Helps AI-agent users, skill authors, maintainers, and teams turn self-improving and proactive agent workflow needs into practical plans, checklists, analyses, code changes, and validation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and teams use this skill to structure self-improving or proactive agent workflows, including bug fixing, setup hardening, reliability improvement, and adjacent skill creation. It produces actionable artifacts that can be used without consulting the original demand sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation rules may cause the skill to influence unrelated requests where a narrower skill would be more appropriate.

Mitigation: Review automatic activation settings before installation and narrow or disable implicit invocation when precision matters.

Risk: Workflow advice may be applied without enough task-specific context.

Mitigation: Require the agent to state assumptions, success criteria, validation steps, and remaining risks before using the output operationally.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/kyro-ma/skills/work-productivity-self-improving-workflow-helper-140424)
- [Requirement Plan](references/requirement-plan.md)
- [Self-improving agent demand signal](https://clawhub.ai/skills/self-improving-agent)
- [Proactive Agent demand signal](https://clawhub.ai/skills/proactive-agent)
- [Self-Improving + Proactive Agent demand signal](https://clawhub.ai/skills/self-improving)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable checklists, workflow templates, assumptions, validation notes, and follow-up risks.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
