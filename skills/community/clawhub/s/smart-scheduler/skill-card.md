## Description: <br>
Coordinate meeting requests, proposed time slots, confirmations, and ICS exports from a local scheduling ledger. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mehulupase01](https://clawhub.ai/user/mehulupase01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create scheduling requests, record participant time-slot proposals, confirm explicit choices, and export shareable calendar files from a local ledger. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting and participant details are stored in a local runtime database. <br>
Mitigation: Use the skill only where local storage of scheduling data is acceptable, and avoid entering sensitive participant details unless the workspace handling is approved. <br>
Risk: Calendar exports are written to the default ICS location or to a user-selected path. <br>
Mitigation: Choose output paths deliberately and review generated calendar files before sharing or importing them. <br>
Risk: A slot can be marked confirmed even when the scheduling conversation is ambiguous. <br>
Mitigation: Confirm slots only after explicit user or participant agreement, and present unresolved options instead of inventing agreement. <br>


## Reference(s): <br>
- [Message Templates](references/message-templates.md) <br>
- [Project Homepage](https://github.com/Mehulupase01/openclaw-skill-suite/tree/main/skills/smart-scheduler) <br>
- [ClawHub Skill Page](https://clawhub.ai/mehulupase01/smart-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands; the helper CLI returns JSON and writes SQLite and ICS files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores meeting and participant details in .runtime/smart-scheduler.db and writes ICS calendar files to the requested output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
