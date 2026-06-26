## Description: <br>
ClaWHub skill synchronization and update helper for checking local skill versions, syncing workspace skills, and reporting update status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check local ClaWHub skill versions, run workspace sync flows, and receive a concise update report for managed skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect local skills and account sync flows with broad automatic authority. <br>
Mitigation: Require an explicit confirmation or dry-run report before any update, sync, or publish action. <br>
Risk: Broad trigger phrases or scheduled execution could start update checks when the user did not intend it. <br>
Mitigation: Narrow the trigger phrases and keep the cron schedule disabled unless the operator explicitly enables it. <br>
Risk: The skill references reading a local ClawHub token file as part of its workflow. <br>
Mitigation: Limit use to trusted workspaces and avoid exposing token contents in generated reports or logs. <br>


## Reference(s): <br>
- [Yq Skill Sync on ClaWHub](https://clawhub.ai/tianheihei002/yq-skill-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include version comparisons, sync status, and recommended follow-up actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
