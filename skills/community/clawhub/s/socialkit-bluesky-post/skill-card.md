## Description:

Publishes a Bluesky post with optional images or a link card through the AT Protocol, using the user's app password, after the user approves it. Use when the user wants to post on Bluesky.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT

## Use Case:

External users can prepare and publish user-approved Bluesky posts, including text posts, posts with images, and link cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A published post is public and appears under the user's Bluesky account.

Mitigation: Review the final text and images before approving publication.

Risk: The skill uses an app password and a cached Bluesky session to publish posts.

Mitigation: Use a dedicated app password, protect the credential file and cached session, and configure only a trusted Bluesky service. Review socialkit-social-core separately because its approval tooling is not included here.

## Reference(s):

- [Bluesky setup](references/setup.md)
- [AT Protocol OAuth client documentation](https://bsky.network/docs/oauth-client)
- [Bluesky rate limits](https://bsky.network/docs/rate-limits)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls]

**Output Format:** [Bluesky post text with optional image alt text or link card metadata; post.json input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts are limited to 300 characters; image posts support 1 to 4 images up to 2 MB each and require alt text. Publishing requires user approval.]

## Skill Version(s):

0.3.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
