## Description: <br>
Trading card analysis, grading guidance, market comps, and eBay listing optimization for sports cards, Pokemon, and other collectible cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmsneaks11-max](https://clawhub.ai/user/mmsneaks11-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, collectors, and trading-card operators use this skill to identify cards, estimate value ranges, decide whether grading is worthwhile, and draft factual eBay listing copy. It can work without credentials and can optionally use host-provided eBay or PSA integrations for live research when those integrations are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated listing copy may include unsupported seller status, feedback, shipping, authentication, scarcity, population, market trend, or investment claims. <br>
Mitigation: Require human review before publication and remove or verify each claim against seller records, card evidence, eBay data, PSA data, and current marketplace terms. <br>
Risk: Portfolio guidance, stop-loss framing, or investment language may be mistaken for financial advice. <br>
Mitigation: Present pricing and grading output as collectible-market context, avoid financial advice wording, and add uncertainty notes for unverified or heuristic estimates. <br>
Risk: Optional eBay and PSA credentials could expose marketplace or account data if handled outside trusted secret management. <br>
Mitigation: Use runtime environment variables or host secret management with least-privilege access, and avoid storing credentials in the skill package or home-directory dotfiles. <br>
Risk: Live eBay or PSA claims may be overstated when integrations are unavailable or were not queried. <br>
Mitigation: State when results are based on user-provided details or heuristics, and only describe live market, population, or certification data after an approved integration has actually returned it. <br>


## Reference(s): <br>
- [Trading Card Specialist Skill](SKILL.md) <br>
- [Optional Credentials and Integration Setup](CREDENTIALS.md) <br>
- [eBay Listing Template Generator](assets/ebay-listing-template.md) <br>
- [Grading Strategy Guide](references/GRADING-STRATEGY.md) <br>
- [Market Research Guide](references/MARKET-RESEARCH.md) <br>
- [Listing Optimization Guide](references/LISTING-OPTIMIZATION.md) <br>
- [Optional Integration Notes](references/INTEGRATIONS.md) <br>
- [Security Notes](references/SECURITY.md) <br>
- [eBay Developer Program](https://developer.ebay.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown responses with card analysis, grading recommendations, eBay listing copy, verification notes, and optional credential setup snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should distinguish heuristic advice from live integration results and should not claim market, population, seller, shipping, or authentication facts unless verified.] <br>

## Skill Version(s): <br>
2.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
