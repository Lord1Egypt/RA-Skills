## Description: <br>
Captures learnings, errors, corrections, and feature requests so agents can maintain local improvement notes and promote useful patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[healersss](https://clawhub.ai/user/healersss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to capture command failures, user corrections, missing capability requests, knowledge gaps, and reusable best practices in local learning files for later review and promotion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive session-derived content in local learning and memory files. <br>
Mitigation: Do not store secrets, credentials, personal data, private transcripts, or sensitive business context in learning or memory files. <br>
Risk: Promoted learnings can influence future agent behavior broadly. <br>
Mitigation: Review entries before promotion and only promote concise, verified guidance that should affect future sessions. <br>
Risk: Always-on hook configurations can inject reminders broadly and inspect command output through CLAUDE_TOOL_OUTPUT. <br>
Mitigation: Prefer project-local hooks over global hooks and avoid empty always-on matchers where possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/healersss/self-improving-agent-local) <br>
- [OpenClaw integration](references/openclaw-integration.md) <br>
- [Hook setup guide](references/hooks-setup.md) <br>
- [Logging examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create or update .learnings/*.md and memory instruction files.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
