## Description:

Web2Labs Studio helps agents upload local files or YouTube/Twitch URLs to produce edited jump-cut videos, vertical shorts, subtitles, thumbnail variants, and cost estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinlow](https://clawhub.ai/user/vinlow)

### License/Terms of Use:

MIT

## Use Case:

External creators and developers use this skill to automate Web2Labs Studio video workflows from an agent, including account setup, upload, progress checks, output retrieval, thumbnail generation, brand setup, and watch-mode processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags credential handling, custom endpoints, deletion, and watch-mode automation as requiring review.

Mitigation: Install only after reviewing the skill, use trusted HTTPS Web2Labs endpoints, and avoid custom WEB2LABS_API_ENDPOINT or WEB2LABS_SOCKET_URL unless the endpoint is controlled by the user.

Risk: Video, transcript, metadata, and account actions are sent to Web2Labs during normal use.

Mitigation: Use the skill only for content the user is comfortable sending to Web2Labs, and confirm the user's rights before processing URL or watch-mode content.

Risk: Credit-spending actions, delete operations, batch workflows, webhooks, and watch mode can have cost or account impact.

Mitigation: Set WEB2LABS_SPEND_POLICY=explicit for budget control and require manual confirmation before delete, batch, webhook, rush, or watch-mode workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vinlow/skills/web2labs-studio)
- [Web2Labs OpenClaw](https://web2labs.com/openclaw)
- [Web2Labs API Docs](https://www.web2labs.com/api/v1/docs)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown and structured tool responses with downloadable media files and metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger cloud video processing, local downloads, account setup, credit spending, webhooks, or watch-mode automation.]

## Skill Version(s):

1.0.1 (source: changelog and package.json, released 2026-02-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
