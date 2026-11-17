## Description:

钢材货源查询 is a steel-trading assistant skill for querying steel spot prices, analyzing price trends, managing inventory, publishing purchase requests, importing and exporting Excel data, and preparing scheduled price reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zgzymllm](https://clawhub.ai/user/zgzymllm)

### License/Terms of Use:

MIT-0

## Use Case:

External steel traders and procurement users can use this skill to query steel market prices, compare trends, publish or search inventory, collect purchase requests, and manage spreadsheet-based inventory workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inventory and contact details may be shared through a fixed Feishu table destination.

Mitigation: Replace the Feishu app token and table ID with a destination controlled by the installing organization, or disable cloud publishing before use.

Risk: Scheduled price reports can send business information to configured push targets.

Mitigation: Disable scheduled pushes by default, verify every recipient and query, and test report output before enabling cron or other automation.

Risk: The skill installs and runs Python dependencies and scripts that access local data files and external market data sources.

Mitigation: Install dependencies in an isolated environment and review file paths, data-source settings, and generated output before operational use.

## Reference(s):

- [钢材货源查询 ClawHub Skill Page](https://clawhub.ai/zgzymllm/skills/steel-source-query)
- [Configuration Template](references/config.template.json)
- [Mysteel Data Source](https://www.mysteel.com)
- [Lange Steel Data Source](https://www.lgmi.com)
- [Documented Feishu Inventory Table](https://my.feishu.cn/base/A27gbl3lDaheavs4sFhcO1K4ngg)

## Skill Output:

**Output Type(s):** [text, markdown, json, files, shell commands, configuration]

**Output Format:** [Markdown or plain text responses, JSON records, shell commands, configuration snippets, and Excel workbooks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON cache and inventory files, generate .xlsx exports, and prepare scheduled report text when scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
