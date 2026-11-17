## Description:

Publishes a text, link, image or video post to the user's personal LinkedIn profile through the official Posts API after the user approves it. Use when the user wants to post on LinkedIn. Company page posting needs a separately approved Community Management API app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare and publish user-approved text, link, image, or video posts to a personal LinkedIn profile. Company-page posting requires a separately approved Community Management API app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sign-in callback receives sensitive authentication response parameters.

Mitigation: Use an HTTPS callback URL you control and avoid copying the supplied third-party URL.

Risk: The skill depends on socialkit-social-core, which is outside this release's inspected package.

Mitigation: Review socialkit-social-core separately before use.

Risk: Published posts are public and may appear on the wrong LinkedIn account if the wrong account is connected.

Mitigation: Connect only the intended account and approve each exact post after reviewing it.

## Reference(s):

- [LinkedIn setup guide](artifact/references/setup.md)
- [LinkedIn Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
- [LinkedIn authorization code flow](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow)
- [LinkedIn API versioning](https://learn.microsoft.com/en-us/linkedin/marketing/versioning)
- [ClawHub release page](https://clawhub.ai/ahmadhussain0335/skills/socialkit-linkedin-post)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown guidance, JSON post configuration, and a LinkedIn post]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts are published to the user's personal LinkedIn profile after explicit approval.]

## Skill Version(s):

0.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
