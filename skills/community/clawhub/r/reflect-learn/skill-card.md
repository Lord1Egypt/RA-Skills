## Description:

Self-improvement through conversation analysis; extracts learnings from corrections and success patterns, proposes updates to agent files, and can draft new skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevengonsalvez](https://clawhub.ai/user/stevengonsalvez)

### License/Terms of Use:


## Use Case:

Developers and agent maintainers use Reflect to analyze conversations for explicit corrections, successful patterns, and reusable lessons, then review proposed updates to agent files or new skills before applying them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose and apply persistent changes to agent instructions or create new skills.

Mitigation: Require explicit user approval, inspect generated diffs, and apply only selected changes that preserve existing structure.

Risk: The optional PreCompact hook can create reflection output during context compaction when auto-reflection is enabled.

Mitigation: Keep auto-reflection disabled until the hook script and settings snippet are reviewed, then use remind-only mode or a pinned hook command when possible.

Risk: The artifact bundle includes private developer session logs.

Mitigation: Remove bundled logs before installation or redistribution and avoid using log contents as public provenance.

Risk: Generated skill names and paths can affect persistent user or project files.

Mitigation: Validate proposed skill names and target paths before file creation, and use a controlled REFLECT_STATE_DIR for state files.

## Reference(s):

- [Reflect Skill Definition](artifact/SKILL.md)
- [Hook Integration Guide](artifact/hooks/README.md)
- [Signal Detection Patterns](artifact/references/signal_patterns.md)
- [Agent Mappings Reference](artifact/references/agent_mappings.md)
- [Skill Template Reference](artifact/references/skill_template.md)
- [Reflection Template](artifact/assets/reflection_template.md)
- [Learnings Schema](artifact/assets/learnings_schema.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reflection reports with diff blocks, shell commands, YAML or JSON state and configuration, and skill file drafts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write reflection files, indexes, learnings state, hook logs, and optional new skill files after review.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
