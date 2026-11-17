## Description:

Helps agent users, skill authors, maintainers, and teams create ontology-style workflow artifacts, checklists, analyses, and implementation support for practical productivity tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, agent users, skill authors, maintainers, and teams use this skill to turn ontology-style productivity needs into concrete plans, templates, checklists, code changes, analyses, or decision support. It is intended for practical bug fixing, setup hardening, reliability improvement, and adjacent workflow creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate too often because its triggers include generic terms and implicit invocation is enabled.

Mitigation: Use explicit invocation or tighten activation wording when precise routing matters.

Risk: Workflow advice could be applied without enough review for the user's local context.

Mitigation: Review generated plans, checklists, code, shell commands, and configuration changes before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-ontology-typed-workflow-helper-080414)
- [Self-Improving + Proactive Agent demand signal](https://clawhub.ai/skills/self-improving)
- [Ontology demand signal](https://clawhub.ai/skills/ontology)
- [Graph view enhancement request](https://github.com/nashsu/llm_wiki/issues/605)
- [OntologyOps reference signal](https://segmentfault.com/a/1190000047947726)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include tailored artifacts, reusable checklists or workflows, and a short verification note.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
