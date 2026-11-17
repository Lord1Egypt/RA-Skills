## Description:

Helps agent users, skill authors, maintainers, and teams create practical self-improving and proactive workflows for bug fixing, setup hardening, reliability improvement, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn self-improving and proactive agent workflow needs into actionable plans, checklists, implementation support, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad keywords and implicit invocation may cause the skill to activate in situations where a more specific helper would be better.

Mitigation: Invoke the skill explicitly by name or narrow its triggers before installation when precise routing is required.

Risk: Generated workflow or implementation guidance may be incomplete or mismatched to a user's local constraints.

Mitigation: Review outputs against the stated success criteria and keep assumptions, limits, and follow-up checks visible before applying changes.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Self-Improving Agent demand reference](https://clawhub.ai/skills/self-improving-agent)
- [Proactive Agent demand reference](https://clawhub.ai/skills/proactive-agent)
- [Self-Improving + Proactive Agent demand reference](https://clawhub.ai/skills/self-improving)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tailored artifacts, reusable checklists or workflows, assumptions, limits, and verification notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
