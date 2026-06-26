## Description: <br>
Fetches and analyzes Whoop recovery, strain, sleep, HRV, and workout data via the Whoop API for daily summaries, trend tracking, and health and training insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vraj1512](https://clawhub.ai/user/vraj1512) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to connect a Whoop account, retrieve personal recovery, sleep, strain, HRV, and workout metrics, and generate daily or weekly summaries and recommendations from those metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Whoop health data and OAuth credentials, including ongoing read access through saved access and refresh tokens. <br>
Mitigation: Install only if you are comfortable granting Whoop health-data access, protect ~/.whoop_token and ~/.whoop_refresh_token, and revoke the Whoop app if tokens or authorization codes may have been exposed. <br>
Risk: Authorization codes or tokens can be exposed if copied into chat tools or other shared channels. <br>
Mitigation: Prefer the local OAuth exchange flow and do not send authorization codes or tokens through Telegram, WhatsApp, or other chats. <br>


## Reference(s): <br>
- [Whoop API Reference](references/whoop-api.md) <br>
- [OAuth Pages Deployment Guide](references/oauth-pages/README.md) <br>
- [Whoop Developer Docs](https://developer.whoop.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/vraj1512/whoop-openclaw-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local Whoop OAuth token files during setup and API use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
