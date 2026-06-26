## Description: <br>
Visualizes Product Manager thoughts (Why, What, How, User Journey) into an editable Excalidraw diagram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sairammahadevan](https://clawhub.ai/user/sairammahadevan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Product managers, developers, and planning teams use this skill to turn unstructured product notes into a structured visual specification covering rationale, requirements, implementation notes, and user journey steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a temporary JSON input file and writes a generated Excalidraw file locally. <br>
Mitigation: Use a user-controlled output folder, remove temporary input files after generation, and review the generated diagram before sharing it. <br>


## Reference(s): <br>
- [Excalidraw JSON Schema Reference](references/excalidraw-schema.md) <br>
- [Excalidraw](https://excalidraw.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with JSON input data, shell commands, and a generated .excalidraw file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Python script writes an Excalidraw JSON file to a user-selected local path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
