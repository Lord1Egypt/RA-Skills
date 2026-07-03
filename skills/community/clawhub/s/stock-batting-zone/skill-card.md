## Description: <br>
Generates a daily A-share high-dividend stock Batting Zone report using a five-factor scoring strategy and can push the report to Huawei negative screen through today-task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loveapleace](https://clawhub.ai/user/loveapleace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate scheduled research reports that rank selected A-share dividend stocks by dividend yield, valuation, ROE, and dividend safety. The generated report is for research reference and is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local OpenClaw today-task auth code before pushing reports. <br>
Mitigation: Review the credential source and run in dry-run mode until the local today-task configuration is approved. <br>
Risk: The push workflow depends on a hardcoded local today-task script path. <br>
Mitigation: Adjust the path for the deployment environment before enabling scheduled unattended runs. <br>
Risk: Stock rankings may be mistaken for investment advice. <br>
Mitigation: Treat outputs as research reference only and review source data and assumptions before taking financial action. <br>


## Reference(s): <br>
- [Five-factor scoring formula](references/scoring-formula.md) <br>
- [ClawHub skill page](https://clawhub.ai/loveapleace/stock-batting-zone) <br>
- [Sina Finance quote endpoint](https://hq.sinajs.cn/list={codes}) <br>
- [Leetab PE percentile endpoint](https://www.leetab.com/stock/{code}/pe) <br>
- [Leetab PB percentile endpoint](https://www.leetab.com/stock/{code}/pb) <br>
- [Eastmoney data endpoint](https://datacenter-web.eastmoney.com/api/data/v1/get?) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, configuration] <br>
**Output Format:** [Markdown report with a JSON task payload and optional dry-run JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily scheduled output is intended to stay under the Huawei negative screen card limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
