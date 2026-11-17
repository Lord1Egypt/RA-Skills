## Description:

Searches Qingbo Open Platform article and public-opinion data by keyword, time range, media type, and sentiment, then returns matching article details or count summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangqiang327](https://clawhub.ai/user/zhangqiang327)

### License/Terms of Use:

MIT

## Use Case:

Developers and users with Qingbo Open Platform credentials use this skill to search web article and public-opinion content by natural-language query, filter results by time, media source, or sentiment, and summarize either article listings or result counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Qingbo API credentials and user search terms to Qingbo over unencrypted HTTP.

Mitigation: Use only with non-sensitive searches until the publisher switches the API request to HTTPS if supported and documents exactly what data is sent externally.

Risk: Sensitive or ambiguous searches could expose user intent to an external service.

Mitigation: Confirm sensitive searches before execution and avoid submitting confidential terms through the skill.

## Reference(s):

- [Qingbo Search on ClawHub](https://clawhub.ai/zhangqiang327/skills/qingbo-search)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text search results or summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns article titles, URLs, publication times, media labels, sentiment labels, or aggregate counts depending on the query.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
