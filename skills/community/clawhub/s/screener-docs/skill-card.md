## Description:

Downloads annual reports, earnings-call transcripts, investor presentations, and credit rating reports for listed Indian companies from links on Screener.in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swblacksmith6](https://clawhub.ai/user/swblacksmith6)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and researchers use this skill to collect a listed Indian company's recent filings and related documents in a local folder for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloads from Screener.in-linked third-party sites save files locally.

Mitigation: Use a dedicated output folder and review downloaded files before opening or sharing them.

Risk: Ambiguous company names can select the wrong company's documents.

Mitigation: Use the match-list or dry-run option to confirm the company before downloading.

Risk: An optional Screener.in session cookie may expose account access if handled carelessly.

Mitigation: Do not set SCREENER_SESSIONID unless login is required, and keep the cookie private.

Risk: Unpinned Python dependencies can change between installations.

Mitigation: Pin and review dependency versions for reproducible deployments.

## Reference(s):

- [Screener Docs on ClawHub](https://clawhub.ai/swblacksmith6/skills/screener-docs)
- [Screener.in](https://www.screener.in)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [Downloaded company documents, a JSON manifest, and a text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents are grouped by company symbol and category; the manifest records source URLs and download statuses.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
