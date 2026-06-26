## Description: <br>
Tushare Openclaw Skill helps agents guide users through Tushare Pro financial data queries for China stocks, funds, futures, bonds, macroeconomic data, and related market information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ulnacranium17](https://clawhub.ai/user/ulnacranium17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to answer questions about Tushare Pro APIs, stock-code formats, token-based access, point consumption, and common data endpoints. It is most useful when a user needs guidance for querying China financial-market data through the Python SDK or HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to use a Tushare token for external API calls. <br>
Mitigation: Keep the token out of public chats and committed files, and provide it only in trusted execution contexts. <br>
Risk: Repeated or high-frequency Tushare queries can consume quota or points. <br>
Mitigation: Monitor Tushare quota and point consumption before running repeated or automated queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ulnacranium17/tushare-openclaw-skill) <br>
- [Tushare Pro](https://tushare.pro) <br>
- [Tushare API documentation](https://tushare.pro/document/2) <br>
- [Tushare points and frequency documentation](https://tushare.pro/document/1?doc_id=290) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and bash code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Tushare API names, stock-code suffix guidance, token setup notes, and quota or point-consumption cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
