## Description:

Solana Dev helps agents plan and implement Solana dApp, wallet, transaction, on-chain program, SDK, testing, and security-review work using modern Solana tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[playdadev](https://clawhub.ai/user/playdadev)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to classify Solana development tasks, select appropriate client, wallet, program, and testing tools, and produce implementation guidance with Solana-specific correctness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release provenance is unavailable, and artifact text may overstate official-source status.

Mitigation: Confirm the publisher and upstream source before treating the skill as official Solana Foundation material.

Risk: Package setup examples may use unpinned dependency installation commands.

Mitigation: Pin reviewed package versions, commit lockfiles, and install in a least-privileged development environment without production secrets.

Risk: Solana transaction, signing, CPI, token, and account-validation guidance can affect fund movement or program authority.

Mitigation: Review generated changes before execution, test on local or non-production clusters first, and require explicit checks for signers, owners, writability, token program variants, and PDA derivation.

## Reference(s):

- [Solana Dev on ClawHub](https://clawhub.ai/playdadev/skills/solana-dev)
- [Publisher profile](https://clawhub.ai/user/playdadev)
- [Solana Documentation](https://solana.com/docs)
- [Next.js + Solana React Hooks](https://solana.com/docs/frontend/nextjs-solana)
- [Solana Kit Docs](https://solana.com/docs/clients/kit)
- [framework-kit Repository](https://github.com/solana-foundation/framework-kit)
- [Anchor Documentation](https://www.anchor-lang.com/)
- [Pinocchio Repository](https://github.com/anza-xyz/pinocchio)
- [LiteSVM](https://github.com/LiteSVM/litesvm)
- [Mollusk](https://github.com/buffalojoec/mollusk)
- [Surfpool](https://docs.surfpool.dev/)
- [Solana Security Best Practices](https://solana.com/docs/programs/security)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file-change summaries, install/build/test commands, and risk notes for signing, fees, CPIs, token transfers, and account validation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
