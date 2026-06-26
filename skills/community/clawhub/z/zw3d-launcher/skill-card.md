## Description: <br>
Launch ZW3D CAD software. Use when the user wants to open, start, or launch ZW3D CAD application. Handles finding the ZW3D executable and launching it with optional file opening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shemin1024](https://clawhub.ai/user/shemin1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ZW3D CAD users use this skill to start ZW3D on Windows and optionally open a specified CAD file. It helps an agent locate a local ZW3D executable from common install paths or the ZW3D_PATH environment variable before launching it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper launches a local executable discovered from common install paths or ZW3D_PATH. <br>
Mitigation: Review the script before use and verify ZW3D_PATH points to the intended zw3d.exe executable. <br>
Risk: Passing an unintended file path could open the wrong CAD file in ZW3D. <br>
Mitigation: Pass only files the user intends to open in ZW3D. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local launch instructions and may run a Python helper that starts a Windows desktop application.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
