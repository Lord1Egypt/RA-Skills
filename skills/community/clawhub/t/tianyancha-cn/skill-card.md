## Description: <br>
企业信息查询 - 天眼查/企查查/爱企查数据查询（Bloomberg 终端中国版） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Business users, analysts, and agents use this skill to look up Chinese company profiles, shareholders, executives, financial data, legal risks, and operating status through Tianyancha, Qichacha, Aiqicha, or official public registries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Third-party business-data APIs may consume quota or create billing impact when called with a user token. <br>
Mitigation: Use a token intended for this workflow, monitor provider quotas and billing, and confirm provider terms before use. <br>
Risk: Company searches may reveal confidential diligence, partnership, or market-research interests to external providers. <br>
Mitigation: Avoid confidential searches unless the provider terms and organizational policy permit that disclosure. <br>
Risk: The artifact shows an optional third-party Python package installation path. <br>
Mitigation: Verify the package source and suitability before installing it in an agent environment. <br>
Risk: Provider data may not be real time. <br>
Mitigation: Treat returned company records as reference data and verify important decisions against authoritative or current sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/tianyancha-cn) <br>
- [Publisher profile](https://clawhub.ai/user/guohongbin-git) <br>
- [Tianyancha open search API example](https://open.api.tianyancha.com/services/open/search/2.0?keyword=%E8%85%BE%E8%AE%AF) <br>
- [Qichacha enterprise lookup API example](https://api.qichacha.com/ECIV4/GetEnterpriseByName?keyword=%E8%85%BE%E8%AE%AF) <br>
- [Aiqicha](https://aiqicha.baidu.com/) <br>
- [National Enterprise Credit Information Publicity System](http://www.gsxt.gov.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with API endpoint examples, curl commands, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include third-party API token usage guidance, provider comparisons, company data fields, and compliance notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
