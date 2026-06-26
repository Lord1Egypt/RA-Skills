## Description: <br>
Queries the CertiK SkyInsights blockchain risk intelligence API to assess wallet and transaction risk, look up on-chain labels or entity details, and run AML screening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certik-ai](https://clawhub.ai/user/certik-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and blockchain risk analysts use this skill to check wallet addresses and transaction hashes for risk signals, labels, entity details, and AML screening results from CertiK SkyInsights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, transaction hashes, chain identifiers, and related request metadata are sent to CertiK SkyInsights. <br>
Mitigation: Use the skill only when this disclosure is acceptable for the user and task; avoid submitting identifiers that should not leave the operating environment. <br>
Risk: The skill requires API credentials for CertiK SkyInsights. <br>
Mitigation: Store SKYINSIGHTS_API_KEY and SKYINSIGHTS_API_SECRET in protected environment configuration or a secret manager, and do not commit them to source control. <br>
Risk: AML screening can consume additional API quota and may take several seconds to complete. <br>
Mitigation: Run screening when the user requests compliance checks or when the skill workflow calls for follow-up screening, and monitor rate limits or quota errors. <br>
Risk: Unsupported chains or malformed addresses can produce invalid-parameter errors or incomplete results. <br>
Mitigation: Use the documented chain identifiers and ask the user to retry with supported parameters when the API reports an unsupported chain or bad request. <br>


## Reference(s): <br>
- [SkyInsights](https://skyinsights.certik.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/certik-ai/skyinsights) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-friendly text summaries with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKYINSIGHTS_API_KEY and SKYINSIGHTS_API_SECRET; AML screening may take about 5-15 seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
