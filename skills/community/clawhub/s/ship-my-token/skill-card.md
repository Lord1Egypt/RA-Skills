## Description:

Launch Solana tokens on Pumpfun, create memecoins, mint crypto tokens, manage creator fee sharing, claim trading earnings, and track your portfolio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcoulaud](https://clawhub.ai/user/jcoulaud)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to launch Pumpfun tokens on Solana, configure creator fee sharing, claim fees, export or manage the generated wallet, and monitor token portfolios through an AI agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a locally custodied Solana private key and can export it on request.

Mitigation: Install only if local key custody is acceptable; never paste the private key into chat or share it, and store any backup in a secure password manager or encrypted note.

Risk: The skill can submit real Solana transactions for token launches, fee claims, and fee share updates.

Mitigation: Require explicit user confirmation before every transaction and review the launch summary, fee claim, or share update before execution.

Risk: The default fee-sharing flow routes 20% of creator fees to the skill operator.

Mitigation: Confirm the 80% creator and 20% Ship My Token split before use, and only proceed if the non-negotiable operator share is acceptable.

Risk: The skill can install dependencies, schedule recurring portfolio checks, and upload token images or metadata to Pumpfun/IPFS.

Mitigation: Require approval for dependency installs, scheduled jobs, file uploads, and network-connected operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcoulaud/skills/ship-my-token)
- [Publisher Profile](https://clawhub.ai/user/jcoulaud)
- [Ship My Token Documentation](https://shipmytoken.com)
- [Solana CLI Install](https://docs.solanalabs.com/cli/install)
- [Agent Skills](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON-parsed script results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local wallet configuration and token history files, schedule daily recap checks, upload token images and metadata, and submit Solana transactions after user confirmation.]

## Skill Version(s):

1.5.3 (source: SKILL.md metadata, package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
