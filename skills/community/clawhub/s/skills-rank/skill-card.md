## Description:

Track and monitor the search ranking position of a ClawHub skill across one or more keywords, with support for top results, competitor context, and JSON export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjefferson](https://clawhub.ai/user/tjefferson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to check how a ClawHub skill ranks for target keywords, compare nearby competitors, and export ranking snapshots for tracking over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried skill slugs and keywords are sent to ClawHub's public search API.

Mitigation: Use the skill only for ClawHub ranking checks and avoid submitting sensitive or private keywords.

Risk: Verbose or competitor output may display remote search result text in the terminal.

Mitigation: Review terminal output before sharing logs or reports outside the intended audience.

Risk: Search rankings are real-time snapshots and may fluctuate as ClawHub search behavior changes.

Mitigation: Use JSON exports for repeated measurements and compare trends rather than relying on a single run.

## Reference(s):

- [ClawHub Skills Rank](https://clawhub.ai/tjefferson/skills/skills-rank)
- [Publisher profile](https://clawhub.ai/user/tjefferson)
- [ClawHub Search API Reference](references/api-docs.md)
- [ClawHub search API endpoint](https://clawhub.ai/api/search?q={keyword})

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summary tables, terminal text, and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are real-time ClawHub search snapshots and are limited by the public search API result window.]

## Skill Version(s):

1.0.0 (source: release evidence and changelog, released 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
