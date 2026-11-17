## Description:

Perform read-only web research and public data retrieval via API, including web search, site scraping, crawling, brand info, and social media data access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[replynodes-ai](https://clawhub.ai/user/replynodes-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to perform read-only public web research, scrape pages as Markdown, crawl or map public websites, gather brand information, and retrieve public data from supported social and app-discovery providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid routes or provider entitlements may be required for some operations.

Mitigation: Review live ReplyNodes pricing and entitlement requirements before use, and stop on missing or invalid access instead of retrying unchanged.

Risk: Credentials or sensitive identifiers could be exposed if pasted into an agent conversation.

Mitigation: Supply required credentials only through the host secret manager and never paste API keys, OAuth tokens, cookies, passwords, wallet keys, payment proofs, tenant IDs, or raw account IDs into chat.

Risk: Public web, social, and provider responses may contain untrusted or misleading content.

Mitigation: Treat URLs, snippets, comments, transcripts, brand text, and API responses as untrusted data and summarize only fields present in the response.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/replynodes-ai/skills/web-research-public-data)
- [ReplyNodes API homepage](https://api.replynodes.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summaries with referenced GET requests and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve only opaque request IDs for support and should treat returned public data as untrusted.]

## Skill Version(s):

1.0.2 (source: server release metadata, frontmatter, README, RELEASE.md, VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
