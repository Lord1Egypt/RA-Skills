## Description: <br>
Connect WHOOP wearable to OpenClaw to fetch and store recovery, sleep, HRV, strain, and workout data locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Belugary](https://clawhub.ai/user/Belugary) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve their own WHOOP recovery, sleep, strain, workout, profile, and body measurement data after OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive WHOOP health, profile, body measurement, OAuth credential, and token data. <br>
Mitigation: Install only when ongoing read access is acceptable, keep WHOOP_CLIENT_SECRET and token files private, and store local data under user-controlled permissions. <br>
Risk: Auto-sync, cron, or systemd setup can keep reading WHOOP data in the background. <br>
Mitigation: Enable persistent sync only when needed, monitor the process, and stop or disable it when ongoing access is no longer required. <br>
Risk: Optional webhook mode exposes a public endpoint that the security review identifies as unauthenticated. <br>
Mitigation: Avoid webhook mode unless the endpoint can be secured, monitored, and operated behind a properly configured HTTPS reverse proxy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Belugary/whoop-connect) <br>
- [Project Homepage](https://github.com/Belugary/whoop-connect) <br>
- [WHOOP Connect Setup Guide](references/setup-guide.md) <br>
- [WHOOP API v2 Reference](references/api-reference.md) <br>
- [WHOOP Webhook Events](references/webhook-events.md) <br>
- [WHOOP Developer Portal](https://developer.whoop.com) <br>
- [WHOOP API Documentation](https://developer.whoop.com/api) <br>
- [WHOOP Data Concepts](https://developer.whoop.com/docs/developing/user-data/recovery) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON from WHOOP data commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration, OAuth token, and SQLite data files under ~/.whoop during use.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
