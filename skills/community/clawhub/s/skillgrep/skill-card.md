## Description: <br>
Use when a user is trying to discover an installable or reusable skill or workflow, especially when they ask for a skill for a task, want to compare nearby skill categories, or need help narrowing discovery results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[littledinoc](https://clawhub.ai/user/littledinoc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search for installable or reusable skills, narrow ambiguous discovery requests, compare nearby skill categories, and receive one to three skill recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill-search prompts, session metadata, and feedback may be sent to the backend. <br>
Mitigation: Avoid entering private project details unless the user has accepted that telemetry may be sent to the backend. <br>
Risk: The skill can move from recommendations into installation guidance without strong consent boundaries. <br>
Mitigation: Require explicit user confirmation before running or presenting install actions as the next step. <br>
Risk: The scanner verdict is suspicious. <br>
Mitigation: Review the skill and its backend data flow before installation or production use. <br>


## Reference(s): <br>
- [Skill Grep on ClawHub](https://clawhub.ai/littledinoc/skillgrep) <br>
- [Publisher Profile](https://clawhub.ai/user/littledinoc) <br>
- [Skill Grep API Base](https://skills.megatechai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown recommendations with optional inline shell commands and JSON-shaped API contract examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns one to three recommendations after at most two retrieval passes and one clarification question.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
