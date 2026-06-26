## Description: <br>
Windows Esm Installer helps Windows users diagnose and repair common OpenClaw/Skill installation issues, including ESM URL path errors, npm timeouts, missing dependencies, and installer script generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support users working on Windows use this skill to diagnose OpenClaw/Skill installation problems, convert Windows paths to file URLs, configure npm mirror settings, and generate runnable installer scripts and an installation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change npm registry settings persistently. <br>
Mitigation: Preview the npm command, confirm whether the registry change is global or project-local, and save the previous registry value before applying changes. <br>
Risk: The skill can create executable Windows installer scripts. <br>
Mitigation: Review generated .bat and .ps1 files, including all command targets and file paths, before running them. <br>
Risk: The security verdict is suspicious because the skill may make configuration changes and write executable files without clear prior consent. <br>
Mitigation: Require explicit user confirmation before running repair actions or generated scripts. <br>


## Reference(s): <br>
- [Windows Esm Installer on ClawHub](https://clawhub.ai/rfdiosuao/windows-esm-installer) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration guidance] <br>
**Output Format:** [Markdown responses with command snippets, generated Windows script files, and INSTALL_REPORT.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write install.bat, install.ps1, and INSTALL_REPORT.md in the current project directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
