## Description:

价值分析师 helps agents apply Graham-style value-investing criteria to screen stocks, assess investor fit, calculate margin of safety, and produce structured investment observations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this Chinese-language skill for preliminary value-investing analysis, including Graham defensive-investor checks, simplified intrinsic-value estimates, margin-of-safety calculations, and risk/action summaries. It is an educational screening aid and should not be used as sole investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce buy, observe, or safety-margin labels that may be mistaken for financial advice.

Mitigation: Treat outputs as educational screening only and require independent investment research before making any trade.

Risk: Margin-of-safety calculations can be misleading when input market or financial data is stale, incomplete, or user-supplied without verification.

Mitigation: Verify prices, ratios, earnings history, dividend history, and other financial data against current authoritative market sources before relying on the analysis.

Risk: Graham criteria may not fit every sector, market structure, or growth-stage company.

Mitigation: Use the skill's industry-adjustment guidance and pair the output with broader due diligence such as moat, cash-flow, and policy-risk analysis.

## Reference(s):

- [Graham Principles Reference](artifact/references/graham-principles.md)
- [Value Analysis Template](artifact/templates/value-analysis-template.md)
- [Maotai Value Analysis Example](artifact/examples/maotai-example.md)
- [ClawHub Skill Page](https://clawhub.ai/lj22503/skills/value-analyzer)
- [ClawHub Publisher Profile](https://clawhub.ai/user/lj22503)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured JSON-style analysis with criteria tables, margin-of-safety calculations, recommendations, risks, and action items.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language financial screening output; recommendation labels are informational and depend on user-provided or independently verified market data.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
