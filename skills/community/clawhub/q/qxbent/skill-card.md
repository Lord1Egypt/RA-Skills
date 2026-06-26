## Description: <br>
启信宝企业信息查询工具，提供企业工商信息、股东信息、主要人员、变更记录等查询功能，支持通过企业名称查询并返回标准化企业数据。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[llx-26](https://clawhub.ai/user/llx-26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to query QiXinBao company data by enterprise name, including registration details, shareholder information, key personnel, and recent change records. It is intended for users who have a QiXinBao API token and need structured company lookup results in Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends company queries and the QiXinBao API token to QiXinBao. <br>
Mitigation: Install only when that data transfer is acceptable, and use a dedicated low-privilege or quota-limited token. <br>
Risk: Dependency risk is unresolved for axios. <br>
Mitigation: Prefer an updated release that pins a patched axios version before broader deployment. <br>
Risk: Security evidence reports under-disclosed token transmission and a scanner-bypass comment. <br>
Mitigation: Review the source before deployment and prefer a release with corrected token-transmission wording and the scanner-bypass comment removed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/llx-26/qxbent) <br>
- [QiXinBao enterprise API endpoint](https://external-api.qixin.com/skill/ent/public) <br>
- [Enterprise information API reference](references/getEnterpriseInformation.md) <br>
- [Shareholder list API reference](references/getPartnerListV3.md) <br>
- [Key personnel API reference](references/getEmployeesListV4.md) <br>
- [Change records API reference](references/getPagingEntBasicInfo.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prose with structured Chinese enterprise lookup results and optional TypeScript or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QXBENT_API_TOKEN plus Node.js and npm; lookup methods return up to 10 shareholders, personnel records, or change records where applicable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
