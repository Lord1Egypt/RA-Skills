## Description:

Verifies whether Chinese GitHub developers appear credible by checking public profiles on Bilibili, Douyin, Xiaohongshu, Zhihu, Juejin, and CSDN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to gather public cross-platform identity signals for a GitHub project author and summarize those signals as an advisory credibility check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public social-profile correlation and follower or activity metrics can produce misleading trust judgments.

Mitigation: Treat results as advisory context only and verify repository history, releases, maintainer behavior, issues, dependencies, and code before relying on a project.

Risk: Absence from a listed Chinese content platform may be misread as suspicious.

Mitigation: Use the skill only for explicitly requested public-profile research and avoid negative conclusions based solely on missing platform accounts.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown table with a short credibility summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and should not be treated as proof of software safety or maintainer trustworthiness.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
