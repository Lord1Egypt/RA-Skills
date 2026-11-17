## Description:

小红书评论分析 helps content creators, operators, brands, and ecommerce teams analyze Xiaohongshu note comments for sentiment, audience intent, user profile signals, and practical optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinherog-star](https://clawhub.ai/user/allinherog-star)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketing operators, brand teams, and ecommerce teams use this skill when they have a Xiaohongshu note link and need comment sentiment, audience intent, user profile clues, and next-step content or conversion recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided Xiaohongshu links, parsed note metadata, and analysis requests are sent to the AI Skills service using the configured API key.

Mitigation: Install only when that data transfer is acceptable for the intended use case, and manage AISKILLS_API_KEY as a secret.

Risk: Changing AISKILLS_BASE_URL changes where requests and the API key are sent.

Mitigation: Review or control AISKILLS_BASE_URL before running the skill, and leave it at the default service endpoint unless a trusted endpoint is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/allinherog-star/skills/xhs-sentiment-dashboard)
- [Input Form Schema](references/form-schema.json)
- [Skill Metadata](references/skill.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON response with comment sentiment, analysis summary, labeled comments, and operating recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaohongshu note link and AISKILLS_API_KEY; returns a single completed analysis task result after polling.]

## Skill Version(s):

1.0.1 (source: server release metadata and user-provided changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
