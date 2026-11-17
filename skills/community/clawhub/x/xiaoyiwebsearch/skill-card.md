## Description:

Uses the Huawei Cloud AI web search API to retrieve real-time web content for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flp516](https://clawhub.ai/user/flp516)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill when they need current web search results, especially for Chinese-language information, news, and fact-checking tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an embedded bearer token that should be treated as exposed.

Mitigation: Rotate or revoke the token before use, remove it from source code, and inject credentials through a secret store or environment variable.

Risk: Dependency packaging is risky, including lockfile sources that should be regenerated with HTTPS and patched versions.

Mitigation: Regenerate the lockfile from a trusted HTTPS registry, review the resulting dependency tree, and keep dependencies patched.

Risk: Search queries are sent to Huawei Cloud.

Mitigation: Avoid confidential search terms unless the user accepts that query data is handled by Huawei Cloud.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flp516/skills/xiaoyiwebsearch)
- [Huawei Cloud AI webSearch endpoint](https://connect-api.cloud.huawei.com/api/aiNetworking/v1/webSearch)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Console text or JavaScript-returned search result arrays, usually summarized by the agent in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search count is configurable and capped by the wrapper at 20 results.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
