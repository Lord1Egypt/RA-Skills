## Description: <br>
Sync TASKS.md current phase and in-progress checklist from the active PLAN.md phase to keep sprint execution aligned. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to compare the active PLAN.md phase with a matching TASKS.md project section, report drift, and optionally update TASKS.md so sprint execution stays aligned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apply mode can replace the target TASKS.md section's in-progress checklist. <br>
Mitigation: Run report mode first, confirm PROJECT_NAME, PLAN_FILE, and TASKS_FILE, and keep version control or a backup before using SYNC_MODE=apply. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/tasks-md-sprint-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and console status output from the sync script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report mode prints drift without file changes; apply mode updates the target TASKS.md current phase and in-progress checklist.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
