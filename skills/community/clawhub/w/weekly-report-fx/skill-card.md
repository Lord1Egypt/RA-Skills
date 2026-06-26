## Description: <br>
AI-powered weekly report generator that scans GitHub issues, pull requests, commits, optional calendar events, reminders, and project files to generate weekly reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fx-world888](https://clawhub.ai/user/fx-world888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and teams use this skill to turn weekly GitHub activity and optional productivity data into concise work summaries, status updates, or standup reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may contain private project or organizational details from GitHub activity and optional productivity sources. <br>
Mitigation: Review generated reports before sharing and limit collection to intended repositories and data sources. <br>
Risk: GitHub data collection can require an OAuth or personal access token for private repositories. <br>
Mitigation: Use a fine-grained read-only GitHub token and pass explicit repositories when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fx-world888/weekly-report-fx) <br>
- [fx-world888 ClawHub profile](https://clawhub.ai/user/fx-world888) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration] <br>
**Output Format:** [Markdown, HTML, or plain text report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports week offset, report style, output format, explicit repository selection, and dry-run sample output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
