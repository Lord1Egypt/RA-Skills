## Description: <br>
Set up reliable browser automation using Chrome DevTools Protocol (CDP) instead of the flaky browser extension relay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarvis563](https://clawhub.ai/user/jarvis563) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to configure OpenClaw browser automation through a local Chrome DevTools Protocol connection, especially when the browser extension relay is unstable. It supports setup, usage, and troubleshooting for headed or headless browser workflows such as scraping, form filling, and social media posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables a persistent Chrome debugging profile that can control logged-in browser sessions. <br>
Mitigation: Use a dedicated Chrome profile only for intended automation accounts and avoid sensitive personal, financial, admin, or production sessions. <br>
Risk: The setup can create an auto-start browser debugging service that remains available after setup. <br>
Mitigation: Disable or remove the LaunchAgent or service when browser automation is not actively needed. <br>
Risk: Browser automation may perform high-impact actions through authenticated sessions. <br>
Mitigation: Require explicit user confirmation before posts, purchases, deletions, account changes, or other irreversible actions. <br>


## Reference(s): <br>
- [Manual Setup](references/manual-setup.md) <br>
- [Stable Browser on ClawHub](https://clawhub.ai/jarvis563/stable-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, JSON, and configuration code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local browser setup and troubleshooting guidance for OpenClaw CDP use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
