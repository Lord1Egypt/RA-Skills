## Description:

Tracks WeChat public accounts across a shared time window and produces evidence-backed comparisons of their articles and engagement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing analysts and public-account operators use this skill to compare competitors' recent posts, engagement, and content themes, with evidence links and reusable reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API requests may incur charges or exceed the intended comparison scope.

Mitigation: Check live pricing and select a budget and account scope before approving paid requests.

Risk: Account and article parameters are sent to an external service, and reports are saved locally.

Mitigation: Use only intended public-account data, keep the API key in a local credential, and review report storage and sharing.

Risk: Incomplete collections or limited samples can misrepresent competitor performance.

Mitigation: Mark partial results and unknown values, retain evidence links, and avoid claiming trends without comparable snapshots.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dunkong/skills/wechat-official-competitor-tracker)
- [WeMedia API guide](https://api.we-media.cn/client/ai-guide)
- [WeMedia product catalog](https://api.we-media.cn/client/products)
- [Multi-account comparison workflow](references/comparison.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Excel, HTML]

**Output Format:** [Evidence-backed summary and locally saved JSON, Markdown, Excel, or HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports indicate the observation window, partial results, supporting evidence, and actual API spend when available.]

## Skill Version(s):

1.4.3 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
