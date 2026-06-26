## Description: <br>
Captures learnings, errors, and corrections so agents can maintain improvement logs and review them before major tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huihuilu](https://clawhub.ai/user/huihuilu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture command failures, user corrections, feature requests, knowledge gaps, and recurring best practices in structured learning logs. It also provides optional hook and promotion workflows for carrying reviewed learnings into future agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requests an unexplained Homebrew dependency for gog. <br>
Mitigation: Confirm the intended package and repository before installation, and do not install the dependency unless the maintainer justifies why it is needed. <br>
Risk: Learning logs can capture sensitive context, command output, or transcripts. <br>
Mitigation: Sanitize entries, avoid raw transcripts and command output, and redact secrets, tokens, private keys, environment variables, and private configuration. <br>
Risk: Promoted learnings and hooks can influence future agent behavior through persistent memory or workspace instruction files. <br>
Mitigation: Require explicit review before promoting entries into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, MEMORY.md, or sharing learnings across sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huihuilu/skill-gii) <br>
- [OpenClaw integration](artifact/references/openclaw-integration.md) <br>
- [Hook setup guide](artifact/references/hooks-setup.md) <br>
- [Examples](artifact/references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and structured log templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .learnings markdown files; hook setup is optional.] <br>

## Skill Version(s): <br>
1.0.5 (source: evidence.release.version and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
