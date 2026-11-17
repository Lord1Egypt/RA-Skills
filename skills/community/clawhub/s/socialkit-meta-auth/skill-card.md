## Description:

Connects the user's own Meta app to their Facebook Pages, linked Instagram professional accounts and Threads profile, and stores the tokens securely. Use before the first Facebook, Instagram or Threads post, when a Meta token expired or was revoked, or to check which Pages and accounts are connected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media account owners use this skill to authorize their own Meta app for Facebook Pages, linked professional Instagram accounts, and Threads. They use it to start or complete sign-in and check which accounts are connected before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Locally stored Meta tokens can grant access to connected accounts if exposed.

Mitigation: Protect the local token directory and revoke authorization through Meta when access is no longer needed.

Risk: Authorizing accounts grants the permissions selected for the Meta app.

Mitigation: Review the accounts and publishing permissions granted, and enable engagement permissions only when needed.

## Reference(s):

- [Meta setup guide](references/setup.md)
- [SocialKit Meta Auth on ClawHub](https://clawhub.ai/ahmadhussain0335/skills/socialkit-meta-auth)
- [Facebook Login for Business](https://developers.facebook.com/docs/facebook-login/facebook-login-for-business/)
- [Instagram content publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- [Threads API getting started](https://developers.facebook.com/documentation/threads/get-started)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON account status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports connected accounts and posting eligibility or token expiry without displaying tokens or app secrets.]

## Skill Version(s):

0.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
