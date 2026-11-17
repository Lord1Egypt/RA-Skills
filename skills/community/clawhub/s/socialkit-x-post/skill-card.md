## Description:

Publishes a post, image or video post, or poll on X (Twitter) through the official X API v2 after showing the pay-per-use cost and getting the user's approval. Use when the user wants to post or tweet on X.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT

## Use Case:

External users can prepare and publish text posts, posts with images or video, and polls to X after reviewing and approving the content and estimated API charge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The separate socialkit-social-core dependency affects the posting workflow.

Mitigation: Review socialkit-social-core before use.

Risk: Publishing from the wrong account or exposing locally stored access tokens.

Mitigation: Connect only the intended account and protect the locally stored tokens.

Risk: An unintended post or unexpected pay-per-use charge.

Mitigation: Review the exact post and media and the estimated charge, then approve before publishing.

## Reference(s):

- [Skill release on ClawHub](https://clawhub.ai/ahmadhussain0335/skills/socialkit-x-post)
- [X setup guide](artifact/references/setup.md)
- [X API pricing](https://docs.x.com/x-api/getting-started/pricing)
- [X developer guidelines](https://docs.x.com/developer-guidelines)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON post data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates text posts, image or video posts, or polls for X.]

## Skill Version(s):

0.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
