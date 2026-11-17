## Description:

Set up a non-custodial dollar-cost averaging strategy on Uniswap for recurring swaps, route selection, approval checks, automation setup, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure a non-custodial Uniswap DCA strategy, compare routes and costs, request confirmation, and set up either agent-triggered or Gelato-based recurring execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may initiate real token approvals and swaps with financial consequences.

Mitigation: Use it only in a wallet-enabled environment after reviewing the skill version, confirming the strategy details, and treating approvals and first swaps as real financial activity.

Risk: Recurring automation or persistence may be overstated relative to the declared tools.

Mitigation: Independently confirm that the local DCA config or Gelato task was created, funded, active, and cancellable before relying on recurring execution.

Risk: Unreviewed install sources can expose wallet-enabled workflows to unexpected behavior.

Mitigation: Install from pinned, reviewed sources and verify file hashes or release metadata before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/setup-dca)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style status updates, confirmation prompts, transaction summaries, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce wallet actions, token approval guidance, swap execution requests, local DCA configuration, and monitoring summaries after explicit user confirmation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
