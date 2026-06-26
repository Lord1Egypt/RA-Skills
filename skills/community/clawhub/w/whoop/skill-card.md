## Description: <br>
WHOOP morning check-in (recovery/sleep/strain) with suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Borahm](https://clawhub.ai/user/Borahm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users with WHOOP accounts use this skill to run a morning recovery, sleep, and strain check-in and receive short day-planning suggestions from the latest available WHOOP data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide long-lived WHOOP health-account credentials. <br>
Mitigation: Treat refresh tokens as passwords, use a private chat or environment, and know how to revoke the WHOOP app credentials. <br>
Risk: The security review reports that referenced runtime scripts are missing from the artifact. <br>
Mitigation: Do not enter WHOOP credentials or enable daily automation until the missing scripts are included and inspected. <br>
Risk: Daily automation may send health-related check-in output to an unintended destination. <br>
Mitigation: Confirm where scheduled messages are delivered before enabling cron or other automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Borahm/whoop) <br>
- [WHOOP OAuth authorization endpoint](https://api.prod.whoop.com/oauth/oauth2/auth) <br>
- [WHOOP OAuth token endpoint](https://api.prod.whoop.com/oauth/oauth2/token) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and short text suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WHOOP OAuth environment variables and a refresh token before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
