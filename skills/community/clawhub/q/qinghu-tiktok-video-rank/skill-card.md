## Description:

按站点、类目及日、周、月周期查询 TikTok 热门视频榜和带货视频榜，返回对应周期的增量数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营和市场分析人员可查询不同站点的 TikTok 热门或带货视频榜，寻找对标视频并比较榜单周期表现。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can change local Node/qhkit tooling before a paid query.

Mitigation: Prefer a preinstalled, pinned qhkit version and review installation steps before running them.

Risk: Configuring the Qinghu API token locally can expose or persist credentials.

Mitigation: Supply the token through a managed secret mechanism rather than shell history or persistent configuration.

Risk: Ranking lookups consume paid credits, with cost varying by returned results.

Mitigation: Check the current credit estimate and obtain user consent before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-tiktok-video-rank)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [青虎AI API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Brief narrative summary; spreadsheet file for 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports site, ranking period, sample size and credits charged; figures are period increments.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
