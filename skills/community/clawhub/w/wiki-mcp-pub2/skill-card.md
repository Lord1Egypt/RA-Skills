## Description:

Provides Wikipedia and Wikimedia research tools through MCP for article discovery, summaries, history, citations, editor activity, and media across multiple languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanfoglia](https://clawhub.ai/user/evanfoglia)

### License/Terms of Use:

MIT

## Use Case:

Researchers, writers, and developers use this skill to find and compare Wikipedia articles, check citations and edit history, and discover related Wikimedia media and public information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wikipedia searches, article titles, and requested usernames or IP addresses are sent to Wikimedia services.

Mitigation: Avoid sensitive lookup terms and use the skill only when that information may be shared with Wikimedia.

Risk: Public editor activity may be misused to profile contributors.

Mitigation: Use editor lookups only for a legitimate research purpose and avoid unnecessary personal profiling.

Risk: Unpinned Python dependencies may change after deployment.

Mitigation: Pin dependencies or deploy in a locked environment.

## Reference(s):

- [Wikipedia MCP on ClawHub](https://clawhub.ai/evanfoglia/skills/wiki-mcp-pub2)
- [Publisher profile](https://clawhub.ai/user/evanfoglia)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-formatted text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include article and media links, citations, edit metadata, and language-specific results.]

## Skill Version(s):

1.6.26 (source: ClawHub release metadata; packaged SKILL.md lists 1.1.14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
