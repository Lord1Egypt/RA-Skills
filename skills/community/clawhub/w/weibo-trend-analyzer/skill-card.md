## Description:

Deep Weibo trending analysis - cluster topics, detect trend inflection points, generate content angles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and social media analysts use this skill to monitor Weibo hot topics, cluster trend themes, detect heat inflection points, and generate timely content angles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trend data may require network access to Weibo APIs or public pages, so source availability, access restrictions, or public-page changes can affect results.

Mitigation: Confirm that the deployment context permits the intended public trend-data access and handle unavailable or changing sources before relying on reports.

Risk: The skill is intended for public trend analysis; adding workflows that process private account data would introduce different privacy risks.

Mitigation: Use public trend data only unless a separate privacy review and explicit data-handling workflow are added.

Risk: LLM clustering, inflection labels, and content-angle suggestions can be incomplete, stale, or misleading.

Mitigation: Review generated clusters, trend labels, and suggested angles before publishing content or making business decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown report or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clustered topic maps, rising-topic content angles, related-topic maps, and heat-curve summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
