## Description: <br>
Provides cloud-powered investment analysis for market sizing, competitor analysis, valuation modeling, and multi-dimensional risk scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhenstaff](https://clawhub.ai/user/zhenstaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, startup founders, and diligence teams use this skill to request investment analysis, including TAM/SAM/SOM estimates, competitor mapping, valuation ranges, and risk assessments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names, financial figures, market questions, and risk inputs are sent to a remote ZhenCap service. <br>
Mitigation: Use only data approved for third-party processing until the vendor, privacy policy, terms, and data-handling commitments are verified. <br>
Risk: The API destination can be overridden with ZHENCAP_API_URL. <br>
Mitigation: Leave ZHENCAP_API_URL unset or set it only to a trusted endpoint controlled by the approved vendor or deployment owner. <br>
Risk: Privacy, support, and security contact claims require confirmation before use with confidential deal data or paid API keys. <br>
Mitigation: Verify the vendor profile, privacy policy, terms of service, and support/security contact channels before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhenstaff/venture-capitalist) <br>
- [ZhenCap documentation](https://www.zhencap.com/docs) <br>
- [ZhenCap privacy policy](https://www.zhencap.com/privacy) <br>
- [ZhenCap terms of service](https://www.zhencap.com/terms) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text returned through MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market-size figures, competitor lists, SWOT analysis, valuation ranges, risk scores, red flags, and recommendations.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact package files report 2.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
