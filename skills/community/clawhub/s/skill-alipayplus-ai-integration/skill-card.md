## Description: <br>
Alipay+ Payment Integration Assistant that provides structured integration guidance for ACQPs and MPPs across user-presented, merchant-presented, online cashier, and online auto debit payment scenarios using current official Alipay+ documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-intl](https://clawhub.ai/user/ant-intl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and payment integration engineers use this skill to plan and implement Alipay+ integrations for acquirer service providers and mobile payment providers. It helps identify the relevant role, payment scenario, official documentation, testing workflow, and implementation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports payment integration workflows where incorrect guidance or generated code could affect payment behavior. <br>
Mitigation: Verify generated guidance and code against the fetched official Alipay+ documentation and your own security review before deployment. <br>
Risk: Integration discussions may involve sensitive API keys, certificates, production credentials, or customer payment data. <br>
Mitigation: Do not paste private credentials or customer payment data into chat; use placeholders and manage secrets through approved secure channels. <br>
Risk: The skill makes live requests to docs.alipayplus.com to retrieve current documentation. <br>
Mitigation: Install and use it only where outbound documentation access is acceptable for the agent environment. <br>


## Reference(s): <br>
- [Alipay+ Documentation Index](https://docs.alipayplus.com/alipayplus/llms.txt) <br>
- [ACQP Get Started with Alipay+ Integration](https://docs.alipayplus.com/alipayplus/alipayplus/get_started_acq/get_started_integration_acq.md) <br>
- [MPP Get Started with Alipay+ Integration](https://docs.alipayplus.com/alipayplus/alipayplus/get_started_mpp/get_started_integration.md) <br>
- [ACQP UAT Checklist](https://docs.alipayplus.com/alipayplus/alipayplus/get_started_acq/uat_checklist.md) <br>
- [Alipay+ Partner Workspace Overview](https://docs.alipayplus.com/alipayplus/alipayplus/worksp_acq/overview_what_is.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ant-intl/skill-alipayplus-ai-integration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and structured integration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require live access to official Alipay+ documentation before giving API parameters, flow details, or code examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
