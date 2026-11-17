## Description:

Helps agent users, skill authors, maintainers, and teams create practical ontology-style productivity workflows, artifacts, checklists, analysis, code changes, and decision support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, developers, skill authors, maintainers, and teams use this skill to turn ontology-style productivity needs into concrete local-friendly workflows, checklists, plans, implementation support, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording and implicit invocation may cause the skill to trigger when the user did not intend to use it.

Mitigation: Prefer explicit invocation by skill name or confirm the ontology-style productivity workflow is relevant before relying on its output.

Risk: Workflow outputs may include incomplete or incorrect guidance for skill authoring, reliability, or setup-hardening tasks.

Mitigation: Review generated plans, code, commands, and configuration against the stated success criteria, then test or scan changes before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-ontology-typed-workflow-helper-020416)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: ontology](https://clawhub.ai/skills/ontology)
- [Ask HN: Does a local, Git-backed LLM compiler for personal notes make sense?](https://news.ycombinator.com/item?id=48968447)
- [OntologyOps complete solution](https://segmentfault.com/a/1190000047947726)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include assumptions, visible limits, validation notes, and next steps when helpful.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
