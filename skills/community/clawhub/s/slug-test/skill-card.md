## Description: <br>
Streams Apple Health data from an iPhone or Apple Watch to a self-hosted webhook server so an OpenClaw agent can analyze recovery, trends, and anomalies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crxiaobailiu-gif](https://clawhub.ai/user/crxiaobailiu-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and health-data users can connect iPhone or Apple Watch HealthKit records to an OpenClaw agent for local analysis, recovery scoring, anomaly checks, and trend questions. The skill is best suited for users who are prepared to self-host and protect a webhook that receives sensitive health records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Apple Health records and can expose them through a public webhook. <br>
Mitigation: Prefer private networking over public tunnels, avoid unnecessary public exposure, and restrict access before pairing or syncing health data. <br>
Risk: Weak or missing admin protection could allow unauthorized pairing, user management, or access to server endpoints. <br>
Mitigation: Set a strong ADMIN_TOKEN, protect pairing links and API tokens, and treat generated user tokens as secrets. <br>
Risk: Synced health records persist locally and may be accessible to agents or local processes. <br>
Mitigation: Store data in an appropriate protected directory, review local file permissions, and limit agent access to only the needed health-data files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/crxiaobailiu-gif/slug-test) <br>
- [HealthClaw TestFlight beta](https://testflight.apple.com/join/SXDjT6vC) <br>
- [Tailscale Funnel](https://tailscale.com/download) <br>
- [Cloudflare Tunnel downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, markdown] <br>
**Output Format:** [Markdown guidance with shell commands, HTTP API examples, and JSON data examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and integration guidance for a webhook-based Apple Health data bridge; resulting health records persist locally as JSON Lines.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
