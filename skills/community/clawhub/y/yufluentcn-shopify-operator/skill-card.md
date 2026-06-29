## Description: <br>
Provides six-stage Shopify store operations coaching for product sourcing, supplier planning, listing, store design, social content, and monitoring through Yufluent cloud execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators and their agents use this skill to gather context about a Shopify store stage and request Yufluent-generated operating plans for sourcing, suppliers, listings, storefront decoration, social content, or monitoring reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can transmit store details, private storefront analytics, proprietary strategy context, and an API key to a remote Yufluent endpoint. <br>
Mitigation: Review the provider's privacy and retention terms before installing; avoid entering sensitive customer or proprietary data unless the user accepts that transfer, and use a scoped or disposable API key where possible. <br>
Risk: TOKENAPI_BASE_URL can redirect skill traffic and credentials to a different endpoint. <br>
Mitigation: Do not override TOKENAPI_BASE_URL except to an endpoint the user controls and trusts, and verify the environment before running the skill. <br>
Risk: Generated Shopify operating plans may contain incorrect, noncompliant, or misleading business guidance. <br>
Mitigation: Require human review before execution and check outputs against Shopify policies, target-market rules, and the actual products being sold. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluentcn-shopify-operator) <br>
- [Yufluent console](https://claw.changzhiai.com) <br>
- [OpenClaw integration](https://claw.changzhiai.com/app/openclaw) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with optional structured tables and CLI run metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY and may use TOKENAPI_BASE_URL to send request data to the Yufluent cloud service.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
