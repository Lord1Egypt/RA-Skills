## Description: <br>
十维 is a Chinese-language stock value analysis skill that guides agents through a ten-module fundamental review covering financial statements, shareholder returns, industry context, peer comparison, ownership changes, shareholding concentration, valuation, conclusions, and risk reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lsh9630](https://clawhub.ai/user/lsh9630) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and agents use this skill to create structured fundamental-analysis reports for A-share, Hong Kong, and US stocks, especially when evaluating whether long-term price declines reflect risk or possible value. The skill is a checklist and reporting framework, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce investment-style conclusions that may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as an analysis checklist and require independent review before making investment decisions. <br>
Risk: Financial filings, prices, valuation metrics, and industry conditions can become stale quickly. <br>
Mitigation: Verify current market data, filings, and industry evidence before relying on any generated conclusion. <br>
Risk: The skill may activate on broad Chinese financial-analysis phrases. <br>
Mitigation: Confirm that the requested task is stock fundamental analysis before applying the framework. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lsh9630/shiwei) <br>
- [Scoring template](references/scoring_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with scoring tables, investment posture, and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires current financial, market, and filing data from external sources; missing data should be marked rather than fabricated.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
