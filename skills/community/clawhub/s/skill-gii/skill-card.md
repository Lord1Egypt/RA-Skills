## Description:

Captures learnings, errors, corrections, feature requests, and recurring task improvements so agents can preserve and promote reusable knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huihuilu](https://clawhub.ai/user/huihuilu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to log command failures, corrections, missing capabilities, and durable process learnings into workspace markdown files for later review or promotion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review flags an unrelated Homebrew gog dependency in the skill metadata.

Mitigation: Review install requirements before deployment and avoid installing the gog dependency unless it is intentionally required by the deployment environment.

Risk: Broad hooks and persistent agent-memory changes can influence future sessions.

Mitigation: Keep hooks project-scoped with narrow matchers, inspect hook output before enabling it, and require explicit approval before writing to shared agent instruction or memory files.

Risk: Cross-session history or messaging can expose more context than intended.

Mitigation: Use cross-session sharing only in trusted environments and send sanitized summaries or file paths instead of raw transcripts, secrets, or full command output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huihuilu/skills/skill-gii)
- [Publisher Profile](https://clawhub.ai/user/huihuilu)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Hooks Setup](artifact/references/hooks-setup.md)
- [Examples](artifact/references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local .learnings markdown files and optional agent instruction files when the user approves promotion.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
