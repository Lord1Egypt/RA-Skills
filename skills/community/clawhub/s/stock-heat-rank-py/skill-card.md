## Description:

Gets real-time TOP50 A-share stock heat rankings by aggregating popularity lists from Wencai, Xueqiu, and Eastmoney.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n1e](https://clawhub.ai/user/n1e)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch and compare currently popular A-share stocks, including composite heat scores and source-specific ranks. It supports market attention monitoring, trend checks, and quick command-line retrieval of ranked stock data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically runs a large obfuscated JavaScript signature generator locally through Node.js.

Mitigation: Run only after reviewing the artifact in a contained environment, and prefer a release with readable source, documented provenance, and pinned Node dependencies.

Risk: The ranking output reflects third-party popularity signals and may be incomplete, unavailable, or unsuitable as financial advice.

Mitigation: Treat results as market-attention data only, verify important values against trusted market data sources, and avoid using the output as the sole basis for trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/n1e/skills/stock-heat-rank-py)
- [Publisher profile](https://clawhub.ai/user/n1e)
- [Wencai](https://www.iwencai.com/)
- [Xueqiu hot stocks](https://xueqiu.com/hot/stock)
- [Eastmoney stock rank endpoint](https://emappdata.eastmoney.com/stockrank/getAllCurrentList)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Console table or JSON emitted by a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes rank, stock code, stock name, source-specific rankings, composite heat score, and platform appearance count.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
