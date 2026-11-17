## Description:

X Expert helps users draft, review, enrich, and publish X (Twitter) posts through a conversational workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thousandsky2024](https://clawhub.ai/user/thousandsky2024)

### License/Terms of Use:

MIT

## Use Case:

Social media operators, creators, and developers use this skill to plan X posts, collect supporting information, generate text or image prompts, review drafts, and optionally publish posts or threads through configured X account credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can directly post tweets, upload media, and delete tweets with live X account credentials.

Mitigation: Use least-privilege X tokens, test with a non-production account first, and require manual review before invoking publishing, media upload, or delete scripts.

Risk: Generated post text or media may be inaccurate, misleading, or unsuitable for the target account.

Mitigation: Review every final post, thread, generated image, and media path before publication.

Risk: The skill depends on multiple third-party APIs and local environment variables for search, image generation, and X account access.

Mitigation: Store credentials only in environment variables, avoid sharing API keys, and configure only the services needed for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thousandsky2024/skills/x-expert)
- [Publisher profile](https://clawhub.ai/user/thousandsky2024)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational text with command-line script outputs and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce draft post text, thread content, image-generation prompts or URLs, search summaries, media upload results, tweet IDs, and tweet URLs.]

## Skill Version(s):

1.0.0 (source: package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
