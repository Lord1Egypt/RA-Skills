## Description: <br>
MoltGuard helps OpenClaw agents install and manage a security guard that detects prompt injection, data exfiltration, command injection, and related agent risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomas-security](https://clawhub.ai/user/thomas-security) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add MoltGuard protection to OpenClaw agents, check protection status, configure account or enterprise enrollment, and manage updates or removal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys or local bridge credentials may expose sensitive access if pasted into shared chats, screenshots, or logs. <br>
Mitigation: Treat API keys as secrets, prefer environment or config-file setup, and review local configuration files when rotating or removing access. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/thomas-security/skill-antivirus) <br>
- [Publisher Profile](https://clawhub.ai/user/thomas-security) <br>
- [MoltGuard Homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install, test, status, account-linking, dashboard, enterprise enrollment, update, and uninstall guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports MoltGuard 6.8.21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
