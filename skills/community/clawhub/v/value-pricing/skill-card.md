## Description:

Evidence-led pricing research for products, services, and other offerings. Use when someone needs to investigate a pricing decision, pricing structure, value metric, or customer evidence. Supports configurable business models, units, segments, and methods; outputs hypotheses and validation plans, not guaranteed prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-kapsalis](https://clawhub.ai/user/c-kapsalis)

### License/Terms of Use:

MIT-0

## Use Case:

Product, pricing, and research teams use this skill to investigate pricing choices for products, services, and other offerings. It helps scope evidence, select suitable research methods, and prepare conditional pricing hypotheses and validation plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can access internal services despite its stated public-web restriction.

Mitigation: Keep the crawler disabled or use network controls that block private, loopback, and link-local destinations until connection-level address enforcement is fixed.

Risk: External model processing can expose selected prompts and source text and may incur charges.

Mitigation: Review and minimize the exact content before approving external model processing.

Risk: The demand-elasticity calculation should not be relied on for pricing decisions until corrected.

Mitigation: Correct the elasticity calculation before relying on it for pricing decisions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/c-kapsalis/skills/value-pricing)
- [Intake and study design](references/1-intake.md)
- [Market references and alternatives](references/2-market.md)
- [Customer value and scenarios](references/3-value.md)
- [Buyer research and simulated panels](references/5-panel.md)
- [Bayesian demand price elasticity](references/9-demand-elasticity.md)
- [Synthesis and pricing hypotheses](references/7-synthesis.md)
- [Validation and handover](references/8-validation.md)
- [Output contract](references/output-contract.md)
- [Methodological literature](references/literature.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, CSV, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown reports and structured JSON, YAML, and CSV study files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conditional hypotheses with stated evidence, assumptions, gaps, uncertainty, and validation steps; no guaranteed prices.]

## Skill Version(s):

0.1.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
