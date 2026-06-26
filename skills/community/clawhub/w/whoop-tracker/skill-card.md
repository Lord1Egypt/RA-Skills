## Description: <br>
Access WHOOP fitness tracker data through the WHOOP API for recovery, sleep, workout, daily strain, body measurement, and profile metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iJaack](https://clawhub.ai/user/iJaack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve user-authorized WHOOP health and fitness data, summarize recent recovery, sleep, workout, strain, profile, and body-measurement metrics, and support personal trend tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive WHOOP health, workout, sleep, body-measurement, name, and email data to the agent and to logs or transcripts. <br>
Mitigation: Use the skill only with data you are comfortable sharing with the agent, avoid unnecessary --json output in shared logs or transcripts, and review outputs before forwarding them. <br>
Risk: Local OAuth credentials and tokens are stored under ~/.whoop and could grant continued access if copied from the machine. <br>
Mitigation: Keep ~/.whoop/credentials.json and ~/.whoop/token.json private, use restrictive file permissions, avoid shared machines, and revoke the WHOOP OAuth grant when access is no longer needed. <br>


## Reference(s): <br>
- [WHOOP OAuth 2.0 Setup](artifact/references/oauth.md) <br>
- [WHOOP API Reference](artifact/references/api-reference.md) <br>
- [WHOOP Developer Portal](https://developer.whoop.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus terminal text or JSON from the helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may contain sensitive WHOOP profile, health, sleep, workout, and body-measurement data when the user runs the scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
