## Description:

Take a blog post URL or text and generate social media posts from it. Use when repurposing content for Twitter, LinkedIn, or creating promotional posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to turn blog URLs or supplied text into ready-to-edit social posts, Twitter threads, and hook variations for Twitter or LinkedIn.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied URLs are fetched from the agent environment without destination safeguards.

Mitigation: Only use trusted public article URLs, and avoid localhost, private-network, and cloud metadata URLs.

Risk: Generated posts may be generic or may not faithfully summarize the source.

Mitigation: Manually review and edit generated posts before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kryzl19/skills/strd-social-post-gen)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown-formatted social media copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces five posts, numbered thread tweets, or ten hook variations depending on the selected script; platform, tone, brand attribution, and hashtags can be configured with environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
