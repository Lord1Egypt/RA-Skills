## Description:

Supports developers building Towns Protocol bots with SDK initialization, slash commands, message handlers, reactions, interactive forms, blockchain operations, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreyz](https://clawhub.ai/user/andreyz)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to build, debug, and deploy Towns Protocol bots on Bun and Base, including messaging, interactive requests, and blockchain transaction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment or entitlement logic may grant access from an unverified transaction hash.

Mitigation: Verify the on-chain receipt status before granting access or entitlements.

Risk: Initializer packages, development webhooks, message logs, and destructive actions can expose credentials, private messages, or user assets if used without review.

Mitigation: Pin and verify setup packages, require webhook request verification, avoid logging raw user messages in production, and require explicit user confirmation for transfers, signatures, deployments, and message deletion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andreyz/skills/towns-protocol)
- [Towns bot documentation](https://docs.towns.com/build/bots)
- [@towns-protocol/bot SDK](https://www.npmjs.com/package/@towns-protocol/bot)
- [Messaging API](references/MESSAGING.md)
- [Blockchain Operations](references/BLOCKCHAIN.md)
- [Interactive Components](references/INTERACTIVE.md)
- [Deployment](references/DEPLOYMENT.md)
- [Debugging](references/DEBUGGING.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
