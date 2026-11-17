## Description:

Tracks product launch buzz and reactions on Twitter using apidojo's Twitter Search scraper, returning tweet volume, sentiment distribution, top voices, geographic spread, and a buzz score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Product marketing, PR, competitive analysis, and launch teams use this skill to monitor Twitter/X reactions to product launches, competitor announcements, and campaign keywords. It helps an agent collect matching posts, classify buzz intensity, summarize sentiment, identify prominent voices, and report launch signal quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Launch, competitor, or campaign search terms are sent to Apify/apidojo for scraping.

Mitigation: Use the skill only with search terms that are acceptable to share with that service and avoid including confidential launch details unless approved.

Risk: APIFY_TOKEN exposure could allow unauthorized actor runs or dataset access.

Mitigation: Store APIFY_TOKEN in environment or secret storage, avoid token-bearing URLs in logs and support tickets, and prefer SDK or header-based authentication.

Risk: Unbounded collection can increase cost and data volume.

Mitigation: Set maxItems and relevant search filters before running the scraper.

Risk: Older product launches can produce misleadingly low buzz measurements.

Mitigation: Run the workflow within the launch monitoring window and state timing limitations in the result summary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/tracking-product-launch-buzz-on-twitter)
- [API Dojo publisher profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables, with optional shell commands and JSON or CSV result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include tweet counts, sentiment distribution, top voices, geographic spread, buzz classifications, and buzz scores.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
