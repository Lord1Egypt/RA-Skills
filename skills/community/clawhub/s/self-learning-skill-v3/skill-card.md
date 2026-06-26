## Description: <br>
A markdown prompt package that guides an AI assistant through ongoing self-review, error tracking, pattern recognition, and analogy-based knowledge transfer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to prompt an AI assistant to review completed work, record mistakes, generalize lessons across similar problems, and maintain learning checklists. It is most useful when the operator wants proactive self-improvement behavior with clear user controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad proactive learning and review behavior that may exceed the user's immediate request. <br>
Mitigation: Require explicit user approval before recurring reviews, autonomous searches, or persistent learning updates are enabled. <br>
Risk: Credential and session handling guidance is under-scoped and mentions tokens, cookies, browser sessions, and environment variables. <br>
Mitigation: Require confirmation before any credential, cookie, session, or environment-variable search, and prevent secrets from being copied into logs or summaries. <br>
Risk: Persistent learning and error records may capture sensitive project or user information. <br>
Mitigation: Keep records scoped to approved project notes and redact secrets, personal data, and confidential task details before storing them. <br>
Risk: The operating instructions are primarily in Chinese, which may be difficult for some operators to audit. <br>
Mitigation: Have a reader fluent in Chinese review the behavior before deployment or provide an approved translation for operators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidme6/self-learning-skill-v3) <br>
- [Publisher profile](https://clawhub.ai/user/davidme6) <br>
- [README](artifact/README.md) <br>
- [Execution guide](artifact/EXECUTE.md) <br>
- [Error log](artifact/ERROR_LOG.md) <br>
- [Examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown guidance with checklists, templates, and example command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can lead the agent to update persistent learning or error records when the user permits that behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
