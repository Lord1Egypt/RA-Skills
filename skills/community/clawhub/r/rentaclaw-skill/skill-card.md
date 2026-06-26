## Description: <br>
List and manage an AI agent on the Rentaclaw marketplace, a decentralized marketplace for AI agent rentals on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buildwithrekt](https://clawhub.ai/user/buildwithrekt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use Rentaclaw to list OpenClaw agents for rental, manage listing details and availability, and view earnings or rental statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, pause, or resume Rentaclaw marketplace listings. <br>
Mitigation: Review listing names, descriptions, categories, prices, agent IDs, and pause or resume actions before approving changes. <br>
Risk: The skill requires a Rentaclaw API key. <br>
Mitigation: Store RENTACLAW_API_KEY in a credential store and avoid exposing it in prompts, logs, or shared outputs. <br>


## Reference(s): <br>
- [ClawHub Rentaclaw Skill](https://clawhub.ai/buildwithrekt/rentaclaw-skill) <br>
- [Rentaclaw](https://www.rentaclaw.io) <br>
- [Rentaclaw API Keys](https://www.rentaclaw.io/dashboard/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration guidance] <br>
**Output Format:** [Markdown or plain text responses with Rentaclaw API actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RENTACLAW_API_KEY and user-provided listing, pricing, and agent identifiers.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence; skill metadata lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
