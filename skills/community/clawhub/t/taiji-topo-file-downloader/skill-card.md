## Description: <br>
Automates locating the node sidebar, opening the configuration file panel, and downloading files from Taiji workflow pages at a.taiji.woa.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m-final](https://clawhub.ai/user/m-final) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to guide browser automation that downloads topology configuration or model files from Taiji workflow pages after checking the active page, sidebar, file list, and local download result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates the user's current Chrome session on a.taiji.woa.com and moves the newest Chrome temporary download file, which could select the wrong file if other downloads are active. <br>
Mitigation: Use it only for the intended Taiji page, avoid concurrent Chrome downloads, confirm the target file name, and review the destination path before running the move and rename command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/m-final/taiji-topo-file-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes browser automation steps, page-state checks, file matching guidance, and a local download rename command pattern.] <br>

## Skill Version(s): <br>
1.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
