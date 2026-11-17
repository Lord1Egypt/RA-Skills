## Description:

帮助亚马逊卖家按市场规模、竞争、利润和新品机会筛选并比较商品类目。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

亚马逊卖家和选品分析人员可按站点、价格、卖家数量等条件筛选类目，并比较市场规模、竞争强度及新品进入机会。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading qhkit can change tools on the user's machine.

Mitigation: Install only if the package is trusted; prefer a pre-provisioned Node/qhkit environment and avoid unpinned upgrades.

Risk: Configuring qhkit may store or overwrite an API token.

Mitigation: Obtain the user's explicit intent before changing credentials; avoid displaying or saving tokens unnecessarily.

Risk: Market-research queries may consume paid credits, especially with larger result sets.

Mitigation: Estimate charges and obtain user approval before paid calls or large batches.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-amazon-market-list)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise category analysis; tabular file for 10 or more results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports marketplace, time period, sample size and credits charged when applicable.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
