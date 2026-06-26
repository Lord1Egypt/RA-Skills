## Description: <br>
Automatically collects financial-news inputs, classifies industry trends, analyzes related stocks, and generates stock and industry analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ligo-gao](https://clawhub.ai/user/ligo-gao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run local stock and industry analysis workflows that summarize financial news, identify hot industries and companies, calculate simple technical indicators, and produce report files for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can present mock or randomized financial data as real-looking stock analysis. <br>
Mitigation: Verify each data source before relying on a report, and clearly label or replace mock/static news and randomized indicators before use. <br>
Risk: Reports include stock scores and buy, watch, or avoid guidance that could be mistaken for investment advice. <br>
Mitigation: Treat reports as informational drafts only and require human financial review before making trading or investment decisions. <br>
Risk: Recurring execution can accumulate SQLite records and report files locally. <br>
Mitigation: Enable scheduled runs only when recurring local analysis is intended, and periodically review the retained database and report files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ligo-gao/stock-industry-analyzer) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Configuration](artifact/config.json) <br>
- [Requirements](artifact/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain-text financial analysis reports with command examples and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write SQLite records and report text files under the local data directory when run in persistent mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
