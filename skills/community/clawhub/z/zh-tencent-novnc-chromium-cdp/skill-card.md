## Description: <br>
Deploys or connects to a visible browser session using Linux noVNC with Chromium and CDP, or Windows Edge/Chrome CDP, so an agent and user can share browser control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kangleizhui](https://clawhub.ai/user/kangleizhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up a shared visible browser for web automation tasks where an agent may need the user to handle login, QR-code, CAPTCHA, slider, or other verification steps. It is most useful for workflows that need a real browser view instead of pure API calls or a hidden headless browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill deploys a remotely controllable browser and exposes a noVNC access surface. <br>
Mitigation: Install it only on a machine dedicated to remote browser automation and restrict noVNC access by IP, VPN, or SSH tunnel where possible. <br>
Risk: The security evidence notes that the skill asks for SSH passwords during setup fallback flows. <br>
Mitigation: Do not share SSH passwords in chat; prefer running privileged setup yourself, using passwordless sudo, or using a temporary key that can be revoked after installation. <br>
Risk: A public CDP debugging port could allow browser takeover. <br>
Mitigation: Keep CDP bound to localhost, do not expose port 9223 publicly, and restrict any exceptional remote debugging access to trusted networks only. <br>
Risk: Persistent services and browser sessions may retain credentials or browsing state after use. <br>
Mitigation: Remove the systemd services, rotate temporary credentials, and clear or discard the dedicated browser profile when the automation task is finished. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kangleizhui/skills/zh-tencent-novnc-chromium-cdp) <br>
- [Publisher profile](https://clawhub.ai/user/kangleizhui) <br>
- [noVNC project](https://github.com/novnc/noVNC) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell, PowerShell, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment steps, browser-control snippets, environment checks, status checks, and user-facing completion guidance.] <br>

## Skill Version(s): <br>
1.0.45 (source: server release evidence, created 2026-06-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
