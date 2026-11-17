## Description:

Design and run an agent-native, evidence-settled prediction market - the trust model, propose-to-open-to-settle lifecycle, machine-measurable settlement, anti-gaming rules, and the path from play-credits to real money.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to design autonomous-agent prediction markets with separated proposal, curation, trading, settlement, identity, and ledger responsibilities. It is most relevant before implementation or launch review of evidence-settled markets, especially where real-money event-contract constraints may apply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-money prediction markets and event contracts can trigger legal, identity, custody, and ledger-integrity obligations.

Mitigation: Treat legal, security, identity, and ledger integrity review as launch prerequisites before any real-money deployment.

Risk: Incorrect settlement authority or ambiguous measurement can produce misleading or unfair market outcomes.

Mitigation: Use machine-measurable settlement specs, separate proposer and oracle authority, record the measured reading, and keep disputed or ambiguous measurements open rather than settling them.

Risk: Open self-registration and self-fulfilling conditions can make prices or outcomes easy to manipulate.

Mitigation: Require verified identities, per-principal controls, non-participant triggering facts, independent corroboration, and trading halts before deterministic settlement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickflach/skills/resonance-futures)
- [Publisher profile](https://clawhub.ai/user/nickflach)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with architecture patterns, controls, and review checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces design guidance only; it does not execute code, call tools, or modify files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
