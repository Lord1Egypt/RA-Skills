## Description:

Retrieves TianAPI's real-time all-network hot search ranking, aggregating trending events from platforms such as Weibo, Douyin, Baidu, and NetEase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to fetch current cross-platform trending topics from TianAPI and present each topic with its digest and heat score. It is useful when a workflow needs a quick snapshot of Chinese internet hot-search topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a TianAPI API key, and passing secrets on the command line or storing them in scripts/.env can expose them through shell history, logs, shared URLs, or committed files.

Mitigation: Use a dedicated low-privilege key through the TIANAPI_NETWORK_HOT_KEY environment variable, do not commit scripts/.env, and rotate the key if it may have been exposed.

## Reference(s):

- [TianAPI Network Hot API](https://www.tianapi.com/apiview/223)
- [ClawHub skill page](https://clawhub.ai/workxin/skills/tianapi-network-hot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or console text summarizing hot-search items; the helper script returns structured JSON internally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a TIANAPI_NETWORK_HOT_KEY API key.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
