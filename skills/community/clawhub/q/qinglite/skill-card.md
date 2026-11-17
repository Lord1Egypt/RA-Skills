## Description:

Simulates login to Qinglite (qinglite.cn) to retrieve a token, or uses an existing token to publish content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccf22222](https://clawhub.ai/user/ccf22222)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to log in to Qinglite with a phone verification code and publish articles, text, images, or videos using a token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login codes and tokens may be exposed through command output, command history, process arguments, or agent logs.

Mitigation: Use the skill only in protected environments, redact logs and command histories, and avoid sharing captured output that contains credentials.

Risk: A leaked token may allow another party to publish through the user's Qinglite account.

Mitigation: Treat tokens as secrets, rotate or revoke exposed tokens when possible, and confirm account ownership before publishing content.

## Reference(s):

- [Qinglite mobile login API endpoint](https://www.qinglite.cn/api/interface/user/user_mobile/login)
- [Qinglite content creation API endpoint](https://www.qinglite.cn/api/interface/content/news/create)

## Skill Output:

**Output Type(s):** [text, shell commands, API calls]

**Output Format:** [Plain text command output and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Qinglite login tokens or publish status returned by API calls.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
