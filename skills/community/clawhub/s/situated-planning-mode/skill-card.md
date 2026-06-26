## Description: <br>
Guides agents through staged, context-sensitive planning questions with described options, subagent research when knowledge is insufficient, and a complete plan output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phallusophy](https://clawhub.ai/user/phallusophy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn vague project ideas into structured plans before execution. It helps clarify goals, constraints, scope, technical approaches, option tradeoffs, and next actions through conversational staged planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may search prior memory during planning. <br>
Mitigation: Restrict memory permissions or review memory access when prior planning context may contain sensitive information. <br>
Risk: The skill may spawn research subagents while evaluating options. <br>
Mitigation: Require approval for subagent research or limit subagent access when private, paid, or sensitive resources are available. <br>
Risk: Planning recommendations may remain uncertain when research cannot be completed. <br>
Mitigation: Mark unresolved items as pending confirmation and review the plan before moving into execution. <br>


## Reference(s): <br>
- [Dynamic Question Generation Mechanism](references/dynamic-questions.md) <br>
- [Error Reference](references/errors.md) <br>
- [Output Format Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Conversational Markdown with optional JSON status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request memory search or subagent research when planning context is insufficient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
