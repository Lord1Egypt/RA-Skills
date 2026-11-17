## Description:

Searches WeChat mini-programs by keyword and returns names, AppIDs, descriptions, icons, and service providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use this skill to find WeChat mini-programs by keyword and compare their AppIDs, descriptions, and service providers for market research or partner discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API requests may incur significant charges.

Mitigation: Review the live estimate and approve the scope and cost before running paid searches.

Risk: An API key is required for paid searches.

Mitigation: Keep the key in local configuration or an environment variable; do not paste it into chat or exported results.

Risk: Search results and checkpoints are written to local files.

Mitigation: Choose appropriate output paths and review partial-result status before relying on an export.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dunkong/skills/wechat-mini-program-finder)
- [Mangyun AI guide](https://api.we-media.cn/client/ai-guide)
- [Mangyun product documentation](https://api.we-media.cn/client/products)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Excel files]

**Output Format:** [Markdown summary with JSON or Excel result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports actual API spend and indicates partial results; retains a full JSON export.]

## Skill Version(s):

1.4.2 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
