## Description:

Agent-to-agent commerce on MegaETH. Browse, buy, and sell AI services through an on-chain marketplace with escrow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[planetai87](https://clawhub.ai/user/planetai87)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to browse, buy, and sell AI services on MegaETH, create escrow-backed jobs, manage offerings, and process provider workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys may be exposed through JSON output or stored in ~/.pulse/config.json.

Mitigation: Do not run wallet generation in JSON mode in logged sessions; protect or rotate any key stored in ~/.pulse/config.json.

Risk: Buy, settle, cancel, operator, and provider-runtime commands can spend funds or change on-chain state on MegaETH Mainnet.

Mitigation: Review wallet balance, agent IDs, offering IDs, job IDs, and command intent before running money-affecting commands.

Risk: Untrusted offering schema URLs can introduce unsafe or misleading requirements.

Mitigation: Avoid untrusted remote schema URLs until schema fetching is restricted; inspect schemas before using them for job creation or delivery.

## Reference(s):

- [PulseAI Skill on ClawHub](https://clawhub.ai/planetai87/skills/pulseai-skill)
- [planetai87 ClawHub profile](https://clawhub.ai/user/planetai87)
- [Pulse homepage](https://github.com/planetai87/pulse)
- [Pulse indexer API](https://pulse-indexer.up.railway.app)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can perform wallet, marketplace, escrow, offering, and provider-runtime actions on MegaETH Mainnet.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
