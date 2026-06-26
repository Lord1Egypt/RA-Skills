## Description: <br>
Use when an agent needs to store, retrieve, list, inspect, or delete files through Vaultline, or when it needs to choose between open and private storage tiers, construct the required wallet-auth headers for private objects, or follow the x402 pay-and-retry flow for uploads and downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[builtbyecho](https://clawhub.ai/user/builtbyecho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Vaultline storage operations, choose between open and private tiers, construct wallet-authenticated requests, and handle x402 payment retries. It is also used to explain that encrypted storage is not live yet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through uploads, deletes, and paid x402 retry flows. <br>
Mitigation: Require confirmation before uploads, deletes, or paid retries, and use a dedicated low-balance wallet for payment-capable operations. <br>
Risk: Private storage depends on wallet-auth headers and does not mean encrypted storage is live. <br>
Mitigation: Provide wallet-auth headers only for intended private operations and avoid sensitive plaintext unless the user accepts the current privacy model. <br>


## Reference(s): <br>
- [Vaultline homepage](https://github.com/BuiltByEcho/vaultline) <br>
- [Vaultline API Examples](references/api-examples.md) <br>
- [Pricing and Tier Selection](references/pricing-and-tier-selection.md) <br>
- [Vaultline ClawHub listing](https://clawhub.ai/builtbyecho/vaultline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP examples, header names, and concise implementation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference wallet-auth headers, Vaultline paths, storage tiers, and x402 pay-and-retry steps.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
