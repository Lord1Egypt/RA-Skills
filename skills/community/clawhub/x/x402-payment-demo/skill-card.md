## Description: <br>
Demo of x402 payment protocol by fetching a protected image. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[Hades-Ye](https://clawhub.ai/user/Hades-Ye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external evaluators use this skill to exercise an x402 payment flow on TRON by requesting a protected image, handling the payment requirement, and displaying the retrieved image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically trigger blockchain payment or permit-signing flows without clear spend limits or confirmation. <br>
Mitigation: Use the default testnet unless deliberately choosing otherwise, and require the agent to show the exact network, recipient, asset, amount, and signature request before any payment or permit signing. <br>
Risk: Using a mainnet endpoint may create real payment exposure. <br>
Mitigation: Keep Nile as the default network for routine testing and use mainnet only after explicit review and approval of the transaction details. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/Hades-Ye/x402-payment-demo) <br>
- [TRON Nile protected demo endpoint](https://x402-tron-demo.aibank.io/protected-nile) <br>
- [TRON Shasta protected demo endpoint](https://x402-tron-demo.aibank.io/protected-shasta) <br>
- [TRON Mainnet protected demo endpoint](https://x402-tron-demo.aibank.io/protected-mainnet) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, files] <br>
**Output Format:** [Agent workflow guidance that may retrieve and display an image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a network argument with Nile as the default; retrieved image files are temporary and should be deleted after display.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
