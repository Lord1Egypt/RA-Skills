## Description:

Take a blog post URL or text and generate social media posts from it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to repurpose article URLs or supplied text into Twitter posts, LinkedIn posts, Twitter threads, and social post hooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to user-supplied URLs from the agent environment.

Mitigation: Use only public URLs, and avoid private, internal, localhost, cloud-metadata, or sensitive draft URLs unless the runtime blocks private-network egress or the skill validates destinations and limits redirects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kryzl19/skills/social-post-generator-agent)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with formatted social posts, numbered thread segments, hook variations, and brief usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output varies by PLATFORM, TONE, BRAND_NAME, HASHTAGS, and the supplied URL or text input.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
