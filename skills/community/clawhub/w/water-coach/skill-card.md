## Description: <br>
Hydration tracking and coaching skill for logging water intake, managing reminders, recording body metrics, and generating hydration analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oristides](https://clawhub.ai/user/oristides) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use Water Coach to set up hydration goals, log water intake and body metrics, schedule reminders, and review daily, weekly, or monthly hydration progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes an unrelated bundled skills/mcporter directory with MCP-control functionality. <br>
Mitigation: Review the bundled mcporter skill before installation and remove it from the package if it is not required for the Water Coach release. <br>
Risk: Water Coach can read local OpenClaw session transcripts for audit message IDs and, when audit_auto_capture is enabled, can show transcript context in audits. <br>
Mitigation: Keep audit_auto_capture disabled unless transcript context is needed, and review the privacy impact before enabling audit context. <br>
Risk: Included tests can write test entries and counters if they run against real tracking data. <br>
Mitigation: Run tests only in an isolated workspace or against disposable data, not against a user's active hydration logs. <br>
Risk: Reminder and dynamic scheduling behavior can create repeated notifications if configured too aggressively. <br>
Mitigation: Configure reminder times and dynamic scheduling limits deliberately during setup and adjust them if notifications become excessive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/oristides/water-coach) <br>
- [Setup guide](artifact/references/setup.md) <br>
- [Log format reference](artifact/references/log_format.md) <br>
- [Dynamic scheduling reference](artifact/references/dynamic.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local CSV and JSON hydration and body-metrics files in the agent workspace.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release metadata and artifact/_meta.json; changelog released 2026-02-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
