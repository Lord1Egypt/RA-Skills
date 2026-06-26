## Description: <br>
Organizes local WeChat chat history by querying conversations, extracting tasks and time-sensitive items, and preparing notes or reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pjpan](https://clawhub.ai/user/pjpan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who manage WeChat conversations can use this skill to search chat history, identify tasks, meetings, contacts, and other key information, then organize the results into Obsidian notes or calendar-ready reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to access private WeChat history and may create additional local copies in Obsidian or calendar-related outputs. <br>
Mitigation: Install only if that access is acceptable, use narrow chat and date limits, and review extracted content before saving or sharing it. <br>
Risk: Setup may require broad local permissions such as macOS Full Disk Access and depends on a third-party WeChat CLI. <br>
Mitigation: Verify the wechat-cli package source before use and grant only the permissions needed for the intended task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pjpan/wechat-smart-organizer) <br>
- [Project homepage](https://github.com/ppj/wechat-smart-organizer) <br>
- [Command reference](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON or file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Obsidian note content, calendar-event details, extracted task lists, and local file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
