## Description: <br>
Supply Chain Bottleneck Analyzer for TikTok Shop sellers. Diagnose cash flow, inventory turnover, affiliate commissions, and return rates. Includes FBT cost analysis, influencer payout optimization, and viral product lifecycle management. No API key required for basic analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External TikTok Shop sellers and ecommerce operators use this skill to analyze supply-chain bottlenecks, cash flow, inventory turnover, affiliate commissions, return rates, and TikTok-specific fulfillment costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cash-flow and payout-cycle assumptions may not match a seller's actual TikTok Shop terms. <br>
Mitigation: Treat outputs as rough analysis and verify payout, fee, return, and fulfillment assumptions against current account data before relying on results. <br>
Risk: Optional TikTok Shop API integration can expose credentials if secrets are pasted into shared terminals or logs. <br>
Mitigation: Use revocable least-privilege credentials, avoid sharing real secrets, and rotate tokens after testing or suspected exposure. <br>
Risk: The documented global npx install command depends on external package/source integrity. <br>
Mitigation: Verify the source and package contents before running global installation commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/phheng/supply-chain-optimization-tiktok) <br>
- [Nexscope AI](https://www.nexscope.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional Python analysis code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Basic analysis does not require an API key; optional TikTok Shop API integration uses user-provided credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
