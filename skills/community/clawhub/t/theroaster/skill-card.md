## Description: <br>
TheRoaster helps agents generate short, safety-filtered humorous roasts for social bot replies, with free limited usage and optional paid on-chain entitlement for higher quotas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bazinshine](https://clawhub.ai/user/bazinshine) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and bot operators use TheRoaster to turn social posts or replies into short banter-style roast comments. The skill is also used to inspect plans, check entitlement, and prepare paid quota purchase flows when a human explicitly requests wallet-based credits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid quota flows involve wallet signing and on-chain USDC transactions on Base. <br>
Mitigation: Before any paid action, verify the Base chain, contract address, USDC amount, tier, duration, and transaction purpose, then require explicit human approval before signing or sending anything. <br>
Risk: Messages sent for roasting are shared with a third-party API service. <br>
Mitigation: Avoid submitting confidential messages or sensitive personal data for roasting. <br>
Risk: Issued API keys can grant paid quota and are shown only once. <br>
Mitigation: Store API keys securely, avoid committing keys or environment files, and rotate or reclaim keys when entitlement or access changes. <br>
Risk: Roast output may become harmful or harassing if used outside the stated banter context. <br>
Mitigation: Apply the documented safety rules: skip tragedy, health, self-harm, protected-class, or non-consensual targeting contexts, and keep outputs short and clearly humorous. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bazinshine/theroaster) <br>
- [TheRoaster API Base URL](https://theroaster.app) <br>
- [Health Endpoint](https://theroaster.app/health) <br>
- [Contract Metadata Endpoint](https://theroaster.app/api/v1/contract) <br>
- [Plans Endpoint](https://theroaster.app/api/v1/plans) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON, Text] <br>
**Output Format:** [Markdown guidance with HTTP examples; API responses are JSON and generated roasts are plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Roasts should be short, humorous, and avoid protected-class attacks, violence, self-harm, and harassment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
