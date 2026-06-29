## Description: <br>
Conducts cross-border ecommerce keyword research and produces structured SEO placement reports for Amazon, Shopify, and TikTok Shop through Yufluent's cloud service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce operators, and agents use this skill to turn product details, seed keywords, competitor terms, market, language, and platform choices into SEO keyword and placement reports for Amazon, Shopify, or TikTok Shop. Reports are intended for human review against seller platform data before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product details and keyword inputs are sent to Yufluent's cloud service using TOKENAPI_KEY. <br>
Mitigation: Review data-sharing expectations before use and avoid sending confidential product information unless the deployment policy permits it. <br>
Risk: TOKENAPI_KEY is required for cloud execution and could be exposed if committed or shared. <br>
Mitigation: Keep the key private, use environment variables or a local .env file, and do not commit secrets to source control. <br>
Risk: SEO placement reports may be misleading if applied without platform-specific validation. <br>
Mitigation: Human reviewers should compare recommendations with Brand Analytics, ad search terms, Shopify Search, or other seller platform data before publishing listings. <br>
Risk: Dependency hygiene can drift for the requests package in controlled deployments. <br>
Mitigation: Pin or update requests to a reviewed patched version as part of deployment review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-seo-pro) <br>
- [Yufluent console](https://claw.changzhiai.com) <br>
- [Yufluent OpenClaw guide](https://claw.changzhiai.com/app/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON SEO reports with optional saved files and explanatory Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY; sends product and keyword inputs to Yufluent's cloud service.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
