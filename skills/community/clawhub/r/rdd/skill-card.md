## Description:

Requirements-Driven Development helps agents converge fuzzy software requirements into traceable, testable specifications before coding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyjohn](https://clawhub.ai/user/anyjohn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to turn raw requirements into work items, structured specs, acceptance criteria, implementation plans, tests, and verification evidence before or during software changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create project-local requirement, specification, decision, or traceability files as part of its workflow.

Mitigation: Review proposed files before committing them, especially generated .rdd artifacts, specs, and traceability mappings.

Risk: Most detailed guidance and templates are in Chinese, which may cause misunderstanding for teams that cannot review Chinese-language artifacts.

Mitigation: Have a qualified reviewer confirm generated requirements and specifications before using them to drive implementation.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/anyJohn/OpenReq/tree/main/skills/rdd)
- [ClawHub skill page](https://clawhub.ai/anyjohn/skills/rdd)
- [RDD architecture design](references/rdd-design.md)
- [RDD file templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured YAML examples, checklists, implementation guidance, and shell commands when verification requires them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project-local requirement, specification, decision, traceability, code, and test artifacts when appropriate.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
