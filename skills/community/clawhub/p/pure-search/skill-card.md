## Description:

A lightweight, API-key-free web search skill based on DuckDuckGo and Trafilatura that returns relevant URLs and clean markdown content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyecho-io](https://clawhub.ai/user/cyecho-io)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Pure Search to run lightweight web searches, fetch result pages, and receive the extracted main content as structured JSON with markdown bodies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to DuckDuckGo and result pages are fetched from third-party websites.

Mitigation: Avoid confidential queries, secrets, internal hostnames, and private URLs; run the skill in an isolated environment with limited network reach.

Risk: Fetched page content is arbitrary third-party material that may be unreliable, adversarial, or unsuitable for direct agent use.

Mitigation: Label returned content as untrusted and have the agent verify important claims against authoritative sources before acting on them.

Risk: The artifact does not show URL validation, resource limits, or pinned dependencies.

Mitigation: Add URL validation, time and size limits, and dependency pinning before using the skill in sensitive or high-trust workflows.

## Reference(s):

- [Pure Search on ClawHub](https://clawhub.ai/cyecho-io/skills/pure-search)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [JSON with query, results, titles, URLs, markdown_content, and errors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches live third-party pages and may return partial results or extraction errors for inaccessible content.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
