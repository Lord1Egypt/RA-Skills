## Description: <br>
Structured retrospectives and execution-memory hygiene for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebclawops](https://clawhub.ai/user/sebclawops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to produce post-task retrospectives, correction logs, weekly reviews, and scoped lesson notes without creating hidden memory or autonomous behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Retrospective notes could capture secrets, sensitive personal information, or hidden preferences if used carelessly. <br>
Mitigation: Follow the skill guardrails and scanner guidance: keep notes visible, review entries before relying on them, and do not store secrets, sensitive personal data, or inferred preferences. <br>
Risk: A lesson could be promoted into broader agent behavior without enough evidence. <br>
Mitigation: Use the documented conservative promotion states and treat candidate rules as recommendations that need review before durable behavior changes. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Promotion Rules](references/promotion-rules.md) <br>
- [Boundaries](references/boundaries.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend visible workspace file updates for retrospective notes; does not require tools, credentials, or external services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
