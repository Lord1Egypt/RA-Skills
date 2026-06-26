## Description: <br>
Captures dialogue learnings, tone mismatches, escalation failures, and conversation-quality issues so agents can review and promote proven conversation patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture conversation failures, tone mismatches, hallucinations, escalation gaps, and feature requests into learning files, then promote recurring patterns into project or workspace memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent conversation logs can capture sensitive or private conversation data. <br>
Mitigation: Use redacted summaries, do not store secrets or private user/customer data, and keep learning files project-scoped. <br>
Risk: Hook reminders and promoted learnings can broadly influence future agent behavior. <br>
Mitigation: Require human review before promoting logs into AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, Copilot instructions, or generated skills. <br>
Risk: Global hook activation can carry conversation-learning behavior into unrelated workspaces. <br>
Mitigation: Prefer opt-in, project-scoped hook configuration with narrow matchers, dedupe, and rate limiting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jose-compu/self-improving-conversation) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends local learning logs when the agent follows the workflow; optional hooks emit reminder text.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
