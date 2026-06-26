## Description: <br>
Analyze memory logs to detect recurring patterns and suggest automations such as cron jobs, skills, workflow shortcuts, or monitoring proposals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power users use this skill to analyze OpenClaw memory logs for recurring workflows and receive actionable proposals for cron jobs, skill drafts, workflow shortcuts, or monitors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw memory logs and stores derived workflow suggestions, which can expose sensitive workflow history. <br>
Mitigation: Install only where local memory-log analysis is acceptable, review generated suggestions before applying them, and reset or delete state.json when retained analysis history is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newageinvestments25-byte/workflow-crystallizer) <br>
- [Pattern Types - Detection Logic](references/pattern-types.md) <br>
- [Suggestion Templates](references/suggestion-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown reports with JSON cron definitions, draft SKILL.md snippets, saved-prompt suggestions, and monitoring proposals.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits reports to at most 3 new suggestions per run at a 60% confidence threshold and stores derived suggestion history in state.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
