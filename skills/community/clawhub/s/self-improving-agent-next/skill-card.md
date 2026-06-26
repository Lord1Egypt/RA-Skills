## Description: <br>
Records errors, corrections, capability gaps, and best practices so agents can reuse lessons across future tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weiyunbyte](https://clawhub.ai/user/weiyunbyte) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to capture command failures, user corrections, external tool issues, capability requests, and reusable practices in structured learning files. Recurring patterns can then be promoted into longer-term agent guidance such as AGENTS.md, SOUL.md, TOOLS.md, or MEMORY.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files can capture sensitive context if agents save raw secrets, tokens, customer data, private prompts, full environment dumps, or sensitive stack traces. <br>
Mitigation: Review entries before saving or promoting them, keep hooks project-scoped where possible, and redact sensitive data from .learnings/, MEMORY.md, AGENTS.md, SOUL.md, TOOLS.md, and cross-session messages. <br>
Risk: Promoted learnings can spread incorrect or misleading guidance across future agent sessions. <br>
Mitigation: Promote only reviewed recurring patterns and keep unresolved or uncertain entries in pending learning files until verified. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to create or update persistent learning entries and, when appropriate, scaffold reusable skills from those entries.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
