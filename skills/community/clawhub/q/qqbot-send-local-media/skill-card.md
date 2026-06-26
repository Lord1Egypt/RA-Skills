## Description: <br>
QQBot Send Local Media stages disposable copies of local files so agents can send files, images, audio, video, or URLs through QQBot while preserving the original file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjuncher](https://clawhub.ai/user/zjuncher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators and end users use this skill when a local file path, attachment, or media URL should be sent through QQBot instead of merely returned as text. It is suited for sending desktop, downloads, or absolute-path media while keeping the original file unchanged. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent could send the wrong local file or QQ destination if it stages an unintended path. <br>
Mitigation: Verify the source path and QQ destination before sending, especially for sensitive documents. <br>
Risk: Changing the bundled staging script could weaken cleanup behavior or cause unsafe file handling. <br>
Mitigation: Keep the bundled staging script unchanged and clean up only the staged path returned by the script. <br>


## Reference(s): <br>
- [QQBot Send Local Media on ClawHub](https://clawhub.ai/zjuncher/qqbot-send-local-media) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and <qqmedia> tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stages a temporary local copy, sends the staged path or URL, then cleans up only the staged copy returned by the staging script.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
