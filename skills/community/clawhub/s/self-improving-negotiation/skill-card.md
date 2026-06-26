## Description: <br>
Captures negotiation strategy failures, concession leaks, BATNA weakness, framing misses, objection handling gaps, escalation misalignment, anchor errors, and agreement quality risks for continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, sales operators, and agent users use this skill to capture negotiation learnings, issues, and feature requests in local markdown logs. It supports recurring review of concession discipline, BATNA readiness, objection handling, escalation timing, and agreement-risk patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional hooks can emit broad negotiation reminders or inspect Bash output for negotiation keywords, including unrelated prompts or commands. <br>
Mitigation: Enable hooks deliberately, keep matchers narrow where possible, and treat hook output as reminder-only guidance. <br>
Risk: Negotiation logs may contain confidential deal terms, pricing, legal positions, or counterparty details. <br>
Mitigation: Avoid storing sensitive details unless workspace access controls, retention rules, and redaction practices are appropriate. <br>
Risk: Negotiation guidance could be mistaken for authority to approve high-impact concessions or final terms. <br>
Mitigation: Require explicit human approval for concessions, pricing, legal commitments, and final agreements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jose-compu/self-improving-negotiation) <br>
- [Examples](references/examples.md) <br>
- [Hooks setup](references/hooks-setup.md) <br>
- [OpenClaw integration](references/openclaw-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and optional hook reminder text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local .learnings markdown files only when the user or agent follows the instructions; optional hooks emit reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
