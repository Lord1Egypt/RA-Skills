## Description: <br>
Venus Project Pm coordinates the Venus kindergarten ERP project-management workflow across Feishu group tabs, Bitable tables, dynamic rosters, planning files, and morning/evening progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spikesubingrui-design](https://clawhub.ai/user/spikesubingrui-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Project managers and developers use this skill to run the Venus ERP progress workflow: sync active reporters, read planning files, collect or track reports, compare status against module milestones and the launch timeline, and produce PM follow-up guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run local Feishu/Bitable workflow commands that create group tabs, sync rosters, seed planning files, collect or track reports, or migrate Base fields. <br>
Mitigation: Install only for the Venus ERP Feishu/Bitable environment, review the referenced venus-bitable-sync.py script and its credentials separately, and require confirmation before mutating commands. <br>
Risk: Stale roster or planning files can lead to incorrect project-management follow-up. <br>
Mitigation: Refresh the roster before morning or evening tracking and compare script output with task_plan.md, findings.md, and progress.md before sending PM guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spikesubingrui-design/venus-project-pm) <br>
- [Project homepage](https://github.com/spikesubingrui-design/venus-project-pm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes mutating Feishu/Bitable workflow commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
