## Description: <br>
Captures learnings, errors, and corrections so coding agents can record failures, user feedback, missing capabilities, and recurring best practices for future improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallersoup](https://clawhub.ai/user/smallersoup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture task learnings, command failures, corrections, feature requests, and recurring patterns in persistent markdown logs. They can later review those records and promote validated guidance into project or agent instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs and cross-session sharing can retain sensitive, private, or stale details beyond the original task. <br>
Mitigation: Redact secrets and private details before logging, keep shared logs intentional, and review entries before committing or reusing them. <br>
Risk: Broad or always-on hooks can inject reminders across many sessions and change agent behavior more often than intended. <br>
Mitigation: Keep hooks project-local, avoid empty matchers for always-on activation unless that behavior is intentional, and enable hook scripts only after review. <br>
Risk: Promoting unreviewed learnings into AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, Copilot instructions, or new skills can preserve incorrect guidance. <br>
Mitigation: Require human review before promotion and keep promoted rules concise, current, and tied to validated recurring patterns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallersoup/self-improving-agent-6) <br>
- [OpenClaw integration guide](references/openclaw-integration.md) <br>
- [Hook setup guide](references/hooks-setup.md) <br>
- [Self-improvement examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, code] <br>
**Output Format:** [Markdown guidance with templates, shell snippets, and optional hook/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent .learnings entries and optional hook reminders; promotion into long-lived instruction files should be reviewed by a human.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
