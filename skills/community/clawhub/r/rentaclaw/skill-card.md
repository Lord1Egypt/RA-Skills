## Description: <br>
List and manage an AI agent on the Rentaclaw marketplace, a decentralized marketplace for AI agent rentals on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buildwithrekt](https://clawhub.ai/user/buildwithrekt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to publish, price, monitor, update, pause, and resume their OpenClaw agent listings on Rentaclaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use account credentials to change live Rentaclaw listings, including prices and availability. <br>
Mitigation: Require explicit user confirmation before listing, updating, pausing, resuming, or changing prices for an agent. <br>
Risk: Webhook URL, hook token, and agent name are sent to Rentaclaw so rental requests can route to the OpenClaw gateway. <br>
Mitigation: Use a dedicated webhook URL and narrowly scoped token for Rentaclaw, and keep these environment variables out of unrelated sessions. <br>


## Reference(s): <br>
- [ClawHub Rentaclaw listing](https://clawhub.ai/buildwithrekt/rentaclaw) <br>
- [Rentaclaw homepage](https://www.rentaclaw.io) <br>
- [Rentaclaw documentation](https://docs.rentaclaw.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown status messages, setup guidance, statistics summaries, and marketplace URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Rentaclaw API credentials and OpenClaw gateway settings supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
