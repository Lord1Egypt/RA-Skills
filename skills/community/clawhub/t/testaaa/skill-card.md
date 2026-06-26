## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaotec](https://clawhub.ai/user/chaotec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to capture corrections, command failures, knowledge gaps, and feature requests as local markdown learning logs that can later be reviewed or promoted into agent guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create durable local memory about sessions, including corrections, failures, and feature requests. <br>
Mitigation: Avoid logging secrets, tokens, private keys, environment variables, full transcripts, or full source/config files; use short sanitized summaries or redacted excerpts. <br>
Risk: Promoting learnings into agent instruction files can change future agent behavior. <br>
Mitigation: Review any proposed changes to AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or Copilot instructions before accepting them. <br>
Risk: Optional hooks and cross-session workflows can inspect command output or share session context. <br>
Mitigation: Keep hooks disabled unless automatic reminders are desired, and use cross-session transcript or messaging features only in trusted environments with sanitized summaries. <br>


## Reference(s): <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates durable local learning logs and may propose promotion into agent instruction files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
