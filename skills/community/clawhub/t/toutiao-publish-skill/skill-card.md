## Description:

Toutiao Publish.Skill helps an agent generate an article from user-provided keywords, log in to Toutiao, fill in the title and body, upload a cover image, and publish the article.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuxucai](https://clawhub.ai/user/liuxucai)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and agents use this skill to create and publish Toutiao articles from keyword prompts, including account login, article drafting, cover upload, publish confirmation, and success checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a logged-in Toutiao account and publish live public content.

Mitigation: Require manual preview and explicit user confirmation before any final publish action.

Risk: The workflow involves phone and password login steps for a real account.

Mitigation: Avoid exposing credentials in chat, logs, screenshots, or reusable scripts; prefer secure session handling where available.

Risk: Cover image prompts are sent to an external image generation service and downloaded locally.

Mitigation: Review prompts and generated images before upload, and avoid sending sensitive or private content to the external service.

Risk: Local puppeteer scripts can interact with a shared browser session through CDP.

Mitigation: Review scripts before execution and run them only in the intended browser profile and workspace.

## Reference(s):

- [Toutiao Publish.Skill ClawHub Page](https://clawhub.ai/liuxucai/skills/toutiao-publish-skill)
- [Detailed Toutiao Publishing Rules](references/detailed-rules.md)
- [Toutiao Publishing Page](https://mp.toutiao.com/profile_v4/graphic/publish)
- [Pollinations Image Generation Endpoint](https://image.pollinations.ai/prompt/{prompt}?width=800&height=600&nologo=true)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce article title and body text, browser automation snippets, local script commands, and publication verification guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
