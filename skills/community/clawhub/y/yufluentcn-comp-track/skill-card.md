## Description: <br>
Analyzes manually pasted competitor listing copy across titles, bullets, descriptions, and keywords to produce differentiation suggestions and opportunity points through Yufluent's cloud harness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators and developers use this skill to compare their product listing copy with manually supplied competitor copy for Amazon, Shopify, or TikTok and receive a cloud-generated competitor analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends manually supplied competitor listing text and optional own product copy to Yufluent's cloud service. <br>
Mitigation: Use it only with content your organization permits sending to the Yufluent service, and avoid confidential or partner-restricted listing material. <br>
Risk: The skill requires TOKENAPI_KEY and can optionally use TOKENAPI_BASE_URL to change the API endpoint. <br>
Mitigation: Store TOKENAPI_KEY as a secret and set TOKENAPI_BASE_URL only when the target endpoint is explicitly trusted. <br>
Risk: Competitor analysis output may be incomplete or misleading if the pasted listing copy is inaccurate or incomplete. <br>
Mitigation: Review the generated report before applying listing changes, and validate recommendations against marketplace policy and business context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluentcn-comp-track) <br>
- [Publisher profile](https://clawhub.ai/user/metahuan) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [Yufluent OpenClaw documentation](https://claw.changzhiai.com/app/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown or JSON returned from a cloud API client, with CLI examples for invocation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY; optional TOKENAPI_BASE_URL overrides the default API endpoint.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
