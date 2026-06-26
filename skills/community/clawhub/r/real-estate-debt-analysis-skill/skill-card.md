## Description: <br>
Analyzes real estate debt portfolios by comparing broker-listed housing prices with Alibaba judicial auction prices and producing investment-support analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yejinlei](https://clawhub.ai/user/yejinlei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agent developers use this skill to evaluate residential real estate debt collateral, compare market and auction price estimates, assess debt coverage and liquidity, and produce investment-oriented reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may present estimated, partly random real estate prices as if they were platform-derived market or auction data. <br>
Mitigation: Treat outputs as rough estimates and verify prices, auction records, and property records with authoritative sources before making decisions. <br>
Risk: The skill can produce investment, legal, and financial-adjacent guidance for debt collateral and judicial auction properties. <br>
Mitigation: Use qualified legal, valuation, and financial review for any real transaction or portfolio action. <br>
Risk: Input data may contain sensitive debt portfolio or property information. <br>
Mitigation: Avoid sending sensitive portfolio data to unknown parser, search, or report-generation services. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yejinlei/real-estate-debt-analysis-skill) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [real_estate_analysis.py](artifact/scripts/real_estate_analysis.py) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, configuration, guidance] <br>
**Output Format:** [JSON analysis results with optional markdown or PDF report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include property-level price estimates, auction discount rates, debt coverage ratios, risk assessments, investment suggestions, summary text, and a report URL.] <br>

## Skill Version(s): <br>
v1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
