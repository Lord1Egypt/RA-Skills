## Description: <br>
Tracks local skill calls and produces daily, weekly, monthly, quarterly, or yearly usage reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superuser-fank](https://clawhub.ai/user/superuser-fank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users tracking OpenClaw skill activity can record skill calls and generate period-based summaries for personal usage review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic local activity tracking and session-history inspection may capture more usage context than intended. <br>
Mitigation: Install only with explicit consent; prefer narrow event-based records and avoid background history scanning unless the user enables it. <br>
Risk: Persistent local usage records may retain skill names, timestamps, and notes longer than desired. <br>
Mitigation: Use a clear disable and deletion process, and review or remove the local usage store when retention is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superuser-fank/skill-usage-tracker-nicki) <br>
- [Publisher profile](https://clawhub.ai/user/superuser-fank) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown-style text report with counts and percentages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports day, week, month, quarter, and year query dimensions; records are stored in local JSON.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
