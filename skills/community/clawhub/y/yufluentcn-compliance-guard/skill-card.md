## Description: <br>
Cross-border compliance and trade reference helper for certification checklists, tariff estimates, labeling requirements, and platform rule checks, returning Yufluent cloud-generated JSON guidance that must be manually verified. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, trade operators, compliance teams, and developers use this skill to request preliminary certification, tariff, labeling, and marketplace-rule guidance for cross-border products. The output is reference material only and is not legal or tax advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends product, supplier, shipment, tariff, platform-rule details, and TOKENAPI_KEY to the configured Yufluent/OpenClaw service. <br>
Mitigation: Install only when that data sharing is acceptable, keep TOKENAPI_KEY out of source control and logs, and use only a trusted TOKENAPI_BASE_URL. <br>
Risk: On 500 or 502 responses, the client falls back from the scoped skill run endpoint to the broader agent orchestration endpoint while sending the same payload and API key. <br>
Mitigation: Review the fallback behavior before deployment and monitor which endpoint handles production requests. <br>
Risk: Compliance, tariff, labeling, and platform-rule outputs may be incomplete or outdated for a specific product, market, or date. <br>
Mitigation: Treat outputs as reference guidance and verify final decisions against official sources or qualified legal, tax, and compliance professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluentcn-compliance-guard) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [OpenClaw console](https://claw.changzhiai.com/app/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Formatted text or structured JSON from the Yufluent compliance service, with CLI examples in Markdown documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY; TOKENAPI_BASE_URL is optional and should only point to a trusted host.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
