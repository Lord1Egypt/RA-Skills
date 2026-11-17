## Description:

Aggregates global technology, finance, AI research, military technology, and policy news from multiple public sources into concise intelligence-style reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bodysuperman](https://clawhub.ai/user/bodysuperman)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users, analysts, and developers use this skill to collect recent public news and research items across preset topics, filter by source or time window, and receive structured summaries for situational awareness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can automatically install Python dependencies and the dependency specifications are not pinned to exact versions.

Mitigation: Install and run the skill in an isolated virtual environment or container, review dependencies before use, and install reviewed versions explicitly instead of relying on the script's automatic pip path.

Risk: Fetched article text and links come from external news and feed sources, including at least one source requested over non-HTTPS.

Mitigation: Treat retrieved content and links as untrusted, review the configured sources before deployment, and prefer HTTPS feeds where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bodysuperman/skills/world-news-aggregator-skill)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [Artifact README](README.md)
- [Artifact skill definition](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report or JSON payload with article titles, sources, timestamps, summaries, links, and source-status information.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configurable by topic/source selection, result limit, time window, and brief, summary, or detailed output mode.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
