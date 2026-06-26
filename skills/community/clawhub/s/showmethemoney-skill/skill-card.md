## Description: <br>
Paid demo skill for StablePay on Solana using USDC. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[bubblevan](https://clawhub.ai/user/bubblevan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to access a paid ShowMeTheMoney demo capability through StablePay on Solana after backend purchase verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts an external backend and may trigger a StablePay USDC payment flow. <br>
Mitigation: Before use, confirm the backend interaction is expected and approve payment only when the amount, network, and recipient flow match the user's intent. <br>
Risk: The paid capability could be used before purchase verification completes. <br>
Mitigation: Do not continue to the paid capability or claim access was purchased unless the backend confirms payment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bubblevan/showmethemoney-skill) <br>
- [Publisher profile](https://clawhub.ai/user/bubblevan) <br>
- [StablePay verification endpoint](https://api.stablepay.co/verify?skill=did:solana:REPLACE_WITH_YOUR_SKILL_DID&agent={AGENT_DID}) <br>
- [ShowMeTheMoney execute endpoint](https://wenfu.cc/showmethemoney) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls] <br>
**Output Format:** [Markdown or plain text response returned from the backend] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a StablePay 0.1 USDC payment on Solana Mainnet before the backend returns the paid result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
