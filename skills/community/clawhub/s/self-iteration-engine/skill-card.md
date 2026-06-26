## Description: <br>
Self-iteration and feedback learning engine for AI agent skills that tracks usage logs, detects performance patterns, triggers skill updates, and proposes new skills from repeated request patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bustes01](https://clawhub.ai/user/bustes01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record skill usage, identify repeated failures or corrections, schedule review cycles, and decide when to update an existing skill or propose a new dedicated skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to persist request details, user corrections, and lessons learned, which can expose sensitive user or project information if logs are not controlled. <br>
Mitigation: Use it only where users have agreed to improvement logging, redact sensitive content before storage, and define retention and deletion rules for usage logs. <br>
Risk: The skill encourages cross-user pattern analysis for new skill creation, which can create privacy and separation concerns. <br>
Mitigation: Limit cross-user analysis to anonymized aggregate patterns and avoid storing identifiable request details across users or workspaces. <br>


## Reference(s): <br>
- [Self-Iteration Engine on ClawHub](https://clawhub.ai/bustes01/self-iteration-engine) <br>
- [ClawHub Homepage Metadata](https://clawhub.ai/BusTes01/self-iteration-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML and Markdown examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces usage log formats, feedback-loop configuration examples, review schedules, update decision criteria, and new-skill proposal templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
