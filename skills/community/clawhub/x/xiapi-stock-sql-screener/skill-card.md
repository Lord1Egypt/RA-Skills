## Description: <br>
Screens A-share stocks with SQL-style conditions through DAXIAPI and returns structured stock data and analysis for custom quantitative screening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to convert custom A-share screening criteria into supported DAXIAPI SQL conditions, run the CLI, and summarize matching stocks with sector, momentum, and risk context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries a third-party DAXIAPI service and relies on the daxiapi-cli package and a locally provided API token. <br>
Mitigation: Install and use it only when DAXIAPI access is intended, trust the CLI package, and keep the token in local CLI configuration or an environment variable. <br>
Risk: The trigger language is broad enough that an agent could start stock-screening API calls when the user's intent is ambiguous. <br>
Mitigation: Confirm that the next action is the stock-screening CLI workflow before allowing network or API calls. <br>
Risk: Generated stock analysis can be incomplete, stale, or mistaken and may be misread as investment advice. <br>
Mitigation: Treat outputs as informational, require the report date and data source, include risk notes and a disclaimer, and avoid absolute buy or sell claims. <br>


## Reference(s): <br>
- [DAXIAPI](https://daxiapi.com) <br>
- [SQL syntax](references/sql-syntax.md) <br>
- [Field list](references/field-list.md) <br>
- [Query examples](references/query-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with CLI command snippets and tabular stock-screening results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DAXIAPI token and a supported recent trading date.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
