## Description: <br>
Safely improve agent capabilities with structured verification, rollback, and promotion gating. Enhances existing evolution workflows with optional SettlementWitness verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nutstrut](https://clawhub.ai/user/nutstrut) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, errors, and workflow learnings, then gate promotion into durable agent memory or instructions with verification and rollback steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs or promoted memory can shape future agent behavior. <br>
Mitigation: Review proposed updates to AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, MEMORY.md, or Copilot instructions before relying on them, and promote only after verification passes. <br>
Risk: Learning entries or verification payloads could include secrets or personal data if users copy raw task context into them. <br>
Mitigation: Keep logs and verification submissions minimal and structured; exclude secrets, API keys, credentials, private keys, seed phrases, hidden prompts, and personal data. <br>
Risk: Optional hooks add recurring reminders during agent sessions. <br>
Mitigation: Enable hooks only when persistent capture is desired, keep them project-scoped where possible, and inspect the shell and OpenClaw hook files before enabling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nutstrut/verified-capability-evolver) <br>
- [OpenClaw integration guide](references/openclaw-integration.md) <br>
- [Hook setup guide](references/hooks-setup.md) <br>
- [Entry examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, configuration snippets, and optional hook code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local learning logs, promotion guidance, hook reminders, and skill scaffolds; optional verification uses minimal structured task data with explicit approval.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
