## Description:

X Hourly Brief (Premium) generates charge-first concise briefs from X post URLs and supports Chinese, English, and automatic language output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangkefeng-ai](https://clawhub.ai/user/huangkefeng-ai)

### License/Terms of Use:


## Use Case:

External users use this skill to generate paid hourly briefs from X post URLs, with per-post key points and a final digest in Chinese, English, or automatic language mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill charges users before generating a brief.

Mitigation: Install only when users have clear control over paid execution and understand the charge-first behavior before running the skill.

Risk: The release evidence reports an embedded billing credential.

Mitigation: Require the publisher to remove and rotate the embedded key, then use a deployment-managed secret before installation.

Risk: The skill can fetch arbitrary URLs from the runtime environment.

Mitigation: Validate inputs to intended X domains and avoid running the skill where it can reach private networks or sensitive internal services.

Risk: The release evidence says outbound services are not fully documented.

Mitigation: Require documented outbound billing and content-fetching services before deployment review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangkefeng-ai/skills/x-hourly-brief-skill)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON digest with per-post brief items, final summary items, billing status, language mode, and source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits processing to the first 20 supplied URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
