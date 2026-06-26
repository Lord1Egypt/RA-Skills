## Description: <br>
Use this skill to fetch TAAPI.IO indicator data for crypto or stocks, including fast single-indicator requests and bulk/multi-construct queries for agentic trading workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to request TAAPI.IO market indicators for crypto or stocks through a local shell helper. It supports single-indicator checks, bulk indicator requests, and multi-construct workflows for market analysis automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TAAPI API secrets can appear in request URLs or failed command output. <br>
Mitigation: Prefer the TAAPI_SECRET environment variable over command-line secrets, avoid sharing logs or failed command output, and rotate the secret if it appears in logs. <br>
Risk: Unofficial TAAPI base URLs can receive secrets and request payloads. <br>
Mitigation: Use the default https://api.taapi.io endpoint unless the alternate endpoint is fully trusted and explicitly approved. <br>
Risk: Live smoke tests send real network requests with TAAPI credentials. <br>
Mitigation: Run live tests only in an isolated session with revocable credentials. <br>


## Reference(s): <br>
- [TAAPI.IO](https://taapi.io/) <br>
- [TAAPI.IO Documentation](https://taapi.io/documentation/) <br>
- [TAAPI.IO Direct Integration](https://taapi.io/documentation/integration/direct/) <br>
- [TAAPI.IO Bulk REST Integration](https://taapi.io/documentation/integration/post-rest-bulk/) <br>
- [TAAPI.IO Multiple Constructs](https://taapi.io/documentation/multiple-constructs/) <br>
- [TAAPI.IO Rate Limits](https://taapi.io/documentation/rate-limits/) <br>
- [TAAPI.IO Indicators](https://taapi.io/indicators/) <br>
- [ClawHub Skill Page](https://clawhub.ai/oscraters/taapi) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TAAPI_SECRET for live requests; curl is required, and jq is required for multi-construct payload generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
