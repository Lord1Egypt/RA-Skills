## Description:

Publishes an Instagram image, carousel, Reel or Story to a Business or Creator account through the official Instagram Graph API, after validating caption limits and getting the user's approval. Use when the user wants to post to Instagram. Personal Instagram accounts are not supported by the API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and publish approved Instagram images, carousels, Reels, or Stories to a linked Business or Creator account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing the wrong account, caption, or media could create an unintended public post.

Mitigation: Review the account, caption, and media before approving each post in the user's terminal.

Risk: Exposed Meta app secrets or access tokens could allow unauthorized account access.

Mitigation: Protect the stored tokens and app secret, keep them out of repositories, and restrict credential file permissions.

Risk: The Instagram publishing workflow depends on separate authentication and approval skills.

Mitigation: Assess those companion skills before installing them; skip Threads setup when using Instagram only.

## Reference(s):

- [Meta setup](references/setup.md)
- [Instagram Content Publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- [Instagram Graph API Error Codes](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/error-codes)
- [ClawHub release](https://clawhub.ai/ahmadhussain0335/skills/socialkit-instagram-post)

## Skill Output:

**Output Type(s):** [Published Instagram content, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Instagram image, carousel, Reel, or Story; setup and review guidance in Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before publishing; Instagram images must be public JPEG URLs, carousels contain 2 to 10 items, and API scheduling is unavailable.]

## Skill Version(s):

0.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
