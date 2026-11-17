## Description:

douyin:api - 抖音开放平台 API

This skill is ready for commercial/non-commercial use.

## Publisher:

[lentiancn](https://clawhub.ai/user/lentiancn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill as a Douyin Open Platform API reference for obtaining a client_token and understanding request parameters, response fields, and common error codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin app credentials such as client_secret could be exposed in shared logs, prompts, or copied curl examples.

Mitigation: Confirm the intended Douyin endpoint before use and avoid placing production client_secret values in shared logs or prompts.

Risk: Using production client_key or client_secret values in a test environment can invalidate production tokens and disrupt live integrations.

Mitigation: Keep test and production Douyin credentials separate and verify the target environment before requesting a client_token.

## Reference(s):

- [douyin.open.client.token API index](references/apidocs/apis.md)
- [douyin.open.client.token reference](references/apidocs/douyin.open.client.token.md)
- [Douyin client_token endpoint](https://open.douyin.com/oauth/client_token/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with API tables and inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents the Douyin client_token request and response; does not execute code.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
