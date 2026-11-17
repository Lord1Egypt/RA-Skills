## Description: <br>
Generates structured weekly reports for individual users, covering completed work, next-week plans, risks, and optional Git or task-record inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual users use this skill to turn work notes, Git commit history, and task records into a structured weekly report with accomplishments, plans, and risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local work context such as Git history, task data, API keys, callback URLs, or external API details without fully explaining data handling. <br>
Mitigation: Keep report generation scoped to specific repositories or files, avoid untrusted callback_url endpoints, and require explicit confirmation before sending internal project details to external APIs. <br>
Risk: Git history and task records can contain confidential project information that may be exposed in generated reports. <br>
Mitigation: Review and redact generated weekly reports before sharing them outside the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/weekly-report-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown weekly report with optional JSON, text, or CSV structured output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local weekly report files and execution logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
