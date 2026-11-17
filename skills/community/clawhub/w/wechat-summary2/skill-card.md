## Description:

Summarizes WeChat Official Account articles from mp.weixin.qq.com links into concise Chinese prose or bullet points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mick2458pan](https://clawhub.ai/user/mick2458pan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to understand WeChat Official Account articles quickly by extracting article text and generating a brief Chinese summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback fetcher can request arbitrary URLs from the agent environment if a user supplies an untrusted link.

Mitigation: Require explicit user confirmation and validate URLs so fallback fetching is limited to trusted WeChat article URLs, ideally https://mp.weixin.qq.com.

Risk: Running the fetcher in an environment with access to internal services or metadata endpoints could expose sensitive network targets.

Mitigation: Run the skill only in a network-restricted environment that cannot reach internal services or sensitive metadata endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mick2458pan/skills/wechat-summary2)
- [Publisher profile](https://clawhub.ai/user/mick2458pan)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Chinese plain text summary, with optional command output from the fallback article fetcher.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summary form adapts to article length: short prose for short articles, a paragraph for medium articles, and bullet points for long articles.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
