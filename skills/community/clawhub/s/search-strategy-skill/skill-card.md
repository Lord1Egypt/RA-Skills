## Description:

Search Strategy Skill helps an agent choose an appropriate search, reading, crawling, or research tool for a query or URL and fall back when a selected tool fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sean810720](https://clawhub.ai/user/sean810720)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route search tasks across web readers, search engines, crawlers, research APIs, and social search tools based on query or URL characteristics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private URLs, internal hostnames, local file paths, or sensitive search terms may be sent to external search and scraping providers.

Mitigation: Review inputs before use, avoid sensitive targets, and deploy only with approved provider and network egress policies.

Risk: URL handling can be abused to read local files or reach internal services, especially when forced engines handle untrusted targets.

Mitigation: Do not use --engine=multi with untrusted URLs; restrict allowed URL schemes and block access to internal networks before deployment.

Risk: External data flows are under-disclosed in the artifact.

Mitigation: Document enabled providers, API keys, and data-sharing behavior for users before installing or running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sean810720/skills/search-strategy-skill)
- [OpenClaw Homepage](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown excerpts, and optional JSON when supported by the selected tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ANSI-colored status lines, external search results, fetched page excerpts, and result limits controlled by command options.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
