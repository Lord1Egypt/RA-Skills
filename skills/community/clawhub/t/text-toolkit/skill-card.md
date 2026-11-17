## Description:

文本转换工具 is an MCP text utility that provides text conversion, formatting, analysis, hashing, UUID, lorem ipsum, and regex functions through the XiaoBenYang API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to handle routine text transformation, formatting, counting, hashing, UUID, lorem ipsum, and regex tasks. The skill routes a user's request to a matching API-backed tool and presents the returned result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text, proprietary documents, private source code, regulated data, tokens, or HMAC secrets may be sent to the XiaoBenYang API.

Mitigation: Do not use the skill with confidential or regulated inputs unless that remote processing is approved and disclosed to the user.

Risk: The skill stores the XiaoBenYang API key locally in a .env file.

Mitigation: Use a scoped API key, keep .env out of source control, restrict local file permissions, and rotate the key if exposure is suspected.

Risk: Server security evidence marks the release as suspicious because remote data exposure is under-disclosed.

Mitigation: Review the skill before installation and document its remote API behavior for users who invoke it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/text-toolkit)
- [cainingnk publisher profile](https://clawhub.ai/user/cainingnk)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown or plain text summaries of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls return success, raw, and message fields; agents should present the raw result clearly to the user.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
