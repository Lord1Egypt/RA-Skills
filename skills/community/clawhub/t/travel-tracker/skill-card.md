## Description: <br>
Manages and summarizes work and personal travel records, generates Excel reports, syncs records to Obsidian, imports travel entries from Apple Calendar, and sets travel reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m646pxhjf4-dot](https://clawhub.ai/user/m646pxhjf4-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users can use this skill to query work and personal travel records, generate weekly, monthly, and quarterly travel reports, sync travel records to Obsidian, import travel-related Apple Calendar entries, and set outbound reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect sensitive Apple Calendar travel entries and location-related data without clear scoping in the artifact. <br>
Mitigation: Review the skill before installing, use an explicit date range, and confirm what calendar data the agent can access before running calendar import workflows. <br>
Risk: The skill may write persistent travel records into an Obsidian vault or generated report folders. <br>
Mitigation: Confirm the destination folder before syncing and use a dry run or preview before allowing persistent writes. <br>


## Reference(s): <br>
- [ClawHub Travel Tracker release](https://clawhub.ai/m646pxhjf4-dot/travel-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/m646pxhjf4-dot) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash command snippets; generated artifacts may include Excel reports and Obsidian Markdown notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect calendar data and write persistent travel records, reports, reminders, and Obsidian notes when the referenced workflows are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
