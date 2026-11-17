## Description:

Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling. Supports both direct HTTP scraping and managed scraping via SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan and perform web scraping workflows with robots.txt checks, terms review, rate limiting, and privacy-aware handling. It supports direct HTTP scraping patterns and managed extraction through SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Managed scraping may send URLs, page content, and contact details to SkillBoss as a third-party processor.

Mitigation: Use a dedicated API key and contact alias, avoid URLs containing secrets, and confirm third-party processing is acceptable for the target data.

Risk: Scraping when robots.txt cannot be verified can create compliance and terms-of-service exposure.

Mitigation: Require explicit approval before proceeding when robots.txt cannot be checked or returns ambiguous results.

Risk: Scrape logs may expose URLs, status details, page content, or user-provided contact information.

Mitigation: Sanitize logs and avoid storing sensitive URLs, personal data, or unnecessary page content.

Risk: LLM analysis of scraped pages can produce untrusted or misleading extracted data.

Mitigation: Treat model analysis as untrusted until validated against source pages and apply additional safeguards before using extracted results.

## Reference(s):

- [Code Patterns](artifact/code.md)
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-scrape)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python code examples and API call patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require SKILLBOSS_API_KEY for managed scraping workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
