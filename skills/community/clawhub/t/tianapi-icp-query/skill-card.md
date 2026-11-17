## Description:

查询网站ICP备案信息，包括备案号、主体名称、备案类型及审核时间等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Chinese website ICP filing details for a supplied domain, including filing number, subject name, filing type, filing status, and update time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The TianAPI key may be exposed through command history, logs, shared URLs, or a scripts/.env file.

Mitigation: Prefer TIANAPI_ICP_KEY as an environment variable, avoid passing keys in commands or URLs, restrict permissions on any .env file, and rotate the key if it may have been exposed.

Risk: The skill depends on external HTTPS requests to TianAPI and may fail when the API key is invalid, quota is exhausted, the API is not enabled, or the network times out.

Mitigation: Check TianAPI response codes, confirm the key and API entitlement before use, and retry only after distinguishing network errors from quota or authorization failures.

## Reference(s):

- [TianAPI ICP Query API](https://www.tianapi.com/apiview/118)
- [ClawHub Skill Page](https://clawhub.ai/workxin/skills/tianapi-icp-query)
- [TianAPI ICP API Endpoint](https://apis.tianapi.com/icp/index)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a TIANAPI_ICP_KEY API key; the helper script performs HTTPS requests to TianAPI.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
