## Description:

Serper Clone provides web, news, image, video, shopping, scholar, patent, places, maps, and autocomplete search through a self-hosted Serper-compatible API powered by SearXNG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulscode](https://clawhub.ai/user/paulscode)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to give OpenClaw agents web search through their own Serper-compatible endpoint, including general search, news, images, videos, shopping, scholar, patents, local places, maps, and autocomplete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and API keys can be exposed if BASE_URL uses plaintext HTTP or the endpoint is not trusted.

Mitigation: Use a trusted Serper Clone endpoint over HTTPS, protect and rotate the API key, and keep the key file owner-readable only.

Risk: The shell helper is an example wrapper and is not robust for untrusted query text.

Mitigation: Review generated shell commands before use and prefer a structured JSON builder when accepting untrusted query text.

## Reference(s):

- [Serper Clone server](https://github.com/paulscode/serper-startos)
- [SearXNG](https://github.com/searxng/searxng)
- [OpenClaw](https://github.com/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured API key file and reachable Serper-compatible BASE_URL.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
