## Description:

查询微信视频号作品评论，支持分页浏览和展开评论回复。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams and analysts use this skill to retrieve comments and replies on a WeChat Video Channel post, review audience feedback, and export larger results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid comment queries can spend Qinghu credits, including on some failed calls.

Mitigation: Check the current estimate and obtain user approval before paid calls; report the actual credits charged.

Risk: Using the wrong Qinghu site or token can prevent access to the intended service.

Mitigation: Confirm the domestic Qinghu site and token configuration before the first query.

Risk: Installing qhkit or Node may change the local environment.

Mitigation: Confirm the user wants the qhkit workflow and approve any npm or Node installation before setup.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shipinhao-comments)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown summary with a table file for 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the credits spent on paid calls; supports paginated results and comment replies.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
