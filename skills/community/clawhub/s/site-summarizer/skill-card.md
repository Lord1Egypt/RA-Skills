## Description:

Site Summarizer fetches URLs, extracts HTML page content, and returns summaries with metadata and lightweight analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcompile](https://clawhub.ai/user/cloudcompile)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to summarize public web pages and extract page metadata, language, keywords, word counts, and read-time estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetcher can reach unintended internal network addresses.

Mitigation: Run the skill only in a constrained environment with egress controls or an allowlist for public domains, and avoid hosts that can reach internal admin services or cloud metadata endpoints unless SSRF protections are fixed.

Risk: Fetched content may be stored locally with limited privacy safeguards.

Mitigation: Avoid sensitive or signed URLs and disable or tightly restrict the cache directory when handling sensitive browsing targets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloudcompile/skills/site-summarizer)
- [Publisher profile](https://clawhub.ai/user/cloudcompile)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON with extracted content, summary, metadata, analysis, status, and cache indicator fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include locally cached fetch results; cache directory, cache TTL, and resolved-IP visibility are configurable with environment variables.]

## Skill Version(s):

4.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
