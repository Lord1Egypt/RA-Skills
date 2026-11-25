## Description:

输入商家已确认的尺码表、量法、单位、适用部位及选码条件，为单个商品（最多20档尺码、5组顾客测量）交付统一单位的尺码表、可复测步骤、按条件筛出的尺码范围和待确认项。适用于客服与商品详情协作；缺少单位、量法或关键尺寸时停止推荐，只有身高体重也不推造适配结论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

客服与商品详情团队可用此技能，将商家确认的尺码数据、量法和选码规则整理成顾客可核对的尺码说明。它按给定条件筛选候选尺码，并在信息不足时列出待确认项。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command is unpinned and retrieves a remote skill version.

Mitigation: Review the intended release and its contents before installing; pin a version where the installer supports it.

Risk: The security scan reports partial coverage, including binary assets outside its analysis scope.

Mitigation: Review files that were not covered by the scan before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xxjrq/skills/shop-size-selection-guide-cn)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown with a normalized size table, measurement steps, eligible size ranges, and confirmation items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For one product, with up to 20 sizes and five customer measurement groups; fit is not guaranteed.]

## Skill Version(s):

1.0.0 (source: server-resolved release, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
