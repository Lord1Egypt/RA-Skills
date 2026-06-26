## Description: <br>
问道云企业信息查询工具，支持通过问道云 API 查询企业基本信息、经营信息、财务信息、舆情信息、企业各类风险指标等功能，当用户需要查询企业相关信息时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guojing1818](https://clawhub.ai/user/guojing1818) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search WenDaoYun for Chinese enterprise records, confirm the exact company, and retrieve business, financial, judicial, risk, and public-record details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WenDaoYun API key. <br>
Mitigation: Keep WENDAOYUN_API_KEY private, store it only in the agent configuration, and rotate it if exposure is suspected. <br>
Risk: Company names and selected lookup requests are sent to WenDaoYun and may consume quota. <br>
Mitigation: Use the skill only for intended company-record lookups and avoid sending unnecessary or sensitive lookup terms. <br>
Risk: Legal, financial, and risk results can be misleading if the wrong company is selected. <br>
Mitigation: Search first and confirm the exact company before requesting detailed records. <br>


## Reference(s): <br>
- [WenDaoYun Open Platform](https://open.wintaocloud.com/home) <br>
- [WenDaoYun API Invoke Endpoint](https://h5.wintaocloud.com/prod-api/api/invoke) <br>
- [ClawHub Skill Page](https://clawhub.ai/guojing1818/wentao-org-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration] <br>
**Output Format:** [Markdown instructions and structured text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WENDAOYUN_API_KEY and sends selected company lookup requests to WenDaoYun.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
