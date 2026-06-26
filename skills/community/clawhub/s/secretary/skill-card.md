## Description: <br>
Manage calendar, draft communications, and track preferences with explicit confirmation before actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users can use this secretary-style skill to draft communications, suggest calendar actions, track commitments, and maintain explicitly stated preferences. Deployment should enforce confirmation before messages, calendar changes, bookings, RSVPs, or memory updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Artifact behavior may direct the agent to send messages, change calendars, book travel, handle RSVPs, or mutate inbox state without clear approval controls. <br>
Mitigation: Restrict the skill to drafting and suggestions unless the user personally confirms each external action. <br>
Risk: The skill maintains detailed local memory about people, preferences, schedules, and work patterns. <br>
Mitigation: Store only preferences and relationship notes the user explicitly approves, and let the user review or remove local memory files. <br>
Risk: Communications written in the user's voice could damage relationships or create obligations if sent without review. <br>
Mitigation: Require review for legally binding, emotional, negotiation, client-sensitive, or relationship-sensitive messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/secretary) <br>
- [Calendar Management](artifact/calendar.md) <br>
- [Daily Operations](artifact/operations.md) <br>
- [Writing On Your Behalf](artifact/writing.md) <br>
- [Memory System Guide](artifact/memory-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with occasional inline shell commands for local setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local secretary memory files only when explicitly approved by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
