## Description: <br>
Generates random self-reflection questions across eight dimensions and twenty-eight topics, with optional heartbeat scheduling, personalization, and usage statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujiajun4433](https://clawhub.ai/user/wujiajun4433) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to receive periodic or manually requested self-reflection prompts for mood, body awareness, thinking, action, relationships, environment, reflection, and future planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Periodic prompts may interrupt users outside their intended schedule. <br>
Mitigation: Review and adjust trigger probability, active hours, and minimum interval before enabling heartbeat triggers. <br>
Risk: Personalization can use conversation history or personal profile context. <br>
Mitigation: Disable personal-context use or previous-answer memory when sensitive context should not be used or retained. <br>
Risk: Reflective answers and backups may retain personal information. <br>
Mitigation: Review the 90-day retention and backup settings before use. <br>
Risk: Referenced install scripts or helper scripts may not be present in the provided artifact evidence. <br>
Mitigation: Do not run referenced install or helper scripts unless the complete package is available and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wujiajun4433/random-question-skill) <br>
- [Publisher profile](https://clawhub.ai/user/wujiajun4433) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain-text reflection prompts with Markdown instructions, shell command snippets, and YAML or JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports configurable trigger probability, active hours, minimum interval, personal-context use, previous-answer memory, retention, and backup settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
