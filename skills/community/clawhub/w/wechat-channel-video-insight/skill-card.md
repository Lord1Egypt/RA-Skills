## Description:

Retrieves a WeChat Channels video's title, publisher, publication time, cover, available media, and engagement data from a shared link, and supports video ID and link conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing WeChat Channels content use the skill to inspect an individual video's published details and engagement from its share link, or to resolve and generate supported video identifiers and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video links or IDs are sent to a paid third-party API.

Mitigation: Review the live cost estimate and authorize paid lookups before running them.

Risk: The service requires a local API key.

Mitigation: Set WM_API_KEY locally and do not include the key in chat or exported results.

Risk: Results are saved to local files.

Mitigation: Choose output paths intentionally and review files before sharing them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dunkong/skills/wechat-channel-video-insight)
- [WeMedia API](https://api.we-media.cn?source=clawhub)
- [WeMedia AI integration guide](https://api.we-media.cn/client/ai-guide)
- [WeMedia API product documentation](https://api.we-media.cn/client/products)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Files]

**Output Format:** [Markdown summary with optional JSON, Markdown, or Excel exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local exports include a complete JSON copy; partial results and actual charges should be disclosed.]

## Skill Version(s):

1.4.2 (source: ClawHub release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
