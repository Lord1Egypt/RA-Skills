## Description: <br>
Manages a local V2Ray proxy by starting or stopping V2Ray and configuring system proxy settings based on network availability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Felixqian4160](https://clawhub.ai/user/Felixqian4160) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and agent users can use this skill to enable, disable, test, or automatically manage a local V2Ray proxy when OpenClaw or shell commands need external network access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes risky command execution through a wrapper that can run supplied shell commands. <br>
Mitigation: Review and replace or remove the eval-based wrapper before use, and run only commands from trusted sources. <br>
Risk: The skill can make persistent shell-profile changes and alter system proxy state. <br>
Mitigation: Confirm whether it edits ~/.bashrc before use, and verify that proxy changes have a clear rollback path. <br>
Risk: Proxy changes may disrupt local network behavior if V2Ray fails to start, stop, or clean up correctly. <br>
Mitigation: Test the on, off, status, and disable-sys flows in a controlled environment before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Felixqian4160/v2ray-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local V2Ray or Xray installation and a configured proxy path before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
