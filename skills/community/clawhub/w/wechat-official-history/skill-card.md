## Description:

Looks up a WeChat official account's past or today's articles by article link or gh_ account ID, with pagination and export options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and analysts use this skill to review an official account's article history, check today's posts, and build a sortable archive for monitoring or competitor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article links or gh_ account IDs are sent to a third-party API, and calls may incur charges.

Mitigation: Review the live price estimate and limit pages before authorizing paid requests.

Risk: An API key and exported article data require care on the user's machine.

Mitigation: Configure the key locally, do not share it in chat, and direct result files to a local path you control.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dunkong/skills/wechat-official-history)
- [We-media AI guide](https://api.we-media.cn/client/ai-guide)
- [We-media products and documentation](https://api.we-media.cn/client/products)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Article summaries and JSON, Markdown, or Excel exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes article titles, publication times and links; reports partial results and actual charges when applicable.]

## Skill Version(s):

1.4.2 (source: skill frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
