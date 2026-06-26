## Description: <br>
用极空间的迅雷下载资源 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengzhxyz](https://clawhub.ai/user/pengzhxyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to guide an agent through creating a Xunlei magnet download task in a logged-in ZSpace browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a logged-in ZSpace browser session and can create a Xunlei download task. <br>
Mitigation: Keep the browser on the intended ZSpace page, confirm the active account, and review the new task after execution. <br>
Risk: Untrusted magnet links may create unwanted or unsafe download tasks. <br>
Mitigation: Use magnet links from trusted sources and verify the link before running the browser automation commands. <br>
Risk: The browser automation depends on visible ZSpace and Xunlei page labels, so page changes may cause the commands to fail or select the wrong control. <br>
Mitigation: Review each browser snapshot and stop if the selected controls are not the intended Xunlei task controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengzhxyz/zspace-xunlei) <br>
- [ZSpace web portal](https://www.zconnect.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw and a browser session already on the intended ZSpace page.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
