## Description: <br>
Captures learnings, errors, corrections, and feature requests so agents can document recurring lessons and promote broadly useful knowledge into project memory or reusable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use this skill to record command failures, user corrections, missing capabilities, API/tool failures, knowledge gaps, and better recurring practices. The recorded entries can be reviewed, resolved, promoted into project memory, or extracted into reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages durable logging and sharing of conversation, error, command, and session context that may include secrets, personal data, customer data, raw prompts, or sensitive command output. <br>
Mitigation: Require redaction before writing logs or sharing entries; avoid recording secrets, tokens, personal data, customer data, raw prompts, and sensitive command output. <br>
Risk: Global or broad prompt hooks can repeatedly inject reminders and capture context outside the intended project scope. <br>
Mitigation: Prefer project-scoped hooks with narrow matchers and avoid global hook activation unless it is explicitly needed. <br>
Risk: Reading or sharing other session transcripts may expose information beyond the active task. <br>
Mitigation: Do not read or share other session transcripts without clear authorization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/self-improving-agent-1-0-2-litiao) <br>
- [Hook setup guide](references/hooks-setup.md) <br>
- [Clawdbot integration](references/clawdbot-integration.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local learning logs, memory updates, hook configuration guidance, and skill scaffolding instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
