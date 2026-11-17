## Description:

Helps AI-agent users and skill authors create practical ontology-style typed workflows, checklists, analyses, and implementation support for productivity and reliability tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI-agent users, skill authors, maintainers, and teams use this skill to turn ontology-style productivity needs into concrete workflows, checklists, plans, code changes, analyses, or decision support. It is intended for local-hardware-friendly work where assumptions, validation notes, and follow-up risks should be visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate too broadly in auto-routing environments because its trigger wording spans productivity, ontology, typed workflows, knowledge graphs, bug fixing, and related implementation support.

Mitigation: Prefer explicit invocation or route it only when the user is working on ontology-style typed workflows, knowledge-graph productivity workflows, or adjacent skill/workflow design.

Risk: As a documentation-only helper, it can produce plausible but context-dependent workflow or implementation guidance that still needs review before adoption.

Mitigation: Review generated plans, checklists, code changes, and configuration advice against the user's stated success criteria before deployment or reuse.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-ontology-typed-workflow-helper-140331)
- [Self-Improving + Proactive Agent demand signal](https://clawhub.ai/skills/self-improving)
- [Ontology demand signal](https://clawhub.ai/skills/ontology)
- [OntologyOps reference signal](https://segmentfault.com/a/1190000047947726)
- [Text knowledge graph construction reference signal](https://segmentfault.com/a/1190000044569069)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with optional code, shell command, checklist, or configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include visible assumptions, validation notes, limits, and remaining risks when helpful.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
