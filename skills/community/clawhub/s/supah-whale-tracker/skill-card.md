## Description: <br>
Real-time whale activity monitoring and smart money following for Base blockchain that tracks large transactions, wallet accumulation patterns, and smart money flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supah-based](https://clawhub.ai/user/supah-based) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query recent whale transfers, wallet activity, token flows, historical whale behavior, and smart-money signals on Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic x402 USDC micropayments may be triggered by API calls with unclear pricing or action boundaries. <br>
Mitigation: Use a wallet with a strict spend cap, require confirmation before paid or alert-style actions, and confirm pricing with the publisher before ongoing use. <br>
Risk: The skill sends requests to a configurable SUPAH API endpoint for on-chain whale-tracking data. <br>
Mitigation: Verify SUPAH_API_BASE before use and review returned data before making trading, financial, or alerting decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/supah-based/supah-whale-tracker) <br>
- [SUPAH website](https://supah.ai) <br>
- [SUPAH API](https://api.supah.ai) <br>
- [x402 documentation](https://www.x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Guidance] <br>
**Output Format:** [Console text and JSON responses from SUPAH API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, curl, outbound access to api.supah.ai, and SUPAH_API_BASE when overriding the default endpoint.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
