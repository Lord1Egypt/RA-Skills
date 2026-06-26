## Description: <br>
Downloads Telegram resources with tdl and sends Server Chan WeChat notifications that include file names, sizes, timing, and success or failure details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tang2606](https://clawhub.ai/user/tang2606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to download specific Telegram channel messages through tdl and receive WeChat notifications when long-running downloads complete or fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled Server Chan SendKey can route private Telegram source links, filenames, sizes, paths, timestamps, and errors to an account the installer may not control. <br>
Mitigation: Replace the SendKey before use and rotate or revoke the exposed key if it belongs to you. <br>
Risk: The skill downloads files from Telegram into a local directory and reports file metadata externally. <br>
Mitigation: Use a dedicated download directory and run it only for Telegram resources and notification recipients you trust. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tang2606/tdl-download-notify) <br>
- [TDL Official Documentation](https://github.com/iyear/tdl) <br>
- [Server Chan](https://sct.ftqq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, json, guidance] <br>
**Output Format:** [Markdown notification content, console text, and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tdl login, Python requests, network access to Telegram and Server Chan, and a configured Server Chan SendKey.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
