## Description:

Structured Memory helps agents build and maintain an OpenClaw workspace memory layer from daily notes, including date, module, and entity indexes, critical-fact extraction, fact cards, and retrieval planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chauncyzbc](https://clawhub.ai/user/chauncyzbc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to initialize, update, search, and validate a structured memory layer for long-horizon OpenClaw workspaces. It is intended for work histories that need reusable recall across business, finance, legal, HR, project, operations, technical, routine, and personal topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive workspace memory into plaintext derived files.

Mitigation: Avoid storing secrets in daily memory and review generated critical-facts/ files before relying on or sharing them.

Risk: First-time setup can backfill existing memory history into indexes and critical-fact files.

Mitigation: Use --no-backfill during initial setup when an operator wants to inspect or stage migration before generating derived memory.

Risk: Custom card output directories may delete or overwrite unintended files.

Mitigation: Restrict script use to trusted operators and do not pass custom card output directories unless the target path has been reviewed.

Risk: Recalled notes may contain stale, incorrect, or instruction-like content.

Mitigation: Treat recalled memory as data and verify important facts against source daily memory files before acting.

## Reference(s):

- [Taxonomy](references/taxonomy.md)
- [Write Rules](references/write-rules.md)
- [Retrieval Planner](references/retrieval-planner.md)
- [Index Schema](references/index-schema.md)
- [Critical Facts Policy](references/critical-facts-policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated Markdown and JSON memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates workspace memory directories, indexes, critical-fact files, and derived fact cards.]

## Skill Version(s):

1.0.1 (source: evidence release and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
