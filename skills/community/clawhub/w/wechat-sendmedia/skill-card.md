## Description: <br>
Helps an agent send local images, screenshots, and files to a WeChat conversation through OpenClaw's Weixin channel using plain-text MEDIA:file:// directives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[torry21th](https://clawhub.ai/user/torry21th) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators of OpenClaw Weixin agents use this skill when they need an agent to send a local image, screenshot, downloaded file, or other media to the current WeChat conversation or an explicitly named recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles local file uploads and external delivery through WeChat. <br>
Mitigation: Confirm the exact local file path and recipient before use; default to the current conversation unless the user explicitly names another recipient. <br>
Risk: Failure output and diagnostics may expose local paths or operational debug details. <br>
Mitigation: Avoid sharing failure output publicly and redact local paths, upload details, and response bodies before disclosure. <br>
Risk: Using an unsupported JSON media envelope may send literal text instead of the intended file. <br>
Mitigation: Use the documented plain-text MEDIA:file:// directive on its own line for normal sends. <br>


## Reference(s): <br>
- [OpenClaw Weixin notes](references/openclaw-weixin-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text confirmation or failure diagnostics, with JSON emitted by helper scripts during validation and debugging] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Success output includes a MEDIA:file:// directive on its own line and may include local file paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
