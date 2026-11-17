## Description:

Helps AI-agent users, skill authors, maintainers, and teams build or improve ontology-style productivity workflows through practical plans, checklists, implementation support, and validation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and AI-agent teams use this skill to turn ontology-style productivity requirements into actionable workflows, templates, checklists, code changes, or decision support. It is intended for practical local-hardware-friendly workflow improvement and skill-authoring support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation keywords may activate the skill for adjacent productivity, graph, or bug-fix requests where another workflow is more appropriate.

Mitigation: Review trigger behavior before deployment and narrow keywords or require explicit invocation in environments where accidental activation would be disruptive.

Risk: Workflow advice or generated artifacts may be incomplete or mismatched to a user's real constraints.

Mitigation: Require the agent to state assumptions, success criteria, validation notes, and remaining risks before the output is used.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [Work Productivity Ontology Typed Workflow Helper on ClawHub](https://clawhub.ai/kyro-ma/skills/work-productivity-ontology-typed-workflow-helper-035116)
- [Popular ClawHub skill demand: Self-Improving + Proactive Agent](https://clawhub.ai/skills/self-improving)
- [Popular ClawHub skill demand: ontology](https://clawhub.ai/skills/ontology)
- [Popular ClawHub skill demand: Multi Search Engine](https://clawhub.ai/skills/multi-search-engine)
- [Popular ClawHub skill demand: AdMapix](https://clawhub.ai/skills/admapix)
- [Vector search isn't the hard part. Deciding what should be searched is](https://news.ycombinator.com/item?id=48939470)
- [OntologyOps complete plan](https://segmentfault.com/a/1190000047947726)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or text with optional code, shell command, checklist, and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, visible limits, validation notes, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
