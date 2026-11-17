## Description:

Trend Scope helps an agent generate public-opinion trend reports from Feedax data, including sentiment, geography, keywords, media sources, and time trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longgggggg](https://clawhub.ai/user/longgggggg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor brands, markets, competitors, and public events, then generate summarized public-opinion analysis reports from requested search terms and filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys, search terms, and filters may be sent to the Feedax report service over unencrypted HTTP.

Mitigation: Install only if the Feedax service is trusted, avoid sensitive queries, and ask the publisher to switch API traffic to HTTPS.

Risk: Generated HTML reports may be unsafe to open or share without review.

Mitigation: Prefer json-only output when possible, review generated reports before opening or sharing them, and ask the publisher to escape HTML output and validate links.

Risk: The HTML report depends on externally loaded chart JavaScript.

Mitigation: Use JSON or Markdown output for sensitive workflows, or require bundled or integrity-protected chart assets before relying on HTML reports.

## Reference(s):

- [Trend Scope on ClawHub](https://clawhub.ai/longgggggg/skills/trend-scope)
- [Feedax service](https://www.feedax.cn)
- [Area code reference data](artifact/assets/area_codes.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, configuration]

**Output Format:** [Conversational summary plus saved JSON, Markdown, and HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and FEEDAX_REPORT_API_KEY; json-only mode can limit output to JSON.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
