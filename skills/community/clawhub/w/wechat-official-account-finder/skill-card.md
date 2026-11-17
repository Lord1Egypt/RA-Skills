## Description:

Finds WeChat official accounts by keyword and retrieves account profiles, including names, descriptions, WeChat IDs, and verified entities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

People researching WeChat official accounts use this skill to identify potential peers, partners, and industry accounts and inspect their profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search and profile queries are sent to the WeMedia service using a local API key.

Mitigation: Use the service only if acceptable, keep WM_API_KEY local, and avoid sharing the key in chat or exports.

Risk: Paid requests and additional pages may incur charges.

Mitigation: Review live cost estimates before approving paid calls and keep page limits modest.

Risk: Export, snapshot, or checkpoint paths can write or replace local files.

Mitigation: Choose output paths deliberately and review existing files before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dunkong/skills/wechat-official-account-finder)
- [WeMedia service](https://api.we-media.cn?source=clawhub)
- [WeMedia AI guide](https://api.we-media.cn/client/ai-guide)
- [WeMedia product documentation](https://api.we-media.cn/client/products)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Excel spreadsheets]

**Output Format:** [Account summaries and optional local JSON, Markdown, or Excel exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include partial results and actual API charges.]

## Skill Version(s):

1.4.2 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
