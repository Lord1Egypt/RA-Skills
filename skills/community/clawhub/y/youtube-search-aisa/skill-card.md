## Description:

Search YouTube videos, channels, and trends via the AISA API using queries, filters, and pagination without requiring Google credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and content researchers use this skill to run YouTube SERP searches, top-video checks, and competitor research through a Python client with locale and filter controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube search queries, country and language filters, pagination/filter tokens, and the AISA API key are sent to api.aisa.one.

Mitigation: Use this skill only when the AISA API relay is acceptable, and avoid private or sensitive research terms.

Risk: The skill is not designed for direct Google API access, fully local browsing, scraping, or account-level YouTube actions.

Mitigation: Choose a different tool when a workflow requires direct Google credentials, local-only processing, browser automation, scraping, or YouTube account actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/youtube-search-aisa)
- [AISA API endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; sends YouTube search queries, country and language filters, and pagination/filter tokens to api.aisa.one.]

## Skill Version(s):

1.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
