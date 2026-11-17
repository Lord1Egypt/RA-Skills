## Description:

Generates UTF-8 PlantUML .puml diagram source files in the workspace, with guidance for sequence diagrams and broader PlantUML syntax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lentiancn](https://clawhub.ai/user/lentiancn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent produce PlantUML diagram source files, especially sequence diagrams, and save them into a dedicated workspace folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PlantUML diagram text could be incorrect or misleading if committed without review.

Mitigation: Review generated .puml files before committing or using them as documentation.

Risk: The skill may create .puml files under plantuml-src/ when invoked.

Mitigation: Check the generated file path and workspace diff before committing changes.

## Reference(s):

- [Sequence Diagram Syntax](references/sequence-diagram.md)
- [PlantUML Documentation](https://plantuml.com/en/)
- [PlantUML Sequence Diagram Documentation](https://plantuml.com/en/sequence-diagram)
- [ClawHub PlantUML Skill Page](https://clawhub.ai/lentiancn/skills/skill-plantuml)

## Skill Output:

**Output Type(s):** [Code, Files, Text]

**Output Format:** [UTF-8 .puml files plus a text response with the generated file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are saved under plantuml-src/ in the workspace.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
