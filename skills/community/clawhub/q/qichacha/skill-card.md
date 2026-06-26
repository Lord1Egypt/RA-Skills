## Description: <br>
根据公司名称查询企业基本信息、知识产权（专利/商标/著作权），数据来源企查查、天眼查等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigxiaoxin](https://clawhub.ai/user/bigxiaoxin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to look up Chinese company registration details and intellectual-property signals from a company name. Outputs should be treated as search-derived summaries until checked against the linked source pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company details and intellectual-property fields may be search-derived, stale, or incomplete. <br>
Mitigation: Treat the report as a lead-generation summary and verify each field against the linked source pages before business, legal, or compliance use. <br>
Risk: The security review reports an undisclosed lookup provider and possible embedded API key. <br>
Mitigation: Require publisher disclosure of the lookup provider, remove and rotate embedded credentials, and review the skill before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bigxiaoxin/qichacha) <br>
- [企查查 search](https://www.qcc.com/web/search) <br>
- [天眼查 search](https://www.tianyancha.com/search) <br>
- [爱企查 search](https://www.aiqicha.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text report with company fields, intellectual-property sections, and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a company name as input; extracted fields may be incomplete or delayed because they come from public search results.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
