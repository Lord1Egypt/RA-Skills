## Description:

提供多种文本转换功能的MCP服务器，包括大小写转换、反转字符串、检测回文等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route simple text transformation requests to XiaoBenYang MCP tools, including case conversion, character reversal, palindrome checks, word counts, character counts, trimming, and capitalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text is sent to a third-party API for processing.

Mitigation: Use the skill only with text that is acceptable to share with XiaoBenYang; avoid secrets, private documents, source code, personal data, and regulated content.

Risk: The XBY API key is stored in a local plaintext .env file.

Mitigation: Use a dedicated, revocable API key, restrict access to the local workspace, and rotate or remove the key after use.

Risk: The skill's text utilities depend on remote service availability and behavior.

Mitigation: Review the skill before deployment and treat API results as remote responses that may fail, change, or require user-facing error handling.

## Reference(s):

- [XiaoBenYang](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured dictionary with success, raw, and message fields; agents summarize the raw API response for users.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value and sends text inputs to XiaoBenYang's API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
