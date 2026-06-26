## Description: <br>
Chinese-language stock and ETF research skill that structures investment questions as a multi-perspective roundtable, using real-time public information checks to support debate, risk review, and traceable conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujintang](https://clawhub.ai/user/yujintang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to discuss whether a stock or ETF is worth buying, selling, holding, comparing, or reviewing after earnings. It is designed for research support through visible bull/bear debate, source checking, risk framing, and follow-up metrics rather than licensed financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outputs may be mistaken for financial advice or may rely on incomplete or time-sensitive market information. <br>
Mitigation: Present conclusions as research support, cite and date key sources, verify cited information independently, and avoid absolute buy or sell instructions. <br>
Risk: The workflow depends on current public web access for prices, filings, news, policy, macroeconomic data, and geopolitical context. <br>
Mitigation: Refuse or defer the analysis when current web search is unavailable, and clearly mark stale, conflicting, or unverified data. <br>
Risk: Users may disclose sensitive portfolio details that could appear in searches, prompts, or agent logs. <br>
Mitigation: Ask only for necessary position context and advise users not to share sensitive portfolio information they would not want included in search or agent logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yujintang/stock-roundtable) <br>
- [Core debate reference](references/core-debate.md) <br>
- [Search recipes](references/search-recipes.md) <br>
- [Industry playbooks](references/industry-playbooks.md) <br>
- [Output templates](references/output-templates.md) <br>
- [Compare mode reference](references/compare-mode.md) <br>
- [Earnings mode reference](references/earnings-mode.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown stock or ETF roundtable with debate rounds, evidence checks, conclusion, risk points, action conditions, and tracking metrics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires current public web research; outputs should be treated as research support and verified by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
