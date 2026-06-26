## Description: <br>
秦丝旺剪 - AI智能视频剪辑 integrates with the QinSilk Wangcut API so agents can create AI video editing tasks, check task status, and download completed videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HuangJT](https://clawhub.ai/user/HuangJT) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users working in Claude Code or OpenClaw use this skill to automate QinSilk Wangcut video creation from scripts, manage recent task queues, inspect task details, and download finished videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow may ask users to provide a Wangcut account password in chat and stores account credentials in a local config.ini file. <br>
Mitigation: Use a limited Wangcut account, avoid sensitive or reused passwords, and keep config.ini out of shared workspaces and version control. <br>
Risk: Credentials and video task content are sent to the configured Wangcut API base URL. <br>
Mitigation: Verify the API base URL before logging in and review the video content and account choice before running automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HuangJT/wangcut) <br>
- [Installation Guide](artifact/docs/INSTALL.md) <br>
- [QinSilk Wangcut](https://cloud.qinsilk.com) <br>
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Configuration instructions, Files] <br>
**Output Format:** [Markdown with Python code snippets, configuration examples, task identifiers, URLs, and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update config.ini and download generated video files to the configured download directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
