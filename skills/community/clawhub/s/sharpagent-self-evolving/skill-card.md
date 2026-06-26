## Description: <br>
SharpAgent Self-Evolving Loop runs a Think-Do-Learn workflow that reflects after tasks, creates verifiable improvement hypotheses, tests them in small experiments, and records lessons as LearningEntry records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a structured reflection, hypothesis, experiment, and lesson-archiving loop after agent tasks so future workflows can improve from recorded outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist lessons and alter future agent behavior without clear user controls. <br>
Mitigation: Install it only when a persistent self-improvement loop is intended, and define where learning records live, how long they remain, and how they are reviewed or deleted. <br>
Risk: Automatically propagated lessons or configuration changes may introduce incorrect or unsuitable guidance into later tasks. <br>
Mitigation: Require explicit approval before applying template, monitor, lifecycle, or other configuration updates, and review lessons before promotion to best practices. <br>
Risk: Reflection records may capture sensitive task details or logs. <br>
Mitigation: Set rules for sensitive tasks before use and restrict what task outputs, logs, and learning records may be stored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/sharpagent-self-evolving) <br>
- [Publisher profile](https://clawhub.ai/user/yezhaowang888-stack) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, text] <br>
**Output Format:** [Markdown guidance with structured reflection, hypothesis, experiment, and LearningEntry templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce persistent learning records and proposals to update templates, monitors, lifecycle gates, or other agent configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
