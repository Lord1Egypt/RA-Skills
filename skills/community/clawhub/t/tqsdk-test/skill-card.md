## Description: <br>
天勤量化 - 期货实时行情与历史数据接口，提供国内期货、期权的实时报价、K线序列与历史数据查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingyiyl](https://clawhub.ai/user/qingyiyl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders, analysts, and developers use this skill to query Tianqin/TQSDK futures and options market data, including real-time quotes, recent K-line series, and historical K-line data for supported contract symbols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Tianqin/TQSDK account credentials for market-data queries. <br>
Mitigation: Configure TQ_USERNAME and TQ_PASSWORD through ClawHub secrets or environment settings, avoid pasting passwords into chat or ordinary parameters, and avoid credential reuse. <br>
Risk: Unpinned dependency ranges can change installed package versions over time. <br>
Mitigation: Use pinned dependency versions for controlled installs when deploying this skill in a production or regulated environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingyiyl/tqsdk-test) <br>
- [TQSDK homepage](https://www.shinnytech.com/tqsdk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API Calls, guidance] <br>
**Output Format:** [Plain text summaries with structured JSON result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TQ_USERNAME and TQ_PASSWORD environment variables; historical K-line queries may require a Tianqin professional account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
