## Description:

Guides and executes browser-extension data collection for Douyin, TikTok, Xiaohongshu, Amazon, and Bilibili, prioritizing a cloud connector with a local connector fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiming1001](https://clawhub.ai/user/yiming1001)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to onboard, configure, run, export, and troubleshoot browser-based collection tasks across supported commerce and social platforms. It can guide first-time setup, resolve connector authorization, run cloud or local collection loops, and report export results to Feishu bitable or CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles authenticated web collection and connector credentials, so misuse or weak handling could expose account-linked data.

Mitigation: Install only when the publisher and collection sources are trusted, avoid saving cloud tokens in preferences when possible, and keep credential handling within documented connector authorization flows.

Risk: Endpoint or bridge command overrides can redirect execution through untrusted connector paths.

Mitigation: Keep cloud and bridge URLs at documented defaults and do not pass untrusted bridge commands or endpoint overrides.

Risk: The security verdict requires review because endpoint, storage, and install controls are under-scoped.

Mitigation: Review the connector and browser extension source before deployment and validate installation sources against the documented guides.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiming1001/skills/web-collection)
- [Web Collection Learning Guide](references/learning-guide.md)
- [Quick start and UI guide](https://vcn5grhrq8y0.feishu.cn/wiki/MoXrwwUN7iiUFkk8eWycs9JqntA?from=from_copylink)
- [Demo scenarios](https://vcn5grhrq8y0.feishu.cn/wiki/GO11wlXkriSwNakXrt2ck0GanEe)
- [Browser extension and connector installation guide](https://vcn5grhrq8y0.feishu.cn/wiki/R6f2w6o7ci1db1kYLK4cgJIYnWh)
- [Bitable configuration and connector authorization guide](https://vcn5grhrq8y0.feishu.cn/wiki/EAtJw2irFiDvMpkZXb4cBjYonNg)
- [Bitable template](https://vcn5grhrq8y0.feishu.cn/base/UKQsbVHpMac293s0cnFc1hq1nDd?table=tblTXM4lclXM6Jzr&view=vew8OdcKHw)
- [QA and troubleshooting guide](https://vcn5grhrq8y0.feishu.cn/wiki/F83hw2w6Xi7EOFkIScrccrQYnnd?from=from_copylink)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands, links, status summaries, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include connector authorization links, Feishu bitable links, CSV export status, command status, collected counts, and short analysis.]

## Skill Version(s):

1.2.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
