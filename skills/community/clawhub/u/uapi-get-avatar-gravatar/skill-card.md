## Description:

Uses the UAPI GET /avatar/gravatar endpoint to look up Gravatar avatar images and explain parameters, calling behavior, and response codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user asks for a Gravatar avatar lookup through UAPI. It helps confirm required query parameters, choose email or MD5 hash input, and prepare the GET /avatar/gravatar request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email-based lookups send an email identifier to an external avatar API.

Mitigation: Prefer the lowercased MD5 hash parameter when available, and avoid submitting another person's raw email address unless sharing that identifier is appropriate.

## Reference(s):

- [Quick Start](references/quick-start.md)
- [Get Gravatar Avatar Operation](references/operations/get-avatar-gravatar.md)
- [Image Resource](references/resources/Image.md)
- [UAPI Base API](https://uapis.cn/api/v1)
- [UAPI](https://uapis.cn)

## Skill Output:

**Output Type(s):** [guidance, API Calls, configuration]

**Output Format:** [Markdown guidance with endpoint, parameter, authentication, and response-code details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide calls that return image binary data from the external avatar API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
