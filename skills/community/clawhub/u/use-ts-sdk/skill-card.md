## Description:

Orchestrates Aptos TypeScript SDK integration for fullstack dApps and routes agents to client setup, account, transaction, view function, type, and wallet adapter guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate @aptos-labs/ts-sdk into Aptos dApps, including client setup, wallet connection, transactions, view functions, and TypeScript typing. It is most useful when a fullstack task spans multiple Aptos SDK concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad frontend or fullstack trigger wording may activate this skill outside Aptos TypeScript SDK tasks.

Mitigation: Confirm the user task involves Aptos TypeScript SDK integration before applying the skill guidance.

Risk: Wallet, API key, and private-key handling guidance can affect application security if adapted incorrectly.

Mitigation: Keep private keys out of frontend bundles and logs, and use server-side environment variables only for sensitive keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iskysun96/skills/use-ts-sdk)
- [Aptos TypeScript SDK documentation](https://aptos.dev/build/sdks/ts-sdk)
- [Aptos TypeScript SDK API reference](https://aptos-labs.github.io/aptos-ts-sdk/)
- [Aptos wallet adapter documentation](https://aptos.dev/build/sdks/wallet-adapter/dapp)
- [aptos-ts-sdk GitHub repository](https://github.com/aptos-labs/aptos-ts-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript code examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only orchestration guidance; may route the agent to granular Aptos SDK skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
