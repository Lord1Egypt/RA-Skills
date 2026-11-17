## Description:

Provides MCP-accessible investment analysis for market sizing, competitor review, valuation estimates, and startup risk scoring through the ZhenCap service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Startup founders, investors, and due diligence teams use this skill to request market size estimates, competitor analysis, valuation ranges, and investment risk assessments from an MCP-enabled agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive startup, investment, financial, or customer information may be sent to the ZhenCap cloud API.

Mitigation: Avoid submitting confidential or regulated information unless the vendor privacy terms, retention practices, and account controls meet the user's requirements.

Risk: The optional ZHENCAP_API_URL environment variable can redirect requests away from the default service endpoint.

Mitigation: Leave ZHENCAP_API_URL unset unless the destination is explicitly trusted and approved.

Risk: Paid-tier use depends on an API key that may appear in terminal output or local configuration.

Mitigation: Store ZHENCAP_API_KEY only in trusted secret storage or private MCP configuration, and avoid sharing logs that include environment variables.

Risk: The security evidence identifies under-scoped and under-verified controls for a cloud service handling business inputs.

Mitigation: Review the ClawHub security summary and vendor privacy, terms, and billing controls before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/venture-capitalist)
- [ZhenCap Website](https://www.zhencap.com)
- [ZhenCap Documentation](https://www.zhencap.com/docs)
- [ZhenCap Privacy Policy](https://www.zhencap.com/privacy)
- [ZhenCap Terms of Service](https://www.zhencap.com/terms)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON examples, shell commands, and MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool responses include success status, returned analysis data, and service attribution when calls succeed.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact files report 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
