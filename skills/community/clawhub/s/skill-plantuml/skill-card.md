## Description: <br>
Helps an agent generate PlantUML sequence and other diagram source files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lentiancn](https://clawhub.ai/user/lentiancn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent create PlantUML .puml diagram source, especially sequence diagrams, and save the generated files in the workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated .puml files may overwrite existing files under plantuml-src if filenames collide. <br>
Mitigation: Review proposed filenames and existing files in plantuml-src before accepting writes when overwrite behavior matters. <br>
Risk: Generated PlantUML diagrams may encode incorrect or incomplete system behavior. <br>
Mitigation: Review the generated PlantUML source and rendered diagram before using it as design or implementation documentation. <br>


## Reference(s): <br>
- [Sequence Diagram Syntax](references/sequence-diagram.md) <br>
- [PlantUML Documentation](https://plantuml.com/en/) <br>
- [PlantUML Sequence Diagram Documentation](https://plantuml.com/en/sequence-diagram) <br>
- [ClawHub Skill Page](https://clawhub.ai/lentiancn/skill-plantuml) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with generated UTF-8 .puml files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated PlantUML files are expected under plantuml-src in the user's workspace.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
