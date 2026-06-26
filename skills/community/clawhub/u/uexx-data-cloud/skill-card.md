## Description: <br>
UEXX Data Cloud answers cryptocurrency market-data questions using cached UEXX data, including sentiment, ETF flows, funding rates, open interest, and long/short ratios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanfanscoin](https://clawhub.ai/user/fanfanscoin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and market analysts use this skill to ask natural-language cryptocurrency market questions and receive interpreted cached market data without manually managing API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto market-data questions are sent to UEXX Data Cloud. <br>
Mitigation: Install only where sending those questions to UEXX is acceptable for the user's privacy and data-use expectations. <br>
Risk: The skill creates or reuses a Free UEXX API key and stores it locally. <br>
Mitigation: Treat ~/.uexx-data-cloud/free_key.json as a secret on shared systems and delete it when no longer needed. <br>
Risk: Changing UEXX_DATA_BASE_URL can redirect requests to a different endpoint. <br>
Mitigation: Set UEXX_DATA_BASE_URL only when intentionally using another trusted UEXX-compatible endpoint. <br>


## Reference(s): <br>
- [UEXX Data Cloud API Catalog](references/api_catalog.md) <br>
- [UEXX Public API Guide](https://bbs.uexx.com/api/v1/public/api-guide) <br>
- [UEXX Data Cloud on ClawHub](https://clawhub.ai/fanfanscoin/uexx-data-cloud) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with natural-language answers and occasional curl or Python examples when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include data timestamps or cache age; raw JSON is not returned by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
