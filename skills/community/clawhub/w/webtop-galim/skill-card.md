## Description: <br>
Check, monitor, and summarize student homework and task status from Webtop, Galim Pro, and Ofek. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaike1](https://clawhub.ai/user/shaike1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents or school-supporting agents use this skill to check homework and task status across Webtop, Galim Pro, and Ofek, summarize urgent or overdue items in Hebrew, and optionally sync Galim due dates to a private calendar. <br>

### Deployment Geography for Use: <br>
Israel <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles children's school portal credentials and local service-account secrets. <br>
Mitigation: Install only when the publisher is trusted, keep environment and service-account files out of repositories and synced folders, and restrict local file permissions. <br>
Risk: Calendar sync can write child task details to Google Calendar. <br>
Mitigation: Use a private dedicated calendar, verify the calendar ID before running, and run calendar sync with --dry-run first. <br>
Risk: The Webtop path delegates to a separate local script outside this artifact. <br>
Mitigation: Review or disable the Webtop path unless the separate local Webtop script is also trusted. <br>
Risk: Generated reports may expose children's homework details to unintended recipients. <br>
Mitigation: Verify any family-update destination before sharing summaries and limit distribution to intended recipients. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shaike1/webtop-galim) <br>
- [Skill README](artifact/SKILL.md) <br>
- [Environment credentials format](artifact/references/env-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Hebrew text or Markdown summaries, optional JSON reports, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include homework counts, visible task details, overdue or urgent status, calendar sync results, and setup checks.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
