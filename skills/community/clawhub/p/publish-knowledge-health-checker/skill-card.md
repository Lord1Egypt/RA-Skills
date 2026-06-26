## Description: <br>
Checks Markdown-style knowledge bases for empty or thin files, broken links, content density, and network completeness, then produces health reports and repair suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xb19960921](https://clawhub.ai/user/xb19960921) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge-base maintainers, and external users can use this skill to inspect Obsidian, Notion exports, Logseq, or Markdown repositories for structural and content-quality issues before cleanup or migration. It can summarize findings, generate HTML health reports, and propose reviewed repair scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate executable repair scripts that delete or bulk-edit files. <br>
Mitigation: Back up the knowledge base and review every generated command, especially rm and sed operations, before running it. <br>
Risk: Generated HTML reports can expose local paths and filenames. <br>
Mitigation: Treat reports as private unless local paths and sensitive filenames are removed. <br>
Risk: Scheduled checks or Feishu/email output can send results to unintended destinations if configured incorrectly. <br>
Mitigation: Confirm the exact cron schedule and destination before enabling scheduled or outbound reporting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xb19960921/publish-knowledge-health-checker) <br>
- [Publisher profile](https://clawhub.ai/user/xb19960921) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with optional HTML reports and generated shell or Python repair scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, filenames, health scores, issue tables, and suggested commands that require review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
