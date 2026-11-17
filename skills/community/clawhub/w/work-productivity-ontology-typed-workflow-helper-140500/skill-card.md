## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical ontology-style workflows, checklists, analyses, implementation support, and validation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, skill authors, maintainers, and teams use this skill to turn ontology-style productivity needs into local-friendly plans, templates, checklists, workflow artifacts, analysis, code changes, or decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad triggers and implicit invocation enabled, so it may be selected for loosely related ontology, productivity, graph, or workflow requests.

Mitigation: Invoke it explicitly for intended tasks or narrow its trigger terms before deployment where selection predictability matters.

Risk: Workflow, code, shell command, or configuration guidance can be incomplete or incorrect for a user's environment.

Mitigation: Review generated artifacts before use and validate them against the stated success criteria, especially before applying code or configuration changes.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-ontology-typed-workflow-helper-140500)
- [Popular ClawHub skill demand: self-improving agent](https://clawhub.ai/skills/self-improving-agent)
- [Popular ClawHub skill demand: ontology](https://clawhub.ai/skills/ontology)
- [Forked CozoDB to give agents cognitive primitives](https://news.ycombinator.com/item?id=48605896)
- [OntologyOps complete plan](https://segmentfault.com/a/1190000047947726)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, code snippets, shell commands, configuration snippets, or workflow artifacts depending on the request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, reusable checklists, and follow-up risks when helpful.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
