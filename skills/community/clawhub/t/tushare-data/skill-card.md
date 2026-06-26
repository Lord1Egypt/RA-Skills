## Description: <br>
Tushare converts Chinese natural-language financial research requests into executable data retrieval, cleaning, comparison, export, and concise analysis workflows for A-share stocks, indexes, ETFs/funds, financial statements, valuation, funds flow, announcements, sectors, concepts, and macro data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lidayan](https://clawhub.ai/user/lidayan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn Chinese-language financial research, screening, comparison, macro, funds-flow, announcement, and export requests into Tushare-backed workflows. It is intended for research support and data preparation, not trading execution or personalized investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Tushare account token and quota. <br>
Mitigation: Provide TUSHARE_TOKEN only in an environment where the agent is permitted to use that account, and keep the token out of prompts, logs, and generated files. <br>
Risk: Financial summaries may be incomplete or unsuitable for investment decisions. <br>
Mitigation: Treat generated market summaries as research support, verify conclusions against authoritative data, and do not use the skill as a substitute for investment advice. <br>
Risk: Requested exports may create local CSV or parquet files. <br>
Mitigation: Specify the output folder and filename before export, then review generated files before using them in downstream analysis or backtests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lidayan/tushare-data) <br>
- [Tushare token registration](https://tushare.pro/register) <br>
- [Tushare data interface catalog](references/数据接口.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown summaries with tables, optional Python or shell snippets, and CSV/parquet export paths when data files are generated] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Tushare API calls and an optional TUSHARE_TOKEN; generated market summaries should be treated as research support rather than investment advice.] <br>

## Skill Version(s): <br>
1.1.16 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
