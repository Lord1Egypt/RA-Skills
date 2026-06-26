## Description: <br>
Plan days, prioritize tasks, and protect focus time with time blocking, weekly reviews, and energy-aware scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users use this skill to plan days and weeks, prioritize important work, create time blocks, and maintain lightweight planning memory for schedule preferences and commitments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local planning memory may contain schedule preferences, focus times, weekly priorities, and commitments. <br>
Mitigation: Use an only-when-asked activation style for less proactive prompting, and delete ~/time-management/ to remove stored planning memory. <br>
Risk: The skill does not access calendar, email, or external services, so schedules may omit commitments the user has not provided. <br>
Mitigation: Treat generated schedules as planning drafts and confirm fixed meetings, deadlines, and constraints before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ivangdavila/time-management) <br>
- [Time Management homepage](https://clawic.com/skills/time-management) <br>
- [Setup process](artifact/setup.md) <br>
- [Memory template](artifact/memory-template.md) <br>
- [Time blocking method](artifact/time-blocking.md) <br>
- [Prioritization frameworks](artifact/prioritization.md) <br>
- [Weekly review process](artifact/weekly-review.md) <br>
- [Common time traps](artifact/traps.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown or plain text guidance with time blocks, review prompts, and planning templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local planning memory in ~/time-management/ when the user explicitly asks to save preferences or review notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
