## Description: <br>
Creates personalized self-learning plans grounded in cognitive science, including learning paths, strategy labels, resource recommendations, reflection prompts, and optional progress-tracking outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thedataq](https://clawhub.ai/user/thedataq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, coaches, and general users use this skill to turn a learning goal, current level, schedule, and preferred style into a structured study plan. It is intended for planning learning paths, selecting study strategies, recommending resources, and tracking progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask the agent to append web-search results to its own resource database. <br>
Mitigation: Require explicit user approval before any file update, or remove the self-update instruction before installation. <br>
Risk: Learning plans and resource recommendations can be incorrect, outdated, or unsuitable for a user's goals. <br>
Mitigation: Review recommended resources and milestones before relying on the plan, especially for time-sensitive or high-stakes learning goals. <br>
Risk: Optional calendar reminders may create events the user did not intend. <br>
Mitigation: Confirm reminder timing, recurrence, titles, and target calendar before creating calendar entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thedataq/self-learning-planner) <br>
- [Learning Science Core Principles](references/learning-science.md) <br>
- [Self-Learning Framework](references/self-learning-framework.md) <br>
- [Topic Mapping Guide](references/topic-mapping-guide.md) <br>
- [Obstacles and Troubleshooting](references/obstacles-troubleshooting.md) <br>
- [Learning Resource Database](resources/resource-database.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown learning plans with optional HTML checklist code and calendar reminder configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include weekly templates, daily checklists, milestone tracking, resource lists, reflection prompts, printable HTML progress views, and reminder schedules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
