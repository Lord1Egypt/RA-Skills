## Description:

帮助用户从青虎 AI 的 Shopee 店铺库中按类目、店铺类型、跨境属性和开店时间筛选店铺。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营人员和研究人员使用此技能筛选 Shopee 各站点的店铺，寻找跨境店、新店和对标店铺。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions may prompt unpinned global package installation or changes to local PATH and shell startup files.

Mitigation: Install qhkit through a trusted, pinned process and require explicit approval before modifying global packages, PATH or shell startup files.

Risk: The skill needs a Qinghu token on the machine and can make billable queries.

Mitigation: Protect the token, review the tool and estimated cost, and obtain the user's consent before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-shop-list)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Concise text summaries and downloadable table files for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shopee shop records are T+1; report site, date, sample size and credits charged.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
