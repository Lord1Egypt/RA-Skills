## Description:

Shang Tsung gives AI agents persistent local memory and identity continuity across restarts by combining Markdown-based session state, daily logs, long-term memory, and numbered SOULS lineage files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrjessek](https://clawhub.ai/user/mrjessek)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give filesystem-capable agents continuity across restarts, compaction, and multi-agent workspace sessions. It provides setup guidance, Markdown templates, and shell commands for maintaining local agent memory and session lineage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files can influence future agent behavior across sessions.

Mitigation: Install in a dedicated private workspace, review and prune memory files regularly, and treat remembered text as notes rather than commands.

Risk: Memory files may contain personal context or sensitive operational details.

Mitigation: Do not store secrets in MEMORY.md, PROOF_OF_LIFE.md, daily logs, or soul files, and load long-term memory only in appropriate private sessions.

Risk: Untrusted workspace writers or unsafe environment overrides can affect what the agent reads or where the helper writes files.

Mitigation: Avoid untrusted writers in the workspace, validate AGENT_NAME values, and use SOULS_DIR overrides only when writes outside the default workspace path are intentional.

## Reference(s):

- [Shang Tsung Skill Page](https://clawhub.ai/mrjessek/skills/shang-tsung)
- [SKILL.md Setup Walkthrough](artifact/SKILL.md)
- [Security Declaration](artifact/SECURITY.md)
- [AGENTS Protocol Template](artifact/references/AGENTS-template.md)
- [PROOF_OF_LIFE Template](artifact/references/proof-of-life-template.md)
- [SOUL Origin Reference](artifact/references/SOUL-ORIGIN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workspace memory files and session-lineage Markdown when the helper script and protocol are used.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json; changelog released 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
