## Description:

Publishes a Threads post (text with optional link, image, video or carousel) through the official Threads API after validating the 500-character and link limits and getting the user's approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media operators use the skill to prepare, validate, and publish user-approved text, link, image, video, or carousel posts to Threads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing creates a public Threads post and may have immediate external effects.

Mitigation: Validate the draft, review the exact content, and explicitly approve it before publishing.

Risk: Threads credentials can grant access to the user's account.

Mitigation: Protect local credential files and keep credentials out of repositories.

Risk: Media is fetched from publicly accessible URLs.

Mitigation: Use only public HTTPS media URLs that are intended to be available to Threads and viewers.

## Reference(s):

- [Meta and Threads setup guide](references/setup.md)
- [Threads API documentation](https://developers.facebook.com/documentation/threads/get-started)
- [SocialKit Threads Post on ClawHub](https://clawhub.ai/ahmadhussain0335/skills/socialkit-threads-post)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Threads post content and a publication result, including a permalink when available]

**Output Parameters:** [A single text post with an optional link, image, video, or carousel]

**Other Properties Related to Output:** [Validates Threads text and link limits; publishing requires user approval; media must be available at public HTTPS URLs.]

## Skill Version(s):

0.3.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
