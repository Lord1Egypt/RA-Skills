## Description: <br>
Captures learnings, errors, feature requests, and corrections in Markdown so agents can review and promote recurring knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biocrfhkust-cloud](https://clawhub.ai/user/biocrfhkust-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to log command failures, user corrections, knowledge gaps, feature requests, and recurring best practices into structured Markdown files. The skill also guides review and promotion of durable learnings into agent memory or instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning notes may preserve sensitive conversation details, credentials, customer data, raw transcripts, or private prompts. <br>
Mitigation: Redact sensitive data before logging and keep learning files project-scoped or ignored from version control when they contain private context. <br>
Risk: Promoted learnings can alter future agent instructions through files such as CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions. <br>
Mitigation: Manually review promoted changes before relying on them as durable agent guidance. <br>
Risk: Optional hooks can inject reminders or inspect command output to detect errors. <br>
Mitigation: Enable hooks only when persistent learning capture is intended, prefer project-level configuration, and review scripts and paths before global installation. <br>


## Reference(s): <br>
- [Self Improvement Skill Page](https://clawhub.ai/biocrfhkust-cloud/self-improving-agent-2) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with templates, inline shell commands, configuration snippets, and optional skill scaffold files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .learnings files, agent memory files, hook configuration, and skill scaffolds when the agent follows the workflow.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
