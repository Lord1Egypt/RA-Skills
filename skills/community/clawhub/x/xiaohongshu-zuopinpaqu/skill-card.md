## Description:

Searches public Xiaohongshu content by keyword, retrieves note details and comments from note URLs, and monitors public creator posts with structured results for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketers, data analysts, and agents use this skill to collect public Xiaohongshu search results, note and comment details, and creator post lists for content research, competitor monitoring, trend analysis, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note or profile URLs, and the GUAIKEI_API_TOKEN to the Guaikei service.

Mitigation: Use a dedicated, revocable token and install only where sharing those inputs with Guaikei is acceptable.

Risk: Crawl results are saved automatically and may contain collected public content or analysis inputs.

Mitigation: Avoid shared workspaces for sensitive investigations, protect the logs directory, and delete old results when no longer needed.

Risk: The server security summary flags token handling and saved crawl results as items users should review before installing.

Mitigation: Review the skill before deployment and rotate or revoke the API token if it may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/xiaohongshu-zuopinpaqu)
- [Guaikei API Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell command examples and structured JSON or table-style CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; results may be saved automatically under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
