## Description:

Chinese-language valuation modeling skill that helps users structure DCF, PE, PB, PEG, WACC, sensitivity-analysis, and scenario-style valuation work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, analysts, finance teams, and learners use this skill to prepare valuation assumptions, compare multiple valuation methods, and generate risk-aware company valuation outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags broad command-execution, file-processing, and API-automation behavior without clear consent boundaries.

Mitigation: Review the skill before installation and keep shell execution, local file access, and external API use disabled unless the user explicitly approves the specific action.

Risk: Valuation workflows may involve sensitive financial inputs, holdings, API keys, or non-public company data.

Mitigation: Use only financial inputs intended for the agent, pass credentials through approved secret handling, and avoid submitting confidential data unless policy allows it.

Risk: Generated valuation recommendations can be misleading when assumptions, market data, or model choices are stale or unsuitable.

Mitigation: Require human review of assumptions, data freshness, and model fit before using outputs for investment, portfolio, or transaction decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/valuation-model-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON and Markdown, with optional HTML or SVG visual output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include valuation scores, model metrics, recommendations, risk factors, confidence values, and data-source metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
