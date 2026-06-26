## Description: <br>
Query an Unraid server via GraphQL for system, array, and Docker status in read-only mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yoshiofthewire](https://clawhub.ai/user/Yoshiofthewire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and developers use this skill to let an agent check Unraid system health, array and parity status, Docker status, API connectivity, and recurring monitoring results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries a configured Unraid API using an API key. <br>
Mitigation: Use a least-privilege API key where possible, keep credentials in environment variables, and do not commit secrets. <br>
Risk: The skill stores local monitoring snapshots, alert state, and logs. <br>
Mitigation: Protect .state or UNRAID_STATE_DIR with appropriate local filesystem permissions. <br>
Risk: Cron setup and certificate-trust commands can affect the host environment. <br>
Mitigation: Review crontab changes and any sudo certificate-trust commands before running them. <br>
Risk: A wrong or untrusted UNRAID_BASE_URL can send requests to the wrong endpoint. <br>
Mitigation: Verify UNRAID_BASE_URL before use and avoid session cookies unless they are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Yoshiofthewire/unraid-claw) <br>
- [Yoshiofthewire publisher profile](https://clawhub.ai/user/Yoshiofthewire) <br>
- [Unraid API documentation](https://docs.unraid.net/API/) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/creating-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Operator-facing Markdown or plain text summaries, with optional JSON report output from bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq; stores snapshots, alert state, and logs under .state or UNRAID_STATE_DIR.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
