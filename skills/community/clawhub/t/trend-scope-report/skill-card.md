## Description:

Generates public-opinion trend reports from Feedax API queries, including sentiment, geography, keyword, media, and time-trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longgggggg](https://clawhub.ai/user/longgggggg)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to turn natural-language monitoring requests into Feedax report CLI calls, then review summaries and saved public-opinion reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and report queries may be sent over an unencrypted HTTP endpoint.

Mitigation: Review before installing; do not use sensitive searches or production API keys unless the endpoint is changed to verified HTTPS.

Risk: Generated HTML reports may include unsafe untrusted content.

Mitigation: Escape report data before opening or sharing HTML reports, and review generated files before distribution.

Risk: Saved reports can contain sensitive search terms, filters, and result content.

Mitigation: Treat saved report files as sensitive and avoid entering directly identifying personal information in report queries.

Risk: Opening HTML reports contacts a third-party CDN for chart rendering.

Mitigation: Use only in environments where the CDN request is acceptable, or replace the external dependency with a vetted local asset.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/longgggggg/skills/trend-scope-report)
- [Feedax API Key Site](https://www.feedax.cn)
- [Artifact README](artifact/README.md)
- [Skill Usage Guide](artifact/skill.md)
- [Area Code Data](artifact/assets/area_codes.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Conversation summary plus saved JSON, Markdown, and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and FEEDAX_REPORT_API_KEY; reports default to the user's Desktop public-opinion report folder.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
