## Description:

Fetches a web page URL through a paid x402-enabled service and returns the main cleaned text or markdown without navigation, ads, or boilerplate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rccola990-cloud](https://clawhub.ai/user/rccola990-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to retrieve readable page content for summarization, fact extraction, or research without operating their own web scraper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested page URLs are sent to the third-party scraping service at store.agentexchange.work.

Mitigation: Use public URLs only, and avoid private, internal, localhost, authenticated, or sensitive document URLs.

Risk: Returned page content can contain untrusted or misleading text from the source website.

Mitigation: Treat fetched content as untrusted data and verify important claims before using them in decisions or downstream outputs.

Risk: Calls may require x402 payment in USDC on Base.

Mitigation: Review the 402 payment terms and price before authorizing each paid request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rccola990-cloud/skills/url-to-clean-content)
- [AgentExchange scrape endpoint](https://store.agentexchange.work/web/scrape?url=<PAGE_URL>)
- [AgentExchange samples](https://store.agentexchange.work/samples)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown or cleaned text returned from a URL fetch, with endpoint usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an x402-capable client and may involve a per-call USDC payment disclosed before payment.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
