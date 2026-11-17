## Description:

Supply Chain Bottleneck Analyzer for TikTok Shop sellers. Diagnose cash flow, inventory turnover, affiliate commissions, and return rates. Includes FBT cost analysis, influencer payout optimization, and viral product lifecycle management. No API key required for basic analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External TikTok Shop sellers and ecommerce operators use this skill to estimate supply-chain cost, margin, inventory, cash-cycle, affiliate commission, and return-rate bottlenecks from provided inputs. The resulting report is a generic estimate and should not be treated as platform-specific financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guidance uses a global, unpinned package install command.

Mitigation: Review before installing; prefer a pinned package version and immutable source commit, and avoid global installation unless needed.

Risk: The skill documents TikTok API secret environment variables while evidence does not show implemented safe secret handling or the promised API behavior.

Mitigation: Do not enter real TikTok API secrets until the skill documents safe secret handling and implements the API behavior.

Risk: Security evidence flags overstated TikTok-specific financial claims and says the report should be treated as a generic estimate.

Mitigation: Validate calculations and benchmarks against current business data before using the report for operational or financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/supply-chain-optimization-tiktok)
- [Publisher profile](https://clawhub.ai/user/phheng)
- [Nexscope AI](https://www.nexscope.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local ecommerce diagnostics from user-supplied numeric inputs; optional TikTok Shop API credentials are documented but not implemented in the calculator evidence.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
