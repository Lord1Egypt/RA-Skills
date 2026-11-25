## Description:

使用用户指定的商品编辑页、商家规则和浏览器环境，按规格、图文、物流、售后整理可见字段的缺项、冲突与人工补充表。不可见字段明确留空，未提供规则不虚构要求；全程默认只读，不保存、不提交、不上架，交付结果保留每条资料来源与处理边界。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

面向需要在发布前复核商品编辑页的商家和运营人员。将用户指定页面中可见的规格、图文、物流和售后信息整理成缺项、冲突与待确认字段，并为每项保留来源和人工处理建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation command is unpinned, and the available scan did not fully inspect three scripts.

Mitigation: Review the installation source and version, and inspect the scripts before installing; the benign verdict is not a guarantee of safety.

## Reference(s):

- [Easy WebBridge source and setup](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)
- [EasyBR release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)
- [EasyBR official download page](https://www.ebrower.com/down.html)
- [ERPNext project reference](https://github.com/frappe/erpnext)
- [ERPNext README](https://github.com/frappe/erpnext/blob/develop/README.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON rows with category, field, status, visible value, source, and suggested human action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [At most 100 rows per run; unseen fields remain pending confirmation, and only explicitly empty values are marked missing.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
