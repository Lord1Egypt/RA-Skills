## Description: <br>
Solana Dev Skill guides agents through Solana dApp, wallet, transaction, on-chain program, client SDK, testing, and security workflows with a framework-kit and @solana/kit-first approach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4rkl](https://clawhub.ai/user/h4rkl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to implement, review, test, and harden Solana applications, clients, payments, and on-chain programs. It is suited for React/Next.js dApp work, wallet-signing flows, Anchor or Pinocchio programs, Codama client generation, and Solana-focused test planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated wallet-signing or payment-flow code could authorize unintended recipients, amounts, fees, or token transfers if applied without review. <br>
Mitigation: Review wallet-signing and payment changes before use, verify recipient and amount displays, and test confirmation and error handling before deployment. <br>
Risk: Package-install guidance can introduce unpinned or unverified dependencies into Solana projects. <br>
Mitigation: Pin and verify new dependencies before applying generated install commands or committing lockfile changes. <br>
Risk: Surfpool or Surfnet state-mutation helpers can alter local cluster state in ways that should not be treated as production behavior. <br>
Mitigation: Keep Surfpool and Surfnet state-mutation workflows confined to local development or CI test environments. <br>


## Reference(s): <br>
- [Solana Dev Skill](https://clawhub.ai/h4rkl/solana-dev-skill) <br>
- [Solana Documentation](https://solana.com/docs) <br>
- [Solana Kit Docs](https://solana.com/docs/clients/kit) <br>
- [Next.js + Solana React Hooks](https://solana.com/docs/frontend/nextjs-solana) <br>
- [@solana/web3-compat](https://solana.com/docs/frontend/web3-compat) <br>
- [framework-kit Repository](https://github.com/solana-foundation/framework-kit) <br>
- [Anchor Documentation](https://www.anchor-lang.com/) <br>
- [Pinocchio Repository](https://github.com/anza-xyz/pinocchio) <br>
- [LiteSVM Repository](https://github.com/LiteSVM/litesvm) <br>
- [Mollusk Repository](https://github.com/buffalojoec/mollusk) <br>
- [Surfpool Documentation](https://docs.surfpool.dev/) <br>
- [Codama Generating Clients](https://solana.com/docs/programs/codama-generating-clients) <br>
- [Solana Security Best Practices](https://solana.com/docs/programs/security) <br>
- [Commerce Kit Documentation](https://commercekit.solana.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent outputs should include changed files, install/build/test commands, and risk notes for signing, fees, CPIs, or token transfers when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
