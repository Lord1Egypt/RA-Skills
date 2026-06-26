## Description: <br>
Yandex Calendar helps agents view, add, search, and sync Yandex.Calendar events through CalDAV using vdirsyncer and khal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gbroccoli](https://clawhub.ai/user/gbroccoli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users with an existing Yandex Calendar CalDAV setup use this skill to let an agent inspect schedules, add events after confirmation, search calendar entries, and synchronize calendar changes through khal and vdirsyncer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar data may contain personal or sensitive information. <br>
Mitigation: Install only for calendar setups the user is comfortable allowing the agent to read and sync. <br>
Risk: Ambiguous event details can lead to incorrect calendar additions. <br>
Mitigation: Review dates, times, durations, titles, and target calendars before allowing event creation. <br>
Risk: Calendar synchronization can propagate unintended changes to configured calendars. <br>
Mitigation: Use configured calendars that are appropriate for agent access and confirm additions before syncing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gbroccoli/yandex-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume khal and vdirsyncer are installed and configured for the user's Yandex Calendar CalDAV account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
