## Description:

整理指定 HTML 站点的本地资源路径，按目录结构发布并验证文件，最后返回入口链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[156554395](https://clawhub.ai/user/156554395)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要发布 HTML 页面或站点的开发者；在用户指定发布范围并授权后，上传站点文件、检查文件访问情况并返回入口链接。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence, reporting a possible path for excluded files to enter a public upload; its inspection coverage is incomplete.

Mitigation: Before publishing, check the generated file list and exclusion warnings against the intended site contents, and treat the scan as incomplete rather than as a safety guarantee.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/156554395/skills/wxb-html-publish)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [Published site files and a concise text report with the entry URL and upload and HTTP verification status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves site paths and filenames; reports upload or verification warnings when present.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
