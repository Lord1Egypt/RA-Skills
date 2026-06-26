## Description: <br>
Scientific Drawing helps agents create research figures such as technical roadmaps, flowcharts, schematics, architecture diagrams, timelines, and data visualizations with Python plotting tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical writers use this skill to draft publication- and grant-ready scientific diagrams, generate Python drawing code, and refine high-resolution figures for academic documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated drawing scripts may write files to an unintended location if fixed output paths or unsafe filenames are used. <br>
Mitigation: Run the skill in a contained workspace, choose a safe output directory, normalize filenames, block path traversal, and review generated scripts before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Files] <br>
**Output Format:** [Markdown with Python code blocks and generated figure file paths; figures are PNG, SVG, or PDF when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to high-resolution scientific figures; output paths and filenames should be reviewed before running generated code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
