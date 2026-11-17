## Description:

Analyzes public Chinese social accounts using public evidence to assess content strategy, posting rhythm, engagement efficiency, top and bottom performer patterns, and comment themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckycat133](https://clawhub.ai/user/luckycat133)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to evaluate public accounts on Bilibili, Douyin, Weibo, Xiaohongshu, and WeChat Official Accounts from a profile URL, nickname, handle, or exported CSV/JSON. It helps produce evidence-bounded account strategy, cadence, engagement, performance, and comment-demand analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles authorized session cookies and OAuth credentials during public-account analysis.

Mitigation: Use it only for public-account analysis the user is authorized to perform, avoid providing session cookies on shared or monitored machines, and clear cached cookies after use.

Risk: The bundled signing server could expose request-signing behavior if run beyond a local protected context.

Mitigation: Do not run scripts/sign_server.py unless it is restricted to loopback and protected by authentication.

Risk: Server security guidance flags the Bilibili cookie path for review before using real account cookies.

Mitigation: Fix and review the Bilibili cookie path before collecting with real account cookies.

## Reference(s):

- [Workflow](references/workflow.md)
- [Artifact Contract](references/artifact-contract.md)
- [Collection Schema](references/collection-schema.md)
- [Metrics and Sampling](references/metrics-and-sampling.md)
- [Model Insights](references/model-insights.md)
- [Comment Insights](references/comment-insights.md)
- [Cookie Guide](references/cookie-guide.md)
- [Bilibili Platform Rules](references/platforms/bilibili.md)
- [Douyin Platform Rules](references/platforms/douyin.md)
- [Weibo Platform Rules](references/platforms/weibo.md)
- [Xiaohongshu Platform Rules](references/platforms/xiaohongshu.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis, JSON/CSV collection artifacts, HTML reports, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should disclose evidence scope, partial collection status, field coverage, and unavailable metrics instead of inferring missing data.]

## Skill Version(s):

0.9.2 (source: server release metadata and VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
