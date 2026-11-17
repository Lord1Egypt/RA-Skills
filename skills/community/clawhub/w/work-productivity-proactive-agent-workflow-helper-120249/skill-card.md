## Description:

Helps AI-agent users, skill authors, maintainers, and teams turn proactive-agent workflow requests into scoped plans, checklists, artifacts, analyses, or implementation support with validation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, skill authors, and AI-agent users use this skill to clarify proactive work-productivity requests, create reusable workflows or artifacts, and validate outputs against visible success criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger words and implicit invocation can cause the skill to be selected for ordinary task or bug-fix requests.

Mitigation: Disable or narrow automatic skill routing when unwanted, and confirm the selected skill before applying guidance to important work.

Risk: Workflow helper outputs can be incomplete or misleading if the user's constraints or success criteria are underspecified.

Mitigation: Review assumptions, validate the result against the stated criteria, and ask for missing information when it materially changes the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-proactive-agent-workflow-helper-120249)
- [Requirement Plan](artifact/references/requirement-plan.md)
- [Popular ClawHub skill demand: Proactive Agent](https://clawhub.ai/skills/proactive-agent)
- [Popular ClawHub skill demand: Self-Improving + Proactive Agent](https://clawhub.ai/skills/self-improving)
- [Popular ClawHub skill demand: ontology](https://clawhub.ai/skills/ontology)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text, with code blocks or configuration snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable checklists, workflow templates, analysis, implementation notes, and a brief verification note.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
