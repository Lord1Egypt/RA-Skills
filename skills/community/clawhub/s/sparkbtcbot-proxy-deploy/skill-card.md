## Description: <br>
Deploy a serverless Spark Bitcoin L2 proxy on Vercel with spending limits, auth, and Redis logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echennells](https://clawhub.ai/user/echennells) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to deploy and manage a Vercel-hosted Spark Bitcoin L2 proxy with Upstash Redis, authenticated REST endpoints, scoped tokens, and spending limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment handles Bitcoin wallet and provider secrets, including a Spark mnemonic, Upstash credentials, and API tokens. <br>
Mitigation: Use a fresh low-balance wallet, keep admin tokens private, avoid pasting real mnemonics or provider tokens into chat, and prefer provider dashboards or local secret tooling for secret entry. <br>
Risk: The skill deploys unpinned remote code from an external repository. <br>
Mitigation: Pin and review the external repository before deployment. <br>
Risk: The deployed proxy can spend Bitcoin through admin-only payment, transfer, and L402 routes. <br>
Mitigation: Set low per-transaction and daily spending caps, use scoped invoice-only tokens for agents, and reserve the admin token for trusted operators. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/echennells/sparkbtcbot-proxy-deploy) <br>
- [sparkbtcbot-proxy Repository](https://github.com/echennells/sparkbtcbot-proxy.git) <br>
- [Lightning L402 Documentation](https://docs.lightning.engineering/the-lightning-network/l402) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash, curl, JSON, and environment-variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment and operations instructions; it does not directly execute the deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
