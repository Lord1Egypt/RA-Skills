## Description: <br>
Automatically upgrade Telnyx account from freemium to professional tier. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teamtelnyx](https://clawhub.ai/user/teamtelnyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agents use this skill when a Telnyx freemium account blocks SMS, voice, number purchasing, porting, or other professional-tier features and the user wants identity-based upgrade assistance through GitHub or LinkedIn. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive GitHub-token and Telnyx account-upgrade actions. <br>
Mitigation: Require explicit user confirmation before submitting an upgrade request, and avoid logging raw GitHub tokens. <br>
Risk: The verification flow sends GitHub or LinkedIn identity data to the Telnyx upgrade service. <br>
Mitigation: Use the skill only when the user explicitly wants a Telnyx account upgrade and trusts the verification endpoint with that identity data. <br>
Risk: The skill can refresh GitHub scopes, create polling jobs, and send cross-channel verification messages. <br>
Mitigation: Require confirmation before scope refresh, cron creation, or cross-channel messaging, and remove polling jobs after a final decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teamtelnyx/telnyx-freemium-upgrade) <br>
- [Publisher profile](https://clawhub.ai/user/teamtelnyx) <br>
- [GitHub CLI](https://cli.github.com) <br>
- [GitHub device authorization](https://github.com/login/device) <br>
- [Telnyx API endpoint](https://api.telnyx.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Telnyx API key plus GitHub CLI authentication or LinkedIn OAuth consent; may write upgrade status cache under ~/.telnyx/upgrade.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
