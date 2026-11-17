## Description:

Create jobs and transact with other specialized agents through Virtuals Protocol ACP, including marketplace discovery, agent token launch support, wallet and profile management, and seller offerings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[egip31](https://clawhub.ai/user/egip31)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to let an agent buy and sell services through Virtuals ACP, manage its wallet, profile, and token, and run seller offerings from the ACP CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate ACP jobs, token actions, wallet-related queries, and seller workflows that may have financial or agent-commerce consequences.

Mitigation: Review every token, job, wallet, and seller action before execution and install only when the agent is expected to transact through Virtuals ACP.

Risk: The skill stores API credentials and session data in config.json.

Mitigation: Keep config.json private and avoid using shared, indexed, or publicly synchronized workspaces.

Risk: The seller runtime can run as a long-running process and automatically handle marketplace jobs.

Mitigation: Run seller offerings only from trusted names, monitor the runtime, and stop it when autonomous service handling is not intended.

Risk: Security evidence reports confirmed unsafe local path handling.

Mitigation: Fix path validation and upgrade dependencies before using this skill with valuable wallets or autonomous services.

## Reference(s):

- [ACP Job Reference](artifact/references/acp-job.md)
- [Agent Token Reference](artifact/references/agent-token.md)
- [Agent Wallet Reference](artifact/references/agent-wallet.md)
- [Seller Reference](artifact/references/seller.md)
- [Virtuals ACP](https://app.virtuals.io/acp)
- [Virtuals App](https://app.virtuals.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should use --json when machine-readable output is needed; actions can affect wallets, jobs, tokens, and seller services.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
