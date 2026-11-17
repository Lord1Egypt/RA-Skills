## Description:

Relationship OS enables AI agents to build human-like relationships with users through event memory, open threads, exclusive memories, agent stances, and relationship growth stages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenhab03](https://clawhub.ai/user/chenhab03)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this OpenClaw skill to add relationship memory, follow-up threads, persistent stances, and stage-based interaction style to an agent. It is intended for companionship-style agent experiences that remember relationship-changing moments across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal events, preferences, inside jokes, emotional context, and follow-up threads in local .relationship files.

Mitigation: Install only in a private workspace, treat .relationship as sensitive private data, and review retention and access controls before use.

Risk: Relationship context is re-injected into later sessions and may affect future agent behavior.

Mitigation: Review captured memories periodically and remove stale, inaccurate, or overly sensitive entries before they are reused.

Risk: Scheduled cron or Telegram follow-ups can send proactive outbound messages.

Mitigation: Require explicit user approval before enabling scheduled or delivered follow-ups, and keep proactive messages traceable to a thread or milestone.

Risk: Debug logs may expose sensitive relationship state or personal context.

Mitigation: Disable debug logging or redact logs before sharing, support access, or deployment outside a private workspace.

Risk: The artifact includes moderation-workaround guidance for roleplay framing.

Mitigation: Remove that guidance before deployment and require the agent to follow the applicable model and platform safety policies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenhab03/skills/relationship-os)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Event Memory Format Specification](references/event-schema.md)
- [Proactive Trigger Rules](references/motivation-rules.md)
- [Selfie Module Rules](references/selfie-rules.md)
- [Relationship Stage Behavior Matrix](references/stage-matrix.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON state files, shell commands, and short agent-facing context snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local .relationship state files and may emit scheduled follow-up commands when enabled.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
