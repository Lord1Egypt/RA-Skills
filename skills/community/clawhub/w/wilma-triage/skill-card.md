## Description: <br>
Daily triage of Wilma school notifications for Finnish parents. Fetches exams, messages, news, schedules, homework, and lesson notes, filters for actionable items, syncs exams to Google Calendar, and reports via chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aikarjal](https://clawhub.ai/user/aikarjal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents and caregivers use this skill to review Wilma school records, surface actionable school notices, and keep selected school events synchronized with Google Calendar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads sensitive Wilma school records, including lesson notes, absences, messages, schedules, grades, and homework. <br>
Mitigation: Install it only where that access is appropriate, confirm local Wilma credentials are trusted, and review MEMORY.md periodically for stored preferences or sensitive context. <br>
Risk: The skill can add or remove school-related events in Google Calendar through the gog CLI. <br>
Mitigation: Use a dedicated school calendar when possible, require duplicate checks before adding events, and review calendar changes when cancelled or modified events are detected. <br>
Risk: The skill depends on separate wilma and gog tools with their own credentials and behavior. <br>
Mitigation: Set up both tools interactively, verify their credentials and permissions before use, and keep their configuration paths limited to the intended local account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aikarjal/wilma-triage) <br>
- [Publisher profile](https://clawhub.ai/user/aikarjal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise Markdown report with optional shell commands and calendar sync notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update MEMORY.md and TOOLS.md preferences and calendar configuration when the user approves or provides setup details.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
