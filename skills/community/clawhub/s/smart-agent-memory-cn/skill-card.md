## Description:

Provides a cross-platform long-term memory system for OpenClaw agents with layered context retrieval, skill-experience memory, structured Markdown, JSON, and SQLite storage, temperature-based archiving, and Node.js-only operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tntest](https://clawhub.ai/user/tntest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw agent users use this skill to persist, search, recall, archive, and summarize long-term agent memory across sessions. It supports scoped context loading, skill-specific experience memory, structured fact and lesson storage, and optional extraction of reusable lesson-based skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores durable, searchable long-term memory under ~/.openclaw/workspace/memory, which can retain sensitive user or business data.

Mitigation: Avoid storing secrets, credentials, regulated personal data, or sensitive business details, and periodically review retained memory files.

Risk: The extract command can generate persistent skills without enough containment.

Mitigation: Do not use the extract command until the path traversal issues are fixed; review generated skills in a non-loaded draft location before installation.

Risk: Suggested cron jobs can automate memory maintenance actions.

Mitigation: Do not enable the suggested cron jobs until the path traversal issues are fixed and the scheduled behavior has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tntest/skills/smart-agent-memory-cn)
- [Publisher profile](https://clawhub.ai/user/tntest)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation, CLI text output, JSON exports, memory files, and generated SKILL.md templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes durable memory files under ~/.openclaw/workspace/memory; the optional extract command can write generated skills under ~/.openclaw/skills/<skill-name>.]

## Skill Version(s):

2.1.1 (source: server release evidence; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
