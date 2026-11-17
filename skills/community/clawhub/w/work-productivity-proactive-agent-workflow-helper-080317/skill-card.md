## Description:

Helps AI-agent users, skill authors, maintainers, and teams turn proactive-agent productivity requests into local-friendly workflows, checklists, implementation support, and validation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to structure proactive productivity tasks such as bug fixing, reliability hardening, workflow planning, and adjacent skill creation. It guides the agent to restate outcomes, plan concise work, ask only material questions, produce the requested artifact, and validate the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause the skill to appear for ordinary task or bug-fix requests where a more specific skill would fit better.

Mitigation: Check whether a narrower skill applies before use and confirm the user's outcome, constraints, inputs, and success criteria.

Risk: Generated workflows, checklists, or implementation suggestions may be incomplete or misleading for the user's specific environment.

Mitigation: Review the output against the stated success criteria and validate code, commands, or configuration changes before relying on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/kyro-ma/skills/work-productivity-proactive-agent-workflow-helper-080317)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: Proactive Agent](https://clawhub.ai/skills/proactive-agent)
- [Popular ClawHub skill demand: Self-Improving + Proactive Agent](https://clawhub.ai/skills/self-improving)
- [Popular ClawHub skill demand: ontology](https://clawhub.ai/skills/ontology)
- [Feed-poll HTTP client hardening issue](https://github.com/wmo-raf/cap-aggregator/issues/78)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code, shell command, checklist, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a tailored artifact, reusable checklist or workflow, and a verification note.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
