## Description: <br>
X2C Distribution and Wallet API - publish video to X2C platform, manage assets (balance, claim X2C, swap to USDC, withdraw, transactions). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to publish video projects to X2C, check review status, add episodes, list projects, and manage X2C wallet balances, claims, swaps, withdrawals, and transaction history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes commands that can claim X2C, swap X2C to USDC, and withdraw USDC. <br>
Mitigation: Require manual confirmation of each wallet-changing action, including amount, destination address, network, and expected fee, before execution. <br>
Risk: The skill depends on an X2C API key that can authorize publishing and wallet operations. <br>
Mitigation: Use the least-privileged X2C API key available and avoid sharing credentials outside the intended user context. <br>
Risk: Publishing steps can create duplicate or unintended X2C projects if run without checking state. <br>
Mitigation: Check existing project status before publishing and follow the documented workflow steps in order. <br>


## Reference(s): <br>
- [X2c Publish on ClawHub](https://clawhub.ai/patches429/x2c-publish) <br>
- [Publisher profile: patches429](https://clawhub.ai/user/patches429) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses X2C_API_KEY or a user-bound credentials JSON file and may produce wallet-changing API requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
