## Description: <br>
Xinqing Journal helps users record Chinese mood journal entries, detect seven mood categories, assign 1-10 scores, extract tags, and generate daily, weekly, monthly, and trend reports using local JSON storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyby99-gif](https://clawhub.ai/user/dyby99-gif) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and personal productivity agents use this skill to keep a local mood journal, summarize mood history, and review emotional trends without sending journal data over the network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Journal entries and mood history may contain sensitive personal information stored on the local filesystem. <br>
Mitigation: Use the skill only when local storage is acceptable, protect the OpenClaw workspace, and treat backups of the journal data as sensitive. <br>
Risk: An anonymized export can still reveal dates, tags, moods, and scores. <br>
Mitigation: Review exported data before sharing it and remove fields such as dates or tags when they could identify the user or private events. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dyby99-gif/xinqing-journal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [CLI text reports and local JSON journal data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Journal entries are stored locally under the OpenClaw workspace; reports summarize the local entries by day, week, month, or trend window.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
