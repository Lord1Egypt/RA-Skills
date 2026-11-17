## Description:

Uses the Baidu Qianfan web search API to retrieve real-time web results for questions that need current information, fact checking, or source-backed answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Baidu-backed web searches, receive structured search results, and answer user questions with current source material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Baidu Qianfan for web retrieval.

Mitigation: Use the skill only for queries appropriate for Baidu processing, and avoid sensitive or regulated data unless approved.

Risk: The skill requires a Baidu Qianfan API key through BAIDU_API_KEY or local configuration.

Mitigation: Prefer platform-managed environment variables, avoid exposing secrets in chats, logs, or screenshots, and rotate the key if disclosure is suspected.

Risk: Dependency installation uses package metadata without an accompanying lockfile in the artifact.

Mitigation: Pin dependencies with a lockfile before deploying in higher-trust environments.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sunshine-del-ux/skills/sunshine-baidu-web-search)
- [Publisher profile](https://clawhub.ai/user/sunshine-del-ux)
- [Baidu Qianfan API documentation](https://cloud.baidu.com/doc/qianfan-api/s/Wmbq4z7e5)
- [LeiAIBot website](https://leiaibot.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON search results plus Markdown answer guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY; default result count is 20 and the maximum is 50.]

## Skill Version(s):

1.0.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
