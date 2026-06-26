## Description: <br>
Captures learnings, errors, and corrections so coding agents can log failures, user corrections, missing capabilities, tool or API issues, knowledge gaps, and better recurring-task approaches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexecuteinc](https://clawhub.ai/user/nexecuteinc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture durable learning notes from errors, corrections, feature requests, and recurring workflow discoveries, then promote useful patterns into agent instruction files after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages agents to persist conversation-derived learnings into future instruction files and across sessions. <br>
Mitigation: Require manual review before writing to AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, Copilot instructions, or other durable agent context files. <br>
Risk: Learning logs may capture sensitive data from command output, conversations, prompts, customer data, credentials, or proprietary context. <br>
Mitigation: Redact tokens, credentials, personal data, customer data, proprietary prompts, and raw transcript excerpts before logging or sharing entries. <br>
Risk: Hook-based reminders can run broadly and repeatedly, increasing the chance of unwanted persistence or prompt-context noise. <br>
Mitigation: Keep hooks project-scoped and avoid global every-prompt activation unless the workspace owner has explicitly accepted that behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nexecuteinc/test-skill-delete-me) <br>
- [OpenClaw integration reference](artifact/references/openclaw-integration.md) <br>
- [Hook setup guide](artifact/references/hooks-setup.md) <br>
- [Logging examples](artifact/references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local learning logs and proposed agent instruction files when the user or agent follows the skill guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
