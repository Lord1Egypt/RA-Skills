## Description: <br>
Default token-efficient assistant discipline: minimal prompts, concise context, and short actionable outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phoenixlucky](https://clawhub.ai/user/phoenixlucky) <br>

### License/Terms of Use: <br>
GPL-3.0 <br>


## Use Case: <br>
Developers and agent users use this skill to guide an assistant toward token-efficient work: classifying the task, reading only necessary context, producing concise outputs, and switching to more detailed handling when accuracy or user intent requires it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The prompt may default to Chinese-language behavior when an operator expects adaptive English responses. <br>
Mitigation: Review the prompt before deployment and adjust language expectations for the target agent or user population. <br>
Risk: Token-minimizing guidance can be over-applied to tasks that need more context, verification, or detailed explanation. <br>
Mitigation: Apply the skill's documented exit conditions for detailed explanations, brainstorming, legal, medical, financial, and time-sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phoenixlucky/zerotoken-skill) <br>
- [Publisher profile](https://clawhub.ai/user/phoenixlucky) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Concise Markdown with task-specific commands, code, configuration snippets, or direct guidance as needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritizes minimal necessary context and short actionable responses; exits compact mode for detailed explanations, brainstorming, high-stakes decisions, or time-sensitive accuracy needs.] <br>

## Skill Version(s): <br>
1.4.0 (source: SKILL.md metadata, package.json, README.md, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
