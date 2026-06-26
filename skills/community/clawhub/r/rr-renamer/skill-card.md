## Description: <br>
Use RenameRegex (RR.exe) as a generic Windows CLI bulk renamer from OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NEXTAltair](https://clawhub.ai/user/NEXTAltair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide preview-first regex bulk renaming with RenameRegex on Windows, including recursive file or directory selection and explicit approval before applying changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk rename operations can unintentionally affect many files or directories if the target folder or regex is too broad. <br>
Mitigation: Use a narrow target folder, run the pretend preview first, inspect the proposed changes carefully, and apply only after explicit user approval. <br>
Risk: The packaged artifact references RR.exe and a wrapper/logging workflow, but the wrapper script is not included in this package. <br>
Mitigation: Verify RR.exe comes from a trusted source and do not rely on wrapper-provided logging or safeguards unless that wrapper is supplied separately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NEXTAltair/rr-renamer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline PowerShell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview-first workflow with explicit user approval before apply.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
