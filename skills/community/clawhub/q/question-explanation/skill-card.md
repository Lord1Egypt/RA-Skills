## Description: <br>
Generate a complete HTML tutorial that explains one or more problems with clear reasoning and embedded SVG or Canvas visuals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vaintwyt](https://clawhub.ai/user/vaintwyt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, educators, and external users use this skill to turn question images, worksheets, exam problems, homework problems, or pasted problem text into a self-contained HTML tutorial with reasoning, solution walkthroughs, and embedded SVG or Canvas visuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local HTML files, which can overwrite prior output if the same filename is reused. <br>
Mitigation: Ask the agent to use a unique filename or a dedicated output folder for each generated tutorial. <br>
Risk: Generated HTML may include active JavaScript or visual content derived from user-provided question material. <br>
Mitigation: Open generated HTML only when the input content is trusted enough to render locally. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration] <br>
**Output Format:** [A saved, self-contained HTML file with embedded CSS, JavaScript, SVG, and Canvas content, followed by a concise completion message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML is intended to be directly viewable locally and uses SVG or Canvas rather than external image assets for teaching visuals.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
