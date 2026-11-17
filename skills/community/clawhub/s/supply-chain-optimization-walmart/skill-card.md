## Description:

Supply Chain Bottleneck Analyzer for Walmart Marketplace sellers. Diagnose cash flow, inventory, WFS costs, and referral fees. Includes comparison with Amazon FBA, lower storage fee optimization, and Walmart Connect ad spend analysis. No API key required for basic analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External Walmart Marketplace sellers and commerce operators use this skill to estimate supply-chain metrics, diagnose inventory, cash-cycle, WFS cost, referral-fee, and advertising bottlenecks, and draft cost-reduction guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review classifies the skill as a rough calculator rather than authoritative Walmart Marketplace financial guidance.

Mitigation: Validate fee, payment-cycle, storage, advertising, and margin formulas against current Walmart Marketplace terms before relying on recommendations.

Risk: The documented global install command is mutable and unpinned.

Mitigation: Install from a pinned CLI version, immutable repository commit, signed release, or project-local dependency path.

Risk: The documentation mentions Walmart API credentials, but the bundled code does not use the documented API integration.

Mitigation: Avoid entering real Walmart credentials unless the integration path is independently reviewed and confirmed necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/supply-chain-optimization-walmart)
- [Nexscope AI](https://www.nexscope.ai/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with metrics tables, cost breakdown, bottleneck diagnosis, summary, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local calculator formulas and benchmark thresholds; no live Walmart API calls are performed by the bundled script.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
