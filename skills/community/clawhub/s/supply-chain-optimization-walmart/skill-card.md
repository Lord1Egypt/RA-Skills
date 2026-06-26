## Description: <br>
Supply Chain Bottleneck Analyzer for Walmart Marketplace sellers. Diagnose cash flow, inventory, WFS costs, and referral fees. Includes comparison with Amazon FBA, lower storage fee optimization, and Walmart Connect ad spend analysis. No API key required for basic analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Walmart Marketplace sellers and e-commerce operators use this skill to diagnose supply chain bottlenecks, compare Walmart Marketplace costs with Amazon FBA, and produce cost-reduction guidance for inventory, fulfillment, referral fees, advertising, and cash cycle decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Walmart-focused business analysis may rely on Amazon/FBA assumptions and could mislead seller decisions. <br>
Mitigation: Review formulas, platform assumptions, payment-cycle handling, and WFS fee handling before using recommendations for Walmart business decisions. <br>
Risk: Optional authenticated Walmart API workflows may involve sensitive credentials. <br>
Mitigation: Treat Walmart API credentials as sensitive, avoid exposing them in shared logs or prompts, and verify the source before global installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phheng/supply-chain-optimization-walmart) <br>
- [Publisher profile](https://clawhub.ai/user/phheng) <br>
- [Nexscope AI](https://www.nexscope.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance, configuration] <br>
**Output Format:** [Markdown report with metrics tables, cost breakdowns, bottleneck diagnosis, and action recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include shell commands for installation and environment variable examples for optional Walmart Marketplace API integration.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
