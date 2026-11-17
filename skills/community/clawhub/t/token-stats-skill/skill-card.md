## Description:

Record and analyze token usage from Codex, Claude Code, OpenClaw, Hermes Agent, OpenCode, DeepSeek Harness, WorkBuddy, WorkBuddy AI, and cached Trae CN account usage with token-stats v0.1.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baijian](https://clawhub.ai/user/baijian)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to collect and analyze token history from local agent stores and, when explicitly requested, synced Trae CN account snapshots. They can also check source coverage and preview recurring offline collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Usage reports and session views can expose sensitive paths and activity history, and Trae CN snapshots may cover account-wide use across devices.

Mitigation: Select only needed agents and dates, request session or task views separately, and keep reports private.

Risk: Trae account access and recurring collection can access sensitive data or persist collection over time.

Mitigation: Approve account access and the specific recurring collection plan explicitly; uninstall the scheduled job to prevent future collection.

Risk: Pinned hashes detect changes to the external CLI but do not audit its implementation.

Mitigation: Use the pinned release and verify its executable before use; treat hash verification as artifact matching, not an independent code audit.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/baijian/skills/token-stats-skill)
- [token-stats v0.1.0 release](https://github.com/baijian/token-stats/releases/tag/v0.1.0)
- [Token Recording](references/token-recording.md)
- [Trae CN](references/trae-cn.md)
- [Local Sessions](references/sessions.md)
- [Recorder Security](references/recorder-security.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Shell commands, Configuration instructions]

**Output Format:** [Token usage summaries and breakdowns in text or JSON, with Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes coverage warnings and source attribution; reports can contain sensitive paths and activity history.]

## Skill Version(s):

0.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
