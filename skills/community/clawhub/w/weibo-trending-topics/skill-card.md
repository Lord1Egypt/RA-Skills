## Description:

Track Weibo hot search trends in real time, including live hot-search topics, category filtering for entertainment, society, technology, and sports, and historical trend comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzxiatian-crypto](https://clawhub.ai/user/dzxiatian-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch current Weibo hot-search topics, inspect category-specific trends, and compare saved trend snapshots to identify newly ranked or dropped topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The usage example makes outbound network requests to Weibo.

Mitigation: Run it only in environments where access to Weibo public endpoints is permitted and expected.

Risk: The historical comparison example reads local JSON files selected by the user.

Mitigation: Use trusted snapshot files and review file paths before running comparison code.

## Reference(s):

- [Weibo Hot Search Endpoint](https://weibo.com/ajax/side/hotSearch)
- [ClawHub Skill Page](https://clawhub.ai/dzxiatian-crypto/skills/weibo-trending-topics)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python examples and concise procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled executable code; examples make network requests to Weibo and may read user-provided local JSON files for comparison.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
