## Description:

Write and publish Tumblr-native posts with AI, including topic shaping through YouMind, long-form and image-led post creation, notes and activity review, and queue control for a Tumblr blog connected in YouMind.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and publishing teams use this skill to draft or adapt content into Tumblr-native text and photo posts, publish through a connected YouMind account, and review Tumblr feedback or queue state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a YouMind API key tied to a connected Tumblr account.

Mitigation: Store the key only in the expected YouMind config file, review the configured base_url before use, and use an account whose permissions match the intended publishing scope.

Risk: The skill can publish posts, change queue order, shuffle queued posts, and delete Tumblr posts.

Mitigation: Require explicit user confirmation before publish, queue, or delete actions, and prefer preview or draft mode before public posting.

Risk: Generated or adapted Tumblr content may be unsuitable for the target audience or may include fragile HTML.

Mitigation: Review generated drafts, keep HTML simple, verify tags and images, and inspect result links after publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindy-youmind/skills/youmind-tumblr-article)
- [YouMind API key settings](https://youmind.com/settings/api-keys?utm_source=youmind-tumblr-article)
- [YouMind connector settings](https://youmind.com/settings/connector?utm_source=youmind-tumblr-article)
- [Tumblr platform DNA](artifact/references/platform-dna.md)
- [Tumblr publishing pipeline](artifact/references/pipeline.md)
- [YouMind Tumblr OpenAPI reference](artifact/references/api-reference.md)
- [Content generation playbook](artifact/references/content-generation-playbook.md)
- [Content adaptation playbook](artifact/references/content-adaptation-playbook.md)
- [Media playbook](artifact/references/media-playbook.md)
- [Engagement playbook](artifact/references/engagement-playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, simple HTML drafts, CLI commands, and structured publishing result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Tumblr draft HTML files and may return Tumblr post IDs, post state, URLs, notes, notifications, followers, limits, or queue status.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
