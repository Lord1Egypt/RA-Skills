## Description: <br>
Search X (Twitter) posts using the xAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[github2cao](https://clawhub.ai/user/github2cao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search X/Twitter posts through xAI, optionally filtering by handles, exclusions, date range, images, or video, and receive summarized results with citations to original posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and filters are sent to xAI under the user's API key and quota. <br>
Mitigation: Use a dedicated or least-privilege xAI API key, avoid sensitive queries, and store the key with appropriate local access controls. <br>


## Reference(s): <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI Console](https://console.x.ai) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON emitted by a Python command-line script, with text, citations, search count, and token usage fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and XAI_API_KEY; supports handle filters, exclusion filters, date bounds, image understanding, and video understanding flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
