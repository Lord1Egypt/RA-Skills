## Description: <br>
Training Swarm helps agents manage training knowledge, generate quizzes and study plans, track learner progress, and prepare proactive reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoshung1981888](https://clawhub.ai/user/gaoshung1981888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, trainers, and operations teams use this skill to turn product or process knowledge into training quizzes, personalized study plans, knowledge cards, progress reports, and reminder workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create persistent local training records under the user's home directory. <br>
Mitigation: Ask for confirmation before creating files and use only user-approved locations and learner data. <br>
Risk: The skill may prepare or trigger WeChat-style external reminders. <br>
Mitigation: Confirm recipient, channel, schedule, and message content before sending any reminder externally. <br>


## Reference(s): <br>
- [Submitted skill definition](artifact/SKILL.md) <br>
- [ClawHub release page](https://clawhub.ai/gaoshung1981888/training-swarm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command snippets and JSON knowledge-card examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local training records, plans, reports, and knowledge cards when the user approves file creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
