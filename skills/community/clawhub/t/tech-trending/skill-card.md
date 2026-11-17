## Description:

Tech Trending helps agents monitor technology trend signals, market data, and startup opportunity criteria using an API-backed signal database and an included CLI script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, analysts, and investors use this skill to collect and interpret cross-platform technology trend signals for market research, startup idea validation, investment signal review, and opportunity assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trend queries are sent to an external Tencent Cloud endpoint.

Mitigation: Avoid sending confidential strategy, customer, or proprietary research terms unless the endpoint's handling and retention are acceptable.

Risk: The analysis lens is China/domestic-market focused and may not fit every geography or market.

Mitigation: Review outputs against the target market context before using them for business or investment decisions.

Risk: The shared /review endpoint is unrelated to trend monitoring and may receive private code if used incorrectly.

Mitigation: Do not submit private code to that endpoint unless the publisher documents appropriate data handling and retention terms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/tech-trending)
- [Publisher profile](https://clawhub.ai/user/lm203688)
- [Tech Trending API endpoint](https://1341839497-kvq7g9wk8p.ap-guangzhou.tencentscf.com)
- [SKILL.md](artifact/SKILL.md)
- [trending.sh](artifact/scripts/trending.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown trend analysis and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included shell script returns API-derived trend signal clusters and methodology summaries; the artifact notes a 20 API calls/month free tier.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
