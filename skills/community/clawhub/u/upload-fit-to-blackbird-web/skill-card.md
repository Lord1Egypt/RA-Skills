## Description: <br>
Automatically batch uploads modified _GM.fit files to the Blackbird Sport web platform with login detection and upload status handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CKboss](https://clawhub.ai/user/CKboss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, athletes, and activity-file maintainers use this skill to upload selected FIT files or directories to the Blackbird Sport web platform through a browser-driven workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uploads user-selected FIT activity files to Blackbird Sport. <br>
Mitigation: Use explicit file paths or narrow globs, review the files before upload, and run the skill only when sharing those activity files with Blackbird Sport is intended. <br>
Risk: The browser workflow may require an interactive login to a Blackbird account. <br>
Mitigation: Log in only on the intended Blackbird Sport domain and account, and close the browser session after verifying the upload result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CKboss/upload-fit-to-blackbird-web) <br>
- [Blackbird Sport upload page](https://www.blackbirdsport.com/user/records/upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python execution instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser automation prompts for manual login when required and prints upload status to the terminal.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
