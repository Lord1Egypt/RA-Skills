## Description:

Saves, loads, verifies, exports, lists, and clears project context so coding agents can resume work across resets, context compaction, and agent switches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckystar513](https://clawhub.ai/user/luckystar513)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use Wdp Ctx to preserve project profiles and timestamped work snapshots, then restore or export that context for future sessions or other agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent project context may store and later show project instructions to agents.

Mitigation: Review generated profile, snapshot, and AGENTS.md content before relying on it, and avoid storing secrets or sensitive values.

Risk: Context may be loaded for the wrong project when projects share the same directory name or lack existing WDP context.

Mitigation: Prefer project-level storage and verify the project slug and loaded documents before using restored context.

Risk: Optional automatic hooks run a local script path to display session reminders.

Mitigation: Enable hooks only after reviewing and trusting the local hook script and settings entry.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luckystar513/skills/wdp-ctx)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent context documents and handoff summaries when applied by an agent.]

## Skill Version(s):

1.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
