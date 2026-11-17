## Description:

Xiaohongshu Matrix Manager helps agents use the Hongshu Matrix API to search Xiaohongshu notes, retrieve note details, publish image-text notes, list accounts, check API usage, and manage accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[admin6016](https://clawhub.ai/user/admin6016)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and run authenticated Hongshu Matrix API requests for Xiaohongshu account management, content search, usage reporting, and publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or unpublished account content could be exposed if placed in URLs or sent over plaintext HTTP.

Mitigation: Use scoped API keys in request headers, do not put keys in URLs, and avoid authenticated or publishing operations unless HTTPS is available.

Risk: Publishing requests can affect public Xiaohongshu accounts and content.

Mitigation: Require manual confirmation of the exact account, title, content, image URLs, topics, and schedule before any publish request.

## Reference(s):

- [API Reference](references/api.md)
- [Hongshu Matrix Platform](https://hongshujuzhen.com)
- [ClawHub Skill Page](https://clawhub.ai/admin6016/skills/xhsmatrixmanager)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python request examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce authenticated HTTP API requests that use user-provided API keys.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
