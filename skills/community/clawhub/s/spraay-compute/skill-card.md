## Description: <br>
Rent GPU compute, run AI model inference, and buy prepaid compute-futures credits paid in USDC over x402 without API keys or accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plagtech](https://clawhub.ai/user/plagtech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to estimate costs, rent GPU or model-inference compute, generate media or embeddings, and manage prepaid compute-futures balances through the Spraay x402 gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent with a funded wallet to spend USDC on paid compute or prepaid compute-futures deposits. <br>
Mitigation: Require explicit user approval and spending caps before paid requests, deposits, or refunds. <br>
Risk: Broad trigger guidance may route generic inference or media-generation requests to paid endpoints. <br>
Mitigation: Prefer free estimate and model-list endpoints first, and avoid configuring this skill as the default handler for generic AI requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/plagtech/spraay-compute) <br>
- [Publisher profile](https://clawhub.ai/user/plagtech) <br>
- [Spraay gateway](https://gateway.spraay.app) <br>
- [x402 discovery catalog](https://gateway.spraay.app/.well-known/x402.json) <br>
- [Endpoint reference](references/endpoints.md) <br>
- [Quickstart examples](examples/quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with endpoint descriptions and inline code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead an agent to make paid x402 requests using a funded USDC wallet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
