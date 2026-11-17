## Description:

QA pass to catch and fix AI-pattern tells in tweets before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media editors use this skill to audit existing tweets for AI-pattern tells and rewrite flagged posts while preserving the core message, voice, requested hashtags, and 280-character limit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Metadata is inconsistent about outbound network access and Ollama use.

Mitigation: Review the metadata before installation and scope any Ollama or local model use to manual style checking.

Risk: Tweet rewrites can unintentionally change voice, meaning, or publishing constraints.

Mitigation: Review each humanized tweet before publishing and preserve user-requested hashtags, voice, and the 280-character limit.

## Reference(s):

- [Tweet Humanizer ClawHub skill page](https://clawhub.ai/nissan/skills/tweet-humanizer)
- [Companion long-form humanizer skill](https://clawhub.com/skills/reddi-humanizer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown sections listing the original tweet, detected flags, humanized rewrite, and character count.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rewrites should remain within 280 characters and preserve explicitly requested hashtags.]

## Skill Version(s):

1.0.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
