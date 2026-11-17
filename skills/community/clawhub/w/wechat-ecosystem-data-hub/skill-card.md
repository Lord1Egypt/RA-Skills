## Description:

Helps users query WeChat ecosystem data through the Mangeyun API, estimate live costs before paid requests, and export results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers can select supported WeChat public account, Channels, search, mini-program, and media-analysis queries, review estimated charges, and receive summaries and data exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid requests to an external data service may incur charges.

Mitigation: Review live cost estimates and approve the scope before running paid requests.

Risk: Uploading selected local media transfers it outside the user's machine.

Mitigation: Upload only media the user has explicitly chosen and approved.

Risk: API credentials could be exposed if shared in chat or exported results.

Mitigation: Configure the API key locally and keep it out of conversations and exports.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dunkong/skills/wechat-ecosystem-data-hub)
- [Mangeyun API homepage](https://api.we-media.cn?source=clawhub)
- [Mangeyun AI guide](https://api.we-media.cn/client/ai-guide)
- [Mangeyun product documentation](https://api.we-media.cn/client/products)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON files, Excel files]

**Output Format:** [Markdown summary with JSON, Markdown, or Excel exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source evidence and actual charges when available; flags partial results.]

## Skill Version(s):

1.4.3 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
