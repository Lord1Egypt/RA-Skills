## Description: <br>
Publishes a local agent skill folder to ClawHub by guiding browser upload, license selection, and release steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infiniteask](https://clawhub.ai/user/infiniteask) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Skill authors and developers use this skill to publish a local skill folder to ClawHub after confirming the folder contents, logged-in account, slug, display name, and license selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish a local folder publicly to ClawHub and accept the MIT-0 license choice. <br>
Mitigation: Require explicit final approval after confirming folder contents, logged-in account, slug, display name, and license selection. <br>
Risk: The workflow may delete SKILL.md.bak and overwrite the clipboard while controlling a Windows file picker. <br>
Mitigation: Review the target folder before execution and warn users before local backup deletion or clipboard use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/infiniteask/publish-agent-skill-infinite) <br>
- [ClawHub publish skill page](https://clawhub.ai/publish-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with PowerShell and Python command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local skill folder path and interactive confirmation for the system file picker upload.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
