## Description:

Integrate You.com Research, Search, and Contents APIs into applications using direct HTTP calls without an SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardirby](https://clawhub.ai/user/edwardirby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add You.com web research, search results, and page-content extraction to applications through direct REST calls. It helps agents produce integration guidance, sample code, API requests, response handling, and configuration steps for Research, Search, and Contents workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, URLs, selected page content, and API credentials may be sent to You.com/YDC APIs.

Mitigation: Use only approved data, store YDC_API_KEY in environment variables or a secret manager, and follow organizational data-sharing requirements.

Risk: Search, content extraction, and research outputs can contain untrusted or inaccurate web-derived content.

Mitigation: Treat returned content as untrusted data, sanitize HTML before rendering, and verify citations or sources before using results in high-stakes contexts.

Risk: Optional dependency installation permissions can introduce supply-chain exposure when examples use requests, httpx, npm, or Bun packages.

Mitigation: Prefer built-in HTTP clients where possible, pin dependencies in an isolated environment, and remove unused install permissions from local workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardirby/skills/youdotcom-api)
- [You.com API platform](https://you.com/platform)
- [You.com Search Operators](https://docs.you.com/search/search-operators)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, JSON examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YDC_API_KEY. Outputs may include cited Markdown answers, raw search result metadata, extracted HTML or Markdown page content, and endpoint-specific request or response schemas.]

## Skill Version(s):

3.0.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
