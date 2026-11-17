## Description:

获取小红书实时热搜榜，帮助用户了解热点并寻找内容选题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和运营人员用它查询小红书实时热搜榜，寻找选题并了解当前热点。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing Node.js and the qhkit package changes the local environment.

Mitigation: Review installation steps and package source before proceeding; verify downloaded Node.js binaries before extraction.

Risk: Using the wrong service site or mishandling an access token can cause authentication failures.

Mitigation: Confirm the intended Qinghu site and token configuration with the user; do not expose the token in responses.

Risk: Paid requests consume Qinghu credits, and failed server calls may still be charged.

Mitigation: Check the current estimate and obtain consent before paid calls; limit repeat attempts and report the actual credits charged.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-rednote-hot-search)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [青虎数据 API key management](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Chinese-language summary; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports actual Qinghu credits consumed for paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
