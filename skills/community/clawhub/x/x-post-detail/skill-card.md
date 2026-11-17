## Description:

Collect one X (Twitter) post and its replies with the official Gecho Bridge MCP tool when the user provides an X post URL and wants post content, author data, engagement, or comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect a known X (Twitter) post, available replies, author data, engagement, and comments through Gecho Bridge, then receive a concise summary and saved result path when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses Gecho Bridge and its Chrome extension with a logged-in X session, so collected X data may reflect what is visible in that active browser context.

Mitigation: Install only if comfortable using Gecho Bridge with the logged-in X session, and save results only to directories appropriate for raw collected X data.

Risk: The documented setup uses the Gecho Bridge package with @latest, which can change behavior over time.

Mitigation: Review or pin the Gecho Bridge package version before use.

Risk: Login, CAPTCHA, verification, region, cookie consent, blocked-page, timeout, or save failures can prevent collection.

Mitigation: Resolve browser prompts manually, report exact tool failures, avoid retries in the same turn, and choose a writable absolute directory for saved results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/x-post-detail)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho website](https://gecho.ai/)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw setup video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes setup video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise summaries, setup commands, links, and saved-path reporting when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the x_post_detail MCP workflow once and summarize 3 to 5 useful fields; raw JSON is not pasted.]

## Skill Version(s):

1.1.38 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
