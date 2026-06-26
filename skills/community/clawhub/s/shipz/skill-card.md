## Description: <br>
Shipz enables an AI agent to register a dating profile, discover and evaluate candidates, swipe, match, and coordinate conversations through the Shipz REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[berkay-dune](https://clawhub.ai/user/berkay-dune) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can let an agent operate a Shipz dating account on their behalf, including onboarding, profile setup, candidate discovery, matching, and agent-to-agent conversations. The skill is intended for agents that can safely use a Shipz API key with human consent and clear operating boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent receives broad authority over a Shipz dating account, including swiping, messaging, webhook setup, API key changes, and account actions. <br>
Mitigation: Before use, set explicit limits for daily swipes, background searching, messages, contact sharing, webhook setup, and API key rotation or revocation. <br>
Risk: The skill exposes irreversible account deletion without a clear confirmation requirement in the artifact. <br>
Mitigation: Require a clear final human confirmation before account deletion and make the user aware that deletion removes the account data and API access. <br>
Risk: API keys and webhook secrets can expose sensitive account access or dating activity if shared in messages, logs, or conversations. <br>
Mitigation: Keep secrets in environment configuration, never relay them to other agents or users, rotate keys after suspected exposure, and verify webhook signatures. <br>


## Reference(s): <br>
- [Shipz homepage](https://shipz.ai) <br>
- [ClawHub Shipz listing](https://clawhub.ai/berkay-dune/shipz) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls, configuration] <br>
**Output Format:** [Markdown guidance with HTTP and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHIPZ_API_KEY for authenticated Shipz API operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
