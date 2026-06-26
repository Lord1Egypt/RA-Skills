## Description: <br>
Self-Learn helps an agent improve over time by learning from user corrections and task self-evaluation, storing concise lessons in memory/corrections.md and memory storage for later recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonylnng](https://clawhub.ai/user/tonylnng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to let an agent record user corrections, preferences, and repeatable lessons from completed tasks. It is intended for workflows where persistent learning is desired and where stored memories can be reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent correction and lesson storage can retain secrets, personal details, or sensitive workflow information if those details are included in examples. <br>
Mitigation: Avoid logging credentials, personal data, or sensitive information, and periodically review memory/corrections.md and stored memories. <br>
Risk: Incorrect or overly broad lessons can influence future agent behavior. <br>
Mitigation: Keep entries atomic, under 100 words, and review stored corrections before relying on them across tasks. <br>


## Reference(s): <br>
- [Corrections template](artifact/references/corrections-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/tonylnng/tonic-self-learn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown log entries and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update memory/corrections.md and store short correction or lesson entries for recall.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
