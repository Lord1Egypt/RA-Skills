## Description:

Lists a WeChat Channels creator’s posts by account ID or share link, including titles, publication dates, identifiers, and optional share links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and researchers use this skill to review a WeChat Channels account’s recent posts, track updates, and export a paginated post list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account IDs, share links, keywords, and query parameters are sent to the publisher API.

Mitigation: Confirm the requested inputs are appropriate to share with api.we-media.cn before running queries.

Risk: A local API key is required for authenticated requests, which may incur charges.

Mitigation: Set WM_API_KEY locally without sharing it in chat; review the current price estimate and approve paid requests first.

Risk: Retrieved results, snapshots, and checkpoints may remain in local files.

Mitigation: Choose and review output paths, limit access to saved results, and remove files when no longer needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dunkong/skills/wechat-channel-author-feed)
- [Publisher API and account setup](https://api.we-media.cn?source=clawhub)
- [Publisher AI integration guide](https://api.we-media.cn/client/ai-guide)
- [Publisher product documentation](https://api.we-media.cn/client/products)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Markdown preview with JSON or Excel exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paginated results can include partial-result status, a full JSON companion file, and optional snapshots or checkpoints.]

## Skill Version(s):

1.4.2 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
