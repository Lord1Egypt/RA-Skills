## Description:

Publishes or schedules a Mastodon post with optional media or a poll on the user's instance after the user approves it. Use when the user wants to toot or post on Mastodon or the fediverse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

People using Mastodon can draft, validate, and publish or schedule a text post, media post, or poll on their own instance. The skill presents the final post for user approval before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The separate socialkit-social-core approval helper was not included in the reviewed release.

Mitigation: Review that dependency before use and confirm its approval behavior.

Risk: The Mastodon access token and any env.sh file containing it are sensitive credentials.

Mitigation: Protect the token and its environment file, and verify the configured HTTPS instance.

Risk: Post visibility defaults to public, and publishing sends the selected text and attachments to the configured instance.

Mitigation: Review the text, attachments, visibility, and schedule before approving the post.

## Reference(s):

- [Mastodon setup](references/setup.md)
- [Mastodon status API documentation](https://docs.joinmastodon.org/methods/statuses/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON post draft and a Mastodon post or scheduled post]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional media with alt text and polls; publishing follows user approval.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
