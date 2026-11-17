## Description:

Creates and manages simulated Solana token dollar-cost averaging strategies with guided setup and commands to list, pause, and resume strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liji3597](https://clawhub.ai/user/liji3597)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to guide creation and management of simulated Solana DCA strategies, collecting token, USDC amount, and schedule details before running Node command-line helpers. It also supports listing, pausing, and resuming existing strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill delegates strategy actions to unaudited shared code outside the package, so simulation-only behavior cannot be verified from the artifact alone.

Mitigation: Install only after reviewing the shared runtime, including strategy storage, scheduler behavior, and any Solana transaction path.

Risk: Strategy actions depend on Telegram user IDs and external shared services.

Mitigation: Verify how Telegram user IDs are authorized and isolated before allowing users to create, pause, resume, or list strategies.

Risk: Users may mistake DCA setup flows for investment advice or live trading capability.

Mitigation: Preserve the simulation disclosure, require confirmation before creating a strategy, and avoid recommending investment frequency or amount.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liji3597/skills/solana-dca)
- [Publisher profile](https://clawhub.ai/user/liji3597)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and SOLANA_NETWORK; command helpers accept user, token, amount, schedule, and strategy identifiers.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
