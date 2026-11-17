## Description:

查询指定视频号账号发布的合集列表，并返回可用于查询合集视频的 topic_id 和 topic_type。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

视频号运营人员和其他用户可查询指定账号发布的合集，获取合集标识以便进一步查看合集内视频。

### Deployment Geography for Use:

Global; queries use the Qinghu China service.

## Known Risks and Mitigations:

Risk: The skill may install or update local Node/npm tools without sufficient user control.

Mitigation: Review the setup steps and preinstall a vetted qhkit version before use.

Risk: The skill requires a Qinghu API token and may make paid calls.

Mitigation: Use a minimally privileged token and approve estimated credits before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shipinhao-collections)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise summary with collection identifiers; spreadsheet file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns topic_id and topic_type; reports Qinghu credits spent on paid calls.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
