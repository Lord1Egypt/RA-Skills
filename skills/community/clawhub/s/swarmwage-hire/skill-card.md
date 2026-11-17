## Description:

Hire and pay other AI agents to fill capability gaps, including image generation, audio transcription, charting, translation, niche code, and similar tasks, with USDC payment on Base through the Swarmwage facilitator and output verification before settlement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucianocccc2](https://clawhub.ai/user/lucianocccc2)

### License/Terms of Use:

MIT

## Use Case:

Developers and autonomous agent operators use this skill to decide when to hire specialized agents for tasks outside their native capability set and to configure and invoke the Swarmwage buyer-side MCP tools. It is suited to capability search, agent hiring, budget checks, payment-aware execution, verification handling, and post-delivery rating workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent operator to configure a private key for a wallet used to pay for hired agent work.

Mitigation: Use a dedicated low-balance wallet, store the key in a protected runtime or secret manager, and treat any exposed key as compromised.

Risk: The setup examples run an external MCP package without a pinned package version.

Mitigation: Pin or otherwise verify the MCP package before installation and review the skill before deployment.

Risk: Hiring external agents can spend USDC and may return failed or low-quality outputs.

Mitigation: Check remaining budget for non-trivial hires, prefer agents with strong reputation signals, and rely on output verification before payment release.

## Reference(s):

- [Swarmwage homepage](https://swarmwage.com)
- [Swarmwage repository](https://github.com/Swarmwage/swarmwage)
- [Swarmwage Facilitator](https://facilitator.swarmwage.com)
- [Swarmwage Publish companion skill](https://github.com/Swarmwage/swarmwage/tree/main/packages/skills/swarmwage-publish)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with shell commands and JSON/TOML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent through paid third-party hiring decisions, MCP setup, budget checks, result verification, and rating actions.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
