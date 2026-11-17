## Description:

Grove CLI guide - philosophy, commands, and quick start.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olshansk](https://clawhub.ai/user/olshansk)

### License/Terms of Use:


## Use Case:

Developers, agents, and Grove users use this skill to install and operate the Grove CLI, evaluate tippable destinations, send micro-tips, monitor balances, and automate common tipping workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install remote code through a curl-to-bash command.

Mitigation: Review the installer before running it, or install only after independently verifying the Grove source and distribution path.

Risk: Included automation scripts can move funds or initiate multiple tips.

Mitigation: Use isolated low-balance wallets, run dry-run modes first, set conservative limits, and require human review before using scripts with real funds.

Risk: Balance monitoring webhooks can disclose account balance information to the configured webhook destination.

Mitigation: Send alerts only to trusted endpoints and avoid including sensitive wallet or account details in logs or webhook destinations.

## Reference(s):

- [Grove homepage](https://grove.city)
- [Grove CLI documentation](https://grove.city/docs/cli)
- [Grove skills documentation](https://grove.city/docs/skills)
- [Grove CLI installer](https://grove.city/install-cli.sh)
- [ClawHub skill page](https://clawhub.ai/olshansk/skills/tip-with-grove)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and automation script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Grove CLI setup, tipping, balance monitoring, batch tipping, and auto-funding workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
