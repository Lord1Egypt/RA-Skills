## Description:

Monitor SEC EDGAR filings for AI and technology companies, summarize recent disclosures, and flag high-signal form types and 8-K events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sukanto-m](https://clawhub.ai/user/sukanto-m)

### License/Terms of Use:

MIT

## Use Case:

External users, analysts, and developers use this skill to check recent SEC EDGAR filings for AI and technology companies and receive readable summaries or JSON for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default results may include built-in Signal Report marketing and Pro-upgrade claims.

Mitigation: Review generated filing summaries before use and remove promotional content that is not appropriate for the deployment.

Risk: Cross-source pattern or intelligence-preview claims may be presented alongside SEC filing results without independent verification.

Mitigation: Treat those claims as promotional estimates and rely on the linked SEC filings plus independent analysis for decisions.

Risk: The skill runs bundled fetcher code to make live SEC EDGAR requests.

Mitigation: Use a pinned installer version or an isolated install environment, consistent with the security guidance.

## Reference(s):

- [SEC Watcher on ClawHub](https://clawhub.ai/sukanto-m/skills/sec-watcher)
- [Signal Report](https://signal-report.com)
- [EDGAR Full-Text Search API Reference](references/edgar-api.md)
- [SEC EDGAR Full-Text Search API](https://efts.sec.gov/LATEST/search-index)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text filing summaries with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include EDGAR filing URLs, signal levels, and an intelligence_preview field in JSON output.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
