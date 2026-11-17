## Description:

Universal Intelligence Agent orchestrates multi-engine web search, web crawling, NLP and LLM analysis, credibility scoring, and structured intelligence reports without requiring API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xincen0725](https://clawhub.ai/user/xincen0725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to gather, crawl, compare, verify, monitor, and summarize web information across multiple sources. It is intended for structured brief or deep intelligence reports with credibility assessment and recoverable state handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad web fetching authority.

Mitigation: Run it with a sandboxed network egress policy and block private and metadata addresses.

Risk: The skill may write local state, reports, WAL files, and monitoring configuration.

Mitigation: Install only where local ~/.uia state files, report output, WAL writes, and possible cron monitoring are acceptable.

Risk: Untrusted session identifiers could affect recovery behavior.

Mitigation: Avoid passing untrusted session IDs when using resume or recovery workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xincen0725/skills/universal-intelligence-agent)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [pyproject.toml](artifact/pyproject.toml)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON-compatible structured results, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Brief and deep report templates include source counts, credibility levels, entities, cross-validation notes, conclusions, and source listings.]

## Skill Version(s):

1.0.0 (source: frontmatter, pyproject.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
