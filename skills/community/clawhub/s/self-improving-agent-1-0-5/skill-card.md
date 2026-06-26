## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[czubi1928](https://clawhub.ai/user/czubi1928) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to record corrections, command failures, feature requests, and reusable workflow lessons so future agent sessions can apply them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist session details into learning files that may later influence agent context. <br>
Mitigation: Install only where persistent learning notes are desired, keep hooks project-scoped, and review logged entries before reuse. <br>
Risk: Logged command output or session notes may include secrets, private data, or sensitive operational details. <br>
Mitigation: Redact secrets and private command output before logging or promoting entries. <br>
Risk: Promoting unreviewed learnings into AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, MEMORY.md, or Copilot instructions can spread incorrect guidance. <br>
Mitigation: Require human review before promoting any learning into shared or persistent instruction files. <br>


## Reference(s): <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [ClawHub Skill Page](https://clawhub.ai/czubi1928/self-improving-agent-1-0-5) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent learning, error, and feature-request entries for later human or agent review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
