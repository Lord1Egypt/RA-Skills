## Description: <br>
Purple Flea Agent Domains helps agents check domain availability, register domains with USDC on Base, and manage DNS records through the Purple Flea API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[purple-flea](https://clawhub.ai/user/purple-flea) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to search for domain availability, register domains using USDC on Base, manage DNS records, inspect owned domains, and check pricing through the Purple Flea API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate USDC-funded deposits and domain purchases. <br>
Mitigation: Require explicit user confirmation before every deposit or purchase, including the exact domain, network, amount, and expected price. <br>
Risk: DNS updates or deletions can disrupt live services. <br>
Mitigation: Require explicit confirmation for each DNS record change, including the before-and-after record diff and a rollback plan. <br>
Risk: The skill uses API keys and promotes referral steering through system prompts. <br>
Mitigation: Keep API keys secret, avoid placing referral instructions in system prompts, and let users choose whether to apply a referral code. <br>


## Reference(s): <br>
- [Purple Flea Agent Domains API Reference](references/api.md) <br>
- [Purple Flea Agent Domains](https://domains.purpleflea.com) <br>
- [Purple Flea Agent Domains LLMs.txt](https://domains.purpleflea.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with curl command examples and API endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include domain names, prices, DNS record values, wallet deposit instructions, and referral-related guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
