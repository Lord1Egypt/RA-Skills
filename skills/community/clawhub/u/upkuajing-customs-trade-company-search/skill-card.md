## Description: <br>
Official skill for upkuajing (跨境魔方). Find companies (找公司) and global buyers using customs trade data. Get trade order details, business contact info, and lead generation tools for import/export market research and supply chain analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upkuajing](https://clawhub.ai/user/upkuajing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External trade, sales, and supply-chain teams use this skill to search customs trade records, identify buyer and supplier companies, inspect shipment patterns, and enrich selected company records with details or contact information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a paid UpKuaJing API key and can create paid searches, contact-detail batches, and recharge flows. <br>
Mitigation: Review current pricing, disclose the expected call or ID count, and require explicit user confirmation before any paid API call or top-up order. <br>
Risk: The API key is sensitive and may be stored in ~/.upkuajing/.env. <br>
Mitigation: Keep the file private, do not paste or display the key in chat, and rotate the key if it is exposed. <br>
Risk: Searches and enrichment calls can retrieve business contact data such as email, phone, social links, and websites. <br>
Mitigation: Limit retrieval to records needed for the user's task and handle exported JSON or JSONL files according to applicable contact-data and sales-outreach policies. <br>


## Reference(s): <br>
- [UpKuaJing Homepage](https://www.upkuajing.com) <br>
- [UpKuaJing Open Platform](https://developer.upkuajing.com/) <br>
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html) <br>
- [Company List API Reference](references/company-list-api.md) <br>
- [Trade List API Reference](references/trade-list-api.md) <br>
- [Company Detail API Reference](references/company-detail-api.md) <br>
- [Contact Fetch API Reference](references/contact-fetch-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scripts return JSON summaries and may write JSONL task result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; paid API calls can retrieve trade records, company details, contact data, account information, pricing, and top-up order links.] <br>

## Skill Version(s): <br>
1.0.6 (source: server evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
