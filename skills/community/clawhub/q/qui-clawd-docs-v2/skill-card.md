## Description:

Smart ClawdBot documentation access with local search index, cached snippets, and on-demand fetch. Token-efficient and freshness-aware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to answer ClawdBot documentation questions by checking local snippets and indexes first, then fetching public docs.clawd.bot pages through SkillBoss API Hub when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send requested ClawdBot documentation URLs to SkillBoss API Hub when local snippets or caches do not answer the question.

Mitigation: Use local snippets and cache first, restrict fetches to public docs.clawd.bot pages, and provide SKILLBOSS_API_KEY only in trusted environments.

Risk: Cached documentation answers may become stale because snippets and pages rely on TTL-based freshness.

Mitigation: Check snippet expiry and refresh or fetch current public documentation when the TTL has expired or the answer affects operations.

## Reference(s):

- [ClawdBot documentation](https://docs.clawd.bot/)
- [ClawdBot skills documentation](https://docs.clawd.bot/tools/skills)
- [ClawdBot multi-agent documentation](https://docs.clawd.bot/concepts/multi-agent)
- [ClawdBot documentation index](https://docs.clawd.bot/llms.txt)
- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/qui-clawd-docs-v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local cached snippets and indexes first; full-page fetches require SKILLBOSS_API_KEY and send requested public documentation URLs to SkillBoss API Hub.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports source skill version 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
