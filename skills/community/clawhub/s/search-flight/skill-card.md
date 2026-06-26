## Description: <br>
AI机票助手实现国内航班搜索、舱位查询、预订下单、机票改期和机票退票，适用于用户询问航班、查询机票价格、提交机票订单、改期航班或退票时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search domestic flights, compare cabin prices, create flight orders, inspect order details, and submit cancellation, change, or refund requests through guided agent commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real bookings, refunds, API keys, and passenger identity data. <br>
Mitigation: Use only with a trusted flight-service provider, require explicit user confirmation for booking, cancellation, change, and refund actions, and avoid entering real passenger ID details until safeguards are reviewed. <br>
Risk: The security summary identifies weak transport, token storage, PII masking, and temporary-file handling safeguards. <br>
Mitigation: Review TLS verification, token storage, PII redaction, and temporary-file handling before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-zry/search-flight) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and plaintext tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and authenticated access to the external flight service; temporary files cache authentication and selected seat data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
