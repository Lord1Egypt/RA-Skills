## Description: <br>
Check WHOOP recovery/sleep/strain each morning and send suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Borahm](https://clawhub.ai/user/Borahm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to retrieve recent WHOOP recovery, sleep, and strain data and produce a short morning wellness report with day-level suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests persistent WHOOP OAuth access to health and wellness data. <br>
Mitigation: Install only after confirming the requested scopes and keep WHOOP credentials, refresh tokens, and cached tokens in private, access-controlled storage. <br>
Risk: The reviewed package references `whoop-auth` and `whoop-morning` executables that are not included in the artifact. <br>
Mitigation: Verify those executables from a trusted source before authorizing WHOOP access or scheduling the skill. <br>
Risk: Scheduled morning reports may expose personal health data if routed to a shared destination. <br>
Mitigation: Send automated reports only to private destinations and review cron or Gateway routing before enabling automation. <br>
Risk: WHOOP refresh-token rotation can fail or be disrupted by concurrent refreshes. <br>
Mitigation: Avoid parallel token refresh jobs and re-run authorization if WHOOP returns token refresh errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Borahm/whoop-morning) <br>
- [WHOOP OAuth authorization endpoint](https://api.prod.whoop.com/oauth/oauth2/auth) <br>
- [WHOOP OAuth token endpoint](https://api.prod.whoop.com/oauth/oauth2/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown or plain text morning report with setup and execution commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WHOOP OAuth environment variables and may use a local token cache for refreshed access tokens.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
