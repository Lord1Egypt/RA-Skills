## Description:

Ethical web data extraction with robots exclusion protocol adherence, throttled scraping requests, and privacy-compliant handling ("Scrape responsibly!").

This skill is ready for commercial/non-commercial use.

## Publisher:

[10oss](https://clawhub.ai/user/10oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Skrape to plan and produce responsible web-scraping guidance, JavaScript implementation patterns, throttled request handling, audit logging, and data-stewardship checks before extracting public web data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included robots.txt verification pattern can permit scraping when permission was not actually verified.

Mitigation: Treat the code as guidance, replace the robots.txt checker with a maintained RFC-compliant parser, and fail closed or require explicit user approval when verification is unknown.

Risk: Web scraping can create legal, privacy, or platform-terms exposure when applied to restricted, personal, or copyrighted content.

Mitigation: Review robots.txt, terms of service, available APIs, data classification, and applicable privacy obligations for each target before collecting or retaining data.

## Reference(s):

- [Skrape ClawHub Skill Page](https://clawhub.ai/10oss/skills/skrape)
- [Implementation Patterns](artifact/code.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript code blocks and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compliance checks, throttling and backoff patterns, audit logging suggestions, and data-handling cautions.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
