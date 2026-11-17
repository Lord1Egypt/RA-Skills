## Description:

Analyzes WeChat public-account articles by fetching article content, extracting titles, timelines, stakeholders, facts, themes, and quotes, and generating reports in Markdown, OpenCLI YAML, or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teenyboy](https://clawhub.ai/user/teenyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to analyze WeChat public-account article URLs and produce structured summaries covering timelines, stakeholders, facts, themes, and notable quotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch user-supplied URLs, creating avoidable network-access risk if arbitrary, redirected, internal, shortened, or private-network URLs are provided.

Mitigation: Run only where outbound web requests are acceptable, prefer clearly valid https://mp.weixin.qq.com article URLs, and add URL allowlisting plus redirect validation before treating the skill as low-risk.

Risk: Dependencies are version-ranged rather than pinned.

Mitigation: Pin and review dependency versions before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teenyboy/skills/wechat-article-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration]

**Output Format:** [Markdown report, OpenCLI YAML adapter, or JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print results to the console or write report files when an output path is provided.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
