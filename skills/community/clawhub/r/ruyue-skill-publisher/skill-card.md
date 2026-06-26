## Description: <br>
OpenClaw Skill Publisher guides agents through creating, generalizing, publishing, updating, and distributing OpenClaw skills on ClawHub and Gitee. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RuyueChina](https://clawhub.ai/user/RuyueChina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to prepare OpenClaw skill packages, publish versions to ClawHub, mirror them to Gitee, and provide installation guidance for users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing commands can expose unintended files or private material. <br>
Mitigation: Verify the destination account, repository, visibility, slug, version, and exact files before publishing. <br>
Risk: Token-based publishing can mishandle account credentials. <br>
Mitigation: Use limited-scope tokens through a secure secret store or prompt, avoid inline tokens in commands, and rotate or revoke tokens after publishing. <br>
Risk: Tool installation and publishing steps may run in environments without enough review. <br>
Mitigation: Scan skill contents for secrets or private material and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RuyueChina/ruyue-skill-publisher) <br>
- [RuyueChina publisher profile](https://clawhub.ai/user/RuyueChina) <br>
- [Gitee skill repository](https://gitee.com/ruyueteam/openclaw-skills) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes publishing checklists, command examples, release-version guidance, and installation instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
