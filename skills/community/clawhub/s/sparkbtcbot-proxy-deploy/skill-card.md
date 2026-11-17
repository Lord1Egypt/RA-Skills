## Description:

Deploy a serverless Spark Bitcoin L2 proxy on Vercel with spending limits, auth, and Redis logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echennells](https://clawhub.ai/user/echennells)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to deploy and configure a Vercel-hosted Spark Bitcoin L2 proxy with Upstash Redis logging, bearer-token access control, and spend limits for agent wallet operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment flow involves wallet recovery words and cloud deployment secrets.

Mitigation: Enter mnemonics, Vercel tokens, Upstash keys, and bearer tokens directly in a local terminal or provider dashboard, not in chat.

Risk: The proxy can spend funds through Spark and Lightning operations.

Mitigation: Use a fresh low-value wallet, conservative per-transaction and daily spending caps, scoped tokens, and a documented token rotation process.

Risk: Mutable deployment tooling and upstream proxy changes can alter behavior after the skill is published.

Mitigation: Review the upstream proxy and deployment flow before installation, pin repository and CLI versions where practical, and restrict L402 payments with domain allowlists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/echennells/skills/sparkbtcbot-proxy-deploy)
- [sparkbtcbot-proxy GitHub repository referenced by the skill](https://github.com/echennells/sparkbtcbot-proxy.git)
- [Lightning L402 documentation](https://docs.lightning.engineering/the-lightning-network/l402)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment steps, environment-variable configuration, token-management commands, and operational guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
