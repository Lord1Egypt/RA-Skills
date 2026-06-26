## Description: <br>
Subscan API query assistant that selects endpoints from local Subscan API references, calls the API for blockchain data, and formats account, block, transaction, staking, governance, and asset results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carlhong](https://clawhub.ai/user/carlhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to query Subscan-supported blockchain data from natural language requests without manually choosing API endpoints or formatting raw responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Subscan API key locally in plaintext. <br>
Mitigation: Use a limited or disposable Subscan API key, avoid sharing the local key file, and rotate or delete the key when it is no longer needed. <br>
Risk: The helper can send the API key to any supplied URL if misused. <br>
Mitigation: Only call URLs that match https://<network>.api.subscan.io and add host validation before broad deployment. <br>
Risk: Queries may expose wallet addresses or on-chain activity in requests to Subscan. <br>
Mitigation: Confirm the intended network and address before execution, and avoid submitting addresses or transaction details that should not be shared with the API provider. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/carlhong/subscan-api) <br>
- [Subscan API Usage Reference](artifact/references/api-usage.md) <br>
- [Endpoint Details](artifact/references/endpoint-details.yaml) <br>
- [Routing Table](artifact/references/routing.yaml) <br>
- [Subscan Swagger API](artifact/swagger/swagger.yaml) <br>
- [Subscan support documentation](https://support.subscan.io) <br>
- [Subscan Pro account](https://pro.subscan.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown summaries with tables, bullet lists, error guidance, and optional raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses confirmed user parameters, local route references, and Subscan response fields to format results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
