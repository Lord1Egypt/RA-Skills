## Description:

分析用户提供的小红书笔记评论，归纳用户反馈、痛点、需求与可行动建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, product and brand researchers, and creators use this skill to analyze comments from a supplied Xiaohongshu note link or note ID. It helps identify feedback themes, pain points, purchase concerns, unmet needs, FAQs, and practical content or product actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an automatically installed, unpinned latest CLI that may change and can access available credentials.

Mitigation: Review the CLI before use, pin a reviewed version, and expose only the required SocialDataX credential to the execution environment.

Risk: Comment data is sent to SocialDataX, and the scan calls for clarity about that disclosure.

Mitigation: Review SocialDataX's data handling terms and confirm that the comments may be sent to the service before running an analysis.

Risk: Security analysis is partial because some local references could not be resolved.

Mitigation: Resolve and review the missing references as part of the security review before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/xhs-comment-insights)
- [SocialDataX API key and skill information](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are scoped to comments and replies returned for the supplied note; state whether the retrieved sample is partial.]

## Skill Version(s):

0.1.13 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
