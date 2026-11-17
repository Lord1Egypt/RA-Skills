## Description:

Launch Solana tokens on Pump.fun via the SolPaw platform. 0.1 SOL one-time fee. Your wallet is the onchain creator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvcidpsyche](https://clawhub.ai/user/lvcidpsyche)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use this skill to guide an OpenClaw agent through registering with SolPaw, configuring wallet/API credentials, and launching a Solana token on Pump.fun with a name, symbol, description, and optional image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires wallet-level secrets, including an API key and Solana private key material.

Mitigation: Use a dedicated low-balance wallet, avoid exposing a main wallet private key as an environment variable, and review credential handling before installation.

Risk: The skill can guide fee payment, transaction signing, token submission, and initial buys against a real Solana token-launch service.

Mitigation: Require explicit human confirmation and transaction review before paying fees, signing, submitting, or making any initial buy.

Risk: The skill depends on outbound calls to the SolPaw API endpoint for registration, CSRF tokens, image upload, launch, and submit operations.

Mitigation: Keep the API endpoint pinned to the intended SolPaw host and review requests before executing shell commands or SDK calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lvcidpsyche/skills/solpaw-skill-v2)
- [SolPaw Website](https://solpaw.fun)
- [SolPaw API Reference](references/api-docs.md)
- [SolPaw API Info](https://api.solpaw.fun/api/v1/info)
- [Pump.fun](https://pump.fun)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, YAML, and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet setup, fee payment, signing, submission, and token-launch instructions that require explicit human confirmation before execution.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact package manifests report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
