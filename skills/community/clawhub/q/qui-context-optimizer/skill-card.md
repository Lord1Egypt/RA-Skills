## Description:

Advanced context management with auto-compaction and dynamic context optimization for use with SkillBoss API Hub LLM services via /v1/pilot, including intelligent compaction, query-aware relevance scoring, hierarchical memory, and chat optimization logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to keep long LLM conversations within context limits by pruning, compacting, scoring, and retrieving relevant archived content. It is aimed at SkillBoss API Hub workflows that need token optimization while preserving recent, high-priority, and system messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain conversation content locally in a searchable archive.

Mitigation: Install only after code review, disable archive storage unless needed, and avoid processing conversations that contain secrets.

Risk: The skill can log optimization events or content-related details back into chat.

Mitigation: Disable chat or content logging unless explicitly needed and review log settings before deployment.

Risk: Retrieved or compacted user-derived content can be reintroduced as system-level context.

Mitigation: Sanitize and clearly delimit retrieved or compacted content before passing it to an LLM, and do not treat it as trusted system instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/qui-context-optimizer)
- [SkillBoss API Hub /v1/pilot endpoint](https://api.heybossai.com/v1/pilot)
- [Clawdbot homepage](https://github.com/clawdbot/clawdbot)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, JSON-compatible message arrays, status text, and archive snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on configured context thresholds, compaction strategies, archive settings, and chat logging preferences.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
