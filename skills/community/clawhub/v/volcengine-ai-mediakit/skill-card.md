## Description:

Volcengine AI MediaKit helps agents upload, process, enhance, translate, analyze, and query audio and video assets, returning task IDs and playback links for completed media jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-ai-mediakit](https://clawhub.ai/user/volc-ai-mediakit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, media operators, and content teams use this skill to drive Volcengine media workflows for editing, enhancement, captioning, translation, content analysis, and playback-link retrieval from agent conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A media-info lookup can automatically publish unpublished videos to obtain playback links.

Mitigation: Use scoped Volcengine credentials and avoid querying sensitive unpublished videos unless publication and shareable playback URLs are acceptable.

Risk: The skill can upload media and submit processing jobs that may create storage, processing, or traffic charges.

Mitigation: Confirm the intended media, VOD space, and expected billing exposure before running jobs, especially on large files or batch requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/volc-ai-mediakit/skills/volcengine-ai-mediakit)
- [Publisher Profile](https://clawhub.ai/user/volc-ai-mediakit)
- [Capability Summary](references/00-detail.md)
- [Billing Instructions](references/00-billing-instructions.md)
- [Media Storage Billing](https://www.volcengine.com/docs/4/76542?lang=zh)
- [Video Editing Billing](https://www.volcengine.com/docs/4/1941016?lang=zh)
- [Media Processing Billing](https://www.volcengine.com/docs/4/1941013?lang=zh)
- [Distribution Acceleration Configuration](https://www.volcengine.com/docs/4/177122)
- [Distribution Acceleration Billing](https://www.volcengine.com/docs/4/1941015?lang=zh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include asynchronous task IDs, playback URLs, media metadata, error JSON, and resume commands for polling long-running jobs.]

## Skill Version(s):

1.0.5 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
