## Description: <br>
Yufluentcn Product Pick analyzes user-provided or authorized marketplace product data from Amazon, TikTok Shop, and AliExpress to score product opportunities, surface blue-ocean candidates, and flag inventory and IP risks through Yufluent's cloud service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators, sourcing teams, and agents use this skill to evaluate product candidates, compare marketplace demand and competition signals, and prepare go, watch, or no-go sourcing recommendations. It is intended for authorized marketplace data, pasted candidate tables, or approved API exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product candidates, search terms, pricing, cost, margin, and inventory-capital context are sent to Yufluent's cloud API. <br>
Mitigation: Use the skill only with data approved for cloud processing, avoid unnecessary sensitive business details, and scope TOKENAPI_KEY to trusted use. <br>
Risk: Automatic marketplace discovery can collect and submit browser-extracted marketplace data. <br>
Mitigation: Run discovery only on authorized pages or approved data sources and review discovered candidates before submitting them for analysis. <br>
Risk: Go, watch, no-go and IP-risk suggestions may be incomplete or unsuitable for final sourcing decisions. <br>
Mitigation: Treat results as decision support, verify IP and compliance risks manually, and perform business review before purchasing inventory. <br>
Risk: Misconfigured TOKENAPI_KEY or BROWSER_SERVICE_URL could expose credentials or route data to an untrusted service. <br>
Mitigation: Store credentials in environment variables or a secure secret manager and point browser and API settings only at trusted services. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/metahuan/skills/yufluentcn-product-pick) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [Publisher profile](https://clawhub.ai/user/metahuan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or text explanations with JSON skill-run results and optional saved output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY. Optional browser discovery uses BROWSER_SERVICE_URL and sends product candidates, search terms, pricing, margin, and inventory-capital context to Yufluent's cloud API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
