## Description: <br>
通过关键词和分类查询企业信息；包含企业基本信息、股东、高管等34个分类。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinxin970620-prog](https://clawhub.ai/user/xinxin970620-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query enterprise registration, shareholder, executive, change-record, annual-report, and related company information by keyword and category. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if pasted into shared chats or logs. <br>
Mitigation: Provide API keys only through private configuration or trusted input channels and avoid logging them. <br>
Risk: Raw company and person records may contain sensitive business identifiers, ownership details, or personal names. <br>
Mitigation: Review raw JSON results before forwarding them and handle the data according to applicable privacy and business policies. <br>
Risk: The skill returns API responses without analysis or formatting. <br>
Mitigation: Validate important results against authoritative sources before using them for business decisions. <br>


## Reference(s): <br>
- [Category Mapping Reference](references/category-map.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xinxin970620-prog/rcd-enterprise) <br>
- [Enterprise Information API Endpoint](https://rcd-test.dfwycredit.com/s1/skill/enterprise) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands] <br>
**Output Format:** [Raw JSON returned from the enterprise-information API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided API key and a selected enterprise-information category.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
