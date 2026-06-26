## Description: <br>
Run a structured weekly agent retrospective that analyzes wins, failures, skill gaps, cron health, and configuration issues from the last 7 days. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidfurlong](https://clawhub.ai/user/davidfurlong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their users use this skill to review recent work, identify recurring failures or skill gaps, and turn findings into prioritized actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creates or proposes recurring automation and persistent local memory/file changes from broad reflection prompts. <br>
Mitigation: Review the planned cron entry and output paths before first use; disable or remove the job if weekly retrospectives are not wanted. <br>
Risk: Retrospectives inspect recent memory and session context, which can expose sensitive work details in generated notes. <br>
Mitigation: Run only in trusted workspaces and review the generated markdown before sharing or committing it. <br>


## Reference(s): <br>
- [Retrospective ClawHub page](https://clawhub.ai/davidfurlong/retrospective) <br>
- [Retrospective Anti-Patterns](references/anti-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown retrospective with tables and prioritized action lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a dated retrospective file and may update memory; first use may add a weekly Friday cron job.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
