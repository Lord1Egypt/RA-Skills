## Description: <br>
Print the full path of the current working directory. Use for identifying your location in the filesystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to confirm the active filesystem location before running navigation-sensitive commands or scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The emitted working-directory path can expose local usernames, project names, or private folder names. <br>
Mitigation: Review or redact the path before sharing it outside the trusted execution context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/pwd-tool) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text path with optional Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reveal local usernames, project names, or private folder names contained in the current working directory path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
