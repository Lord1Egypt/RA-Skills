## Description:

Web Reader Pro extracts web page content for OpenClaw using a multi-tier Jina, Scrapling, and WebFetch fallback strategy with routing, caching, quality scoring, and domain learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch article content, extract page text, handle dynamic JavaScript-heavy pages, and read WeChat official account articles. It returns extracted title and content with metadata about the extraction tier, quality score, cache state, and learned domain routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching arbitrary URLs and routing through third-party extraction services can expose sensitive, authenticated, signed, or internal-network URLs.

Mitigation: Install and run the skill in an isolated environment with limited filesystem and network access, and avoid internal or secret-bearing URLs unless third-party routing is disabled and internal-network fetches are blocked.

Risk: The Scrapling installer uses unpinned npm/npx installation behavior and can create a persistent command wrapper.

Mitigation: Review or replace the installer before use, prefer pinned package versions, and avoid persistent npx wrappers in managed environments.

## Reference(s):

- [Web Reader Pro ClawHub release](https://clawhub.ai/0xcjl/skills/web-reader-pro)
- [Skill documentation](artifact/SKILL.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Python dictionary or JSON-like result plus plain-text CLI output with extracted markdown content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include title, content, URL, extraction tier, quality score, cache status, learned route metadata, timestamp, and optional error details.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
