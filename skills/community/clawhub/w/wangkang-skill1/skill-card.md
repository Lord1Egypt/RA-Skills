## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangkang5](https://clawhub.ai/user/wangkang5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture command failures, user corrections, feature requests, and reusable workflow lessons in structured markdown files for later review or promotion into agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived notes can persist into future agent behavior or instruction files. <br>
Mitigation: Review entries before saving or promotion, and require explicit user approval before adding guidance to agent instruction or memory files. <br>
Risk: Learning logs may capture secrets, personal data, proprietary snippets, or transcript contents. <br>
Mitigation: Keep entries short and sanitized, and avoid logging credentials, personal data, proprietary content, or raw conversation excerpts. <br>
Risk: Global or broad hooks can add automatic reminders in untrusted workspaces. <br>
Mitigation: Use the skill only in trusted workspaces, avoid global hooks, and narrow hook matchers when hook activation is enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangkang5/wangkang-skill1) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured learning, error, and feature request entries that may be reviewed before promotion into agent instruction files.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
