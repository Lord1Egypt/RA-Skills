## Description: <br>
Captures support delays, misdiagnoses, escalation gaps, SLA breaches, knowledge gaps, and churn signals so agents can turn recurring support issues into reusable guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support agents and support engineering teams use this skill to record ticket failures, SLA breaches, knowledge gaps, feature requests, and churn signals. The captured patterns can be promoted into KB articles, troubleshooting trees, escalation matrices, canned responses, runbooks, or follow-on skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad hook activation can add persistent reminders or detection behavior across agent sessions. <br>
Mitigation: Install in a dedicated support workspace, prefer project-level setup, use support-specific hook matchers, and keep optional PostToolUse detection disabled unless it is explicitly needed. <br>
Risk: Support logs may accidentally capture customer PII, credentials, raw ticket text, or regulated data. <br>
Mitigation: Store only anonymized summaries and ticket IDs in .learnings/, and avoid writing secrets, regulated data, or verbatim customer messages. <br>
Risk: Promoted support learnings can change team behavior or agent instructions in SOUL.md, AGENTS.md, TOOLS.md, or generated skills. <br>
Mitigation: Require human review before changing persistent agent guidance, operational runbooks, or enabling extracted skills. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jose-compu/self-improving-support) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands, JSON configuration snippets, hook code, and structured log-entry templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends support learning files under .learnings/ and can emit opt-in hook reminders.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
