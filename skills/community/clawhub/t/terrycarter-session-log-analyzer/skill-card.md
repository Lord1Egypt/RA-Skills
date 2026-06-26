## Description: <br>
View and analyze session logs, generate PDF reports, and sync to Notion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect agent session logs, summarize activity and errors, create PDF reports, and optionally sync reports to a Notion database on demand or through a daily schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring access to private session logs and Notion upload may expose sensitive operational data. <br>
Mitigation: Use a narrowly scoped Notion integration and database, review generated reports before upload, and avoid enabling the cron job until the processed data and removal steps are understood. <br>
Risk: The artifact describes analysis, sync, and cron scripts that are not present in the submitted artifact. <br>
Mitigation: Inspect the referenced scripts from a trusted source before running manual analysis, Notion sync, or scheduled reporting. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/terrycarter1985/terrycarter-session-log-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/terrycarter1985) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus generated PDF report files and Notion report entries when configured.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Notion credentials for Notion sync.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
