## Description: <br>
Search X (Twitter) posts using the xAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perfectworldltd](https://clawhub.ai/user/perfectworldltd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and external users use this skill to search X/Twitter posts through xAI Grok, including searches filtered by handles, excluded handles, date ranges, and image or video understanding options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and optional filters are sent to xAI for processing and may include sensitive or confidential information. <br>
Mitigation: Use a dedicated, revocable xAI API key and avoid submitting private or confidential information in search queries. <br>
Risk: The skill requires an xAI API key that could incur usage or expose account access if mishandled. <br>
Mitigation: Store the key in the XAI_API_KEY environment variable or OpenClaw configuration, monitor xAI usage, and rotate or revoke the key when needed. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/perfectworldltd/x-search-1-0-0) <br>
- [xAI X Search Documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI Console](https://console.x.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON object containing status, query, text summary, citations, search count, and token usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include links to original X posts; searches require python3 and XAI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
