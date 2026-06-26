## Description: <br>
Generate SVG images using text LLM instead of image generation APIs for illustrations, icons, cartoons, diagrams, and other simple visual content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juliantsaiii](https://clawhub.ai/user/juliantsaiii) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create simple SVG-based images and optionally render them to PNG without calling a dedicated image generation API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can run local conversion commands using an output path supplied through command-line input. <br>
Mitigation: Use fixed filenames in a constrained temporary directory, prevent untrusted prompts from choosing paths, validate output paths, and prefer argument-array process APIs such as execFile or spawn. <br>


## Reference(s): <br>
- [SVG Artist ClawHub Release](https://clawhub.ai/juliantsaiii/svg-artist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with SVG code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce SVG files and PNG render outputs when the helper workflow is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
