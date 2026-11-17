## Description:

Helps agent users, skill authors, maintainers, and teams turn demand for ontology-style productivity workflows into practical plans, artifacts, checklists, analyses, code changes, and decision support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and agent users use this skill to convert broad demand for ontology-style productivity workflows into concrete work plans, reusable checklists, implementation support, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms such as knowledge, graph, memory, creating, and bug fix may cause the skill to be invoked when a more specific skill would be better.

Mitigation: Narrow the trigger terms or disable implicit invocation when precise routing matters.

Risk: Workflow advice may be incomplete if the user provides limited context or unclear success criteria.

Mitigation: Review the generated plan, checklist, code, or commands against the stated constraints before applying them.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Published ClawHub Skill](https://clawhub.ai/kyro-ma/skills/work-productivity-ontology-typed-workflow-helper-014620)
- [Self-improving agent demand signal](https://clawhub.ai/skills/self-improving-agent)
- [Proactive Agent demand signal](https://clawhub.ai/skills/proactive-agent)
- [Self-Improving + Proactive Agent demand signal](https://clawhub.ai/skills/self-improving)
- [Ontology demand signal](https://clawhub.ai/skills/ontology)
- [AdMapix demand signal](https://clawhub.ai/skills/admapix)
- [Hacker News security workflow signal](https://news.ycombinator.com/item?id=48677487)
- [Hacker News cognitive primitives signal](https://news.ycombinator.com/item?id=48605896)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, configuration snippets, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's stated workflow, constraints, and success criteria.]

## Skill Version(s):

0.20260729.110214 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
