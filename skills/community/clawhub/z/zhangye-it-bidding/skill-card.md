## Description:

Searches current-month IT and informatization bidding announcements for Zhangye City across public procurement sources and appends extracted project records to a predefined Excel tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xizhima](https://clawhub.ai/user/xizhima)

### License/Terms of Use:

MIT-0

## Use Case:

Public-sector procurement researchers and operations staff use this skill to find Zhangye-area IT and digital project bidding notices for the current month, extract key announcement fields, deduplicate against an existing tracker, and update an Excel workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can append rows to a specified Excel tracker without a required confirmation step before saving.

Mitigation: Confirm the workbook path before running the skill and keep a backup of important trackers.

Risk: Procurement source pages may be unavailable or individual notices may have incomplete fields.

Mitigation: Record skipped or inaccessible sources in the run summary and leave unavailable fields blank instead of guessing.

## Reference(s):

- [张掖市信息化项目标讯搜索参考资料](references/bidding_sources.md)
- [甘肃省公共资源交易网](https://ggzyjy.gansu.gov.cn)
- [张掖市公共资源交易中心](https://ggzy.zhangye.gov.cn)
- [甘肃政府采购网](https://www.ccgp-gansu.gov.cn)
- [中国政府采购网](https://www.ccgp.gov.cn)
- [中国招标投标公共服务平台](https://www.cebpubservice.com)
- [全国公共资源交易平台](https://www.ggzy.gov.cn)

## Skill Output:

**Output Type(s):** [Text, Files, Guidance]

**Output Format:** [Excel workbook updates plus a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends deduplicated rows to the target Excel tracker and reports counts for searched platforms, found announcements, valid projects, new entries, and skipped duplicates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
