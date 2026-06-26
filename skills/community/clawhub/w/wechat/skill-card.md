## Description: <br>
Install OpenClaw's official WeChat plugin and complete account pairing via QR code scan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manifoldor](https://clawhub.ai/user/manifoldor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to install the WeChat plugin, open a local QR-code pairing page, and save the paired WeChat account for OpenClaw messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically installs remote code for the WeChat plugin. <br>
Mitigation: Install only if you trust the publisher and Tencent WeChat npm package, and prefer a pinned installer where possible. <br>
Risk: The pairing flow stores WeChat account credentials for later OpenClaw use. <br>
Mitigation: Review generated account files after pairing and keep token revocation or deletion steps available. <br>
Risk: The local pairing server and channel configuration can expose the connected account if left broader than intended. <br>
Mitigation: Run on a trusted machine and network, close the local server when pairing completes, and verify the OpenClaw channel allowlist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manifoldor/wechat) <br>
- [Publisher profile](https://clawhub.ai/user/manifoldor) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, files, guidance] <br>
**Output Format:** [Local QR-code web page, OpenClaw configuration updates, and JSON account files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install the Tencent WeChat OpenClaw plugin, poll WeChat pairing status, store a WeChat token under the user's OpenClaw state directory, and restart the OpenClaw gateway.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
