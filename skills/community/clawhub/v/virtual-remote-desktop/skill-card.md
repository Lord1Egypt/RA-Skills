## Description: <br>
KasmVNC-based virtual desktop for headless Linux with AI-first automation and human handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangxin15435](https://clawhub.ai/user/zhangxin15435) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation operators use this skill to run a headless Linux desktop with KasmVNC, allow short manual intervention for captcha, risk-control, MFA, or login approval, and then resume AI-controlled browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote desktop sessions can expose sensitive browser state, screenshots, and temporary VNC credentials. <br>
Mitigation: Use the default 127.0.0.1 bind with SSH tunneling, avoid public binding unless tightly firewalled and time-limited, and clean ~/.openclaw/vrd-data after sensitive sessions. <br>
Risk: Installation and startup can make persistent system changes, including sudo package installation and an ssl-cert group change. <br>
Mitigation: Install only on systems where these changes are acceptable and review the package installation and group membership impact before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangxin15435/virtual-remote-desktop) <br>
- [KasmVNC release API used by installer](https://api.github.com/repos/kasmtech/KasmVNC/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and environment variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Action scripts can return base64 screenshots, cursor coordinates, command status text, and health/status output.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence; artifact metadata reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
