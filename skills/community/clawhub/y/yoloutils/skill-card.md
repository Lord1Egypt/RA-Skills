## Description: <br>
Yolo Utilities helps agents give command-level guidance for the yoloutils label, merge, copy, remove, change, crop, labelimg, resize, classify, and test workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netkiller](https://clawhub.ai/user/netkiller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and computer vision engineers use this skill when preparing, inspecting, transforming, and testing YOLO datasets or model outputs with the yoloutils command-line toolkit. It focuses on required parameters, command behavior, side effects, limitations, and execution examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Several documented yoloutils workflows can overwrite, remove, or clean local dataset files and output directories. <br>
Mitigation: Run commands on copied sample data first, verify source and target paths, and use --clean, remove, or in-place change only when file deletion or overwriting is acceptable. <br>
Risk: The skill depends on local yoloutils behavior and local dependencies, models, paths, and classes.txt files being present and correct. <br>
Mitigation: Confirm the command or script is trusted and installed locally, check required Python packages and model files, and validate outputs with label statistics, sampled output directories, CSV files, or generated data.yaml files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/netkiller/yoloutils) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples, pre-checks, side-effect notes, and validation steps for local YOLO utility workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
