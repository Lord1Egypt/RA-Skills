## Description:

Stock Roundtable guides agents through evidence-based bull and bear debates for stock and ETF analysis, including earnings, valuation, risk, position-management, and comparison questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujintang](https://clawhub.ai/user/yujintang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to structure stock or ETF research as a visible debate that checks public market information before reaching a conclusion. It is suited to buy, sell, hold, earnings-reaction, valuation, risk, position-management, and two-security comparison questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat generated hold, reduce, stop-loss, or take-profit conditions as trading instructions.

Mitigation: Present outputs as informational research support, preserve the skill's non-advice disclaimer, and require users to verify market data and make independent decisions.

Risk: Market data, earnings, policy, macroeconomic, or geopolitical information may be stale, incomplete, or conflicting.

Mitigation: Use current public sources during execution, cite source timing, acknowledge conflicts, and avoid strong conclusions without at least one higher-confidence source.

Risk: The workflow depends on internet search; without it, analysis can become unreliable.

Mitigation: Follow the skill's refusal path when current web access is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yujintang/skills/stock-roundtable)
- [Publisher profile](https://clawhub.ai/user/yujintang)
- [Core debate reference](references/core-debate.md)
- [Search recipes](references/search-recipes.md)
- [Output templates](references/output-templates.md)
- [Examples](references/examples.md)
- [Compare mode reference](references/compare-mode.md)
- [Earnings mode reference](references/earnings-mode.md)
- [Industry playbooks](references/industry-playbooks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research discussion with evidence checks, round-by-round debate, conclusions, risk points, and follow-up metrics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current market information to support conclusions; outputs are informational and not financial advice.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
