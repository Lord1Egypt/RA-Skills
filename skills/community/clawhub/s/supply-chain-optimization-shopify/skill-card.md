## Description:

Supply Chain Bottleneck Analyzer for Shopify/DTC stores that diagnoses cash flow, inventory, shipping costs, customer acquisition efficiency, CAC/LTV, 3PL cost optimization, and ad spend benchmarks without requiring an API key for basic analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopify and DTC operators, ecommerce analysts, and developers use this skill to calculate supply-chain metrics, diagnose bottlenecks, and review cash flow, inventory, shipping, and customer-acquisition tradeoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global, unpinned npx-based installation may resolve changing package contents.

Mitigation: Verify the exact source before installation and pin or vendor a reviewed release where possible.

Risk: Credential examples mention Shopify and ShipBob tokens, while the reviewed script does not appear to need or use those tokens.

Mitigation: Do not export real tokens for basic analysis; if integrating separately, use least-privilege scopes and avoid storing secrets in shell history.

Risk: Financial output is a rough calculator and the reviewed artifact retains some Amazon/FBA assumptions despite Shopify/DTC positioning.

Mitigation: Treat results as advisory estimates and validate formulas, benchmarks, and store data before making operational or financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/supply-chain-optimization-shopify)
- [Nexscope AI](https://www.nexscope.ai/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with tables, code blocks, and ranked recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts optional JSON command-line input for calculator parameters; basic analysis does not require API keys.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
