## Description: <br>
Provides cross-border trade compliance reference guidance for certification checklists, tariff estimates, labeling requirements, and marketplace rule checks through Yufluent's cloud compliance service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, compliance teams, and ecommerce operators use this skill to gather structured reference guidance for export certifications, HS code and tariff estimates, labeling requirements, and platform restrictions before human review against official sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends product, market, tariff, and compliance details to Yufluent's cloud service using TOKENAPI_KEY. <br>
Mitigation: Install and run it only when that data sharing is acceptable, keep TOKENAPI_KEY secret, and use only trusted endpoints. <br>
Risk: Compliance, certification, tariff, and platform-rule outputs are reference guidance and may be incomplete or out of date. <br>
Mitigation: Verify results with official rules, current regulations, and qualified legal, tax, customs, or certification professionals before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluent-clawhub-publish-yufluentcn-compliance-guard) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [Yufluent OpenClaw](https://claw.changzhiai.com/app/openclaw) <br>
- [Yufluent API key registration](https://claw.changzhiai.com/login) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, Shell commands] <br>
**Output Format:** [Structured JSON or formatted text/Markdown printed by the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY; optional TOKENAPI_BASE_URL should be left unset or set only to a trusted endpoint.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
