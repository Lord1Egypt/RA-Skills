## Description: <br>
Generates a 15-slide client presentation framework from a selected SketchUp model file, with reserved areas for design screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[137984917-cyber](https://clawhub.ai/user/137984917-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Interior design teams and presentation authors use this skill to create a standard client-facing PPTX outline from a SketchUp project file. It is intended to speed up report preparation while leaving visual renderings and screenshots for the user to add manually. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated PPTX may overwrite an existing file if the output path points to an important presentation. <br>
Mitigation: Write to a new or backed-up output path before editing the generated presentation. <br>
Risk: The skill creates a presentation framework and does not parse SketchUp geometry or automatically generate screenshots. <br>
Mitigation: Review the generated slides and manually add the SketchUp screenshots or renderings needed for the client report. <br>
Risk: Running the bundled script requires the python-pptx dependency. <br>
Mitigation: Install python-pptx only from a trusted package source in the intended local Python environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/137984917-cyber/sketchup-ppt-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples; generated PPTX file when the bundled script is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script expects an input .skp path, output .pptx path, and optional project name and style.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
