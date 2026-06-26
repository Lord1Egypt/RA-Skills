## Description: <br>
Full lifecycle goal management: from vague vision to filed, tracked, and automated long-term plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyxin-del](https://clawhub.ai/user/joeyxin-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to clarify long-term goals, split them into milestones and atomic tasks, persist goal plans as Markdown files, generate reminder payloads, and review progress over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Goal details may include sensitive personal, financial, career, or health information that is saved locally and may be remembered across sessions. <br>
Mitigation: Use explicit save commands, avoid storing unnecessary sensitive details, and periodically review or delete generated goal files and memory pointers. <br>
Risk: Generated reminder payloads can keep resurfacing outdated or sensitive goal details after the user's situation changes. <br>
Mitigation: Review scheduled reminders after material plan changes and remove or update reminders that no longer match the current goal. <br>


## Reference(s): <br>
- [Shenzhen Financial Planning Reference](references/shenzhen-financial-planning.md) <br>
- [Secretary Skill ClawHub Page](https://clawhub.ai/joeyxin-del/secretary-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational guidance, Markdown plan files, and JSON cron reminder payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local goal and plan files when the user saves a goal; produces reminder configuration payloads when scheduling is requested.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
