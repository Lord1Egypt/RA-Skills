## Description:

Searches WeChat Channels accounts and related videos by keyword and returns account names, video titles, and identifiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and partnership teams use this skill to find WeChat Channels accounts and videos, assess candidate matches, and prepare evidence-based shortlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords, WeChat URLs, and authenticated requests are sent to a third-party API.

Mitigation: Confirm that sharing these inputs is acceptable; keep the API key in local environment or configuration, never in chat.

Risk: Paid API calls can incur charges, including across multiple pages.

Mitigation: Review the live cost estimate and page scope before authorizing execution with --yes.

Risk: Result and checkpoint files are written to local paths.

Mitigation: Choose output and checkpoint paths deliberately and limit access to saved data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dunkong/skills/wechat-channel-finder)
- [We-Media API guide](https://api.we-media.cn/client/ai-guide)
- [We-Media product documentation](https://api.we-media.cn/client/products)
- [We-Media API homepage](https://api.we-media.cn?source=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Excel files]

**Output Format:** [Markdown summary with optional JSON or Excel result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports actual cost and partial results; saves full JSON alongside formatted output.]

## Skill Version(s):

1.4.2 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
