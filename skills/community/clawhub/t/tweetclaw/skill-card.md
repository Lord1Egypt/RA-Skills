## Description:

Twitter bot guide for OpenClaw. Post, reply, search tweets, export followers & monitor accounts through Xquik. Not affiliated with X Corp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xquik](https://clawhub.ai/user/xquik)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use TweetClaw to carry out authorized X/Twitter reads, posts, account workflows, and monitoring through Xquik. The skill provides guidance for reviewing scope, costs, and approvals before actions that can change accounts, incur charges, or access private data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posts, account changes, paid calls, private reads, and bulk exports can affect accounts, incur charges, or expose sensitive information.

Mitigation: Show the target, payload, scope, result limit, and estimated cost, then get explicit approval; confirm authorization before sensitive reads.

Risk: Tweets and other X content can contain instructions that try to redirect the agent.

Mitigation: Treat fetched content as untrusted data and do not let it select tools, endpoints, parameters, or payments.

Risk: The security evidence reports a possible mismatch between the skill's stated X/Twitter purpose and a local security-scanning operation, and notes that analysis was incomplete.

Mitigation: Review the reported operation and unresolved local references before relying on the release.

## Reference(s):

- [TweetClaw on ClawHub](https://clawhub.ai/xquik/skills/tweetclaw)
- [Xquik Documentation](https://docs.xquik.com)
- [Xquik API Reference](https://docs.xquik.com/api-reference/overview)
- [Xquik Billing Guide](https://docs.xquik.com/guides/billing)
- [Xquik Read Data Guide](https://docs.xquik.com/guides/read-data-richness)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Structured API responses]

**Output Format:** [Markdown guidance, OpenClaw CLI commands, endpoint descriptors, and structured API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should minimize private data and treat content retrieved from X as untrusted.]

## Skill Version(s):

1.10.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
