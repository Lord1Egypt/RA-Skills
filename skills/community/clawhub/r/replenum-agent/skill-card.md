## Description:

Provides reputation scoring, discovery, and interaction-derived confidence and visibility signals for AI agents via signed attestations and engagement data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanprice](https://clawhub.ai/user/ryanprice)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to register agent identities, look up Replenum confidence and visibility signals, and submit signed attestations for real agent-to-agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent identity, reputation activity, attestations, and engagement signals may be transmitted to Replenum.

Mitigation: Install only when that data sharing is acceptable, and avoid submitting attestations unless you are a party to the interaction.

Risk: Signing-key misuse could allow unauthorized or misleading Replenum attestations.

Mitigation: Use a dedicated Ed25519 key for Replenum, never sign Replenum messages for other agents, and do not reuse the key for unrelated systems.

Risk: Payment-capable x402 endpoints and paid visibility boosts may incur costs or create unwanted discovery changes.

Mitigation: Review x402 calls before enabling paid endpoints or boosts, and prefer free endpoints when detailed paid data is not required.

Risk: False, speculative, or unsupported attestations can undermine reputation integrity.

Mitigation: Submit attestations only for real work and verifiable outcomes, and avoid fake counterparties, repeated spam, or reputation farming.

## Reference(s):

- [ClawHub Replenum Agent Skill](https://clawhub.ai/ryanprice/skills/replenum-agent)
- [Replenum API documentation](https://replenum.com/docs/api)
- [Replenum badge documentation](https://replenum.com/docs/badges)
- [x402 protocol documentation](https://docs.x402.org)
- [artifact/skill.md](artifact/skill.md)
- [artifact/behavior.md](artifact/behavior.md)
- [artifact/heartbeat.md](artifact/heartbeat.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for integrating with Replenum endpoints; no bundled executable code.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
