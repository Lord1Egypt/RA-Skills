## Description:

Visualizes Product Manager thoughts (Why, What, How, User Journey) into an editable Excalidraw diagram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sairammahadevan](https://clawhub.ai/user/sairammahadevan)

### License/Terms of Use:


## Use Case:

Product managers, founders, and product teams use this skill to turn unstructured product notes into a structured Excalidraw visual spec covering why, what, how, and user journey sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes local files, including a temporary JSON input file and an Excalidraw output file.

Mitigation: Use a dedicated output folder, review the output path before running the command, and delete only the temporary input file created for the diagram.

Risk: The generated diagram may omit, oversimplify, or misframe product requirements supplied in free-form notes.

Mitigation: Review the generated Excalidraw file with product and engineering stakeholders before treating it as a specification.

## Reference(s):

- [Excalidraw JSON Schema Reference](references/excalidraw-schema.md)
- [Excalidraw](https://excalidraw.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON input structure, shell commands, and a generated .excalidraw JSON file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a temporary JSON input file and a local Excalidraw output file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
