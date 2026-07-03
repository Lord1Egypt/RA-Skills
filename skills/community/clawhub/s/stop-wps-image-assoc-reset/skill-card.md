## Description: <br>
Permanently prevent WPS Office from hijacking image file associations and restore user control over default image viewers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibiubiu233i](https://clawhub.ai/user/ibiubiu233i) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Windows users and support engineers use this skill to generate step-by-step PowerShell guidance for stopping WPS Office from repeatedly resetting image file associations and for restoring user control through Windows default-app settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes broad PowerShell operations that can change scheduled tasks, registry entries, and installed WPS files. <br>
Mitigation: Before running commands, export affected registry keys, list the matched tasks and files, confirm they are only WPS image-viewer components, and prefer renaming or quarantining files over deletion. <br>
Risk: Normal WPS behavior may be affected by persistent changes to image-viewer components. <br>
Mitigation: Be prepared to repair or reinstall WPS, and re-check file associations after WPS updates because the behavior may return. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ibiubiu233i/stop-wps-image-assoc-reset) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell code blocks and procedural guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes persistent Windows and WPS changes that require user review and may require administrator privileges.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
